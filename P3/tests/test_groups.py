from datetime import datetime, timezone
from app.db import get_db

def test_join_group(client, auth, app):
    auth.register()
    auth.login()
    with app.app_context():
        db = get_db()
        group_id = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()['ID']
    response = client.post(f'/groups/join/{group_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"You successfully joined the group." in response.data

def test_leave_group(client, auth, app):
    auth.register()
    auth.login()
    with app.app_context():
        db = get_db()
        group_id = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()['ID']
        user_id = db.execute("SELECT ID FROM User WHERE Email = ?", ("test1@example.com",)).fetchone()['ID']
        db.execute("INSERT INTO Membership (UserID, GroupID, Role, JoinDate) VALUES (?, ?, ?, ?)",
                   (user_id, group_id, 'Member', datetime.now(timezone.utc).date()))
        db.commit()
    response = client.post(f'/groups/leave/{group_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"You successfully left the group." in response.data

def test_my_groups(client, auth, app):
    auth.register()
    auth.login()
    with app.app_context():
        db = get_db()
        group_id = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()['ID']
        user_id = db.execute("SELECT ID FROM User WHERE Email = ?", ("test1@example.com",)).fetchone()['ID']
        db.execute("INSERT INTO Membership (UserID, GroupID, Role, JoinDate) VALUES (?, ?, ?, ?)",
                   (user_id, group_id, 'Member', datetime.now(timezone.utc).date()))
        db.commit()
    response = client.get('/groups/my-groups')
    assert response.status_code == 200
    assert b"My Groups" in response.data

def test_create_group_success(client, auth, app):
    auth.register()
    auth.login()

    response = client.post('/groups/create', data={
        'name': 'Running Club',
        'description': 'Run every morning',
        'website': 'https://running.com',
        'address': '2150 Commonwealth Ave',
        'category_id': 3,
        'affiliated': 'on',
        'college': 'Boston College',
        'requires_dues': 'on',
        'skill_level': 'Beginner'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Group created successfully.' in response.data

    with app.app_context():
        db = get_db()
        group = db.execute("SELECT * FROM ActivityGroup WHERE Name = 'Running Club'").fetchone()
        assert group is not None


def test_create_group_missing_name(client, auth):
    auth.register()
    auth.login()

    response = client.post('/groups/create', data={
        'name': '',
        'description': 'desc',
        'website': 'http://example.com',
        'address': 'Los Angeles',
        'category_id': 1,
        'affiliated': 'on',
        'college': 'Boston University',
        'requires_dues': 'on',
        'skill_level': 'Intermediate'
    })
    assert b'Group name is required.' in response.data

def test_create_group_invalid_college(client, auth):
    auth.register()
    auth.login()

    response = client.post('/groups/create', data={
        'name': 'UCLA Basketball',
        'description': 'Test',
        'website': '',
        'address': '',
        'category_id': 1,
        'affiliated': 'on',
        'college': 'UCLA',
        'requires_dues': '',
        'skill_level': 'Advanced'
    })
    assert b'Invalid college selected for an affiliated group.' in response.data

def test_delete_group(client, auth, app):
    auth.register()
    auth.login()

    response = client.post('/groups/create', data={
        'name': 'Running Club',
        'description': 'Run every morning',
        'website': 'https://running.com',
        'address': '2150 Commonwealth Ave',
        'category_id': 3,
        'affiliated': 'on',
        'college': 'Boston College',
        'requires_dues': 'on',
        'skill_level': 'Beginner'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Group created successfully.' in response.data

    with app.app_context():
        db = get_db()
        group = db.execute("SELECT * FROM ActivityGroup WHERE Name = 'Running Club'").fetchone()
        assert group is not None

    