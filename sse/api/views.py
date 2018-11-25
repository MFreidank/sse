from django.db.models import Q
from functools import reduce
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from sse.core.models import Article
from sse.core.models import Entity
from .serializers import EntitySerializer
from .serializers import ArticleSerializer


class AutocompletionView(ListAPIView):

    allowed_methods = ['post']
    queryset = Entity.objects.all()

    def filter_queryset(self, queryset):
        query = self.request.data.get('query')
        return queryset.filter(name__startswith=query)

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = EntitySerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class SearchView(ListAPIView):

    allowed_methods = ['post']
    queryset = Article.objects.all()

    @classmethod
    def get_filter(cls, search_entities):
        return reduce(
            lambda q_1, q_2: q_1 & q_2,
            map(lambda entity: Q(abstract__contains=entity), search_entities)
        )

    def filter_queryset(self, queryset):
        entities = self.request.data.get('query')
        return queryset.filter(SearchView.get_filter(entities))

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = ArticleSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
