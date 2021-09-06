import sys
from sqlalchemy.exc import OperationalError

from buying_frenzy import create_app

try:
    app = create_app()
except OperationalError as e:
    print('[ERROR] make sure your database is ready to serve', file=sys.stderr)
    exit(1)

if __name__ == '__main__':
    app.run()
