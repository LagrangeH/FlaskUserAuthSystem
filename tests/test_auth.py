from faker import Faker

from src.flaskuserauthsystem.database.models import User
from src.flaskuserauthsystem import db


fake = Faker()


def test_signup_successful(client, app):
    fake_password = fake.password()
    app.config['WTF_CSRF_ENABLED'] = False

    response = client.post('/auth/signup', data={
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake_password,
        'confirm_password': fake_password,
    })

    assert response.status_code == 302
    assert response.location == '/profile'
    app.config['WTF_CSRF_ENABLED'] = True


def test_signup_email_already_registered(client, app):
    app.config['WTF_CSRF_ENABLED'] = False
    fake_password = fake.password()
    fake_email = fake.email()

    db.session.add(User(
        username=fake.user_name(),
        email=fake_email,
        password_hash=fake.password(),
    ))
    db.session.commit()

    response = client.post('/auth/signup', data={
        'username': fake.user_name(),
        'email': fake_email,
        'password': fake_password,
        'confirm_password': fake_password,
    })

    assert response.status_code == 200
    assert response.location is None


def test_signup_username_already_registered(client, app):
    app.config['WTF_CSRF_ENABLED'] = False
    fake_password = fake.password()
    fake_username = fake.user_name()

    db.session.add(User(
        username=fake_username,
        email=fake.email(),
        password_hash=fake.password(),
    ))
    db.session.commit()

    response = client.post('/auth/signup', data={
        'username': fake_username,
        'email': fake.email(),
        'password': fake_password,
        'confirm_password': fake_password,
    })

    assert response.status_code == 200
    assert response.location is None


# def test_signup_password_not_matching(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass
#
#
# def test_signup_password_too_short(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_too_long(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_uppercase(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_lowercase(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_number(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_special_character(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_whitespace(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_username(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_password_no_email(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_email_invalid(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_empty_username(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_empty_email(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_empty_password(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
#
#
# def test_signup_empty_confirm_password(client, app):
#     app.config['WTF_CSRF_ENABLED'] = False
#     pass    # TODO: add test
