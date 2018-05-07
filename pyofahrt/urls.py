"""pyofahrt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

admin.site.site_header = 'Ofahrt Verwaltung'

urlpatterns = [
    url(r'^',
        include(
            'ofahrtbase.urls', namespace='ofahrtbase', app_name='ofahrtbase')),
    url(r'^members/',
        include('members.urls', namespace='members', app_name='members')),
    url(r'^staff/', include('staff.urls', namespace='staff',
                            app_name='staff')),
    url(r'^faq/', include('faq.urls', namespace='faq', app_name='faq')),
    url(r'^workshops/',
        include('workshops.urls', namespace='workshops',
                app_name='workshops')),
    url(r'^wiki/', include('wiki.urls', namespace='wiki', app_name='wiki')),
    url(r'^admin/', admin.site.urls)
]
