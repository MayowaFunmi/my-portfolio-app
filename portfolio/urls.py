from django.urls import path
from .views import RegisterView, ListUserView, ProjectView, ListProjectsView, ContactMeView, ListContactMeView, LogoutView

app_name = 'project'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('list_users/', ListUserView.as_view(), name='list_user'),
    path('create_project/', ProjectView.as_view(), name='create_project'),
    path('list_projects/', ListProjectsView.as_view(), name='list_projects'),
    path('create_contact/', ContactMeView.as_view(), name='create_contact'),
    path('list_contacts/', ListContactMeView.as_view(), name='list_contacts'),
    path('logout/', LogoutView.as_view(), name='logout'),
]