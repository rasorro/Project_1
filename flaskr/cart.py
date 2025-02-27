from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/')
def cart():
    db = get_db()
    # cart_items = db.execute(
    #    'SELECT * FROM Shoppint_Cart'
    # ).fetchall()
    return render_template('cart/cart.html')#, cart_items=cart_items)

@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    db = get_db()
    #if request.method == 'POST':
        #shipping_address = request.form['shipping_address']
        #billing_address = request.form['billing_address']
        #payment_method = request.form['payment_method']
        #order_notes = request.form['order_notes']

        # Insert the order into the Orders table
        #db.execute(
        #    'INSERT INTO Orders (CustomerID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry) VALUES (?,
    return render_template('cart/checkout.html')