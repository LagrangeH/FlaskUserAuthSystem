from datetime import datetime

from flask_login import UserMixin

from . import get_db


class User(UserMixin, get_db().Model):
    id = get_db().Column(get_db().Integer, primary_key=True)
    username = get_db().Column(get_db().String(80), unique=True, nullable=False)
    email = get_db().Column(get_db().String(120), unique=True, nullable=False)
    password_hash = get_db().Column(get_db().String(128), nullable=False)
    registration_date = get_db().Column(get_db().DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username!r}>'

    def __int__(self):
        return self.id
