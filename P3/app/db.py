"""
Provides functions to initialize and interact with the SQLite database
"""

import sqlite3
import click
from flask import current_app, g

EMPLOYEE_ID = None

def get_db():
    """
    Get a database connection. Defaults to the main database ('DATABASE').
    """
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
    """
    Initializes the database by creating the necessary tables if they do not exist.
    """
    
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    if db.execute("SELECT COUNT(*) FROM User").fetchone()[0] == 0:
        db.executescript(current_app.open_resource('seed_data.sql').read().decode('utf8'))

    db.commit()

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