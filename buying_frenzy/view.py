from typing import Generator
from flask import current_app
from dateutil.parser import parse
from datetime import datetime

from .service import RestaurantService, CustomerService

logger = current_app.logger

class View():

    @classmethod
    def list_restaurant(cls, dt: str=None) -> list:
        logger.info(f'start {cls.__name__}.list_restaurant({dt})...')
        dt = parse(dt) if dt else datetime.now()
        return [i for i in RestaurantService.list_available_restaurant_by(dt)]
    
    @classmethod
    def list_by_dish_count_and_price_range(cls, restaurant_count: int, action: str, dish_count: int, **kwargs) -> Generator:
        logger.info(f'start {cls.__name__}.list_by_dish_count_and_price_range({restaurant_count}, {action}, {dish_count}, {kwargs})...')
        for i in RestaurantService.list_by_dish_count_and_price_range(restaurant_count, action, dish_count, **kwargs):
            yield dict(
                restaurant_name = i[0],
                dish_count = i[1]
            )

    @classmethod
    def search_by_type_and_term(cls, type_: str, term: str) -> Generator:
        logger.info(f'start {cls.__name__}.search_by_type_and_term({type_}, {term})')
        return (RestaurantService.search_by_type_and_term(term) if type_ == 'restaurant' 
            else CustomerService.search_by_type_and_term(term))

    @classmethod
    def buy(cls, user_id: int, restaurant_id: int, dish_id: int):
        logger.info(f'start {cls.__name__}.buy({user_id}, {restaurant_id}, {dish_id})...')
        CustomerService.buy(user_id, restaurant_id, dish_id)