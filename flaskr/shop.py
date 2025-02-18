from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT ProductID, ProductName, UnitPrice, c.CategoryID, CategoryName'
        ' FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID'
        ' ORDER BY CategoryName DESC'
    ).fetchall()
    return render_template('shop/index.html', products=products)
