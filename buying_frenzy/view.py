from flask import current_app
from dateutil.parser import parse
from datetime import datetime

from .service import RestaurantService

logger = current_app.logger

def list_restaurant(dt: str=None):
    logger.debug(f'start function list_restaurant({dt})')
    dt = parse(dt) if dt else datetime.now()
    print(f'datetime {dt}')
    RestaurantService.list_available_restaurant_by(dt)
    
    