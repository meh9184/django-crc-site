from django.conf.urls import url
from article import views

from search.views import ArticleSearchView

urlpatterns = [
    url(r'^$', views.mainpage),
    url(r'^mainpage$', views.mainpage),
    # url(r'^home$', views.home),
    url(r'^home$', ArticleSearchView.as_view(), name='haystack_search'),
    url(r'^articleList$', views.articleList),
    url(r'^articleBody$', views.articleBody),
    url(r'^keyword$', views.keyword),
    url(r'^saveTags$', views.tags),
    url(r'^tagList$', views.tagList, name='tagList'),
    url(r'^tagList/datatest$', views.datatest),
    url(r'^tagkeyword$', views.tagkeyword),
    url(r'^tagBody$', views.tagBody),
    url(r'^datatest$', views.datatest, name='datatest'),
    url(r'^tagBodyAll$', views.tagBody),
    url(r'^loginok$', views.loginok),
    url(r'^board$', views.board),
    url(r'^serviceNotice$', views.serviceNotice),
    url(r'^treeVisualization$', views.treeVizualization),
    # url(r'^test2$', views.test2),
    # url(r'^confirmSentence$', views.confirmSentence),
    # url(r'^editTags$', views.editTags)
]
