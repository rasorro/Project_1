"""
Provides functions to initialize and interact with the SQLite database
"""

import sqlite3
import click
from flask import current_app, g

EMPLOYEE_ID = None

def get_db(database='P1_DATABASE'):
    """
    Get a database connection. Defaults to the main database ('DATABASE').
    Use 'P3_DATABASE' for the secondary database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config[database],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initializes the database by creating the necessary tables if they do not exist.
    """
    db = get_db("P3_DATABASE") # pylint: disable=invalid-name
    db.executescript("""CREATE TABLE IF NOT EXISTS [User] (
        [ID] INTEGER PRIMARY KEY,
        [Name] TEXT NOT NULL,
        [Email] TEXT UNIQUE NOT NULL,
        [Affiliation] TEXT CHECK ([Affiliation] IN ('student', 'alumnus', 'resident')),
        [College] TEXT CHECK (([Affiliation] = 'resident' AND [College] IS NULL) OR
            ([Affiliation] != 'resident' AND [College] IN ('Boston University', 'Northeastern University', 'Harvard University',
            'Massachusetts Institute of Technology', 'Boston College', 'Emerson College', 'Suffolk University',
            'Berklee College of Music', 'Simmons University', 'Wentworth Institute of Technology', 'University of Massachusetts Boston',
            'Tufts University', 'Lesley University', 'New England Conservatory of Music', 'Massachusetts College of Art and Design')))
    );

    CREATE TABLE IF NOT EXISTS [Category] (
        [ID] INTEGER PRIMARY KEY,
        [Name] TEXT UNIQUE NOT NULL,
        [Description] TEXT
    );

    CREATE TABLE IF NOT EXISTS [ActivityGroup] (
        [ID] INTEGER PRIMARY KEY,
        [Name] TEXT NOT NULL,
        [Description] TEXT,
        [Website] TEXT,
        [ContactUserID] INTEGER REFERENCES [User]([ID]) ON DELETE SET NULL,
        [Email] TEXT REFERENCES [User]([Email]) ON DELETE SET NULL,
        [Address] TEXT,
        [CategoryID] INTEGER,
        [AffiliatedWithCollege] BOOLEAN,
        [College] TEXT CHECK (([AffiliatedWithCollege] = 1 AND [College] IN ('Boston University', 'Northeastern University', 'Harvard University',
            'Massachusetts Institute of Technology', 'Boston College', 'Emerson College', 'Suffolk University',
            'Berklee College of Music', 'Simmons University', 'Wentworth Institute of Technology', 'University of Massachusetts Boston',
            'Tufts University', 'Lesley University', 'New England Conservatory of Music', 'Massachusetts College of Art and Design'))
        OR ([AffiliatedWithCollege] = 0 AND [College] IS NULL)),
        [RequiresDues] BOOLEAN,
        [SkillLevel] TEXT CHECK ([SkillLevel] IN ('beginner', 'intermediate', 'advanced')),
        FOREIGN KEY ([CategoryID]) REFERENCES [Category]([ID]) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS [Event] (
        [EventID] INTEGER PRIMARY KEY,
        [GroupID] INTEGER NOT NULL REFERENCES [ActivityGroup]([ID]) ON DELETE CASCADE,
        [Name] TEXT NOT NULL,
        [Location] TEXT,
        [Description] TEXT,
        [Date] DATE NOT NULL,
        [StartTime] TIME,
        [EndTime] TIME,
        [Frequency] TEXT
    );

    CREATE TABLE IF NOT EXISTS [Membership] (
        [Role] TEXT CHECK ([Role] IN ('member', 'organizer')),
        [JoinDate] DATE,
        [UserID] INTEGER REFERENCES [User]([ID]) ON DELETE CASCADE,
        [GroupID] INTEGER REFERENCES [ActivityGroup]([ID]) ON DELETE CASCADE,
        PRIMARY KEY ([UserID], [GroupID])
    );

    CREATE TABLE IF NOT EXISTS [UserInterest] (
        [UserID] INTEGER REFERENCES [User]([ID]) ON DELETE CASCADE,
        [CategoryID] INTEGER REFERENCES [Category]([ID]) ON DELETE CASCADE,
        PRIMARY KEY ([UserID], [CategoryID])
    );
    """)
    db.executescript("""
        INSERT INTO User (ID, Name, Email, Affiliation, College) VALUES
(1, 'Alice Johnson', 'alice.johnson@example.com', 'student', 'Boston University'),
(2, 'Bob Smith', 'bob.smith@example.com', 'alumnus', 'Northeastern University'),
(3, 'Carol White', 'carol.white@example.com', 'resident', NULL),
(4, 'David Lee', 'david.lee@example.com', 'student', 'Harvard University'),
(5, 'Emily Chen', 'emily.chen@example.com', 'alumnus', 'Massachusetts Institute of Technology'),
(6, 'Frank Nguyen', 'frank.nguyen@example.com', 'resident', NULL),
(7, 'Grace Kim', 'grace.kim@example.com', 'student', 'Suffolk University'),
(8, 'Henry Zhao', 'henry.zhao@example.com', 'student', 'Tufts University'),
(9, 'Isabel Torres', 'isabel.torres@example.com', 'alumnus', 'Boston College'),
(10, 'Jake Martin', 'jake.martin@example.com', 'resident', NULL),
(11, 'Kelly Brooks', 'kelly.brooks@example.com', 'student', 'Lesley University'),
(12, 'Leo Patel', 'leo.patel@example.com', 'alumnus', 'Emerson College'),
(13, 'Maria Gonzalez', 'maria.gonzalez@example.com', 'student', 'Berklee College of Music'),
(14, 'Nina Rossi', 'nina.rossi@example.com', 'alumnus', 'Massachusetts College of Art and Design'),
(15, 'Oscar Rivera', 'oscar.rivera@example.com', 'resident', NULL);

INSERT INTO Category (ID, Name, Description) VALUES
(1, 'Sports', 'Athletic and recreational activities'),
(2, 'Music', 'Musical performance and appreciation groups'),
(3, 'Technology', 'Clubs focused on programming, robotics, and innovation'),
(4, 'Volunteering', 'Community service and volunteering opportunities'),
(5, 'Art', 'Visual and performing arts groups'),
(6, 'Cooking', 'Culinary groups and cooking clubs'),
(7, 'Outdoors', 'Outdoor recreation and nature activities');

INSERT INTO ActivityGroup (ID, Name, Description, Website, ContactUserID, Email, Address, CategoryID, AffiliatedWithCollege, College, RequiresDues, SkillLevel) VALUES
(1, 'Boston Runners', 'A running club for all levels', 'http://bostonrunners.org', 1, 'alice.johnson@example.com', '123 Boylston St, Boston, MA', 1, TRUE, 'Boston University', TRUE, 'intermediate'),
(2, 'Tech Innovators', 'A club for technology enthusiasts', 'http://techinnovators.com', 2, 'bob.smith@example.com', '456 Massachusetts Ave, Boston, MA', 3, TRUE, 'Northeastern University', FALSE, 'advanced'),
(3, 'Boston Volunteers', 'Volunteer work across the city', 'http://bostonvolunteers.org', 3, 'carol.white@example.com', '789 Commonwealth Ave, Boston, MA', 4, FALSE, NULL, FALSE, 'beginner'),
(4, 'Boston Jazz Band', 'Local jazz music group', 'http://bostonjazz.org', 4, 'david.lee@example.com', '321 Huntington Ave, Boston, MA', 2, TRUE, 'Harvard University', TRUE, 'advanced'),
(5, 'Outdoor Explorers', 'Hiking and nature trips around Boston', 'http://outdoorexplorers.org', 5, 'emily.chen@example.com', '555 Beacon St, Boston, MA', 7, FALSE, NULL, FALSE, 'intermediate'),
(6, 'Culinary Collective', 'Cooking classes and recipe sharing', 'http://culinarycollective.com', 6, 'frank.nguyen@example.com', '12 Tremont St, Boston, MA', 6, FALSE, NULL, TRUE, 'beginner'),
(7, 'Boston Artists', 'Collaborative art projects and workshops', 'http://bostonartists.org', 7, 'grace.kim@example.com', '78 Newbury St, Boston, MA', 5, TRUE, 'Suffolk University', TRUE, 'intermediate'),
(8, 'CodeCraft', 'Coding bootcamps and hackathons', 'http://codecraft.org', 8, 'henry.zhao@example.com', '246 Albany St, Boston, MA', 3, TRUE, 'Tufts University', FALSE, 'advanced'),
(9, 'Symphony Society', 'Classical music appreciation and performance', 'http://symphonysociety.org', 9, 'isabel.torres@example.com', '111 Huntington Ave, Boston, MA', 2, TRUE, 'Boston College', TRUE, 'advanced'),
(10, 'Volunteer Heroes', 'Helping underserved communities', 'http://volunteerheroes.org', 10, 'jake.martin@example.com', '333 Washington St, Boston, MA', 4, FALSE, NULL, FALSE, 'beginner');

INSERT INTO Event (EventID, GroupID, Name, Location, Description, Date, StartTime, EndTime, Frequency) VALUES
(1, 1, 'Weekly Long Run', 'Boston Common', 'Sunday morning long run', '2025-05-11', '08:00', '10:30', 'weekly'),
(2, 2, 'Hackathon', 'MIT Media Lab', '24-hour coding event', '2025-06-01', '10:00', '10:00', 'annual'),
(3, 3, 'Community Cleanup', 'Charles River Esplanade', 'Help clean up the riverbank', '2025-05-15', '09:00', '12:00', 'monthly'),
(4, 4, 'Jazz Night', 'Scullers Jazz Club', 'Evening jazz performance', '2025-05-20', '19:00', '22:00', 'monthly'),
(5, 5, 'Spring Hike', 'Blue Hills Reservation', 'Group hike to enjoy nature', '2025-05-22', '09:00', '15:00', 'quarterly'),
(6, 6, 'Cooking Workshop', 'Boston Public Market', 'Learn to make pasta', '2025-06-10', '17:00', '19:00', 'monthly'),
(7, 7, 'Gallery Showcase', 'ICA Boston', 'Showcase of member artwork', '2025-06-18', '18:00', '21:00', 'quarterly'),
(8, 8, 'Python Bootcamp', 'Tufts Computer Lab', 'Two-day intensive Python course', '2025-07-01', '09:00', '17:00', 'semiannual'),
(9, 9, 'Chamber Concert', 'Jordan Hall', 'Evening chamber music concert', '2025-07-15', '19:30', '21:30', 'annual'),
(10, 10, 'Food Drive', 'Boston Food Bank', 'Volunteer to collect and sort donations', '2025-05-30', '10:00', '14:00', 'monthly');

INSERT INTO Membership (Role, JoinDate, UserID, GroupID) VALUES
('member', '2025-01-10', 1, 1),
('organizer', '2024-09-05', 2, 2),
('member', '2025-03-15', 3, 3),
('organizer', '2023-12-01', 4, 4),
('member', '2025-02-20', 5, 5),
('member', '2025-04-05', 6, 6),
('organizer', '2024-11-15', 7, 7),
('member', '2025-01-25', 8, 8),
('organizer', '2024-10-10', 9, 9),
('member', '2025-03-30', 10, 10),
('member', '2025-02-01', 11, 7),
('member', '2025-03-10', 12, 2),
('organizer', '2024-07-01', 13, 9),
('member', '2025-02-18', 14, 5),
('member', '2025-03-27', 15, 3);

INSERT INTO UserInterest (UserID, CategoryID) VALUES
(1, 1),
(1, 3),
(2, 3),
(3, 4),
(4, 2),
(5, 1),
(5, 3),
(6, 4),
(7, 5),
(8, 3),
(9, 2),
(10, 4),
(11, 5),
(12, 6),
(13, 2),
(14, 5),
(15, 4);
    """)
    db.commit()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """
    Allows the user to initialize the database. It calls the `init_db` function to set up
    the necessary tables and insert default data.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Initializes the Flask application by setting up database teardown and CLI commands.
    Args: app (Flask): The Flask application instance.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
