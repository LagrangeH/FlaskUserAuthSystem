from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from loguru import logger as log


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)


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

    # Create tables if they don't exist
    # from db.models import User
    #
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)
