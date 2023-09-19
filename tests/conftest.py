import os
import tempfile
import pytest
from app import create_app
from db import create_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), mode='rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Fixture for the app: creates the database and its tables, inserts test data; calls the factory and passes
    test_config to configure the application and database for testing """
    # file descriptor and path to the TEMPORARY file
    db_fd, db_path = tempfile.mkstemp()

    # test configuration of the app and database
    app = create_app(
        {'TESTING': True,
         'DATABASE': db_path}
    )

    with app.app_context():
        create_db()
        # query to the test database(written in the data.sql)
        get_db().executescript(_data_sql)

    yield app

    # temporary file is closed and removed after the test is over
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A client used in tests to make requests to the application without running the server"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Calls Click commands registered with the application"""
    return app.test_cli_runner()


class AuthActions(object):
    """POST- and GET-requests to authorization functions with the help of a client"""

    def __init__(self, client):
        # client-fixture
        self._client = client

    def login(self, username='test_name', password='test'):
        return self._client.post('/login', data={'username': username, 'password': password})

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    """Sends a class with its methods to each test"""
    return AuthActions(client)
