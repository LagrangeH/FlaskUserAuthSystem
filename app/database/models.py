from datetime import datetime

from flask_login import UserMixin

from . import DB


class User(UserMixin, DB.obj.Model):
    id = DB.obj.Column(DB.obj.Integer, primary_key=True)
    username = DB.obj.Column(DB.obj.String(80), unique=True, nullable=False)
    email = DB.obj.Column(DB.obj.String(120), unique=True, nullable=False)
    password_hash = DB.obj.Column(DB.obj.String(128), nullable=False)
    registration_date = DB.obj.Column(DB.obj.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username!r}>'

    def __int__(self):
        return self.id
