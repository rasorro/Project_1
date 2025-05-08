"""
Handles the browsing and searching functionality for products in the shop.
"""

import uuid
from flask import (
    Blueprint, flash, g, render_template, request, session, Response, redirect, url_for
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
    sel_college = request.args.get('college')
    sel_skill_level = request.args.get('SkillLevel')

    query = """
        SELECT e.EventID, e.Name, e.Date, e.StartTime, e.Location,
               g.Name AS GroupName, g.College, g.SkillLevel, c.Name as CategoryName
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

    if sel_college:
        query += " AND g.College = ?"
        args.append(sel_college)

    if sel_skill_level:
        query += " AND g.SkillLevel = ?"
        args.append(sel_skill_level)
        
    query += " ORDER BY e.Date ASC"
    
    events = db.execute(query, args).fetchall()
    
    categories = db.execute("SELECT ID, Name FROM Category").fetchall()
    groups = db.execute("SELECT ID, Name FROM ActivityGroup").fetchall()
    colleges = db.execute("""
                          SELECT DISTINCT College 
                          FROM ActivityGroup 
                          WHERE College IS NOT NULL AND College != ''
                          ORDER BY College""").fetchall()
    skill_levels = db.execute("SELECT DISTINCT SkillLevel FROM ActivityGroup").fetchall()
    
    return render_template('events/index.html', events=events, categories=categories, groups=groups, 
                           skill_levels=skill_levels,colleges=colleges, search=search_term, 
                           category_id=sel_category_id, group_id=sel_group_id, college=sel_college,
                           skill_level=sel_skill_level)


@bp.route('/<int:event_id>')
def event_details(event_id) -> Response:
    """
    View details of a specific event and show buttons depending on user role..
    Returns: Response: The rendered 'event_details.html' template with event details.
    """
    db = get_db()
    event = db.execute("""
        SELECT e.*, g.Name AS GroupName, u.Name as HostName, g.Email as HostEmail
        FROM Event e
        JOIN ActivityGroup g ON e.GroupID = g.ID
        LEFT JOIN User u ON g.ContactUserID = u.ID
        WHERE e.EventID = ?
    """, (event_id,)).fetchone()
    
    if event is None:
        flash("Event not found.")
        return redirect(url_for("events.index"))

    user_role = None
    is_member = False

    if g.user:
        role_row = db.execute("""
            SELECT Role FROM Membership
            WHERE UserID = ? AND GroupID = ?
        """, (g.user['ID'], event['GroupID'])).fetchone()

        if role_row:
            user_role = role_row['Role']
            is_member = True
    
    return render_template('events/event_details.html', event=event, user_role=user_role, is_member=is_member)

@bp.route('/create/', methods=['GET', 'POST'])
def create_event():
    """
    Allows the user to create a new event for a group.
    """
    db = get_db()

    group_id = request.args.get('group_id')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        start_time = request.form['start_time'] or None
        end_time = request.form['end_time'] or None
        location = request.form['location']
        frequency = request.form['frequency'] or None

        error = None

        if not name:
            error = 'Event name is required.'
        elif not date:
            error = 'Event date is required.'
        elif not group_id:
            error = 'You must select a group.'

        if error is None:
            try:
                db.execute("""
                    INSERT INTO Event (GroupID, Name, Location, Description, Date, StartTime, EndTime, Frequency)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    group_id, name, location, description, date, start_time, end_time, frequency
                ))
                db.commit()
                event_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                flash('Event created successfully.')
                return redirect(url_for('events.event_details', event_id=event_id))
            except db.IntegrityError:
                error = 'Failed to create event.'

        flash(error)

    groups = db.execute('SELECT ID, Name FROM ActivityGroup').fetchall()
    categories = db.execute('SELECT ID, Name FROM Category').fetchall()  # Optional, in case you want to show categories

    return render_template('events/create_event.html', groups=groups, categories=categories)


@bp.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    """
    Deletes an event from the database.
    Args:
        event_id (int): The ID of the event to delete.
    """
    db = get_db()
    user_id = g.user['ID']

    authorized = db.execute("""
        SELECT 1 FROM Event e
        JOIN ActivityGroup g ON e.GroupID = g.ID
        JOIN Membership m ON g.ID = m.GroupID
        WHERE e.EventID = ? AND m.UserID = ? AND m.Role = 'Organizer'
    """, (event_id, user_id)).fetchone()

    if not authorized:
        flash("You are not authorized to delete this event.")
        return redirect(url_for('events.event_details', event_id=event_id))

    db.execute("DELETE FROM Event WHERE EventID = ?", (event_id,))
    db.commit()
    flash("Event deleted successfully.")
    return redirect(url_for('groups.group_details', group_id=g.get('event_group_id', 0)))