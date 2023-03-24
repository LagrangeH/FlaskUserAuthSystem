import secrets

from src.flaskuserauthsystem.config import env


DEBUG: bool = env.bool("FLASK_DEBUG", default=False)
SECRET_KEY: str = env.str("SECRET_KEY", default=secrets.token_hex())
WTF_CSRF_SECRET_KEY: str = env.str("WTF_CSRF_SECRET_KEY", default=secrets.token_hex())
SQLALCHEMY_DATABASE_URI: str = env.str(
    "SQLALCHEMY_DATABASE_URI",
    validate=lambda x: x.startswith("sqlite://"),
)
