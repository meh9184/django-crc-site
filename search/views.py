from haystack.forms import SearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
# Create your views here.


class ArticleSearchView(SearchView):
    template_name = 'article/list.html'
    queryset = SearchQuerySet()
    form_class = SearchForm

    def get_queryset(self):
        queryset = super(ArticleSearchView, self).get_queryset()
        # further filter queryset based on some set of criteria

        print queryset.count()

        return queryset.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleSearchView, self).get_context_data(*args, **kwargs)
        # do something

        print context

        return context