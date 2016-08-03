from django.conf.urls import url
from workshops import views
from django.contrib.auth.decorators import permission_required

app_name = 'workshops'

urlpatterns = [
    url(r'^$', permission_required("workshops.can_use")(views.OverviewView.as_view()), name='overview'),
    url(r'^(?P<pk>[0-9]+)$', permission_required("workshops.can_use")(views.WorkshopView.as_view()), name='show'),
    url(r'^(?P<pk>[0-9]+)/edit$', permission_required("workshops.can_use")(views.WorkshopEditView.as_view()), name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete$', permission_required("workshops.can_use")(views.WorkshopDeleteView.as_view()), name='delete'),
    url(r'^(?P<pk>[0-9]+)/reassign$', permission_required("workshops.assignworkshop")(views.WorkshopAssignView.as_view()), name='reassign'),
    url(r'^(?P<pk>[0-9]+)/take$', permission_required("workshops.can_use")(views.WorkshopView.as_view()), name='take'),
    url(r'^create$', permission_required("workshops.can_use")(views.WorkshopCreateView.as_view()), name='create')
]
