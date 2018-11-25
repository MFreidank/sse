from pytest_factoryboy import register
from sse.core.models import Article
from sse.core.models import Entity
from sse.api.views import SearchView
from sse import factories
import pytest
import random


register(factories.ArticleFactory)
register(factories.EntityFactory)


@pytest.fixture(autouse=True)
def articles(article_factory):
    _articles = [
        article_factory()
        for i in range(10)
    ]
    yield _articles


@pytest.fixture
def article(article_factory, search_entities):
    words_with_entities = factories.fake.text().split() + search_entities
    random.shuffle(words_with_entities)
    _article = article_factory(abstract=' '.join(words_with_entities))

    for entity in search_entities:
        assert entity in _article.abstract

    yield _article
    

@pytest.fixture(autouse=True)
def entities(entity_factory):
    _entities = [
        entity_factory(name=name)
        for name in ['diabetes', 'lsd', 'aspirine', 'diazepam', 'caffeine', 'cancer']
    ]
    yield _entities


@pytest.fixture
def search_entities():
    yield ['lsd', 'diabetes']


@pytest.mark.django_db
def test_queryset_filter(search_entities, article):
    assert article in Article.objects.filter(SearchView.get_filter(search_entities))
