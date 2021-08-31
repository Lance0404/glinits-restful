from flask import (
    Blueprint,
    jsonify,
    current_app,
    request
)

from buying_frenzy.errors import Common

logger = current_app.logger
bp = Blueprint('hello', __name__, url_prefix='/hello')
# `url_prefix` will be prepended to the route
# for example to call the hello() function from REST API
# would be sth like this: http://127.0.0.1:5000/hello/hello

@bp.route('/hello', methods=['GET'])
def hello():
    logger.debug('hello world')
    logger.debug(f'request {request}')
    res = {'msg': 'ok', 'status': True}
    return jsonify(res), 200

@bp.route('/hello_err', methods=['GET'])
def hello_err():
    logger.error('hello err')
    raise Common()