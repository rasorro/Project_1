import pytest
from flask import g, session
from app.db import get_db


def test_register_get(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register(auth, app):
    response = auth.register()
    assert response.status_code == 200
    assert b'Log Out' in response.data
    
    with app.app_context():
        db = get_db()
        user = db.execute("SELECT * From User WHERE Email = ?",
                          ("test1@example.com",)).fetchone()
        auth_row = db.execute("SELECT * From [Authentication] WHERE UserID = ?", (user["ID"],)).fetchone()
        assert user is not None
        assert auth_row is not None


@pytest.mark.parametrize(
    ('name', 'email', 'affiliation', 'college', 'password', 'message'),
    [
        ('', 'test@example.com', 'Student', 'Boston University', 'test', b'Name is required'),
        ('Test', '', 'Student', 'Boston University', 'test', b'Email is required'),
        ('Test', 'test@example.com', 'Student', 'Boston University', '', b'Password is required'),
        ('Test', 'test@example.com', 'Student', '', 'test', 'College is required for students.'),
        ('Test', 'test@example.com', 'Resident', 'Boston University', 'test', 'College should be blank for residents.'),
        ('Test', 'alice.johnson@example.com', 'Student', 'Boston University', 'test', b'A user with that email already exists.'),
    ]
)
def test_register_validate_input(client, name, email, affiliation, college, password, message):
    response = client.post(
        '/auth/register',
        data={
            'name': name,
            'email': email,
            'affiliation': affiliation,
            'college': college,
            'password': password,}
    )
    assert message in response.data


def test_login(client, auth):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Log In' in response.data
    auth.register()
    auth.logout()
    response = auth.login()
    assert b'Log Out' in response.data


@pytest.mark.parametrize(
    ('email', 'password', 'message'),
    [
        ('test@example.com', 'test', b'Incorrect email.'),
        ('test1@example.com', 'tes', b'Incorrect password.'),
    ]
)
def test_login_validate_input(auth, email, password, message):
    auth.register()
    auth.logout()
    response = auth.login(email=email, password=password)
    assert message in response.data


def test_logout(client, auth):
    auth.register()
    auth.login()
    response = auth.logout()
    assert b'Log In' in response.data
    with client:
        auth.logout()
        assert 'userID' not in session


def test_protected_route(client, auth):
    response = client.get('/groups/my-groups')
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]
    location = response.headers["Location"]
    
    auth.register()
    response = client.post(location, data={
        'email': 'test1@example.com',
        'password': 'test'
    }, follow_redirects=True)
    assert b'My Groups' in response.data