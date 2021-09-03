# TODO: find a lib that binds corresponding messages to status code
# TODO: try to handle all errors in `buying_frenzy/errors.py`
from flask import jsonify, current_app

from buying_frenzy.errors import Common, DishNotInRestaurant, UserNoMoney

@current_app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
    
@current_app.errorhandler(DishNotInRestaurant)
def dish_not_in_restaurant(error):
    return 'Dish not in restaurant', 404

@current_app.errorhandler(UserNoMoney)
def dish_not_in_restaurant(error):
    return 'User does not have enough money', 404

@current_app.errorhandler(Common)
def handle_common(error):
    return 'Test Error', 400

