import click
import json
from typing import Generator, Iterator
from deprecated import deprecated

from buying_frenzy.factory import app
from buying_frenzy.utility import (
    drop_all_tables, process_restaurant_data, process_user_data,
    integrate_restaurant_and_user_data
)

@app.cli.command("drop-all")
def drop_all():
    """
    drop all tables for a fresh start
    """
    app.logger.info('to drop all tables')
    drop_all_tables()
    app.logger.info('all tables dropped')

def json_to_generator(path: str) -> Generator:
    """
    read large json file directly into a Generator type 
    """
    return (i for i in json.load(open(path)))

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
    integrate_restaurant_and_user_data(resta_generator, user_generator)


if __name__ == '__main__':
    app.run()
