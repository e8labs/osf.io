from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.UserList.as_view(), name=views.UserList.view_name),
    url(r'^(?P<user_id>\w+)/$', views.UserDetail.as_view(), name=views.UserDetail.view_name),
    url(r'^(?P<user_id>\w+)/logs/$', views.UserLogs.as_view(), name=views.UserLogs.view_name),
    url(r'^(?P<user_id>\w+)/nodes/$', views.UserNodes.as_view(), name=views.UserNodes.view_name),
    url(r'^(?P<user_id>\w+)/institutions/$', views.UserInstitutions.as_view(), name=views.UserInstitutions.view_name),
    url(r'^(?P<user_id>\w+)/registrations/$', views.UserRegistrations.as_view(), name=views.UserRegistrations.view_name),
    url(r'^(?P<user_id>\w+)/relationships/institutions/$', views.UserInstitutionsRelationship.as_view(), name=views.UserInstitutionsRelationship.view_name),
]
