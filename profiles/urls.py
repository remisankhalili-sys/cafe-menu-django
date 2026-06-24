from django.urls import path
from . import views


urlpatterns = [
  path('', views.profile_page, name='profile_page'), 
  path('panel', views.panel_user, name='login_user'),
  path('editprofile', views.edit_profile, name='edit_profile')
]