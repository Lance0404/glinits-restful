from flask import Blueprint
from flask_restx import Api, Resource

# `url_prefix` of Blueprint leads to swagger url
# http://127.0.0.1:5000/hello/
bp = Blueprint('hello', __name__, url_prefix='/hello')

api = Api(bp, version="1.0", title="What the fuck API", description="A simple hello API")

# `namespace` will append extra string to the path
# http://127.0.0.1:5000/hello/hello_ns
ns = api.namespace("hello_ns", description="hello operations")

# todo = api.models(
#     "Todo", {"task": fields.String(required=True, description="The task details")}
# )

@ns.route("/<string:name>")
@ns.doc(responses={404: "Not Found"}, params={"name": "Who you greet to"})
class Hello(Resource):

    @ns.doc(description=f"say hello to someone")
    def get(self, name):
        """greet someone""" 
        # return 404 will show customized string
        return f'hi {name}'


"""
# can `api` and `bp` co-exist? No, they cannot.
@bp.route('/hello', methods=['GET'])
def hello():
    current_app.logger.debug('hello world')
    current_app.logger.debug(f'request {request}')
    res = {'msg': 'ok', 'status': True}
    return jsonify(res)

@bp.route('/hello_err', methods=['GET'])
def hello_err():
    current_app.logger.error('hello err')
    raise Common
"""    