from flask import current_app
from dateutil.parser import parse
from datetime import datetime

from .service import RestaurantService

logger = current_app.logger

def list_restaurant(dt: str=None):
    logger.debug(f'start function list_restaurant({dt})')
    time = parse(dt).timetz() if dt else datetime.now().timetz()
    print(f'time {time}')
    RestaurantService.list_restaurant_by(time)
    
    