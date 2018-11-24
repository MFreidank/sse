from haystack import indexes
from sse.core.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):

    abstract = indexes.TextField(document=True, use_template=True)
    title = indexes.TextField(model_attr="address")

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.address, obj.city, obj.zip_code
        ))

    def get_model(self):
        return Location

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created__lte=timezone.now()
        )
