import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'ABCDE', 'password': 'password'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM Authentication WHERE userID = 'ABCDE'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('test1', '', b'Password is required.'),
    ('test1', 'test', b'User TEST1 is already registered.'),
    ('test', 'password', b'user_ID must be 5 characters'),
    ('test2', 'password', b'You should be redirected automatically'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_register_existing_customer_no_password(client, app):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO Customers (CustomerID) VALUES ('ABCDE')")
        db.commit()

    response = client.post(
        '/auth/register', data={'username': 'ABCDE', 'password': 'password'}
    )
    assert b'CustomerID ABCDE already exists but does not have a password.' in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['userID'] == 'TEST1'
        assert g.user['userID'] == 'TEST1'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test1', 'a', b'Incorrect password.'),
    ('test1', 'test', b'You should be redirected automatically'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


"""
update /protected_route to route to checkout page (when it exists)
def test_protected_route(client):
    response = client.get('/protected_route')
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
"""