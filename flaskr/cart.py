from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db, employee_id

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/view', methods=('GET', 'POST'))
def cart():
    db = get_db()
    cart_items = db.execute(
        '''
        SELECT sc.productID, p.ProductName, sc.quantity, p.UnitPrice, 
                (sc.quantity * p.UnitPrice) AS TotalPrice
        FROM Shopping_Cart sc
        JOIN Products p ON sc.productID = p.ProductID
        '''
        ).fetchall()

    # Debugging: Print the cart contents
    print("Cart items:", cart_items)

    return render_template('cart/cart.html', cart_items=cart_items)

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
        #use employee_id as val for employee_id
        #db.execute(
        #    'INSERT INTO Orders (CustomerID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry) VALUES (?,
    return render_template('cart/checkout.html')

@bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_item(product_id):
    db = get_db()
    db.execute(
        'DELETE FROM Shopping_Cart WHERE productID = ?',
        (product_id,)
    )
    db.commit()
    flash('Item removed from cart!')
    return redirect(url_for('cart.cart'))