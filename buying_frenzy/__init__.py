__version__ = '0.1.0'

import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from werkzeug.middleware.proxy_fix import ProxyFix

from .settings import Config
from .models import db

def create_app(test_config: dict = None):
    """
    a factory function take cares of how the app should be initiated, including the config for db

    precedence of configuration stretagy (according to the logic of this function):
    1. .flaskenv (used by docker-compose `env_file`)
    2. .env (used by local development with `flask run`)
    3. from_object()
    4. from_pyfile() or from_mapping() (overrides all above)
    """
    # `instance_relative_config` is required for from_pyfile() to find the file
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.logger.info(f'flask app is up by Lance!')

    if test_config is None:
        app.config.from_object(Config())
        # load the instance config, if it exists, when not testing
        # intake python file that won't be commited to SC
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, test_config.get('DB_NAME', 'test.db'))
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    # with this, tables will be created once the app is started
    with app.app_context():

        from .cli import bp as cli_bp
        from .endpoints.v1.hello import bp as hello_bp
        from .endpoints.v1.restaurant import bp as restaurant_bp

        app.register_blueprint(cli_bp)
        app.register_blueprint(hello_bp)
        app.register_blueprint(restaurant_bp)

        db.init_app(app)
        db.create_all()
        db.session.commit()

    return app
