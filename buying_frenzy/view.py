import json
from typing import Generator, Tuple
from flask import current_app
from dateutil.parser import parse
from datetime import datetime

from .entity import RestaurantEntity, CustomerEntity
from .service import RestaurantService, CustomerService

class View():

    @classmethod
    def list_restaurant(cls, dt: str=None) -> list:
        current_app.logger.info(f'start {cls.__name__}.list_restaurant({dt})...')
        dt = parse(dt) if dt else datetime.now()
        return [i for i in RestaurantService.list_available_restaurant_by(dt)]
    
    @classmethod
    def list_by_dish_count_and_price_range(cls, restaurant_count: int, action: str, dish_count: int, **kwargs) -> Generator:
        current_app.logger.info(f'start {cls.__name__}.list_by_dish_count_and_price_range({restaurant_count}, {action}, {dish_count}, {kwargs})...')
        for i in RestaurantService.list_by_dish_count_and_price_range(restaurant_count, action, dish_count, **kwargs):
            yield dict(
                restaurant_name = i[0],
                dish_count = i[1]
            )

    @classmethod
    def search_by_type_and_term(cls, type_: str, term: str) -> Generator:
        current_app.logger.info(f'start {cls.__name__}.search_by_type_and_term({type_}, {term})')
        return (RestaurantService.search_by_type_and_term(term) if type_ == 'restaurant' 
            else CustomerService.search_by_type_and_term(term))

    @classmethod
    def buy(cls, user_id: int, restaurant_id: int, dish_id: int):
        current_app.logger.info(f'start {cls.__name__}.buy({user_id}, {restaurant_id}, {dish_id})...')
        CustomerService.buy(user_id, restaurant_id, dish_id)

# FIXME: below functions could be refactored to be neater
def json_to_generator(path: str) -> Generator:
    """
    read large json file directly into a Generator type 
    """
    return (i for i in json.load(open(path)))

def integrate_restaurant_and_user_data(restaurant_data: Generator, user_data: Generator) -> Tuple[Generator, Generator]:
    """After preprocessing the whole purchaseHistory of a user can be discarded

    Goal:
    1. increase `cashBalance` of restaurants accordingly
    2. decrease `cashBalance` of users accordingly (this does not require restaurant data)
    """
    current_app.logger.info('start integrate_restaurant_and_user_data()...')

    # TODO: could it be optimized?
    restaurant_gain = dict()
    modified_user_data = get_restaurant_gain_and_modify_user_data(restaurant_gain, user_data)
    # the `restaurant_gain` will only be completed if the whole `modified_user_data` was iterated through

    # CAVEAT: use list comprehension to exhaust generator & create another generator from that list 
    # TODO: is there a better way?
    new_user_data = (j for j in [i for i in modified_user_data])
    # current_app.logger.debug(restaurant_gain)

    new_restaurant_data: Generator = (process_a_restaurant_cash_balance(i, restaurant_gain) for i in restaurant_data)
    # current_app.logger.info('finished integrate_restaurant_and_user_data()')
    return (new_restaurant_data, new_user_data,)

def get_restaurant_gain_and_modify_user_data(restaurant_gain: dict, user_data: Generator) -> Generator:
    """Try to get the most out of the user_data generator,
    cause it can only be iterated once.
    """
    # current_app.logger.info('start get_restaurant_gain_and_modify_user_data()...')
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

def process_a_restaurant_cash_balance(a_resta: dict, restaurant_gain: dict) -> dict:
    """Modify `a_resta` in place
    """
    # current_app.logger.debug(f"[{a_resta['restaurantName']}] cashBalance before: {a_resta['cashBalance']}")
    # CAVEAT: `restaurant_gain` dict might not contain all restaurants as keys if there is no user consume record
    a_resta['cashBalance'] += restaurant_gain.setdefault(a_resta['restaurantName'], 0)
    # current_app.logger.debug(f"[{a_resta['restaurantName']}] cashBalance after: {a_resta['cashBalance']}")
    return a_resta

def process_restaurant_data(data: Generator):
    """Import data to database
    """
    current_app.logger.info('start process_restaurant_data()...')
    for i in data:
        RestaurantService.create(RestaurantEntity(i))
        # FIXME: do one for quick test
        # break
    current_app.logger.info('finished process_restaurant_data()')        


def process_user_data(data: Generator):
    """Import user data to database
    """
    current_app.logger.info('start process_user_data()...')
    for i in data:
        CustomerService.create(CustomerEntity(i))
        # FIXME: do one for quick test
        # break
    current_app.logger.info('finished process_user_data()')

# FIXME: deprecated
def process_a_restaurant_against_all_user(a_resta: dict, user_data: Generator) -> dict:
    """Update the `cashBalance` of a restaurant by scanning through all the users' purchaseHistory

    The dishName matters not.
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