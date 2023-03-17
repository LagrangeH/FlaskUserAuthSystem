import secrets

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from loguru import logger as log

from src.flaskuserauthsystem.database import DB
from src.flaskuserauthsystem.database.models import User
from src.flaskuserauthsystem.database.queries import get_user_by_id
from src.flaskuserauthsystem.log_config import configure_logging


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
        return get_user_by_id(user_id)

    # Blueprints registration
    from src.flaskuserauthsystem.blueprints import main, auth
    main.bp.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # Database creation
    from src.flaskuserauthsystem.database import models
    DB.obj.create_all()

    log.debug(f"App created with debug={debug}")
    return app


if __name__ == '__main__':
    create_app(debug=True).run()
