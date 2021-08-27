from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from buying_frenzy import db
from buying_frenzy.default_settings import Config
from buying_frenzy.model import *
# https://stackoverflow.com/a/20749534
# models should be imported and run before any db related operation 
# e.g. create_all(), drop_all()

def create_app():
    """
    database will be create if not exist
    """
    app = Flask(__name__)
    app.logger.info(f'flask app is up by Lance!')
    app.config.from_object(Config())

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()

        from .api.v1.hello import bp as hello_bp
        
        app.register_blueprint(hello_bp, url_prefix='/v1')
        # above will overwrite the `url_prefix` defined in the Blueprint() constructor
    return app

app = create_app()
