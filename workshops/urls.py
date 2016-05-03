from django.conf.urls import patterns, url
from workshops import views
from django.contrib.auth.decorators import permission_required

app_name = 'workshops'

urlpatterns = [
    url(r'^$', permission_required("workshops.can_use")(views.OverviewView.as_view()), name='overview'),
    url(r'^(?P<pk>[0-9]+)$', permission_required("workshops.can_use")(views.WorkshopView.as_view()), name='show'),
    url(r'^(?P<pk>[0-9]+)/edit$', permission_required("workshops.can_use")(views.WorkshopView.as_view()), name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete$', permission_required("workshops.can_use")(views.WorkshopView.as_view()), name='delete'),
    url(r'^(?P<pk>[0-9]+)/reassign$', permission_required("workshops.assignworkshop")(views.WorkshopView.as_view()), name='reassign'),
    url(r'^(?P<pk>[0-9]+)/take$', permission_required("workshops.can_use")(views.WorkshopView.as_view()), name='take')
]
