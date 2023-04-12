from flask_login import current_user

from tests import authorized_user


def test_index(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == '/auth/signin'
    assert not current_user.is_authenticated


@authorized_user
def test_index_authed(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == '/profile'


def test_profile(client):
    response = client.get('/profile')
    assert response.status_code == 302
    assert response.location == '/auth/signin?next=%2Fprofile'
    assert not current_user.is_authenticated


@authorized_user
def test_profile_authed(client):
    response = client.get('/profile')
    assert response.status_code == 200
    assert response.location is None
