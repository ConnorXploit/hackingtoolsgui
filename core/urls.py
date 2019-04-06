from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('module/create/', views.createModule, name="createmod"),
    path('category/create/', views.createCategory, name="createcat"),
]