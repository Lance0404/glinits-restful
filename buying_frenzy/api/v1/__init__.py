# TODO: this file is having duplicated functionality as `buying_frenzy/api/__init__.py`
from flask import jsonify

from .hello import bp

@bp.errorhandler(404)
def error_404(e):
    response = dict(status=0, msg="404 Error from server")
    return jsonify(response), 404

@bp.errorhandler(500)
def error_500(e):
    response = dict(status=0, msg="500 Error from server")
    return jsonify(response), 500