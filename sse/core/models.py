from django.db import models


class Article(models.Model):
    abstract = models.TextField()
    journal = models.TextField()
    title = models.TextField()


class Author(models.Model):
    affiliation = models.TextField()
    articles = models.ManyToManyField('Article')
    email = models.EmailField()
    name = models.TextField()


class Domain(models.Model):
    name = models.TextField()


class Entity(models.Model):
    concept_code = models.TextField()
    domain = models.ForeignKey('Domain', on_delete=models.PROTECT)
    entities = models.ManyToManyField('Article')
    name = models.TextField()
    omop_id = models.IntegerField()
    vocabulary_id = models.TextField()


class Match(models.Model):
    article = models.ForeignKey('Article', on_delete=models.PROTECT)
    entity = models.ForeignKey('Entity', on_delete=models.PROTECT)
    length = models.IntegerField()
    offset = models.IntegerField()


class Tag(models.Model):
    articles = models.ManyToManyField('Article')
    description = models.TextField()
    name = models.TextField()
