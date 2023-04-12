import secrets

from src.flaskuserauthsystem.config import env

# Flask
DEBUG: bool = env.bool("FLASK_DEBUG", default=False)
SECRET_KEY: str = env.str("SECRET_KEY", default=secrets.token_hex())

# Flask-WTF
RECAPTCHA_PUBLIC_KEY: str = env.str(
    "RECAPTCHA_PUBLIC_KEY",
    validate=lambda x: bool(x),
)
RECAPTCHA_PRIVATE_KEY: str = env.str(
    "RECAPTCHA_PRIVATE_KEY",
    validate=lambda x: bool(x),
)
WTF_CSRF_SECRET_KEY: str = env.str("WTF_CSRF_SECRET_KEY", default=secrets.token_hex())

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI: str = env.str(
    "SQLALCHEMY_DATABASE_URI",
    validate=lambda x: x.startswith("sqlite://"),
)

# Flask-Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = DEBUG
MAIL_USERNAME = 'maxsergeev39@gmail.com'
MAIL_PASSWORD = env.str("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = 'maxsergeev39@gmail.com'
# MAIL_MAX_EMAILS =
# MAIL_SUPPRESS_SEND =
# MAIL_ASCII_ATTACHMENTS = False
