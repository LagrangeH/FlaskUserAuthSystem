from tests import fake


def test_404(client):
    response = client.get('/invalid_url')
    assert response.status_code == 404


def test_csrf_missing(client):

    fake_password = fake.password()

    response = client.post('/auth/signin', data={
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake_password,
        'confirm_password': fake_password,
    })

    assert response.status_code == 400
    assert b"The CSRF token is missing" in response.data

