from dotenv import load_dotenv
import django
import os
import pytest


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env.testing'))


django.setup()


@pytest.fixture
def api_key():
    yield os.environ.get('AZURE_COGNITIVE_API_KEY')
