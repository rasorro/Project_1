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
        user_id = request.form['username'].upper()        
        password = request.form['password']
        
        db = get_db() # pylint: disable=invalid-name
        error = None
        
        if not user_id:
            error = 'Username is required.'
        elif len(user_id) !=5:
            error = 'user_ID must be 5 characters'
        elif not password:
            error = 'Password is required.'
        if error is None:
            user_exists = db.execute(
                "SELECT userID FROM Authentication WHERE userID = ?", (user_id,)
            ).fetchone()
            if user_exists:
                error = f"User {user_id} is already registered."
        if error is None:
            customer_exists = db.execute(
                "SELECT CustomerID FROM Customers WHERE CustomerID = ?", (user_id,)
            ).fetchone()
            if customer_exists:
                error = f'CustomerID {user_id} already exists but does not have a password.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Customers (CustomerID) VALUES (?)", (user_id,)
                )
                db.execute(
                    "INSERT INTO Authentication (userID, passwordHash) VALUES (?, ?)",
                    (user_id, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {user_id} registration failed."
            else:
                return redirect(url_for("auth.login"))
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
        user_id = request.form['username'].upper()
        password = request.form['password']
        db = get_db()  # pylint: disable=invalid-name
        error = None
        user = db.execute(
            'SELECT * FROM Authentication WHERE userID = ?', (user_id,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['passwordHash'], password):
            error = 'Incorrect password.'
        if error is None:
            db.execute('UPDATE Shopping_Cart SET shopperID = ? WHERE shopperID = ?',
            (user_id, session.get('userID')))
            db.commit()
            session.clear()
            session['userID'] = user['userID']
            return redirect(url_for('index'))
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
            'SELECT * FROM Authentication WHERE userID = ?', (user_id,)
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
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
