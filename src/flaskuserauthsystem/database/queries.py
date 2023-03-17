from loguru import logger as log
from sqlalchemy import func

from .models import User
from . import DB


def is_username_registered(username) -> bool:
    return bool(User.query.filter(func.lower(User.username) == func.lower(username)).first())


def is_email_registered(email) -> bool:
    return bool(User.query.filter(func.lower(User.email) == func.lower(email)).first())


def create_user(new_user: User):
    DB.obj.session.add(new_user)
    DB.obj.session.commit()
    log.debug(f'{new_user} has been registered!')


def get_user_by_email(email) -> User | None:
    return DB.obj.session.query(User).filter_by(email=email).first()


def get_user_by_username(username) -> User | None:
    return DB.obj.session.query(User).filter_by(username=username).first()


def get_user_by_id(user_id) -> User | None:
    return DB.obj.session.query(User).filter_by(id=user_id).first()
