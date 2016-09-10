from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from staff import views

app_name = 'staff'

urlpatterns = [
    url(r'^signup$', views.SignUpView.as_view(), name='signup'),
    url(r'^signup/orga$', views.SignUpOrgaView.as_view(), name='signuporga'),
    url(r'^signup/workshop$', views.SignUpWorkshopView.as_view(), name='signupworkshop'),
    url(r'^signup/success$', views.SuccessView.as_view(), name='success'),
    url(r'^login$', login, {'template_name': 'admin/login.html'}, name='login'),
    url(r'^logout$', logout, {'next_page': reverse_lazy('ofahrtbase:index')}, name='logout'),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
    url(r'^success$', views.SuccessView.as_view(), name='successcontact'),
    url(r'^changepassword$', views.PasswordView.as_view(), name='changepassword'),
    url(r'^changepassword/success$', views.PasswordSuccessView.as_view(), name='changepasswordsuccess'),
    url(r'^createsuperuser$', views.CreateSuperuserView.as_view(), name='createsuperuser'),
]
