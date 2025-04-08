"""
Defines the `create_app` function, which initializes and configures
a Flask application instance. It sets up the database, registers blueprints,
and loads configuration settings.
"""

import os
from flask import Flask

from . import db
from . import auth
from . import shop
from . import cart

def create_app(test_config=None) -> Flask:
    """
    Creates and configures the flask application

    Parameters:
        test_config : dict, optional
            A dictionary of configuration settings for testing purposes.

    Returns:
        Flask
       	    A configured Flask application instance.
	"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'northwind.db'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(shop.bp)
    app.add_url_rule('/', endpoint='index')

    app.register_blueprint(cart.bp)
    app.add_url_rule('/', endpoint='cart')

    return app
