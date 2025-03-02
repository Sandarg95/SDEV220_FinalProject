from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('', views.menu, name='menu'),
    path('menu/', views.menu, name='menu'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
]
