import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS Authentication (
            userID TEXT PRIMARY KEY REFERENCES Customers(CustomerID) ON DELETE CASCADE,
            passwordHash TEXT NOT NULL,
            sessionID TEXT
        );
    """)
    db.commit()

@click.command('test-db')
def test_db_command():
    db = get_db()
    result = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print([row["name"] for row in result])

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(test_db_command)

