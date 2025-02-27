import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_ID = request.form['username'].upper()
        password = request.form['password']
        db = get_db()
        error = None
        if not user_ID:
            error = 'Username is required.'
        elif len(user_ID) !=5:
            error = 'user_ID must be 5 characters'
        elif not password:
            error = 'Password is required.'
        if error is None:
            user_exists = db.execute(
                "SELECT userID FROM Authentication WHERE userID = ?", (user_ID,)
            ).fetchone()
            if user_exists:
                error = f"User {user_ID} is already registered."
        """
        Need to update below , maybe some sort of authentication allowing them to
        verify with other info in northwind database (e.g., postal code + phone)
        """
        if error is None:
            customer_exists = db.execute(
                "SELECT CustomerID FROM Customers WHERE CustomerID = ?", (user_ID,)
            ).fetchone()
            if customer_exists:
                error = f'CustomerID {user_ID} already exists but does not have a password.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Customers (CustomerID) VALUES (?)", (user_ID,)
                )
                db.execute(
                    "INSERT INTO Authentication (userID, passwordHash) VALUES (?, ?)",
                    (user_ID, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {user_ID} registration failed."
            else:
                return redirect(url_for("auth.login"))      
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_id = request.form['username'].upper()
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM Authentication WHERE userID = ?', (user_id,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['passwordHash'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['userID'] = user['userID']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('userID')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Authentication WHERE userID = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view