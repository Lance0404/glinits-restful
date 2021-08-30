from flask import (
    Blueprint,
    jsonify,
    current_app,
    request
)

from ..errors import InvalidUrlPath
from ...view import (
    list_restaurant, list_by_dish_count_and_price_range,
)

logger = current_app.logger
bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@bp.route('/list')
def list():
    """http://localhost:5000/v1/restaurant/list
    """
    logger.info('start list()...')
    # logger.debug(f'request.args {request.args}')
    datetime = request.args.get('datetime')
    open_restaurants = list_restaurant(datetime) if datetime else list_restaurant()
    return jsonify(counts=len(open_restaurants), open_restaurants=open_restaurants)

# TODO: add pagination someday
@bp.route('/list/<restaurant_count>/dish/<action>/<dish_count>/price')
def list_top_restaurant_by_dish_count(restaurant_count: str, action: str, dish_count: int):
    """List top y restaurants that have more or less than x number of dishes within a price range
    
    Example:
    http://localhost:5000/v1/restaurant/list/5/dish/less/10/price
    """
    logger.info(f'start list_top_restaurant_by_dish_count()...')
    if action not in ['more', 'less']:
        raise InvalidUrlPath(f'{request.url}')

    try:
        restaurant_count = int(restaurant_count)
        dish_count = int(dish_count)
    except ValueError as e:
        raise InvalidUrlPath(f'{request.url}')
    
    list_by_dish_count_and_price_range(restaurant_count, action, dish_count,
        max = request.args.get('max', float('inf')), 
        min = request.args.get('min', 0)
    )
    return jsonify()