from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('popup/<string>', views.home, name="home"),
    # Core URLs
    path('core/module/create/', views.createModule, name="createmod"),
    path('core/module/config/', views.configModule, name="configmod"),
    path('core/module/save/<string>', views.configModule, name="savemod"),
    path('core/script/save/', views.createScript, name="createscript"),
    path('core/category/create/', views.createCategory, name="createcat"),
    path('core/config/look_for_changes/', views.config_look_for_changes, name="config_look_for_changes"),
    # Modules URLs
    # ht_crypter
    path('modules/ht_crypter/cryptfile/', views.ht_crypter_cryptFile, name="test_ht_crypter"),
    path('modules/ht_crypter/encrypt/', views.ht_crypter_encrypt, name="test_ht_crypter_encrypt"),
    path('modules/ht_crypter/decrypt/', views.ht_crypter_decrypt, name="test_ht_crypter_decrypt"),
    path('modules/ht_crypter/getRandomKeypair/', views.ht_crypter_getRandomKeypair, name="test_ht_crypter_getRandomKeypair"),
    path('modules/ht_crypter/generate_keypair/', views.ht_crypter_generate_keypair, name="test_ht_crypter_generate_keypair"),
    # ht_shodan
    path('modules/ht_shodan/getIPListfromServices/', views.ht_shodan_getIPListfromServices, name="test_ht_shodan"),
    path('modules/ht_shodan/getIPListfromServices/', views.ht_shodan_getIPListfromServices, name="test_ht_shodan_getIPListfromServices"),
    # ht_nmap
    path('modules/ht_nmap/getConnectedDevices/', views.ht_nmap_getConnectedDevices, name="test_ht_nmap"),
]