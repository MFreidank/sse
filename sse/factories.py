import factory

from sse.core import models


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Article


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Author


class DomainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Domain


class EntityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Entity

    concept_code = '1'
    domain = factory.SubFactory(DomainFactory)
    omop_id = 1

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for article in extracted:
                self.articles.add(article)


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Match


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag
