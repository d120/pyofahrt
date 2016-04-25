from django.conf.urls import patterns, url
from ofahrtbase import views

app_name = 'ofahrtbase'

urlpatterns = [
    url(r'^$', views.WelcomeView.as_view(), name='index'),
    url(r'^schedule/$', views.ScheduleView.as_view(), name='schedule')
]
