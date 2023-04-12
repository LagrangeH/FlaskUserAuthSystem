from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from src.flaskuserauthsystem import db
from src.flaskuserauthsystem.database.recovery_link import RecoveryLink
from src.flaskuserauthsystem.database.user import User
from tests import fake


def test_create_user(app):
    username, email, password = fake.user_name(), fake.email(), fake.password()
    user = User(username=username, email=email, password_hash=password)
    user.create()
    db_user = User.get_by_username(username)

    assert db_user.id is not None
    assert db_user.username is not None
    assert db_user.email is not None
    assert db_user.password_hash is not None
    assert db_user.registration_date <= datetime.utcnow()


def test_create_recovery_password(app):
    # Create a user to associate with the recovery password
    username, email, password = fake.user_name(), fake.email(), fake.password()
    user = User(username=username, email=email, password_hash=password)
    user.create()
    db_user = User.get_by_username(username)

    # Create a recovery password for the user
    recovery_password = RecoveryLink(user_id=db_user.id)
    recovery_password.create()
    # db_recovery_password = RecoveryPassword.query.filter_by(user_id=db_user.id).first()

    # Check that the recovery password was added to the database
    # assert db_recovery_password in db.session

    # Check that the link token is unique
    # with pytest.raises(IntegrityError):
    #     recovery_password2 = RecoveryPassword(user_id=user.id, password_hash=recovery_password_hash, link_token=recovery_password.link_token)
    #     recovery_password2.create()

    # Check that the expiration_date and attempts fields were set correctly
    # assert recovery_password.expiration_date > 0
    # assert recovery_password.attempts > 0


"""
import pytest
from datetime import datetime, timedelta
from myapp.models import RecoveryPassword, User


@pytest.fixture(scope="module")
def new_user():
    user = User(name="Test User", email="test@example.com")
    user.create()
    return user


@pytest.fixture(scope="module")
def new_recovery_password(new_user):
    password = RecoveryPassword(
        user_id=new_user.id,
        password_hash="test_password_hash",
        expiration_date=timedelta(days=1),
        attempts=10,
    )
    password.create()
    return password


def test_create_recovery_password(new_user):
    password = RecoveryPassword(
        user_id=new_user.id,
        password_hash="test_password_hash",
        expiration_date=timedelta(days=1),
        attempts=10,
    )
    password.create()

    assert password.id is not None
    assert password.user_id == new_user.id
    assert password.password_hash == "test_password_hash"
    assert password.link_token is not None


def test_delete_recovery_password(new_recovery_password):
    password_id = new_recovery_password.id
    new_recovery_password.delete()

    assert RecoveryPassword.get_by_id(password_id) is None


def test_is_expired_recovery_password(new_recovery_password):
    new_recovery_password.creation_date = datetime.utcnow() - timedelta(days=2)
    assert new_recovery_password.is_expired() is True

    new_recovery_password.creation_date = datetime.utcnow()
    assert new_recovery_password.is_expired() is False


def test_delete_if_expired_recovery_password(new_recovery_password):
    new_recovery_password.creation_date = datetime.utcnow() - timedelta(days=2)
    new_recovery_password.delete_if_expired()

    assert RecoveryPassword.get_by_id(new_recovery_password.id) is None


def test_is_valid_recovery_password(new_recovery_password):
    assert new_recovery_password.is_valid("test_password_hash") is True
    assert new_recovery_password.is_valid("wrong_password_hash") is False


def test_decrease_attempts_recovery_password(new_recovery_password):
    new_recovery_password.decrease_attempts()
    assert new_recovery_password.attempts == 9


def test_get_by_link_token_recovery_password(new_recovery_password):
    password_by_link = RecoveryPassword.get_by_link_token(new_recovery_password.link_token)

    assert password_by_link.id == new_recovery_password.id
    assert password_by_link.user_id == new_recovery_password.user_id
    assert password_by_link.link_token == new_recovery_password.link_token


def test_get_all_by_user_id_recovery_password(new_recovery_password):
    all_passwords = RecoveryPassword.get_all_by_user_id(new_recovery_password.user_id)

    assert len(all_passwords) == 1
    assert all_passwords[0].id == new_recovery_password.id
    assert all_passwords[0].user_id == new_recovery_password.user_id
    assert all_passwords[0].link_token == new_recovery_password.link_token


def test_get_by_id_recovery_password(new_recovery_password):
    password_by_id = RecoveryPassword.get_by_id(new_recovery_password.id)

    assert password_by_id.id == new_recovery_password.id
    assert password_by_id.user_id == new_recovery_password.user_id
    assert password_by_id.link_token == new_recovery_password.link_token

"""
