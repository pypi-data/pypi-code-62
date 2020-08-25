from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('email/', views.emailView, name='email'),
    path('success/', views.successView, name='success'),
    path('news/',views.PostView.as_view(),name='news'),
    path('test/',views.koronaInfo,name='test')
    
]
