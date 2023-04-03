def test_auth_redirect(client):
    response = client.get('/auth')
    assert response.status_code == 308


def test_signup(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200


def test_signin(client):
    response = client.get('/auth/signin')
    assert response.status_code == 200


def test_reset_password(client):
    response = client.get('/auth/reset-password')
    assert response.status_code == 200


def test_restore_password_without_token(client):
    response = client.get('/auth/restore-password')
    assert response.status_code == 404


# TODO: Write test for restore-password with token
# def test_restore_password_with_token(client):
#     response = client.get('/auth/restore-password/123')
#     assert response.status_code == 200


def test_signout_redirect(client):
    response = client.get('/auth/signout')
    assert response.status_code == 302
    assert response.location == '/'
