from typing import Generator, Tuple
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

def integrate_restaurant_and_user_data(restaurant_data: Generator, user_data: Generator) -> Tuple[Generator, Generator]:
    """After preprocessing the whole purchaseHistory of a user can be discarded

    Goal:
    1. increase `cashBalance` of restaurants accordingly
    2. decrease `cashBalance` of users accordingly (this does not require restaurant data)
    """
    app.logger.info('start integrate_restaurant_and_user_data()')

    # TODO: could it be optimized?
    restaurant_gain = dict()
    modified_user_data = get_restaurant_gain_and_modify_user_data(restaurant_gain, user_data)
    # the `restaurant_gain` will only be complete if the whole `modified_user_data` was iterated through

    # CAVEAT: use list comprehension to exhaust generator & create another generator from that list 
    # TODO: is there a better way?
    new_user_data = (j for j in [i for i in modified_user_data])
    app.logger.debug(restaurant_gain)

    new_restaurant_data: Generator = (process_a_restaurant_cash_balance(i, restaurant_gain) for i in restaurant_data)

    return tuple(new_user_data, new_restaurant_data)

def get_restaurant_gain_and_modify_user_data(restaurant_gain: dict, user_data: Generator) -> Generator:
    """Try to get the most out of the user_data generator,
    cause it can only be iterated once.
    """
    for i in user_data:
        # print(f"original [{i['name']}] cashBalance: {i['cashBalance'] }")
        for j in i['purchaseHistory']:
            # case 1: process cashBalance for restaurant
            restaurant_gain.setdefault(j['restaurantName'], float())
            restaurant_gain[j['restaurantName']] += j['transactionAmount']

            # case 2: process cashBalance for user
            i['cashBalance'] -= j['transactionAmount']
        # remove the `purchaseHistory` key & its value which is no longer used
        # use pop() instead of `del` to avoid potential KeyError
        i.pop('purchaseHistory', None)    
        # print(f"finalized [{i['name']}] cashBalance: {i['cashBalance'] }")
        yield i

def process_a_restaurant_cash_balance(a_resta: dict, restaurant_gain: dict):
    """Modify `a_resta` in place
    """
    print(f"[{a_resta['restaurantName']}] cashBalance before: {a_resta['cashBalance']}")
    a_resta['cashBalance'] += restaurant_gain[a_resta['restaurantName']]
    print(f"[{a_resta['restaurantName']}] cashBalance after: {a_resta['cashBalance']}")
    


# FIXME: currently not used 
def process_a_restaurant_against_all_user(a_resta: dict, user_data: Generator) -> dict:
    """Update the `cashBalance` of a restaurant by scanning through all the users' purchaseHistory

    The dishName matters not.

            "purchaseHistory": [
            {
                "dishName": "Salmon Traymore",
                "restaurantName": "Wild Salsa",
                "transactionAmount": 10.6,

    """
    print(f"original [{a_resta['restaurantName']}] cashBalance: {a_resta['cashBalance']}")
    for i in user_data:
        print(f"user [{i['name']}]")
        for j in i['purchaseHistory']:
            if j['restaurantName'] == a_resta['restaurantName']:
                a_resta['cashBalance'] += j['transactionAmount']
                print(f"change made: {a_resta['cashBalance']}")
        # the `user_data` generator seems exhausted after one thorough loop
    print(f"final [{a_resta['restaurantName']}] cashBalance: {a_resta['cashBalance']}")
