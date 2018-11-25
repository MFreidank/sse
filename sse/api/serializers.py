from rest_framework import serializers
from rest_framework.serializers import Serializer
from sse.core.models import Article
from sse.core.models import Entity


class EntitySerializer(Serializer):

    name = serializers.CharField(required=False)

    class Meta:
        model = Entity
        fields = ('name', )


class ArticleSerializer(Serializer):

    title = serializers.CharField(required=False)
    abstract = serializers.TextField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'abstract')
