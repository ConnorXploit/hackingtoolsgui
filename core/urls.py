from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('module/create/', views.createModule, name="createmod"),
    path('module/config/', views.configModule, name="configmod"),
    path('module/save/<string>', views.configModule, name="savemod"),
    path('category/create/', views.createCategory, name="createcat"),
]