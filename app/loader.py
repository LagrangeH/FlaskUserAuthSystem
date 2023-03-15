import secrets

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from loguru import logger as log


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.secret_key = secrets.token_hex()
db = SQLAlchemy(app)
login_manager = LoginManager(app)


def configure_logging(debug=False):
    if debug:
        log.add(
            'logs/debug.log',
            level='DEBUG',
            colorize=True,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=False,
        )


def run_app(debug=False):
    configure_logging(debug=debug)
    app.run(debug=True)
