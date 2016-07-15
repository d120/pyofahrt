from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from wiki import views

app_name = 'wiki'


urlpatterns = [
    url(r'^$', views.mainview, name='mainpage'),
    url(r'^(?P<pk>[-\w]+)$', permission_required('wiki.can_use')(views.PageView.as_view()), name='show'),
    url(r'^(?P<pk>[-\w]+)/(?P<id>[-\w]+)$', permission_required('wiki.can_use')(views.PageVersionView.as_view()), name='version'),
    url(r'^(?P<title>[-\w]+)/create$', permission_required('wiki.can_use')(views.PageCreateView.as_view()), name='create'),
    url(r'^(?P<title>[-\w]+)/edit$', permission_required('wiki.can_use')(views.PageEditView.as_view()), name='edit'),
    url(r'^(?P<title>[-\w]+)/history$', permission_required('wiki.can_use')(views.PageHistoryView.as_view()), name='history'),
]
