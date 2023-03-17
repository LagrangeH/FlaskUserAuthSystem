def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_signup(client):
    response = client.get('/')
    assert response.status_code == 200

