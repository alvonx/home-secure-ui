from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('post/<str:slug>/', views.postdetail, name='postdetail'),
    path('tags/', views.alltags, name='alltags'),
    path('tag/<str:slug>/', views.tagdetail, name='tagdetail'),
]
