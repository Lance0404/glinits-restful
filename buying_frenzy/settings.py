import os

class Config(object):
    """
    Precedence order:
    1. defaults in this class
    2. .flaskenv
    3. .env (can override all above)
    """

    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://lance:lance123@localhost:5432/glinits')
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False))
    SQLALCHEMY_ENGINE_OPTIONS = {
                                # 'pool': QueuePool(creator),
                                 'pool_size' : 10,
                                 'pool_recycle':120,
                                 'pool_pre_ping': True
                                 }
# TODO: require further study on this
# (Pdb) app.config.get('SQLALCHEMY_ENGINE_OPTIONS')
# {'pool_size': 10, 'pool_recycle': 120, 'pool_pre_ping': True}

    # FIXME: only required for for postman, further testing required
    # beware that this setting will fix the server name
    # SERVER_NAME = str(os.environ.get('SERVER_NAME', '127.0.0.1:5000'))
    
