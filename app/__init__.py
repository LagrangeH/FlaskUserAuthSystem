import secrets

from flask import Flask
from flask_login import LoginManager
from loguru import logger as log

from database import DB
from database.models import User
from database.queries import get_user_by_id
from log_config import configure_logging


def create_app(debug: bool = False) -> Flask:
    configure_logging(debug=debug)

    # App initialization
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.secret_key = secrets.token_hex()
    app.debug = debug

    # Database initialization
    app.app_context().push()
    DB.obj.init_app(app)

    # Login manager initialization
    login_manager = LoginManager()
    login_manager.login_view = 'signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        return get_user_by_id(user_id)

    # Blueprints registration
    from blueprints import main, auth
    main.bp.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # Database creation
    from database import models
    with app.app_context():
        DB.obj.create_all()

    log.debug(f"App created with debug={debug}")
    return app
