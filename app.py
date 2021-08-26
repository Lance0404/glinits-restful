from buying_frenzy.factory import app, drop_all_tables, elt_from_json_to_db

@app.cli.command("drop-all")
def drop_all():
    """
    drop all tables for a fresh start
    """
    app.logger.info('to drop all tables')
    drop_all_tables()
    app.logger.info('all tables dropped')


@app.cli.command("etl")
def etl():
    app.logger.info('to etl')
    elt_from_json_to_db()


if __name__ == '__main__':
    app.run()
