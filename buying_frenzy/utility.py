from typing import Generator
from buying_frenzy import db
from .entity import CustomerEntity, RestaurantEntity
from .service import RestaurantService, CustomerService
from .factory import app

# put utilies here to keep app.py concise
def drop_all_tables():
    db.drop_all()
    db.session.commit()

def process_restaurant_data(data: Generator):
    """Import data to database
    """
    app.logger.info('start processing restaurant data')
    while True:
        try:
            item = next(data)
        except StopIteration:
            break
        else:
            RestaurantService.create(RestaurantEntity(item))
            # FIXME: do one for quick parse test, remember to remove the break
            break
    app.logger.info('finished processing restaurant data')        


def process_user_data(data: Generator):
    """Import user data to database
    """
    app.logger.info('start processing user data')
    while True:
        try:
            item = next(data)
        except StopIteration:
            break
        else:
            CustomerService.create(CustomerEntity(item))
            # FIXME: do one for quick parse test, remember to remove the break
            break
    app.logger.info('finished processing user data')  