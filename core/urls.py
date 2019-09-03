from django.urls import path, include
from . import views

# import hackingtools as ht
# from hackingtools.core import Config

urlpatterns = [
    path('', views.home, name="home"),
    path('documentation/<module_name>', views.documentation, name="documentation"),
    path('popup/<string>', views.home, name="home"),
    # Core URLs
    path('core/module/create/', views.createModule, name="createmod"),
    path('core/module/config/', views.configModule, name="configmod"),
    path('core/module/save/<string>', views.configModule, name="savemod"),
    path('core/script/save/', views.createScript, name="createscript"),
    path('core/category/create/', views.createCategory, name="createcat"),
    path('core/config/look_for_changes/', views.config_look_for_changes, name="config_look_for_changes"),
    path('core/pool/switchPool/', views.switchPool, name="switchPool"),
    path('core/pool/add_pool_node/', views.add_pool_node, name="add_pool_node"),
    # Modules URLs
    # ht_crypter
    path('modules/ht_crypter/test_ht_crypter/', views.ht_crypter_cryptFile, name="test_ht_crypter"),
    # ht_rsa
    path('modules/ht_rsa/encrypt/', views.ht_rsa_encrypt, name="test_ht_rsa_encrypt"),
    path('modules/ht_rsa/decrypt/', views.ht_rsa_decrypt, name="test_ht_rsa_decrypt"),
    path('modules/ht_rsa/getRandomKeypair/', views.ht_rsa_getRandomKeypair, name="test_ht_rsa_getRandomKeypair"),
    path('modules/ht_rsa/generate_keypair/', views.ht_rsa_generate_keypair, name="test_ht_rsa_generate_keypair"),
    # ht_shodan
    path('modules/ht_shodan/getIPListfromServices/', views.ht_shodan_getIPListfromServices, name="test_ht_shodan"),
    path('modules/ht_shodan/getIPListfromServices/', views.ht_shodan_getIPListfromServices, name="test_ht_shodan_getIPListfromServices"),
    # ht_nmap
    path('modules/ht_nmap/getConnectedDevices/', views.ht_nmap_getConnectedDevices, name="test_ht_nmap"),
    path('modules/ht_nmap/getConnectedDevices/', views.ht_nmap_getConnectedDevices, name="test_ht_nmap_getConnectedDevices"),
    # ht_metadata
    path('modules/ht_metadata/get_image_exif/', views.ht_metadata_get_metadata_exif, name="test_ht_metadata_get_image_exif"),
    # ht_bruteforce
    path('modules/ht_bruteforce/crackZip/', views.ht_bruteforce_crackZip, name="test_ht_bruteforce_crackZip"),
    # ht_unzip
    path('modules/ht_unzip/extractFile/', views.test_ht_unzip_extractFile, name="test_ht_unzip_extractFile"),
    # ht_virustotal
    path('modules/ht_virustotal/isBadFile/', views.test_ht_virustotal_isBadFile, name="test_ht_virustotal_isBadFile"),
    # ht_objectdetection
    path('modules/ht_objectdetection/predictImage/', views.test_ht_objectdetection_predictImage, name="test_ht_objectdetection"),
    path('modules/ht_objectdetection/predictImage/', views.test_ht_objectdetection_predictImage, name="test_ht_objectdetection_predictImage"),
    path('modules/ht_objectdetection/trainFromZip/', views.test_ht_objectdetection_trainFromZip, name="test_ht_objectdetection_trainFromZip"),
    path('modules/ht_objectdetection/predictFromZip/', views.test_ht_objectdetection_predictFromZip, name="test_ht_objectdetection_predictFromZip")
]

# for mod in ht.getModulesNames():
#     main_function_config = Config.getConfig(parentKey='modules', key=mod, subkey='django_form_main_function')
#     functions_config = Config.getConfig(parentKey='modules', key=mod, subkey='django_form_module_function')
#     if main_function_config:
#         urlpatterns += path('modules/{mod}/test_{mod}'.format(mod=mod), eval('views.test_{mod}'.format(mod=mod)), "test_{mod}".format(mod=mod))
#     for function_conf in functions_config:
#         try:
#             func_call = function_conf["__function__"]
#             urlpatterns += path('modules/{mod}/{func_call}'.format(func_call=func_call), eval('views.{mod}_{func_call}'.format(mod=function_conf, func_call=func_call)), "test_{func_call}".format(func_call=func_call))
#         except:
#             print('Error loading', function_conf)