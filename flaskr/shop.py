from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.db import get_db

bp = Blueprint('shop', __name__)

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

    active_category = None
    if category_id:
        active_category = db.execute('SELECT CategoryID, CategoryName FROM Categories WHERE CategoryID = ?', (category_id,)).fetchone()

    return render_template('shop/browse_or_search.html', products=products, categories=categories, active_category=active_category, search_query=search_query)

@bp.route('/product/<int:product_id>')
def product_details(product_id):
    db = get_db()

    product_info = db.execute(
        '''SELECT ProductID, ProductName, UnitPrice, QuantityPerUnit
           FROM Products
           WHERE ProductID = ?''', (product_id,)).fetchone()

    return render_template('shop/product_details.html', product_info=product_info)
