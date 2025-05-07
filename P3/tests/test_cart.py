import pytest
from flask import g, session
from app.db import get_db


def test_cart(client, auth):
    response = client.get('/cart')
    assert response.status_code == 200
    assert b'Cart' in response.data
    assert b'Your cart is empty.' in response.data
    auth.login()
    response = client.get('/cart')
    assert b'Example item-1' in response.data
    assert b'Example item-2' not in response.data


def test_checkout_get(client, auth):
    response = client.get('/cart/checkout')
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login()
    response = client.get('/cart/checkout')
    assert response.status_code == 200
    assert b'Checkout' in response.data


def test_checkout_post(client, app, auth):
    auth.login()    
    with app.app_context():  
        db = get_db()
        expired_cart = db.execute(
            'SELECT * FROM [Shopping_Cart] WHERE added_at <= DATETIME("now", "-1 month")'
        ).fetchone()
        assert expired_cart is not None
        response = client.post('/cart/checkout', data={
            'ship_name': 'Test User',
            'shipping_address': '123 Test St',
            'ship_city': 'Boston',
            'ship_region': 'Massachusetts',
            'ship_postal_code': '12345',
            'ship_country': 'USA'
        })
        expired_cart = db.execute(
            'SELECT * FROM [Shopping_Cart] WHERE added_at <= DATETIME("now", "-1 month")'
        ).fetchone()
        assert expired_cart is None
        assert response.status_code == 302
        assert response.headers["Location"] == "/cart"
        order = db.execute(
            'SELECT * FROM [Orders] WHERE ShipName = "Test User"'
        ).fetchone()
        assert order is not None
        assert order['ShipAddress'] == '123 Test St'
        assert order['ShipCity'] == 'Boston'
        assert order['ShipRegion'] == 'Massachusetts'
        assert order['ShipPostalCode'] == '12345'
        assert order['ShipCountry'] == 'USA'
        employee_id = order['EmployeeID']
        assert employee_id is not None
        employee_name = db.execute(
            'SELECT * FROM [Employees] WHERE EmployeeID = ?',
            (employee_id,)
        ).fetchone()
        assert employee_name['LastName'] == 'WEB'
        cart = db.execute(
            'SELECT * FROM [Shopping_Cart] WHERE shopperID = "TEST1"'
        ).fetchone()
        assert cart is None
    
    
@pytest.mark.parametrize(('shipping_name', 'shipping_address', 'shipping_city', 'shipping_region', 'shipping_postal_code', 'shipping_country' , 'message'), (
    ('', '123 Test St', 'Boston', 'Massachussetts', '12345', 'USA', b'Please fill out all fields'),
    ('123 Test St', '', 'Boston', 'Massachussetts', '12345', 'USA', b'Please fill out all fields'),
    ('123 Test St', '123 Test St', '', 'Massachussetts', '12345', 'USA', b'Please fill out all fields'),
    ('123 Test St', '123 Test St', 'Boston', '', '12345', 'USA', b'Please fill out all fields'),
    ('123 Test St', '123 Test St', 'Boston', 'Massachussetts', '', 'USA', b'Please fill out all fields'),
    ('123 Test St', '123 Test St', 'Boston', 'Massachussetts', '12345', '', b'Please fill out all fields'),
))
def test_checkout_post_validate_input(client, auth, shipping_name, shipping_address, shipping_city, shipping_region, shipping_postal_code, shipping_country, message):
    auth.login()
    response = client.post('/cart/checkout', data={
        'ship_name': shipping_name,
        'shipping_address': shipping_address,
        'ship_city': shipping_city,
        'ship_region': shipping_region,
        'ship_postal_code': shipping_postal_code,
        'ship_country': shipping_country
    })
    assert message in response.data
    

def test_remove_item(client, auth):
    auth.login()
    response = client.get('/cart')
    assert b'Example item-1' in response.data
    response = client.post('/cart/remove/1')
    assert response.status_code == 302
    assert response.headers["Location"] == "/cart"
    response = client.get('/cart')
    assert b'Example item-1' not in response.data