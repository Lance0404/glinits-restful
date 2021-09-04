# TODO: this file is having duplicated functionality as `buying_frenzy/endpoints/__init__.py`
# TODO: try to handle all errors in `buying_frenzy/errors.py`
from flask import jsonify

from .hello import bp as bp_hello
from .restaurant import bp as bp_restaurant
from buying_frenzy.errors import Common, DishNotInRestaurant, UserNoMoney

@bp_hello.errorhandler(404)
def error_404(e):
    response = dict(status=0, msg="404 Error from server")
    return jsonify(response), 404

@bp_hello.errorhandler(500)
def error_500(e):
    response = dict(status=0, msg="500 Error from server")
    return jsonify(response), 500

@bp_restaurant.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
    
@bp_restaurant.errorhandler(DishNotInRestaurant)
def dish_not_in_restaurant(error):
    return 'Dish not in restaurant', 404

@bp_restaurant.errorhandler(UserNoMoney)
def dish_not_in_restaurant(error):
    return 'User does not have enough money', 404

@bp_restaurant.errorhandler(Common)
def handle_common(error):
    return 'Test Error', 400    