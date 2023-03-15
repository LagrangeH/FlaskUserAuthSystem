import functools
import secrets

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from loguru import logger as log

from database import get_db


# login_manager = LoginManager()
# login_manager.login_view = 'signin'
# login_manager.init_app(app)


def configure_logging(debug=False) -> None:
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


def create_app(debug: bool = False) -> Flask:
    """
    Creates Flask app. When calling app.run() method, debug parameter is passed automatically.
    :param debug: debug mode for logging and for Flask app
    :return:
    """
    configure_logging(debug=debug)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.secret_key = secrets.token_hex()
    app.app_context().push()

    db = get_db(app=app)

    from blueprints import main, auth
    main.bp.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    from database import models
    with app.app_context():
        db.create_all()

    def _run(func: callable, d: bool = False) -> callable:
        """
        Decorator for app.run() method.
        It allows to automatically pass debug parameter to app.run() method
        from debug argument of create_app() to avoid passing it manually.
        """
        if func.__name__ != 'run':
            raise ValueError('Passed function is not app.run() method')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(d, *args, **kwargs)

        return wrapper

    app.run = _run(app.run, debug)

    return app
