from django.urls import path
from . import views
 
urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('', views.index, name='index'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
    path('reviews/new/<int:product>/', views.review_new, name='review_new'),
]