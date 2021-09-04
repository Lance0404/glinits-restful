__version__ = '0.1.0'

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from .settings import Config

db = SQLAlchemy()
from buying_frenzy import models
# https://stackoverflow.com/a/20749534
# models should be imported and run before any db related operation

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
    app.logger.info(f'flask app is up by Lance!')
    app.config.from_object(Config())

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # intake python file that won't be commited to SC
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # with this, tables will be created once the app is started
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()

    return app
