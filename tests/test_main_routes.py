def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_profile(client):
    response = client.get('/profile')
    assert response.status_code == 302
