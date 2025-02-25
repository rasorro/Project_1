from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('shop', __name__)

def index():
    db = get_db()
    products = db.execute(
        'SELECT ProductID, ProductName, UnitPrice, c.CategoryID, CategoryName'
        ' FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID'
        ' ORDER BY CategoryName DESC'
    ).fetchall()
    return render_template('shop/index.html', products=products)

@bp.route('/')
def browse_or_search():
    db = get_db()
    category_id = request.args.get('category')
    search_query = request.args.get('search')

    query = ('SELECT ProductID, ProductName, UnitPrice, c.CategoryID, CategoryName'
        ' FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID')

    params = []

    if category_id:
        query += ' WHERE p.CategoryID = ?'
        params.append(category_id)
    elif search_query:
        query += ' WHERE p.ProductName LIKE ?'
        params.append(f'%{search_query}%')

    query += ' ORDER BY CategoryName'

    products = db.execute(query, params).fetchall()

    categories = db.execute('SELECT CategoryID, CategoryName FROM Categories').fetchall()

    return render_template('shop/browse_or_search.html', products=products, categories=categories)

@bp.route('/product/<int:product_id>')
def product_details(product_id):
    db = get_db()

    product_info = db.execute(
        '''SELECT ProductID, ProductName, UnitPrice, QuantityPerUnit
           FROM Products
           WHERE ProductID = ?''', (product_id,)).fetchone()

    if product_info is None:
        abort(404, "Item not available")

    return render_template('shop/product_details.html', product_info=product_info)
