from typing import Generator
from flask import current_app
from dateutil.parser import parse
from datetime import datetime

from .service import RestaurantService

logger = current_app.logger

def list_restaurant(dt: str=None) -> list:
    logger.info(f'start list_restaurant({dt})...')
    dt = parse(dt) if dt else datetime.now()
    return [i for i in RestaurantService.list_available_restaurant_by(dt)]
    
def list_by_dish_count_and_price_range(restaurant_count: int, action: str, dish_count: int, **kwargs):
    logger.info(f'start list_by_dish_count_and_price_range({restaurant_count}, {action}, {dish_count}, {kwargs})...')
    RestaurantService.list_by_dish_count_and_price_range(restaurant_count, action, dish_count, **kwargs)
    breakpoint()