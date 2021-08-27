from typing import Generator
from buying_frenzy import db
from .entity import Restaurant as RestaurantEntity
from .service import RestaurantService

# put utilies here to keep app.py concise
def drop_all_tables():
    db.drop_all()
    db.session.commit()

def process_restaurant_data(data: Generator):
    """
    import data to psql
    """
    # def do(item: dict):
    #     rest = RestaurantEntity(item)
    #     print(rest)

    # TODO: structure data
    while True:
        try:
            item = next(data)
        except StopIteration:
            break
        else:
            RestaurantService.create(RestaurantEntity(item))
            # do one for quick parse test
            break


def process_user_data(data: Generator):
    """
    import data to psql
    """
    pass