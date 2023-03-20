import secrets
from dataclasses import dataclass
from pathlib import Path

from environs import Env
from loguru import logger as log

env = Env()
env.read_env(path=str(Path("envs/.env").resolve()))


DEBUG: bool = env.bool("FLASK_DEBUG", default=False)
FLASK_TEST: bool = env.bool("FLASK_TEST", default=False)
SECRET_KEY: str = env.str("SECRET_KEY", default=secrets.token_hex())
RECAPTCHA_PUBLIC_KEY: str = env.str("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY: str = env.str("RECAPTCHA_PRIVATE_KEY")
WTF_CSRF_SECRET_KEY: str = env.str("WTF_CSRF_SECRET_KEY", default=secrets.token_hex())
SQLALCHEMY_DATABASE_URI: str = env.str(
    "SQLALCHEMY_DATABASE_URI",
    validate=lambda x: x.startswith("sqlite://"),
)
