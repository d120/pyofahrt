from django.conf.urls import patterns, url
from tasks import views

app_name = 'tasks'

urlpatterns = [
    url(r'^$', views.OverviewView.as_view(), name='overview'),
    url(r'^(?P<pk>[0-9]+)$', views.TicketView.as_view(), name='showticket'),
    url(r'^(?P<ticket>[0-9]+)/comment$', views.CommentView.as_view(), name='comment'),
    url(r'^(?P<ticket>[0-9]+)/push$', views.push, name='push'),
    url(r'^(?P<ticket>[0-9]+)/close$', views.close, name='close'),
    url(r'^(?P<ticket>[0-9]+)/reopen$', views.reopen, name='reopen'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.TicketEditView.as_view(), name='edit'),
    url(r'^(?P<pk>[0-9]+)/assign$', views.TicketAssignView.as_view(), name='assign'),
    url(r'^(?P<ticket>[0-9]+)/finish$', views.finish, name='finish'),
    url(r'^newticket/(?P<category>[0-9]+)$', views.TicketCreateView.as_view(), name='createinit'),
    url(r'^newticket$', views.TicketCreateView.as_view(), name='create')
]
