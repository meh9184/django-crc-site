import datetime
from haystack import indexes
from article.models import Entries


class EntriesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    aDate = indexes.DateTimeField(model_attr='aDate')

    def get_model(self):
        return Entries

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""

        return self.get_model().objects.filter(aDate__lte=datetime.datetime.now())
        # return self.get_model().objects.filter()
