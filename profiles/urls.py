from django.urls import path
from . import views
from cafe_login.views import logout_view 


urlpatterns = [
  path('', views.profile_page, name='profile_page'), 
  path('panel/', views.panel_user, name='login_user'),
  path('editprofile/', views.edit_profile, name='edit_profile'),
  path('logout/', logout_view, name='profile_logout'),
]