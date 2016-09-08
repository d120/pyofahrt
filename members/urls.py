from django.conf.urls import url
from members import views
from django.contrib.auth.decorators import permission_required

app_name = 'members'

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^success/$', views.SuccessView.as_view(), name='success'),
    url(r'^list/$', views.MemberlistView.as_view(), name='list'),
    url(r'^roomassignment/$', permission_required('members.member.edit')(views.RoomassignmentView.as_view()), name='roomassignment'),
]
