from django.urls import path, include
from . import views

import hackingtools as ht
from hackingtools.core import Config, Logger

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
    path('core/pool/add_pool_node/', views.add_pool_node, name="add_pool_node")
]

# Automatically creates the URL's get by the modules and the configurations
for mod in ht.getModulesNames():
    main_function_config = Config.getConfig(parentKey='modules', key=mod, subkey='django_form_main_function')
    if main_function_config:
        if '__function__' in main_function_config:
            try:
                func_call = main_function_config['__function__']

                url_path = 'modules/{mod}/{func_call}/'.format(mod=mod, func_call=func_call)
                view_object = eval('views.{func_call}'.format(func_call=func_call.split('test_')[1]))

                urlpatterns.append(path(url_path, view_object, name=func_call))

            except:
                Logger.printMessage(message='urls.py', description='There is no View for the URL \'{mod_url}\''.format(mod_url=func_call), color=Logger.Fore.YELLOW)

    functions_config = Config.getConfig(parentKey='modules', key=mod, subkey='django_form_module_function')
    
    if functions_config:
        for function_conf in functions_config:
            if '__function__' in functions_config[function_conf]:
                try:
                    func_call = functions_config[function_conf]["__function__"]
                    url_path = 'modules/{mod}/{func_call}/'.format(mod=function_conf, func_call=func_call)
                    view_object = eval('views.{func_call}'.format(func_call=func_call.split('test_')[1]))

                    urlpatterns.append(path(url_path, view_object, name=func_call))

                except Exception as e:
                    Logger.printMessage(message='urls.py', description='There is no View for the URL \'{mod_url}\''.format(mod_url=func_call), color=Logger.Fore.YELLOW)
