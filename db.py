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
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
