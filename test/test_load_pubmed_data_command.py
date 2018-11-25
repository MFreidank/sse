from django.core.management import call_command
from sse.core.models import Article
from sse.core.models import Author
from sse.core.models import Match
from sse.core.models import Tag
import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ATHENA_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'processed',
    'vocabularies-tiny'
)


@pytest.fixture
def args():
    yield []


@pytest.fixture
def opts():
    yield {
		'automaton_file': os.path.join(DATA_DIR, 'automaton.pkl'),
        'entrez_email': 'diegovs87@yahoo.fr',
    }

@pytest.fixture
def athena_args():
    yield []


@pytest.fixture
def athena_opts():
    yield {
		'concept_file': os.path.join(ATHENA_DATA_DIR, 'CONCEPT.csv'),
		'synonyms_file': os.path.join(ATHENA_DATA_DIR, 'CONCEPT_SYNONYM.csv'),
    }


@pytest.fixture(autouse=True)
def called_commands(args, opts, athena_args, athena_opts):
    call_command('load_athena_data', *athena_args, **athena_opts)
    call_command('load_pubmed_data', *args, **opts)
    yield


@pytest.mark.skip
@pytest.mark.django_db
def test_load_pubmed_data_creates_domains_correctly():
    assert False
