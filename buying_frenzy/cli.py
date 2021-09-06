import click
import json
from flask import current_app, Blueprint
from flask.cli import with_appcontext
from sqlalchemy.exc import OperationalError
from sqlite3 import IntegrityError

from . import db
from .view import json_to_generator, integrate_restaurant_and_user_data, process_restaurant_data, process_user_data

from buying_frenzy.endpoints.v1.restaurant import api
from .errors import CommitError

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.command("drop-all")
def drop_all():
    """
    drop all tables for a fresh start
    """
    current_app.logger.info('to drop all tables')
    db.drop_all()
    db.session.commit()
    current_app.logger.info('all tables dropped')

# FIXME: might not be necessary, cause every time db is invoked, the app will be invoked 
@bp.cli.command("create-all")
def create_all():
    """
    drop all tables for a fresh start
    """
    current_app.logger.info('to create all tables')
    db.create_all()
    db.session.commit()
    current_app.logger.info('all tables created')

@bp.cli.command("pre-etl")
@with_appcontext
@click.option('--dir', default='data')
def pre_etl(dir: str):
    """Preprocess raw data before loading them into database

    checked which has more items:
    cat data/restaurant_with_menu.json| grep -c 'openingHours'
    2203

    cat data/users_with_purchase_history.json | grep -c 'purchaseHistory'
    1000

    Restaurant items is more than User data, but we still need to use user data to loop through restaurant data
    """
    resta_generator = json_to_generator(f'{dir}/restaurant_with_menu.json')
    user_generator = json_to_generator(f'{dir}/users_with_purchase_history.json')
    (new_resta_generator, new_user_generator) = integrate_restaurant_and_user_data(resta_generator, user_generator)
    process_restaurant_data(new_resta_generator)
    process_user_data(new_user_generator)

# FIXME: to be checked!
@bp.cli.command("postman")
def to_postman():
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    with open('data/glinits.json', 'w') as outfile:
        json.dump(data, outfile)

# FIXME: deprecated
@bp.cli.command("etl")
@click.argument("path")
def etl(path):
    """Run command at project root like:
    `flask etl data/restaurant_with_menu.json`
    or 
    `flask etl data/users_with_purchase_history.json`

    This only naively load raw data into database without preprocessing
    """
    current_app.logger.info('start ETL')
    data_generator = json_to_generator(path)
    if 'restaurant_with_menu' in path:
        process_restaurant_data(data_generator)
    elif 'users_with_purchase_history' in path:
        process_user_data(data_generator)
    current_app.logger.info('end ETL')