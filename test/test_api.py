from pytest_factoryboy import register
from rest_framework.test import APIClient
from sse.core.models import Entity
from sse import factories
import pytest


register(factories.ArticleFactory)
register(factories.DomainFactory)
register(factories.EntityFactory)


@pytest.fixture(scope="session")
def client():
    yield APIClient()


@pytest.fixture(scope="session")
def payload():
    yield {'query': 'as'}


@pytest.fixture(autouse=True)
def entities(entity_factory):
    for name in ['diabetes', 'lsd', 'aspirine', 'diazepam', 'caffeine', 'cancer']:
        entity_factory(name=name)
    yield 


@pytest.mark.django_db
def test_autocompletion_endpoint(client, payload):
    result = client.post('/api/autocompletion/', payload, format='json')
    assert 200 == result.status_code
    assert {'name': 'aspirine'} in result.json()
