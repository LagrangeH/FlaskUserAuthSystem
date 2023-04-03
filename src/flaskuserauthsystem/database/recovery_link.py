import secrets
from datetime import datetime, timedelta

from loguru import logger as log

from src.flaskuserauthsystem import db
from src.flaskuserauthsystem.utils.password import check_password


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
    def create(self):
        db.session.add(self)
        db.session.commit()
        log.debug(f'{self} has been created!')

    @log.catch()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        log.debug(f'{self} has been deleted!')

    @log.catch()
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.creation_date + self.lifetime or self.attempts <= 0

    @log.catch()
    def delete_if_expired(self):
        if self.is_expired():
            self.delete()

    @log.catch()
    def is_valid(self, password_hash) -> bool:
        return check_password(self.password_hash, password_hash)

    @log.catch()
    def decrease_attempts(self):
        self.attempts -= 1
        db.session.commit()

    @classmethod
    @log.catch()
    def get_by_link_token(cls, link_token, /):
        return db.session.query(RecoveryLink).filter_by(link_token=link_token).first()

    @classmethod
    @log.catch()
    def get_all_by_user_id(cls, user_id, /):
        return db.session.query(RecoveryLink).filter_by(user_id=user_id).all()

    @classmethod
    @log.catch()
    def get_by_id(cls, _id, /):
        return db.session.query(RecoveryLink).filter_by(id=_id).first()
