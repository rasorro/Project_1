from app.db import get_db

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

def test_event_filter_by_skillLevel(client, auth, app):
    auth.register()
    auth.login()