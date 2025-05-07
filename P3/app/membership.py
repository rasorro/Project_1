"""
Handles the shopping cart functionality, including viewing the cart,
checking out, and removing items from the cart.
"""

from datetime import datetime

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for, session, Response
)

from app.auth import login_required
from app.db import get_db


bp = Blueprint('membership', __name__, url_prefix='/mygroups')


@bp.route('', methods=('GET', 'POST'))
def cart() -> Response:
    """
    Retrieves the items in the user's shopping cart from the database
    and renders the 'cart.html' template to display the cart contents.
    Returns: Response: The rendered 'cart.html' template with the user's cart items.
    """
    db = get_db() # pylint: disable=invalid-name
    customer_id = session.get('userID')
    cart_items = db.execute(
        '''
        SELECT sc.productID, p.ProductName, SUM(sc.quantity) AS quantity, p.UnitPrice,
            (SUM(sc.quantity) * p.UnitPrice) AS TotalPrice
        FROM Shopping_Cart sc
        JOIN Products p ON sc.productID = p.ProductID
        WHERE sc.shopperID = ?
        GROUP BY sc.productID, p.ProductName, p.UnitPrice
        ''',
        (customer_id,)
    ).fetchall()
    return render_template('cart/cart.html', cart_items=cart_items)


@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout() -> Response:
    """
    Handles the checkout process. Args: request (Request): The incoming HTTP request
    containing the user's form data for checkout.
    Returns: Response: The rendered 'checkout.html' template
    or a redirect after the order is placed successfully.
    """
    if request.method == 'POST':
        db = get_db() # pylint: disable=invalid-name
        customer_id = session.get('userID')
        order_date = datetime.now()
        ship_name = request.form['ship_name']
        shipping_address = request.form['shipping_address']
        ship_city = request.form['ship_city']
        ship_region = request.form['ship_region']
        ship_postal_code = request.form['ship_postal_code']
        ship_country = request.form['ship_country']
        error = None
        if not ship_name or not shipping_address or not ship_city or not ship_region or not ship_postal_code or not ship_country: # pylint: disable=line-too-long, too-many-boolean-expressions
            error = 'Please fill out all fields.'
        if error is None:
            db.execute(
            'INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', # pylint: disable=line-too-long
            (customer_id, current_app.config.get('EMPLOYEE_ID'), order_date, ship_name,
            shipping_address, ship_city, ship_region, ship_postal_code, ship_country)
            )
            db.commit()
            db.execute(
                'DELETE FROM Shopping_Cart WHERE shopperID = ?',
                (customer_id,)
            )
            db.execute("DELETE FROM Shopping_Cart WHERE added_at <= DATETIME('now', '-1 month')")
            db.commit()
            flash('Order placed successfully!')
            return redirect(url_for('membership.cart'))
        flash(error)
    return render_template('cart/checkout.html')


@bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_item(product_id) -> Response:
    """
    Remove an item from the shopping cart.
    Args: product_id (int): The ID of the product to be removed from the cart.
    Returns: Response: A redirect to the cart page after the item is removed.
    """
    db = get_db()  # pylint: disable=invalid-name
    customer_id = session.get('userID')
    db.execute(
        'DELETE FROM Shopping_Cart WHERE shopperID = ? and productID = ?',
        (customer_id, product_id,)
    )
    db.commit()
    flash('Item removed from cart!')
    return redirect(url_for('membership.cart'))
