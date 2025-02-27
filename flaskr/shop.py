from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from unidecode import unidecode

bp = Blueprint('shop', __name__)

def create_unidecode_function(db):
    db.create_function("unidecode", 1, unidecode)

@bp.route('/')
def browse_or_search():
    db = get_db()
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
        get_category_name_query = 'SELECT CategoryID, CategoryName FROM Categories WHERE CategoryID = ?'
        active_category = db.execute(get_category_name_query, (category_id,)).fetchone()
    elif search_query:
        query += ' WHERE unidecode(p.ProductName) LIKE unidecode(?)'
        params.append(f'%{search_query.strip()}%')

    query += ' ORDER BY ProductName'

    products = db.execute(query, params).fetchall()

    categories = db.execute('SELECT CategoryID, CategoryName FROM Categories').fetchall()

    return render_template('shop/browse_or_search.html', products=products, categories=categories, active_category=active_category, search_query=search_query)

@bp.route('/product/<int:product_id>')
def product_details(product_id):
    db = get_db()

    product_info = db.execute(
        '''SELECT ProductID, ProductName, UnitPrice, QuantityPerUnit
           FROM Products
           WHERE ProductID = ?''', (product_id,)).fetchone()

    return render_template('shop/product_details.html', product_info=product_info)
