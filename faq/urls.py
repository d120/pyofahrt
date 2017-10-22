from django.conf.urls import url
from faq import views

app_name = 'faq'

urlpatterns = [url(r'^$', views.FaqView.as_view(), name='overview')]
