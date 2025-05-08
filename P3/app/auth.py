"""
Defines authentication routes and functionality.
Provides user registration, login, and logout features.
"""

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register() -> str:
    """
    Handles user registration by validating the username and password,
    checking for existing users, and storing the user's credentials in the database.
    Returns: - A redirect to the login page if registration is successful.
    - The registration page with an error message if registration fails.
    """

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        affiliation = request.form['affiliation']
        college = request.form['college'] or None 
        password = request.form['password']
        
        db = get_db() # pylint: disable=invalid-name
        error = None
        
        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
            
        if error is None:
            try:
                db.execute(
                    "INSERT INTO User (Name, Email, Affiliation, College) VALUES (?, ?, ?, ?)",
                    (name, email, affiliation, college)
                )
                user = db.execute(
                    "SELECT ID FROM User WHERE Email = ?",
                    (email,)
                ).fetchone()

                db.execute(
                    "INSERT INTO Authentication (UserID, PasswordHash) VALUES (?, ?)",
                    (user['ID'], generate_password_hash(password))
                )

                db.commit()
            except db.IntegrityError:
                error = "A user with that email already exists."
            else:
                session.clear()
                session['userID'] = user['ID']
                return redirect(url_for('index'))
            
        flash(error)
        
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login() -> str:
    """
    Verifies provided username and password. If request method is GET,
    renders the login form. If POST, processes the form data, and authenticates
    the user. Returns: - A redirect to the homepage if login is successful.
    - The login page with an error message if login fails.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()  # pylint: disable=invalid-name
        error = None
        
        user = db.execute(
            """
            SELECT u.ID, u.Name, a.PasswordHash
            FROM User u
            JOIN Authentication a ON u.ID = a.UserID
            WHERE u.Email = ?
            """, (email,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['passwordHash'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['userID'] = user['ID']
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        
        flash(error)
        
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    Loads the currently logged-in user into the global object `g`.
    This function is used by routes to check if the user is authenticated.
    Returns: None.
    """
    user_id = session.get('userID')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM User WHERE ID = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout() -> str:
    """
    Logs the user out by clearing the session data and redirecting
    to the homepage. Returns: - A redirect to the homepage after logging out.
    """
    session.clear()
    return redirect(url_for('index'))


def login_required(view) -> callable:
    """
    A decorator to enforce that a user must be logged in to access a specific view.
    Args: view: The view function to be wrapped.
    Returns: A wrapped view function that enforces login requirements.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view
