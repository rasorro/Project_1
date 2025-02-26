import pytest
from flask import g, session
from flaskr.db import get_db

@pytest.mark.parametrize(('category', 'search', 'message'), (
    ('', '', b'<h2>Products</h2>'),
    ('1', '', b'Example item-1'),
    ('', 'item-1', b'Example item-1'),
    ('1', 'item', b'Example item-1'),
))
def test_browse_or_search(client, category, search, message):
    response = client.get('/', query_string={'category': category, 'search' : search})
    assert response.status_code == 200
    assert message in response.data

@pytest.mark.parametrize(('product_id', 'message'), (
    ('', b'No item provided'),
    ('1', b'Example item-1'),
    ('2', b'Example item-2'),
    ('3', b'Item not available'),
))
def test_product_details(client, product_id, message):
    response = client.get(f'/product/{product_id}')
    if product_id in ['1', '2']:
        assert response.status_code == 200
        assert message in response.data
    else:
        assert response.status_code == 404