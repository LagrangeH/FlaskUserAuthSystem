from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from loguru import logger as log


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


@log.catch()
def _register_blueprints(app: Flask) -> None:
    from src.flaskuserauthsystem.blueprints import main, auth, errors
    app.register_blueprint(errors.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)


@log.catch()
def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    # Load the configuration from the instance folder
    if testing:
        from src.flaskuserauthsystem.config import app_test_config as config
    else:
        from src.flaskuserauthsystem.config import app_config as config

    app.config.from_object(config)

    # Disable standard Flask's logger that will be redirected to Loguru
    app.logger.disabled = True

    from src.flaskuserauthsystem.config.log_config import configure_logging
    configure_logging(debug=app.config['DEBUG'], testing=testing)

    # Initialize the extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from src.flaskuserauthsystem.database.user import User
    from src.flaskuserauthsystem.database.recovery_link import RecoveryLink

    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        return User.get_by_id(user_id)

    login_manager.login_view = 'auth.signin'

    with app.app_context():
        db.create_all()

    _register_blueprints(app)

    return app
