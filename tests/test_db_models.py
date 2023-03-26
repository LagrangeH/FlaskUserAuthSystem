from datetime import datetime

from src.flaskuserauthsystem import db
from src.flaskuserauthsystem.database import queries
from src.flaskuserauthsystem.database.models import User
from tests import fake


def test_create_user(app):
    username, email, password = fake.user_name(), fake.email(), fake.password()
    user = User(username=username, email=email, password_hash=password)

    db.session.add(user)
    db_user = queries.get_user_by_username(username)

    assert db_user.id is not None
    assert db_user.username is not None
    assert db_user.email is not None
    assert db_user.password_hash is not None
    assert db_user.registration_date <= datetime.utcnow()
