from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from tasks import views

app_name = 'tasks'


urlpatterns = [
    url(r'^$', permission_required('tasks.can_use')(views.OverviewView.as_view()), name='overview'),
    url(r'^(?P<pk>[0-9]+)/$', permission_required('tasks.can_use')(views.TicketView.as_view()), name='showticket'),
    url(r'^(?P<ticket>[0-9]+)/comment/$', permission_required('tasks.can_use')(views.CommentView.as_view()), name='comment'),
    url(r'^(?P<ticket>[0-9]+)/push/$', permission_required('tasks.can_use')(views.push), name='push'),
    url(r'^(?P<ticket>[0-9]+)/close/$', permission_required('tasks.can_use')(views.close), name='close'),
    url(r'^(?P<ticket>[0-9]+)/reopen/$', permission_required('tasks.can_use')(views.reopen), name='reopen'),
    url(r'^(?P<pk>[0-9]+)/edit/$', permission_required('tasks.can_use')(views.TicketEditView.as_view()), name='edit'),
    url(r'^(?P<pk>[0-9]+)/assign/$', permission_required('tasks.can_use')(views.TicketAssignView.as_view()), name='assign'),
    url(r'^(?P<ticket>[0-9]+)/finish/$', permission_required('tasks.can_use')(views.finish), name='finish'),
    url(r'^newticket/(?P<category>[0-9]+)/$', permission_required('tasks.can_use')(views.TicketCreateView.as_view()), name='createinit'),
    url(r'^newticket/$', permission_required('tasks.can_use')(views.TicketCreateView.as_view()), name='create')
]
