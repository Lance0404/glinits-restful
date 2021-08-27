import os

class Config(object):
    DEBUG = True
    TESTING = False
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://lance:lance123@localhost:5432/glinits')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE', 10))
    SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get('SQLALCHEMY_POOL_TIMEOUT', 30))
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get('SQLALCHEMY_POOL_RECYCLE', 30))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get('SQLALCHEMY_MAX_OVERFLOW', 15))