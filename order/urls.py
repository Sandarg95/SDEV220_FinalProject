from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('', views.menu, name='menu'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('menu/', views.menu, name='menu'),
    path('place_order/', views.place_order, name='place_order'),
    path('place_order_admin/', views.place_order_admin, name='place_order_admin'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_history_admin/', views.order_history_admin, name='order_history_admin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('summary/', views.summary, name='summary'),
    path('order/update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('order/update_food_item/<int:food_id>/', views.update_food_item, name='update_food_item'),

]
