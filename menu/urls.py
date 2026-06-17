from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_home, name='menu_home'),
    path('item/<int:pk>/', views.menu_item_detail, name='menu_item_detail'),
]