from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='news_overview'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in_user, name='login'),
    path('logout/', views.log_out_user, name='logout'),
    path('news_detail/<str:id>', views.news_detail, name='news_detail'),
    path('authenticate_news/<str:id>', views.authenticate_news, name='authenticate_news'),
    path('thankyou/', views.thankyou, name='thankyou')
]
