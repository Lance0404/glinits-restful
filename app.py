import click
import json
from typing import Generator, Iterator

from buying_frenzy.factory import app
from buying_frenzy.utility import drop_all_tables, process_restaurant_data, process_user_data

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
def etl(path):
    """
    run command at project root like:
    `flask etl data/restaurant_with_menu.json`
    or 
    `flask etl data/users_with_purchase_history.json`
    """
    app.logger.info('do ETL')

    data_generator = json_to_generator(path)
    if 'restaurant_with_menu' in path:
        app.logger.info('start processing restaurant data')
        process_restaurant_data(data_generator)
    elif 'users_with_purchase_history' in path:
        app.logger.info('start processing user data')
        process_user_data(data_generator)
    
if __name__ == '__main__':
    app.run()
