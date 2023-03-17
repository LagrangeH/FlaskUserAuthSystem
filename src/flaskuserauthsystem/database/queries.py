from loguru import logger as log

from .models import User
from . import DB


def is_username_registered(username) -> bool:
    # TODO: make case insensitive
    return DB.obj.session.query(User.id).filter_by(username=username).scalar() is not None


def is_email_registered(email) -> bool:
    # TODO: make case insensitive
    return DB.obj.session.query(User.id).filter_by(email=email).scalar() is not None


def create_user(new_user: User):
    DB.obj.session.add(new_user)
    DB.obj.session.commit()
    log.debug(f'{new_user} has been registered!')


def get_user_by_email(email) -> User | None:
    return DB.obj.session.query(User).filter_by(email=email).first()
