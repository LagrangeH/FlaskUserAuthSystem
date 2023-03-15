from loguru import logger as log

from .models import User
from . import get_db


def is_username_registered(username) -> bool:
    # TODO: make case insensitive
    return get_db().session.query(User.id).filter_by(username=username).scalar() is not None


def is_email_registered(email) -> bool:
    # TODO: make case insensitive
    return get_db().session.query(User.id).filter_by(email=email).scalar() is not None


def create_user(new_user: User):
    get_db().session.add(new_user)
    get_db().session.commit()
    log.debug(f'{new_user} has been registered!')


def get_user_by_email(email) -> User | None:
    return get_db().session.query(User).filter_by(email=email).first()
