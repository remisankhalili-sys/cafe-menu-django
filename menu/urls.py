from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_home, name='menu_home'),
    path('item/<int:pk>/', views.menu_item_detail, name='menu_item_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:pk>/', views.cart_update, name='cart_update'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('checkout/', views.checkout, name='checkout'),
]