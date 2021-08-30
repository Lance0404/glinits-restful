from flask import (
    Blueprint,
    jsonify,
    current_app,
    request
)

from ..errors import InvalidUrlPath
from ...view import View

logger = current_app.logger
bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@bp.route('/list')
def list():
    """http://localhost:5000/v1/restaurant/list
    """
    logger.info('start list()...')
    # logger.debug(f'request.args {request.args}')
    datetime = request.args.get('datetime')
    open_restaurants = View.list_restaurant(datetime) if datetime else View.list_restaurant()
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
        logger.error(e)
        raise InvalidUrlPath(f'{request.url}')
    
    data = View.list_by_dish_count_and_price_range(restaurant_count, action, dish_count,
        max = request.args.get('max', float('inf')), 
        min = request.args.get('min', 0)
    )
    return jsonify([i for i in data])

@bp.route('/search/<type_>/<term>')
def search_by(type_: str, term: str):
    """
    Search for restaurants or dishes by name, ranked by relevance to search term

    Did not implement fancy recommendation algorithm under the hood
    """
    logger.info('start search_by(type={type}, term={term})...')
    if type_ not in ('restaurant', 'dish'):
        raise InvalidUrlPath(f'{request.url}')
    return jsonify([[i[0], i[1]] for i in View.search_by_type_and_term(type_, term)])

@bp.route('/user/<user_id>/buy/<restaurant_id>/<dish_id>')
def buy(user_id: str, restaurant_id: str, dish_id: str):
    """"
    Process a user purchasing a dish from a restaurant, handling all relevant data changes in an atomic transaction

    Always one at a time!

    TODO: consider using restaurant pk or dish id for search

    Example:
    http://localhost:5000/v1/restaurant/user/<user_id>/buy/<restaurant_id>/<dish_id>
    """
    logger.info(f'start buy({user_id}, {restaurant_id}, {dish_id})')
    try:
        user_id = int(user_id)
        restaurant_id = int(restaurant_id)
        dish_id = int(dish_id)
    except ValueError as e:
        logger.error(e)
        raise InvalidUrlPath(f'{request.url}')
    View.buy(user_id, restaurant_id, dish_id)
        
    return jsonify()