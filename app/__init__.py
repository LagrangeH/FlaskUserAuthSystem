import functools
import secrets

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from loguru import logger as log

from database import DB
from log_config import configure_logging


# login_manager = LoginManager()
# login_manager.login_view = 'signin'
# login_manager.init_app(app)


def create_app(debug: bool = False) -> Flask:
    configure_logging(debug=debug)

    # App initialization
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.obj'
    app.secret_key = secrets.token_hex()
    app.debug = debug
    # app.teardown_appcontext(close_db)

    # Database initialization
    app.app_context().push()
    DB.obj.init_app(app)

    # Blueprints registration
    from blueprints import main, auth
    main.bp.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # Database creation
    from database import models
    with app.app_context():
        DB.obj.create_all()

    return app
