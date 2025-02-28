from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db, employee_id
from datetime import datetime

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/view', methods=('GET', 'POST'))
def cart():
    db = get_db()
    cart_items = db.execute(
        '''
        SELECT sc.productID, p.ProductName, SUM(sc.quantity) AS quantity, p.UnitPrice, 
            (SUM(sc.quantity) * p.UnitPrice) AS TotalPrice
        FROM Shopping_Cart sc
        JOIN Products p ON sc.productID = p.ProductID
        GROUP BY sc.productID, p.ProductName, p.UnitPrice
        '''
    ).fetchall()
    return render_template('cart/cart.html', cart_items=cart_items)

@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    if request.method == 'POST':
        db = get_db()
        customer_id = session.get('userID')
        order_date = datetime.now()
        shipping_address = request.form['shipping_address']
        ship_city = request.form['ship_city']
        ship_postal_code = request.form['ship_postal_code']
        ship_country = request.form['ship_country']
        billing_address = request.form['billing_address']
        card_number = request.form['card_number']
        order_notes = request.form['order_notes']

        db.execute(
           'INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, ShipAddress, ShipCity, ShipPostalCode, ShipCountry) VALUES (?, ?, ?, ?, ?, ?, ?)',
           (customer_id, employee_id, order_date, shipping_address, ship_city, ship_postal_code, ship_country)
        )
        db.commit()

        db.execute(
            'DELETE FROM Shopping_Cart WHERE shopperID = ?',
            (customer_id,)
        )
        
        db.execute("DELETE FROM Shopping_Cart WHERE added_at <= DATETIME('now', '-1 month')")

        db.commit()

        flash('Order placed successfully!')
        return redirect(url_for('cart.cart'))

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