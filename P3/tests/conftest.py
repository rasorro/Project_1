import os
import tempfile

import pytest
from app import create_app
from app.db import get_db, init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
         'SECRET_KEY': 'dev',
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, name='Test User', email='test1@example.com', password='test', affiliation='Student', college='Boston College'):
        return self._client.post(
            '/auth/register',
            data={
                'name': name,
                'email': email,
                'password': password,
                'affiliation': affiliation,
                'college': college
            },
            follow_redirects=True
        )

    def login(self, email='test1@example.com', password='test'):
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/auth/logout', follow_redirects=True)

@pytest.fixture
def auth(client):
    return AuthActions(client)
