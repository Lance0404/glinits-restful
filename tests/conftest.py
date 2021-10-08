import pytest
import os

from buying_frenzy import create_app

@pytest.fixture(scope='module')
def app():
    test_config = {
        "TESTING": True,
        "DB_NAME": 'test.db', 
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }    
    app = create_app(test_config)    
    yield app
    # teardown
    os.remove(f"instance/{test_config['DB_NAME']}")

@pytest.fixture(scope='module')
def test_client(app):
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def runner(app):  
    yield app.test_cli_runner()