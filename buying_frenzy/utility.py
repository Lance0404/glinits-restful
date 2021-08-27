from typing import Generator
from buying_frenzy import db
from .entity import RestaurantEntity
from .service import RestaurantService
from .factory import app

# put utilies here to keep app.py concise
def drop_all_tables():
    db.drop_all()
    db.session.commit()

def process_restaurant_data(data: Generator):
    """
    import data to database
    """
    app.logger.info('start processing restaurant data')
    while True:
        try:
            item = next(data)
        except StopIteration:
            break
        else:
            RestaurantService.create(RestaurantEntity(item))
            # do one for quick parse test
            break
    app.logger.info('finished processing restaurant data')        


def process_user_data(data: Generator):
    """
    import user data to database
    """
    app.logger.info('start processing user data')
    pass