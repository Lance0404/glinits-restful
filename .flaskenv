# public env var
# See `buying_frenzy/default_settings.py` for more info

# FLASKR_SETTINGS=setting.cfg

# deployed as containerized flask app
SQLALCHEMY_DATABASE_URI=postgresql://lance:lance123@glinits_psql:5432/glinits

# to align with nginx config
SERVER_NAME=localhost