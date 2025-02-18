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
        elif not password:
            error = 'Password is required.'

        """
        Currently, in order for successful registration, user_ID must correspond
        to an existing CustomerID. Functionality needs to be added for registering
        completely new Customers.
        """
        customer_exists = db.execute(
            "SELECT CustomerID FROM Customers WHERE CustomerID = ?", (user_ID,)
        ).fetchone()
        if not customer_exists:
            error = f'No such Customer ID: {user_ID}. Please use a valid Customer ID.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Authentication (userID, passwordHash) VALUES (?, ?)",
                    (user_ID, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {user_ID} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_id = request.form['username']
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
            'SELECT * FROM Authentication WHERE id = ?', (user_id,)
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
