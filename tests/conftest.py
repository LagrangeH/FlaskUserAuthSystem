import pytest
from src.flaskuserauthsystem.app import create_app


@pytest.fixture
def app():
    application = create_app(debug=False)
    application.config['TESTING'] = True
    return application


@pytest.fixture
def client(application):
    return application.test_client()
