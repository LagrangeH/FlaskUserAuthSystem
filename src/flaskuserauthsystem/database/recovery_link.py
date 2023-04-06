import secrets
from datetime import datetime, timedelta
from typing import Optional

from loguru import logger as log

from src.flaskuserauthsystem import db


class RecoveryLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # TODO: Check uniqueness
    link_token = db.Column(db.String(128), nullable=False, unique=True, default=secrets.token_urlsafe(32))
    attempts = db.Column(db.Integer, nullable=False, default=10)
    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    lifetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + timedelta(days=1))

    def __repr__(self):
        return f'<RecoveryLink password {self.id!r} for user {self.id}>'

    def __int__(self):
        return self.id

    @log.catch()
    def update(self) -> None:
        """
        Update recovery link in database
        :return:
        """
        db.session.commit()
        log.debug(f'{self} has been updated!')

    @log.catch()
    def create(self) -> None:
        """
        Create new recovery link in database
        :return:
        """
        db.session.add(self)
        self.update()
        log.debug(f'{self} has been created!')

    @log.catch()
    def delete(self) -> None:
        """
        Delete recovery link from database
        :return:
        """
        db.session.delete(self)
        self.update()
        log.debug(f'{self} has been deleted!')

    @log.catch()
    def is_expired(self) -> bool:
        """
        Checks for link expiration based on time and number of `attempts`
        :return:
        """
        return datetime.utcnow() > self.creation_date + self.lifetime or self.attempts <= 0

    @log.catch()
    def decrease_attempts(self) -> None:
        """
        Decrease `attempts` of recovery link
        :return:
        """
        self.attempts -= 1
        self.update()

    @log.catch()
    def use_link(self) -> None:
        """
        Delete recovery link if it is expired or decrease attempts
        :return:
        """
        if self is None:
            return None
        if self.is_expired():
            return self.delete()
        self.decrease_attempts()

    @staticmethod
    @log.catch()
    def _get_first(**kwargs) -> Optional['RecoveryLink']:
        """
        Get the first recovery link from the database by the given parameter[s]
        :param kwargs: Parameters to filter by
        :return: RecoveryLink object or None
        """
        link: RecoveryLink | None = db.session.query(RecoveryLink).filter_by(**kwargs).first()
        if link is not None:
            link.use_link()
        return link

    @classmethod
    @log.catch()
    def get_by_id(cls, _id: int, /) -> Optional['RecoveryLink']:
        """
        Get recovery link by id
        :param _id:
        :return:
        """
        return cls._get_first(id=_id)

    @classmethod
    @log.catch()
    def get_by_link_token(cls, link_token: str, /) -> Optional['RecoveryLink']:
        """
        Get recovery link by token
        :param link_token:
        :return: RecoveryLink object or None
        """
        return cls._get_first(link_token=link_token)

    @staticmethod
    @log.catch()
    def get_all_by_user_id(user_id: int, /) -> list[Optional['RecoveryLink']]:
        """
        Get all recovery links for some user by user id
        :param user_id:
        :return: List of RecoveryLink objects
        """
        return db.session.query(RecoveryLink).filter_by(user_id=user_id).all()
