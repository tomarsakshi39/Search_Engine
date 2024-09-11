import pytest
import sys
import os

# Add the directory containing 'app.py' to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING']=True
    with flask_app.app_context():
        yield flask_app
        

@pytest.fixture
def client(app):
    return app.test_client()