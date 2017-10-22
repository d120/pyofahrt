from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from wiki import views

app_name = 'wiki'


urlpatterns = [
    url(r'^$', views.mainview, name='mainpage'),
    url(r'^(?P<title>.+)/create/$', permission_required('wiki.can_use')(views.PageCreateView.as_view()), name='create'),
    url(r'^(?P<title>.+)/edit/$', permission_required('wiki.can_use')(views.PageEditView.as_view()), name='edit'),
    url(r'^(?P<title>.+)/history/$', permission_required('wiki.can_use')(views.PageHistoryView.as_view()), name='history'),
    url(r'^(?P<pk>.+)/version/(?P<id>[-\w]+)/$', permission_required('wiki.can_use')(views.PageVersionView.as_view()), name='version'),
    url(r'^(?P<pk>.+)/$', permission_required('wiki.can_use')(views.PageView.as_view()), name='show'),
]
