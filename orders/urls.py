# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
     path('create/', views.order_create, name='order_create'),
    path('verify/', views.otp_verify, name='otp_verify'),
    path('my-orders/', views.user_orders, name='user_orders'),
]