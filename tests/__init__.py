import functools

from faker import Faker
from flask_login import login_user, logout_user, current_user

from src.flaskuserauthsystem.database.user import User


fake = Faker()


def authorized_user(test_func: callable):
    @functools.wraps(test_func)
    def wrapper(client, *args, **kwargs):
        with client:
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password_hash=fake.password(),
            )

            user.create()
            login_user(user)
            test_result = test_func(client, *args, **kwargs)
            assert current_user.is_authenticated
            logout_user()
            assert not current_user.is_authenticated
            return test_result

    return wrapper
