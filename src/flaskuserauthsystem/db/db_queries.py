from flaskuserauthsystem.loader import db
from db_models import User


def is_username_registered(username) -> bool:
    # TODO: make case insensitive
    return db.session.query(User.id).filter_by(username=username).scalar() is not None


def is_email_registered(email) -> bool:
    # TODO: make case insensitive
    return db.session.query(User.id).filter_by(email=email).scalar() is not None
