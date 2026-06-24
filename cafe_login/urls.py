from django.urls import path
from . import views

urlpatterns = [
    path('phone/', views.login_phone, name='request_phone'),
    path('code/', views.verify_code, name='request_code'),
    path('registry/', views.registry, name='registry'),
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', views.logout_view, name='logout'),
    path('rest_password', views.reset_password, name='reset_password')
]