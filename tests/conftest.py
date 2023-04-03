import os
from pathlib import Path

import pytest

from src.flaskuserauthsystem import db
from src.flaskuserauthsystem import create_app


@pytest.fixture
def app():
    # Without this, tests will return an ImportError
    for path in Path.cwd().glob('src/*'):
        os.chdir(path)
        break

    _app = create_app(testing=True)

    yield _app

    with _app.app_context():
        db.drop_all()
        db.session.commit()
        db.session.close()
    # os.remove('../../instance/test.db')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
