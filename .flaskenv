# public env var
# FLASK_APP=buying-frenzy
# FLASKR_SETTINGS=setting.cfg
RESTX_ERROR_404_HELP=false

# ==== Database-related ====
# use psql container name instead when the web was also initiated as container
SQLALCHEMY_DATABASE_URI=postgresql://lance:lance123@localhost:5432/glinits
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_MAX_OVERFLOW=60
SQLALCHEMY_POOL_TIMEOUT=30
SQLALCHEMY_POOL_RECYCLE=30
