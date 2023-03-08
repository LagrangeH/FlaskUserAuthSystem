from db_models import User
from loader import db


def username_registered(username) -> bool:
    # TODO: make case insensitive
    return db.session.query(User.id).filter_by(username=username).scalar() is not None


def email_registered(email) -> bool:
    # TODO: make case insensitive
    return db.session.query(User.id).filter_by(email=email).scalar() is not None
