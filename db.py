import time
import mysql.connector
from flask import g, current_app

def get_db():
    if "db" not in g:
        cfg = current_app.config
        g.db = mysql.connector.connect(
            host     = cfg["MYSQL_HOST"],
            port     = cfg["MYSQL_PORT"],
            user     = cfg["MYSQL_USER"],
            password = cfg["MYSQL_PASSWORD"],
            database = cfg["MYSQL_DB"],
        )
        g.query_log = []
    return g.db

def get_cursor():
    db = get_db()
    return LoggingCursor(db, g.query_log)

def get_query_log():
    return getattr(g, "query_log", [])

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)


class LoggingCursor:
    def __init__(self, db, log):
        self._cursor = db.cursor(dictionary=True)
        self._log    = log

    def execute(self, query, params=None):
        start = time.perf_counter()
        self._cursor.execute(query, params)
        elapsed = (time.perf_counter() - start) * 1000
        clean = " ".join(query.split())
        self._log.append({"sql": clean, "ms": round(elapsed, 2)})

    def fetchall(self):
        return self._cursor.fetchall()

    def fetchone(self):
        return self._cursor.fetchone()
