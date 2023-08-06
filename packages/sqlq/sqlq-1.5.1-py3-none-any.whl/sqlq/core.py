from omnitools import args, key_pair_format, join_path, abs_main_dir
from threadwrapper import *
from easyrsa import *
import datetime
import sqlite3
import asyncio
import shutil
import queue
import json
import os


__ALL__ = ["SqlQueue"]


class SqlQueue:
    def worker(self, _db) -> None:
        def bak_path(db):
            now = datetime.datetime.now()
            a, b = os.path.splitext(os.path.basename(db))
            c = os.path.join(
                os.path.dirname(db),
                "bak",
                str(now.year),
                str(now.month).zfill(2),
                str(now.day).zfill(2),
                str(now.hour).zfill(2),
                str(now.minute).zfill(2),
                "{}.{}.{}".format(a, int(time.time()*1000), b[1:])
            )
            os.makedirs(os.path.dirname(c), exist_ok=True)
            return c
        def connect_db(db):
            conn = sqlite3.connect(db)
            self.__exc(conn, "PRAGMA locking_mode=EXCLUSIVE;")
            return conn
        def disconnect_db(conn):
            self.__exc(conn, "PRAGMA locking_mode=NORMAL;")
            commit_db(conn)
            conn.close()
        def commit_db(conn):
            conn.commit()
            result = self.__exc(conn, "PRAGMA journal_mode;")
            journal_mode = result[0]["journal_mode"]
            if journal_mode == "wal":
                self.__exc(conn, "PRAGMA wal_checkpoint(PASSIVE);")
        def backup(db):
            new_db = bak_path(db)
            shutil.copyfile(db, new_db)
        def do_backup(conn):
            disconnect_db(conn)
            backup(_db)
            self.do_backup = False
            return connect_db(_db)
        try:
            conn = connect_db(_db)
            if self.auto_backup:
                conn = do_backup(conn)
            prev_commit_ts = time.time()
            prev_backup_ts = time.time()
            while not self.terminate:
                time_commit_diff = (time.time()-prev_commit_ts)*1000
                time_backup_diff = (time.time()-prev_backup_ts)*1000
                if self.do_commit or time_commit_diff > self.timeout_commit:
                    commit_db(conn)
                    self.do_commit = False
                    prev_commit_ts = time.time()
                elif self.do_backup or (self.auto_backup and (time_backup_diff > self.timeout_backup)):
                    conn = do_backup(conn)
                    prev_backup_ts = time.time()
                elif self.sqlq.qsize() > 0:
                    tid, sql, data, row_factory = self.sqlq.get()
                    self.exc_result[tid] = self.__exc(conn, sql, data, row_factory)
                    # self.sqlq.task_done()
                time.sleep(1/1000)
            disconnect_db(conn)
            if self.auto_backup:
                backup(_db)
        except:
            self.ioerror = True
            self.exploded_reason = traceback.format_exc()
            queue_left = []
            while self.sqlq.qsize():
                queue_left.append(self.sqlq.get())
            if queue_left:
                open(bak_path(_db)+".queue", "wb").write(json.dumps(queue_left).encode())
        self.worker_dead = True

    def __exc(self, conn: sqlite3.Connection, sql: str, data: tuple = (), row_factory: str = "row"):
        mode = ""
        try:
            if row_factory == "list":
                conn.row_factory = None
            else:
                conn.row_factory = sqlite3.Row
            db = conn.cursor()
            if sql.endswith(";"):
                sql = sql[:-1]
            mode = ""
            if len(data) != 0:
                if isinstance(data[0], list):
                    data = tuple([tuple(_) for _ in data])
                if isinstance(data[0], tuple):
                    mode = "many"
                else:
                    mode = "data"
            elif len(sql.split(";")) > 1:
                mode = "script"
            else:
                mode = "sql"
            if mode == "many":
                db.executemany(sql, data)
            elif mode == "data":
                db.execute(sql, data)
            elif mode == "sql":
                db.execute(sql)
            elif mode == "script":
                db.executescript(sql)
            result = db.fetchall()
            if row_factory == "list":
                result = [list(row) for row in result]
            else:
                result = [dict(row) for row in result]
            return result
        except Exception as e:
            p("error: [{}] {}( {} ) due to {}".format(mode, sql, data, e))
            p(debug_info()[0])
            return e

    def wait_task_to_finish(self, attribute_name, attribute_name2=None):
        if not hasattr(self, attribute_name):
            raise AttributeError("no {} in self".format(attribute_name))
        if attribute_name2:
            if not hasattr(self, attribute_name2):
                raise AttributeError("no {} in self".format(attribute_name2))
        setattr(self, attribute_name, True)
        while getattr(self, attribute_name) if not attribute_name2 else not getattr(self, attribute_name2):
            time.sleep(1/1000)
        return True

    def wrap_under_is_server(self, task):
        if self.is_server:
            return self.wait_task_to_finish(task)
        else:
            return self.sc().request(command=task[3:], data=args())

    def backup(self):
        return self.wrap_under_is_server("do_backup")

    def commit(self):
        return self.wrap_under_is_server("do_commit")

    def stop(self):
        if self.is_server:
            self.wait_task_to_finish("terminate", "worker_dead")

    def __init__(
            self, *,
            server: bool = False, db: str = "",
            timeout_commit: int = 60*1000, auto_backup: bool = False, timeout_backup: int = 60*1000,
            export_functions = None
    ) -> None:
        self.is_server = server
        self.do_commit = False
        self.do_backup = False
        self.terminate = False
        self.exc_result = {}
        self.timeout_commit = None
        self.auto_backup = None
        self.timeout_backup = None
        self.sqlq = None
        self.sqlq_worker = None
        self.worker_dead = None
        self.functions = None
        self.ioerror = False
        self.exploded_reason = None
        self.sc = None
        if self.is_server:
            self.timeout_commit = timeout_commit
            self.auto_backup = auto_backup
            self.timeout_backup = timeout_backup
            self.sqlq = queue.Queue()
            self.sqlq_worker = threading.Thread(target=self.worker, args=(db,))
            self.sqlq_worker.daemon = True
            self.sqlq_worker.start()
            self.worker_dead = False
            self.functions = dict(sql=self.sql, backup=self.backup, commit=self.commit)
            if export_functions:
                self.functions.update(export_functions=export_functions)

    async def _sql_async(self, tid: int, sql: str, data: tuple = (), row_factory: str = "row", _cmd: str = "sql", loop: asyncio.AbstractEventLoop = None) -> list:
        if self.is_server:
            if _cmd == "sql":
                self.sqlq.put([tid, sql, data, row_factory])
                while True:
                    try:
                        return self.exc_result.pop(tid)
                    except:
                        await asyncio.sleep(2/1000, loop=loop)
            else:
                try:
                    return self.functions[_cmd](*[sql, data, row_factory])
                except Exception as e:
                    return e
        else:
            return self.sc().request(command=_cmd, data=args(sql, data, row_factory))

    def _sql(self, tid: int, sql: str, data: tuple = (), row_factory: str = "row", _cmd: str = "sql") -> list:
        if self.is_server:
            if _cmd == "sql":
                self.sqlq.put([tid, sql, data, row_factory])
                while True:
                    try:
                        return self.exc_result.pop(tid)
                    except:
                        time.sleep(2/1000)
            else:
                try:
                    return self.functions[_cmd](*[sql, data, row_factory])
                except Exception as e:
                    return e
        else:
            return self.sc().request(command=_cmd, data=args(sql, data, row_factory))

    def sql_(self, exc_type: str, sql: str, data: tuple = (), row_factory: str = "row",
            result= None, key= None, _cmd: str = "sql") -> list:
        if result is None:
            result = {}
        if key is None:
            key = 0
        try:
            sql = " ".join([line.strip() for line in sql.splitlines() if not line.strip().startswith("--")]).strip()
        except:
            pass

        def job1():
            return self._sql(threading.get_ident(), sql, data, row_factory, _cmd)

        def job2():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            twa = ThreadWrapper_async(asyncio.Semaphore(1), loop=loop)
            twa.add(job=self._sql_async(threading.get_ident(), sql, data, row_factory, _cmd), result=result, key=key)
            twa.wait()

        tw = ThreadWrapper(threading.Semaphore(1))
        if exc_type == "async":
            tw.add(job=job2)
        else:
            tw.add(job=job1, result=result, key=key)
        tw.wait()
        if isinstance(result[key], Exception):
            if isinstance(result[key], sqlite3.OperationalError):
                if "i/o" in str(result[key]).lower():
                    self.ioerror = True
                    try:
                        raise result[key]
                    except:
                        self.exploded_reason = traceback.format_exc()
            raise result[key]
        return result[key]

    def sql(self, *args, **kwargs):
        return self.sql_("", *args, **kwargs)

    def sql_async(self, *args, **kwargs):
        return self.sql_("async", *args, **kwargs)


class SqlQueueE(SqlQueue):
    def __init__(self, *, host = "127.199.71.10", db_port: int = None, key_pair: key_pair_format = None, **kwargs) -> None:
        super().__init__(**kwargs)
        port = db_port if db_port else 39292
        from encryptedsocket import SC, SS
        if self.is_server:
            if key_pair is None:
                key_pair = EasyRSA(bits=1024).gen_key_pair()
            self.ss = SS(key_pair=key_pair, functions=self.functions, host=host, port=port, silent=True)
            thread = threading.Thread(target=self.ss.start)
            thread.daemon = True
            thread.start()
        else:
            self.sc = lambda: SC(host=host, port=port)

    def stop(self):
        super().stop()
        if self.is_server:
            self.ss.stop()
        return True


class SqlQueueU(SqlQueue):
    def __init__(self, *, host = "127.199.71.10", db_port: int = None, **kwargs) -> None:
        super().__init__(**kwargs)
        port = db_port if db_port else 39292
        from unencryptedsocket import SC, SS
        if self.is_server:
            self.ss = SS(functions=self.functions, host=host, port=port, silent=True)
            thread = threading.Thread(target=self.ss.start)
            thread.daemon = True
            thread.start()
        else:
            self.sc = lambda: SC(host=host, port=port)

    def stop(self):
        super().stop()
        if self.is_server:
            self.ss.stop()
        return True


