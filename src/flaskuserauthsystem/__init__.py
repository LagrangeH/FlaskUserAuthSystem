from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    if testing:
        from src.flaskuserauthsystem.config import app_test_config as config
    else:
        from src.flaskuserauthsystem.config import app_config as config

    app.config.from_object(config)

    from src.flaskuserauthsystem.config.log_config import configure_logging
    configure_logging(debug=app.config['DEBUG'])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from src.flaskuserauthsystem.database.models import User
    from src.flaskuserauthsystem.database.queries import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        return get_user_by_id(user_id)

    login_manager.login_view = 'auth.signin'

    with app.app_context():
        db.create_all()

    from src.flaskuserauthsystem.blueprints import main, auth, errors
    app.register_blueprint(errors.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app
