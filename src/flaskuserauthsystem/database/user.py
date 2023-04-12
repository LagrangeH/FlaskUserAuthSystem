from datetime import datetime
from typing import Optional

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
    def update(self) -> None:
        """
        Update user in database
        :return:
        """
        db.session.commit()
        log.debug(f'{self} has been updated!')

    @log.catch()
    def create(self) -> None:
        """
        Create user in database
        :return:
        """
        db.session.add(self)
        self.update()
        log.debug(f'User <{self}> has been registered!')

    @log.catch()
    def delete(self) -> None:
        """
        Delete user from database
        :return:
        """
        db.session.delete(self)
        self.update()
        log.debug(f'User <{self}> has been deleted!')

    @staticmethod
    @log.catch()
    def is_username_registered(username: str, /) -> bool:
        """
        Checks if the username exists in the `user` db table
        :param username:
        :return:
        """
        return bool(User.query.filter(
            func.lower(User.username) == func.lower(username)
        ).first())

    @staticmethod
    @log.catch()
    def is_email_registered(email: username, /) -> bool:
        return bool(User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).first())

    @staticmethod
    @log.catch()
    def get_by_email(email, /) -> Optional['User']:
        """
        Check for None value should be implemented in the caller!
        :param email:
        :return:
        """
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    @log.catch()
    def get_by_username(username, /) -> Optional['User']:
        """
        Check for None value should be implemented in the caller!
        :param username:
        :return:
        """
        return db.session.query(User).filter_by(username=username).first()

    @staticmethod
    @log.catch()
    def get_by_id(_id, /) -> Optional['User']:
        """
        Check for None value should be implemented in the caller!
        :param _id:
        :return:
        """
        return db.session.query(User).filter_by(id=_id).first()
