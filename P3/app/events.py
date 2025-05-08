"""
Handles the browsing and searching functionality for products in the shop.
"""

import uuid
from flask import (
    Blueprint, flash, render_template, request, session, Response
)
from unidecode import unidecode
from app.db import get_db


bp = Blueprint('events', __name__)


def create_unidecode_function(db):  #pylint: disable=invalid-name
    """
    Creates a custom SQLite function for unidecoding strings.
    Args: db (Connection): The database connection object.
    """
    db.create_function("unidecode", 1, unidecode)


@bp.route('/')
def index() -> Response:
    """
    Show all events, with optional search and filters.
    Supports:
      - search (by event name or description)
      - category_id
      - group_id
    """
    db = get_db()
    create_unidecode_function(db)
    
    search_term = request.args.get('search', '').strip()
    sel_category_id = request.args.get('category_id')
    sel_group_id = request.args.get('group_id')
    
    query = """
        SELECT e.EventID, e.Name, e.Date, e.StartTime, e.Location,
               g.Name AS GroupName, c.Name as CategoryName
        FROM Event e
        JOIN ActivityGroup g ON e.GroupID = g.ID
        JOIN Category c ON g.CategoryID = c.ID
        WHERE 1=1
    """
    args = []
    
    if search_term:
        query += " AND (unidecode(e.Name) LIKE unidecode(?) OR unidecode(e.Description) LIKE unidecode(?))"
        args.extend([f'%{search_term}%', f'%{search_term}%'])
        
    if sel_category_id:
        query += " AND c.ID = ?"
        args.append(sel_category_id)
    
    if sel_group_id:
        query += " AND g.ID = ?"
        args.append(sel_group_id)
        
    query += " ORDER BY e.Date ASC"
    
    events = db.execute(query, args).fetchall()
    
    categories = db.execute("SELECT ID, Name FROM Category").fetchall()
    groups = db.execute("SELECT ID, Name FROM ActivityGroup").fetchall()
    
    return render_template('events/index.html', events=events, categories=categories, groups=groups, search=search_term, category_id=sel_category_id, group_id=sel_group_id)


@bp.route('/<int:event_id>')
def event_details(event_id) -> Response:
    """
    View details of a specific event.
    Returns: Response: The rendered 'event_details.html' template with event details.
    """
    db = get_db()
    event = db.execute("""
        SELECT e.*, g.Name AS GroupName, g.ContactName as HostName, g.Email as HostEmail
        FROM Event e
        JOIN ActivityGroup g ON e.GroupID = g.ID
        WHERE e.EventID = ?
    """, (event_id,)).fetchone()
    
    return render_template('events/event_details.html', event=event)