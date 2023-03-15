from loguru import logger as log

from flask import g, Flask
from flask_sqlalchemy import SQLAlchemy


def get_db(app: Flask = None) -> SQLAlchemy:
    if 'db' not in g:
        g.db = SQLAlchemy()
        g.db.init_app(app)
    return g.db


def close_db(e=None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()
