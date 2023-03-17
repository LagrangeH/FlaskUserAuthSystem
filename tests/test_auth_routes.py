def test_auth(client):
    response = client.get('/auth')
    assert response.status_code in (302, 308)


def test_signup(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200


def test_signin(client):
    response = client.get('/auth/signin')
    assert response.status_code == 200


def test_reset_password(client):
    response = client.get('/auth/reset-password')
    assert response.status_code == 200


def test_restore_password(client):
    response = client.get('/auth/restore-password')
    assert response.status_code == 200


def test_signout(client):
    response = client.get('/auth/signout')
    assert response.status_code == 302
