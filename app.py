import click
from deprecated import deprecated
from flask import json

from buying_frenzy.factory import app
from buying_frenzy.utility import (
    drop_all_tables, process_restaurant_data, process_user_data,
    integrate_restaurant_and_user_data, json_to_generator
)
from buying_frenzy.endpoints.v1.restaurant import api

@app.cli.command("drop-all")
def drop_all():
    """
    drop all tables for a fresh start
    """
    app.logger.info('to drop all tables')
    drop_all_tables()
    app.logger.info('all tables dropped')

@app.cli.command("pre-etl")
def pre_etl():
    """Preprocess raw data before loading them into database

    checked which has more items:
    cat data/restaurant_with_menu.json| grep -c 'openingHours'
    2203

    cat data/users_with_purchase_history.json | grep -c 'purchaseHistory'
    1000

    Restaurant items is more than User data, but we still need to use loop through restaurant data
    """

    resta_generator = json_to_generator('data/restaurant_with_menu.json')
    user_generator = json_to_generator('data/users_with_purchase_history.json')
    (new_resta_generator, new_user_generator) = integrate_restaurant_and_user_data(resta_generator, user_generator)
    process_restaurant_data(new_resta_generator)
    process_user_data(new_user_generator)

# FIXME: currently not used
@app.cli.command("etl")
@click.argument("path")
@deprecated
def etl(path):
    """Run command at project root like:
    `flask etl data/restaurant_with_menu.json`
    or 
    `flask etl data/users_with_purchase_history.json`

    This only naively load raw data into database without preprocessing
    """
    app.logger.info('start ETL')
    data_generator = json_to_generator(path)
    if 'restaurant_with_menu' in path:
        process_restaurant_data(data_generator)
    elif 'users_with_purchase_history' in path:
        process_user_data(data_generator)
    app.logger.info('end ETL')

@app.cli.command("postman")
def to_postman():
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    with open('data/glinits.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    app.run()
