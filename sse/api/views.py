from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from sse.core.models import Entity
from .serializers import EntitySerializer


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
