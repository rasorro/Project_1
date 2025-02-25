from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@bp.route('/')
def cart():
    db = get_db()
    # cart_items = db.execute(
    #    'SELECT * FROM Shoppint_Cart'
    # ).fetchall()
    return render_template('checkout/cart.html')#, cart_items=cart_items)
