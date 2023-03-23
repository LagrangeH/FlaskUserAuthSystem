import os
import secrets
from pathlib import Path

import pytest

from src.flaskuserauthsystem.app import create_app
from loguru import logger as log


@pytest.fixture
def app():
    # Without this, tests will return an ImportError
    for path in Path.cwd().glob('src/*'):
        os.chdir(path)
        break

    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
