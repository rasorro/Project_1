import pytest
from flask import g, session
from app.db import get_db


@pytest.mark.parametrize(('category', 'search', 'message'), (
    ('', '', b'Products'),
    ('1', '', b'Products in Example category-1'),
    ('', 'item-1', b'Search results for "item-1"'),
    ('1', 'item', b'Products in Example category-1'),
    ('', 'item-3', b'No products found.'),
))
def test_browse_or_search(client, category, search, message):
    response = client.get('/', query_string={'category': category, 'search' : search})
    assert response.status_code == 200
    assert message in response.data


@pytest.mark.parametrize(('product_id', 'message'), (
    ('', b'No item provided'),
    ('1', b'Example item-1'),
    ('2', b'Example item-2'),
    ('3', b'Product not found'),
))
def test_product_details(client, product_id, message):
    response = client.get(f'/product/{product_id}')
    if product_id:
        assert response.status_code == 200
        assert message in response.data
    else:
        assert response.status_code == 404
        
def test_product_details_add_to_cart_signed_out(client, app, auth):
    response = client.post('/product/1', data={'quantity': 1})
    assert b'Product added to cart successfully' in response.data
    response = client.get('/cart')
    assert b'Example item-1' in response.data
    auth.login()
    response = client.get('/cart')
    assert b'Example item-1' in response.data
    with app.app_context():
        db = get_db()
        cart = db.execute(
            'SELECT * FROM [Shopping_Cart] WHERE shopperID = ?', ('TEST1',)
        ).fetchone()
        assert cart is not None