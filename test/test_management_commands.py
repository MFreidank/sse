from django.core.management import call_command
from django.test import TestCase
from sse.core.models import Domain
from sse.core.models import Entity
import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@pytest.mark.django_db
def test_load_athena_data_creates_domains_correctly():
    args = []
    opts = {
		'concept_file': os.path.join(DATA_DIR, 'concepts.csv'),
		'synonyms_file': os.path.join(DATA_DIR, 'synonyms.csv'),
    }
    call_command('load_athena_data', *args, **opts)
    assert 2 == Domain.objects.count()

@pytest.mark.django_db
def test_load_athena_data_creates_entities_correctly():
    args = []
    opts = {
		'concept_file': os.path.join(DATA_DIR, 'concepts.csv'),
		'synonyms_file': os.path.join(DATA_DIR, 'synonyms.csv'),
    }
    call_command('load_athena_data', *args, **opts)
    assert 4 == Entity.objects.count()
