# TODO: find a lib that binds corresponding messages to status code
from flask import jsonify, current_app

from buying_frenzy.errors import Common

@current_app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
    
@current_app.errorhandler(Common)
def handle_common(error):
    return 'msg from handle_common()', 400

