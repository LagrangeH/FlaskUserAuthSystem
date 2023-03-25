from tests import authorized_user


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


@authorized_user
def test_profile_authorized(client):
    response = client.get('/profile')
    assert response.status_code == 200


def test_profile(client):
    response = client.get('/profile')
    assert response.status_code == 302
