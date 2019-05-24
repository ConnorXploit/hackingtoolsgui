from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('module/create/', views.createModule, name="createmod"),
    path('module/config/', views.configModule, name="configmod"),
    path('module/save/<string>', views.configModule, name="savemod"),
    path('script/save/', views.createScript, name="createscript"),
    path('category/create/', views.createCategory, name="createcat"),
]

# Crypter
urlpatterns += [
    path('test/module/crypter/cryptfile/', views.ht_crypter_cryptFile, name="test_ht_crypter"),
    path('test/module/crypter/encrypt/', views.ht_crypter_encrypt, name="test_ht_crypter_encrypt"),
    path('test/module/crypter/decrypt/', views.ht_crypter_decrypt, name="test_ht_crypter_encrypt"),
]