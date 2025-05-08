from app.db import get_db
from datetime import date
from datetime import datetime, timezone

def test_event_index_page(client, auth):
    auth.register()
    auth.login()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Events' in response.data

def test_event_search(client, auth, app):
    auth.register()
    auth.login()
    with app.app_context():
        db = get_db()
        group_id = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()['ID']
        db.execute("""
            INSERT INTO Event (GroupID, Name, Description, Date)
            VALUES (?, ?, ?, '2025-12-31')
        """, (group_id, 'Databases Class', 'Learn about databases',))
        db.commit()
    response = client.get('/?search=databases')
    assert response.status_code == 200
    assert b'Databases Class' in response.data

def test_event_filter_by_category(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        group = db.execute("""
            SELECT ID, CategoryID FROM ActivityGroup WHERE CategoryID IS NOT NULL LIMIT 1
        """).fetchone()
        db.execute("""
            INSERT INTO Event (GroupID, Name, Description, Date)
            VALUES (?, ?, ?, '2025-11-11')
        """, (group['ID'], 'CS Speaker Engagement', 'Come to learn about the future of quantum computing'))
        db.commit()

    response = client.get(f"/?category_id={group['CategoryID']}")
    assert response.status_code == 200
    assert b'Speaker Engagement' in response.data

def test_event_filter_by_group(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        group = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()
        db.execute("""
            INSERT INTO Event (GroupID, Name, Description, Date)
            VALUES (?, ?, ?, '2025-11-11')
        """, (group['ID'], 'CS Speaker Engagement', 'Come to learn about the future of quantum computing'))
        db.commit()
    response = client.get(f"/?group_id={group['ID']}")
    assert response.status_code == 200
    assert b'Speaker Engagement' in response.data

def test_event_filter_by_college(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        group = db.execute("""
            SELECT ID, College FROM ActivityGroup WHERE College IS NOT NULL LIMIT 1
        """).fetchone()
        db.execute("""
            INSERT INTO Event (GroupID, Name, Description, Date)
            VALUES (?, ?, ?, '2025-11-11')
        """, (group['ID'], 'CS Speaker Engagement', 'Come to learn about the future of quantum computing'))
        db.commit()

    response = client.get(f"/?college={group['College']}")
    assert response.status_code == 200
    assert b'Speaker Engagement' in response.data

def test_event_filter_by_skillLevel(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        group = db.execute("""
            SELECT ID, SkillLevel FROM ActivityGroup WHERE SkillLevel IS NOT NULL LIMIT 1
        """).fetchone()
        db.execute("""
            INSERT INTO Event (GroupID, Name, Description, Date)
            VALUES (?, ?, ?, '2025-11-11')
        """, (group['ID'], 'CS Speaker Engagement', 'Come to learn about the future of quantum computing'))
        db.commit()

    response = client.get(f"/?SkillLevel={group['SkillLevel']}")
    assert response.status_code == 200
    assert b'Speaker Engagement' in response.data

def test_create_event_success(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        group_id = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()['ID']

    response = client.post(
        f'/create/?group_id={group_id}',
        data={
            'name': '24HourCode',
            'description': 'Coding competition',
            'date': '2025-12-12',
            'start_time': '09:00',
            'end_time': '18:00',
            'location': 'Schiller',
            'frequency': 'Once'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Event created successfully' in response.data

    with app.app_context():
        db = get_db()
        event = db.execute("SELECT * FROM Event WHERE Name = ? AND Location = ?", ('24HourCode', 'Schiller')).fetchone()
        assert event is not None
        assert event['Location'] == 'Schiller'

def test_create_event_failure(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        group_id = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()['ID']

    response = client.post(
    f'/create/?group_id={group_id}',
    data={
        'name': '',  # Intentionally blank to test validation
        'description': 'Test Event',
        'date': '2025-12-12',
        'start_time': '',
        'end_time': '',
        'location': 'Auditorium',
        'frequency': ''
    },
    follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Event name is required.' in response.data


def test_delete_event_success(client, auth, app):
    auth.register()
    auth.login()

    with app.app_context():
        db = get_db()
        user = db.execute("SELECT ID, Email FROM User WHERE Email = ?", ("test1@example.com",)).fetchone()
        group = db.execute("SELECT ID FROM ActivityGroup LIMIT 1").fetchone()

        db.execute("INSERT INTO Membership (UserID, GroupID, Role, JoinDate) VALUES (?, ?, 'Organizer', ?)",
                   (user["ID"], group["ID"], datetime.now(timezone.utc).date()))

        db.execute("""INSERT INTO Event (GroupID, Name, Description, Date)
                      VALUES (?, ?, ?, ?)""",
                   (group["ID"], "Trash Event", "To be removed", "2025-12-31"))
        event_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.commit()

    response = client.post(f"/delete/{event_id}", follow_redirects=True)

    assert response.status_code == 200
    assert b"Event deleted successfully." in response.data

    with app.app_context():
        db = get_db()
        event = db.execute("SELECT * FROM Event WHERE EventID = ?", (event_id,)).fetchone()
        assert event is None
