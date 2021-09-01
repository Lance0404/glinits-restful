from flask import Blueprint, jsonify, current_app, request
from flask_restx import Api, Resource

from buying_frenzy.errors import InvalidUrlPath
from ...view import View

logger = current_app.logger

# FIXME: found at most 400 in database  
MAX_DISH_PRICE=500

# `url_prefix` of Blueprint leads to swagger url
# http://127.0.0.1:5000/v1/
bp = Blueprint('restaurant', __name__, url_prefix='/v1')

# `doc` only append to the swagger url, does not affect the resource routes
# http://127.0.0.1:5000/v1/doc/
api = Api(bp, version="1.0", title="Buying Frenzy", doc='/doc/', description="Buying Frenzy APIs")

# `namespace` will append extra string to the path
# http://127.0.0.1:5000/v1/restaurant
ns_rest = api.namespace("restaurant", description="restaurant operations")
# http://127.0.0.1:5000/v1/user
ns_user = api.namespace("user", description="customer operations")

# FIXME: intiated two parsers, ugly
parser_1 = ns_rest.parser()
parser_1.add_argument('datetime', type=str, default='08/31/2021 10:37 PM', location='args', help='datetime should be str')

parser_2 = ns_rest.parser()
parser_2.add_argument('min', type=float, default=0, location='args', help='price range lower bound')
parser_2.add_argument('max', type=float, default=500, location='args', help='price range upper bound')

@ns_rest.route("/list")
@ns_rest.doc(responses={404: "What the fuck is going on"})
class ListOpeningRestaurant(Resource):

    @ns_rest.doc(parser=parser_1, description="list opened restaurant by datetime")
    def get(self):
        """list opened restaurant"""
        logger.info('start list()...')
        datetime = parser_1.parse_args(strict=True).get('datetime')
        open_restaurants = View.list_restaurant(datetime) if datetime else View.list_restaurant()
        return jsonify(counts=len(open_restaurants), open_restaurants=open_restaurants)
        
# FIXME: defaults set on path variable not shown on swagger
@ns_rest.route("/list/<int:restaurant_count>/dish/<string:action>/<int:dish_count>/price", defaults={'restaurant_count': 5, 'action': 'less', 'dish_count': 10})
@ns_rest.doc(responses={404: "What the fuck is going on"})
class ListTopRestaurantByDishAndPrice(Resource):
    
    @ns_rest.doc(params=dict(restaurant_count='top y restaurants', action='[more/less]', dish_count='x number of dishes'), parser=parser_2, description="List top y restaurants that have more or less than x number of dishes within a price range")
    def get(self, restaurant_count: int, action: str, dish_count: int):
        """List top y restaurants by dish count within a price range"""
        args = parser_2.parse_args(strict=True)
        if action not in ['more', 'less']:
            raise InvalidUrlPath(f'{request.url}')
        data = View.list_by_dish_count_and_price_range(restaurant_count, action, dish_count,
            max = args['max'] if args.get('max', None) else MAX_DISH_PRICE, 
            min = args['min'] if args.get('min', None) else 0
        )
        return jsonify([i for i in data])

@ns_rest.route("/search/<string:type_>/<string:term>")
@ns_rest.doc(responses={404: "What the fuck is going on"})
class SearchBy(Resource):
    """
    Did not implement fancy recommendation algorithm under the hood
    """

    @ns_rest.doc(params=dict(type_='[restaurant/dish]', term='to search for'), description="Search for restaurants or dishes by name, ranked by relevance to search term")
    def get(self, type_: str, term: str):
        """Search for restaurants or dishes by name, ranked by relevance"""
        logger.info(f'start search_by(type={type_}, term={term})...')
        if type_ not in ('restaurant', 'dish'):
            raise InvalidUrlPath(f'{request.url}')
        return jsonify([[i[0], i[1]] for i in View.search_by_type_and_term(type_, term)])

@ns_user.route("/<int:user_id>/buy/<int:restaurant_id>/<int:dish_id>")
@ns_user.doc(responses={404: "What the fuck is going on"})
class Buy(Resource):
    """
    Always one at a time!
    TODO: consider using restaurant pk or dish id for search
    """
    
    @ns_user.doc(params=dict(user_id='start from 0', restaurant_id='start from 1', dish_id='start from 1'), description="Process a user purchasing a dish from a restaurant, handling all relevant data changes in an atomic transaction")
    def put(self, user_id: int, restaurant_id: int, dish_id: int):
        """User buy a dish from a restaurant"""
        logger.info(f'start buy({user_id}, {restaurant_id}, {dish_id})')
        View.buy(user_id, restaurant_id, dish_id)
        return jsonify('transaction successful')

