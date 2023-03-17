def test_404(client):
    response = client.get('/invalid_url')
    assert response.status_code == 404
