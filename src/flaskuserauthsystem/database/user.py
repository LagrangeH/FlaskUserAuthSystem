from datetime import datetime

from flask_login import UserMixin
from loguru import logger as log
from sqlalchemy import func

from src.flaskuserauthsystem import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recovery_links = db.relationship(
        'RecoveryLink',
        backref='user',
        lazy=True
    )

    def __repr__(self):
        return f'<User {self.username!r}>'

    def __int__(self):
        return self.id

    @log.catch()
    def create(self):
        db.session.add(self)
        db.session.commit()
        log.debug(f'User <{self}> has been registered!')

    @log.catch()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        log.debug(f'User <{self}> has been deleted!')

    @classmethod
    @log.catch()
    def is_username_registered(cls, username, /) -> bool:
        return bool(User.query.filter(
            func.lower(User.username) == func.lower(username)
        ).first())

    @classmethod
    @log.catch()
    def is_email_registered(cls, email, /) -> bool:
        return bool(User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).first())

    @classmethod
    @log.catch()
    def get_by_email(cls, email, /):
        return db.session.query(User).filter_by(email=email).first()

    @classmethod
    @log.catch()
    def get_by_username(cls, username, /):
        return db.session.query(User).filter_by(username=username).first()

    @classmethod
    @log.catch()
    def get_by_id(cls, _id, /):
        return db.session.query(User).filter_by(id=_id).first()
