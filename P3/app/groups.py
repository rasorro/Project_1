"""
Handles the shopping cart functionality, including viewing the cart,
checking out, and removing items from the cart.
"""

from datetime import datetime, timezone

from flask import (
    Blueprint, g, current_app, flash, redirect, render_template, request, url_for, session, Response
)

from app.auth import login_required
from app.db import get_db
from unidecode import unidecode


bp = Blueprint('groups', __name__, url_prefix='/groups')


@bp.route('/join/<int:group_id>', methods=['POST'])
@login_required
def join_group(group_id):
    """
    Allows the logged-in user to join a group.
    If already a member, does nothing.
    """
    db = get_db()
    user_id = g.user['ID']

    existing = db.execute(
        'SELECT 1 FROM Membership WHERE UserID = ? AND GroupID = ?',
        (user_id, group_id)
    ).fetchone()

    if existing:
        flash('You are already a member of this group.')
    else:
        db.execute(
            'INSERT INTO Membership (UserID, GroupID, Role, JoinDate) VALUES (?, ?, ?, ?)',
            (user_id, group_id, 'Member',  datetime.now(timezone.utc).date())
        )
        db.commit()
        flash('You successfully joined the group.')

    return redirect(url_for('groups.group_details', group_id=group_id))


@bp.route('/leave/<int:group_id>', methods=['POST'])
@login_required
def leave_group(group_id):
    """
    Allows the logged-in user to leave a group.
    """
    db = get_db()
    user_id = g.user['ID']

    existing = db.execute(
        'SELECT 1 FROM Membership WHERE UserID = ? AND GroupID = ?',
        (user_id, group_id)
    ).fetchone()

    if existing:
        db.execute(
            'DELETE FROM Membership WHERE UserID = ? AND GroupID = ?',
            (user_id, group_id)
        )
        db.commit()
        flash('You successfully left the group.')
    else:
        flash('You are not a member of this group.')

    return redirect(url_for('groups.group_details', group_id=group_id))


@bp.route('/my-groups')
@login_required
def my_groups():
    """
    Displays the user's groups and their membership info.
    """
    db = get_db()
    user_id = g.user['ID']
    groups = db.execute(
        """
        SELECT g.ID, g.Name, g.Description, m.Role, m.JoinDate
        FROM Membership m
        JOIN ActivityGroup g ON m.GroupID = g.ID
        WHERE m.UserID = ?
        """,
        (user_id,)
    ).fetchall()

    return render_template('groups/my_groups.html', groups=groups)

@bp.route('/groups/<int:group_id>')
def group_details(group_id):
    """
    Displays the details of a specific group.
    """
    db = get_db()
    
    group = db.execute("""
        SELECT g.*, c.Name AS CategoryName
        FROM ActivityGroup g
        JOIN Category c ON g.CategoryID = c.ID
        WHERE g.ID = ?
    """, (group_id,)).fetchone()

    if group is None:
        flash('Group not found.')
        return redirect(url_for('groups.my_groups'))

    members = db.execute(
        """
        SELECT u.Name, m.Role, m.JoinDate
        FROM Membership m
        JOIN User u ON m.UserID = u.ID
        WHERE m.GroupID = ?
        ORDER BY m.Role DESC, m.JoinDate ASC
        """,
        (group_id,)
    ).fetchall()
    
    events = db.execute(
        """
        SELECT * FROM Event
        WHERE GroupID = ?
        ORDER BY Date ASC
        """,
        (group_id,)
    ).fetchall()
    
    user_role = None
    is_member = False
    if g.user:
        user_role = db.execute(
            """
            SELECT Role
            FROM Membership
            WHERE UserID = ? AND GroupID = ?
            """,
            (g.user['ID'], group_id)
        ).fetchone()
        
        if user_role:
            is_member = True
            user_role = user_role['Role']

    return render_template('groups/group_details.html',  group=group, members=members, events=events, user_role=user_role, is_member=is_member)

def create_unidecode_function(db):  #pylint: disable=invalid-name
   """
   Creates a custom SQLite function for unidecoding strings.
   Args: db (Connection): The database connection object.
   """
   db.create_function("unidecode", 1, unidecode)




@bp.route('/')
def index() -> Response:
   """
   Show all activity groups, with optional search and filters.
   Supports:
     - search (by group name or description)
     - category_id
     - college
     - skill_level
   """
   db = get_db()
   create_unidecode_function(db)
  
   search_term = request.args.get('search', '').strip()
   sel_category_id = request.args.get('category_id')
   sel_college = request.args.get('college')
   sel_skill_level = request.args.get('skill_level')


   query = """
       SELECT g.ID, g.Name, g.Description, g.AffiliatedWithCollege, g.College,
              g.SkillLevel, c.Name AS CategoryName
       FROM ActivityGroup g
       LEFT JOIN Category c ON g.CategoryID = c.ID
       WHERE 1=1
   """
   args = []
  
   if search_term:
       query += " AND (unidecode(g.Name) LIKE unidecode(?) OR unidecode(g.Description) LIKE unidecode(?))"
       args.extend([f'%{search_term}%', f'%{search_term}%'])
      
   if sel_category_id:
       query += " AND c.ID = ?"
       args.append(sel_category_id)
  
   if sel_college:
       query += " AND g.College = ?"
       args.append(sel_college)


   if sel_skill_level:
       query += " AND g.SkillLevel = ?"
       args.append(sel_skill_level)
      
   query += " ORDER BY g.Name ASC"
  
   groups = db.execute(query, args).fetchall()
  
   categories = db.execute("SELECT ID, Name FROM Category").fetchall()
   colleges = db.execute("""
                         SELECT DISTINCT College
                         FROM ActivityGroup
                         WHERE College IS NOT NULL AND College != ''
                         ORDER BY College""").fetchall()
   skill_levels = db.execute("SELECT DISTINCT SkillLevel FROM ActivityGroup WHERE SkillLevel IS NOT NULL").fetchall()
  
   return render_template('groups/index.html', groups=groups, categories=categories,
                          colleges=colleges, skill_levels=skill_levels, search=search_term,
                          category_id=sel_category_id, college=sel_college, skill_level=sel_skill_level)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    """
    Allows the user to create a new activity group.
    Their Membership role for this group will be organizer.
    """
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        website = request.form['website']
        address = request.form['address']
        category_id = request.form['category_id']
        affiliated = request.form.get('affiliated') == 'on'
        college = request.form['college'] if affiliated else None
        requires_dues = request.form.get('requires_dues') == 'on'
        skill_level = request.form['skill_level']

        error = None
        
        if not name:
            error = 'Group name is required.'
            
        if affiliated and not college:
            error = 'College is required for affiliated groups.'

        if affiliated and college not in [
            row['College'] for row in db.execute("""
                SELECT DISTINCT [College]
                FROM [User]
                WHERE [College] IS NOT NULL
                UNION
                SELECT DISTINCT [College]
                FROM [ActivityGroup]
                WHERE [College] IS NOT NULL
            """).fetchall()
        ]:
            error = 'Invalid college selected for an affiliated group.'

        if error is None:
            try:
                db.execute("""
                    INSERT INTO ActivityGroup
                        (Name, Description, Website, ContactUserID, Email, Address, CategoryID,
                         AffiliatedWithCollege, College, RequiresDues, SkillLevel)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, description, website, g.user['ID'], g.user['Email'], address,
                    category_id, affiliated, college, requires_dues, skill_level
                ))
                group_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                db.execute("""
                    INSERT INTO Membership (UserID, GroupID, Role, JoinDate)
                    VALUES (?, ?, 'Organizer', ?)
                """, (g.user['ID'], group_id, datetime.now().date()))
                print("yes3")
                db.commit()
                flash('Group created successfully.')
                return redirect(url_for('groups.group_details', group_id=group_id))

            except db.IntegrityError:
                error = 'Failed to create group.'
        
        flash(error)

    categories = db.execute('SELECT ID, Name FROM Category').fetchall()
    return render_template('groups/create_group.html', categories=categories)
