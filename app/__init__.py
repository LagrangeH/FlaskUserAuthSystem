import secrets

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
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
    app.config['RECAPTCHA_PUBLIC_KEY'] = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    app.config['RECAPTCHA_PRIVATE_KEY'] = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    app.config['WTF_CSRF_SECRET_KEY'] = secrets.token_hex()
    app.secret_key = secrets.token_hex()
    app.debug = debug

    # Pushing app context
    app.app_context().push()

    # Database initialization
    DB.obj.init_app(app)

    # Login manager initialization
    login_manager = LoginManager(app)
    login_manager.login_view = 'signin'

    # CSRF protection initialization
    csrf = CSRFProtect(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        print(f"User {user_id} loaded\n{User.query.get(user_id)}")
        return User.query.get(user_id)

    # Blueprints registration
    from blueprints import main, auth
    main.bp.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # Database creation
    from database import models
    DB.obj.create_all()

    log.debug(f"App created with debug={debug}")
    return app
