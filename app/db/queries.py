from loguru import logger as log

from .models import User
from loader import db


def is_username_registered(username) -> bool:
    # TODO: make case insensitive
    return db.session.query(User.id).filter_by(username=username).scalar() is not None


def is_email_registered(email) -> bool:
    # TODO: make case insensitive
    return db.session.query(User.id).filter_by(email=email).scalar() is not None


def create_user(new_user: User):
    db.session.add(new_user)
    db.session.commit()
    log.debug(f'{new_user} has been registered!')
