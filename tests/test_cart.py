import pytest
from flask import g, session
from flaskr.db import get_db

def test_cart(client, auth):
    response = client.get('/cart/')
    assert response.status_code == 200
    assert b'Cart' in response.data
    # needs tests for cart items

def test_checkout_get(client, auth):
    response = client.get('/cart/checkout')
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login()
    response = client.get('/cart/checkout')
    assert response.status_code == 200
    assert b'Checkout' in response.data

def test_checkout_post(client, auth, app):
    auth.login()
    response = client.post('/cart/checkout', data={
        'shipping_name': 'Test User',
        'shipping_address': '123 Test St',
        'shipping_city': 'Boston',
        'shipping_region': 'Massachusetts',
        'shipping_postal_code': '12345',
        'shipping_country': 'USA'
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    with app.app_context():
        db = get_db()
        order = db.execute(
            'SELECT * FROM [Orders] WHERE ShipName = "Test User"'
        ).fetchone()
        assert order is not None
        assert order['ShipAddress'] == '123 Test St'
        assert order['ShipCity'] == 'Boston'
        assert order['ShipRegion'] == 'Massachusetts'
        assert order['ShipPostalCode'] == '12345'
        assert order['ShipCountry'] == 'USA'
        cart = db.execute(
            'SELECT * FROM [Shopping_Cart] WHERE ShipName = "Test User"'
        ).fetchone()
        assert order is None
    
@pytest.mark.parametrize(('shipping_name', 'shipping_address', 'shipping_city', 'shipping_region', 'shipping_postal_code', 'shipping_country' , 'message'), (
    ('', '123 Test St', 'Boston', 'Massachussetts', '12345', 'USA', b'Shipping Name is required.'),
    ('123 Test St', '', 'Boston', 'Massachussetts', '12345', 'USA', b'Shipping Address is required.'),
    ('123 Test St', '123 Test St', '', 'Massachussetts', '12345', 'USA', b'Shipping City is required.'),
    ('123 Test St', '123 Test St', 'Boston', '', '12345', 'USA', b'Shipping Region is required.'),
    ('123 Test St', '123 Test St', 'Boston', 'Massachussetts', '', 'USA', b'Shipping Postal Code is required.'),
    ('123 Test St', '123 Test St', 'Boston', 'Massachussetts', '12345', '', b'Shipping Country is required.'),
))
def test_checkout_post_validate_input(client, auth, shipping_name, shipping_address, shipping_city, shipping_region, shipping_postal_code, shipping_country, message):
    auth.login()
    response = client.post('/cart/checkout', data={
        'shipping_name': shipping_name,
        'shipping_address': shipping_address,
        'shipping_city': shipping_city,
        'shipping_region': shipping_region,
        'shipping_postal_code': shipping_postal_code,
        'shipping_country': shipping_country
    })
    assert message in response.data