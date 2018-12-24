from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import TemplateView

from article import views



urlpatterns = [
    url(r'', include('article.urls')),
    url(r'^article/', include('article.urls', namespace='article')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', views.signup, name='signup'),
    url(
        r'^accounts/login/',
        auth_views.login,
        name='login',
        kwargs={
            'template_name': 'article/loginForm.html'
        }
    ),
    url(
        r'^accounts/logout/',
        auth_views.logout,
        {'next_page': '/mainpage'}
    ),
    url(r'^search/', include('haystack.urls'))

]

