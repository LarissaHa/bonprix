from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('', views.index, name='index'),
    path('products/<int:pk>/', views.product_detail_sort, name='product_detail_sort'),
    path('products/<int:pk>/stars/<slug:star>/', views.product_detail_star, name='product_detail_star'),
    path('products/<int:pk>/topic/<slug:topic_safe>/', views.product_detail_topic, name='product_detail_topic'),
    path('products/<int:pk>/sort/<slug:sort>/', views.product_detail_sort, name='product_detail_sort'),
    path('products/', views.product_list, name='product_list'),
    path('reviews/new/<int:product>/', views.review_new, name='review_new'),
    path('reviews/new/', views.review_new_unknown, name='review_new_unknown'),
]