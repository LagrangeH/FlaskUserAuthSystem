import secrets

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from loguru import logger as log


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(debug: bool = False) -> Flask:
    from src.flaskuserauthsystem.log_config import configure_logging
    configure_logging(debug=debug)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['RECAPTCHA_PUBLIC_KEY'] = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    app.config['RECAPTCHA_PRIVATE_KEY'] = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    app.config['WTF_CSRF_SECRET_KEY'] = secrets.token_hex()
    app.secret_key = secrets.token_hex()
    app.debug = debug

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from src.flaskuserauthsystem.database.models import User
    from src.flaskuserauthsystem.database.queries import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        return get_user_by_id(user_id)

    from src.flaskuserauthsystem.blueprints import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    log.debug(f"App created with debug={debug}")
    return app
