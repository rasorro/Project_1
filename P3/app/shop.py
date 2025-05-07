"""
Handles the browsing and searching functionality for products in the shop.
"""

import uuid
from flask import (
    Blueprint, flash, render_template, request, session, Response
)
from unidecode import unidecode
from app.db import get_db


bp = Blueprint('shop', __name__)


def create_unidecode_function(db):  #pylint: disable=invalid-name
    """
    Creates a custom SQLite function for unidecoding strings.
    Args: db (Connection): The database connection object.
    """
    db.create_function("unidecode", 1, unidecode)


@bp.route('/')
def browse_or_search() -> Response:
    """
    Browse products by category or search for products.
    Returns: Response: The rendered 'browse_or_search.html' template
    with product listings and category filters.
    """
    db = get_db()  #pylint: disable=invalid-name
    create_unidecode_function(db)
    category_id = request.args.get('category')
    search_query = request.args.get('search')

    query = ('SELECT ProductID, ProductName, UnitPrice, c.CategoryID, CategoryName'
        ' FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID')

    params = []

    active_category = None
    if category_id:
        query += ' WHERE p.CategoryID = ?'
        params.append(category_id)
        get_category_name_query = 'SELECT CategoryID, CategoryName FROM Categories WHERE CategoryID = ?' #pylint: disable=line-too-long
        active_category = db.execute(get_category_name_query, (category_id,)).fetchone()
    elif search_query:
        query += ' WHERE unidecode(p.ProductName) LIKE unidecode(?)'
        params.append(f'%{search_query.strip()}%')

    query += ' ORDER BY ProductName'

    products = db.execute(query, params).fetchall()

    categories = db.execute('SELECT CategoryID, CategoryName FROM Categories').fetchall()

    return render_template('shop/browse_or_search.html', products=products, categories=categories, active_category=active_category, search_query=search_query)  #pylint: disable=line-too-long


@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def product_details(product_id) -> Response:
    """
    View details of a specific product and add it to the shopping cart.
    Returns: Response: The rendered 'product_details.html' template with product details.
    """
    db = get_db()  #pylint: disable=invalid-name
    if request.method == 'POST':
        if 'userID' not in session:
            session['userID'] = str(uuid.uuid4())
        quantity = int(request.form['quantity'])
        db.execute(
            'INSERT INTO [Shopping_Cart] (shopperID, productID, quantity) VALUES (?, ?, ?)',
            (session.get('userID'), product_id, quantity)
        )
        db.commit()
        flash('Product added to cart successfully!')
    product_info = db.execute(
        '''SELECT ProductID, ProductName, UnitPrice, QuantityPerUnit
           FROM Products
           WHERE ProductID = ?''', (product_id,)).fetchone()
    return render_template('shop/product_details.html', product_info=product_info)
