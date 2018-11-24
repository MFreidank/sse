from django.core.management import call_command
from django.test import TestCase
from sse.core.models import Domain
from sse.core.models import Entity
from sse.core.models import Synonym
import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def args():
    yield []


@pytest.fixture
def opts():
    yield {
		'concept_file': os.path.join(DATA_DIR, 'concepts.csv'),
		'synonyms_file': os.path.join(DATA_DIR, 'synonyms.csv'),
    }


@pytest.fixture(autouse=True)
def called_command(args, opts):
    call_command('load_athena_data', *args, **opts)
    yield


@pytest.mark.django_db
def test_load_athena_data_creates_domains_correctly(args, opts):
    assert 2 == Domain.objects.count()


@pytest.mark.django_db
def test_load_athena_data_creates_entities_correctly(args, opts):
    assert 4 == Entity.objects.count()


@pytest.mark.django_db
def test_load_athena_data_creates_synonyms_correctly(args, opts):
    assert 12 == Synonym.objects.count()
