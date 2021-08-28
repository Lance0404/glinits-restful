from flask import (
    Blueprint,
    jsonify,
    current_app,
    request
)

# from ...factory import app
# from ..errors import Common
from ...view import list_restaurant

# logger = app.logger
bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@bp.route('/list')
def list():
    """http://localhost:5000/v1/restaurant/list
    """
    # TODO: list currently opened restaurant
    # logger.debug(f'request.args {request.args}')
    datetime = request.args.get('datetime')
    if datetime:
        list_restaurant(datetime)
    else:
        list_restaurant()    
    return jsonify(msg='list all open restaurant')