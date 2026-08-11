from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('about-us/', views.about_us, name='about_us'),
    path('<str:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.product_detail, name='product_detail'),
    path('comment/add/<int:product_id>/', views.add_comment, name='add_comment'),
    
]