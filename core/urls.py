from django.urls import path, include
from . import views

from core.library import hackingtools as ht
from core.library.hackingtools.core import UtilsDjangoViewsAuto

import time, os, json, datetime

urlpatterns = [
    path('', views.home, name="home"),
    path('documentation/<module_name>', views.documentation, name="documentation"),
    path('popup/<string>', views.home, name="home"),
    # Core URLs
    path('core/module/create/', views.createModule, name="createmod"),
    path('core/module/remove/', views.removeModule, name="removeModule"),
    path('core/module/config/', views.configModule, name="configmod"),
    path('core/module/save/<string>', views.configModule, name="savemod"),
    path('core/script/save/', views.createScript, name="createscript"),
    path('core/category/create/', views.createCategory, name="createcat"),
    path('core/config/look_for_changes/', views.config_look_for_changes, name="config_look_for_changes"),
    path('core/logger/getLogs/', views.getLogs, name="getLogs"),
    path('core/pool/getNodeId/', views.getNodeId, name="getNodeId"),
    path('core/pool/switchPool/', views.switchPool, name="switchPool"),
    path('core/pool/add_pool_node/', views.add_pool_node, name="add_pool_node"),
    path('core/connections/startNgrok/', views.startNgrok, name="startNgrok"),
    path('core/repositories/downloadInstallModule/', views.downloadInstallModule, name="downloadInstallModule"),
    path('core/serverDjango/restartServerDjango/', views.restartServerDjango, name="restartServerDjango"),
    path('pool/execute/', views.poolExecute, name="execute")
]

functions_not_loaded = []

def loadModuleUrls(moduleName):
    main_function_config = ht.Config.getConfig(parentKey='modules', key=moduleName, subkey='django_form_main_function')
    functions_config = ht.Config.getConfig(parentKey='modules', key=moduleName, subkey='django_form_module_function')

    if not functions_config:
        functions = ht.getFunctionsNamesFromModule(moduleName)
        if functions and 'help' in functions:
            functions.remove('help')
        if functions:
            functions_config = {}
            for func in functions:
                new_conf = ht.DjangoFunctions.createModuleFunctionView(moduleName, functionName=func)
                if new_conf:
                    functions_config[func] = new_conf[func]
    else:
        for function in ht.getFunctionsNamesFromModule(moduleName):
            if not function in functions_config and not 'help' == function:
                new_conf = ht.DjangoFunctions.createModuleFunctionView(moduleName, functionName=function)
                if new_conf:
                    functions_config[function] = new_conf[function]

    main_not_loaded = None

    if main_function_config:
        if '__function__' in main_function_config:
            try:
                func_call = main_function_config['__function__']

                url_path = 'modules/{cat}/{mod}/{func_call}/'.format(cat=ht.getModuleCategory(moduleName), mod=moduleName.replace('ht_', ''), func_call=func_call)
                to_import = 'from .views_modules.{category} import views_{mod}'.format(category=ht.getModuleCategory(moduleName), mod=moduleName)
                exec(to_import)
                to_execute = 'views_{mod}.{func_call}'.format(mod=moduleName, func_call=func_call)
                view_object = eval(to_execute)

                urlpatterns.append(path(url_path, view_object, name=func_call))
            
            except ImportError as e:
                ht.Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(to_import=to_import), color=ht.Fore.YELLOW)
                UtilsDjangoViewsAuto.loadModuleFunctionsToView(moduleName, ht.getModuleCategory(moduleName))
                loadModuleUrls(moduleName)
                if functions_not_loaded and func_call in functions_not_loaded:
                    functions_not_loaded.remove(func_call)
                functions_not_loaded.append(func_call)
                UtilsDjangoViewsAuto.createTemplateFunctionForModule(moduleName, ht.getModuleCategory(moduleName), func_call)

            except Exception as e:
                ht.Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(mod_url=func_call), color=ht.Fore.YELLOW)
                if functions_not_loaded and func_call in functions_not_loaded:
                    functions_not_loaded.remove(func_call)
                functions_not_loaded.append(func_call)
                UtilsDjangoViewsAuto.createTemplateFunctionForModule(moduleName, ht.getModuleCategory(moduleName), func_call)
    else:
        pass
        #Logger.printMessage(message='loadModuleUrls', description='{mod} has no main function'.format(mod=mod), color=ht.Fore.YELLOW)

    if functions_config:
        for function_conf in functions_config:
            if '__function__' in functions_config[function_conf]:
                try:
                    func_call = functions_config[function_conf]["__function__"]
                    url_path = 'modules/{cat}/{mod}/{func_call}/'.format(cat=ht.getModuleCategory(moduleName), mod=moduleName.replace('ht_', ''), func_call=func_call)
                    to_import = 'from .views_modules.{category} import views_{mod}'.format(category=ht.getModuleCategory(moduleName), mod=moduleName)
                    exec(to_import)
                    to_execute = 'views_{mod}.{func_call}'.format(mod=moduleName, func_call=func_call)
                    view_object = eval(to_execute)

                    urlpatterns.append(path(url_path, view_object, name=func_call))
            
                except ImportError as e:
                    ht.Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(to_import=to_import), color=ht.Fore.YELLOW)
                    UtilsDjangoViewsAuto.loadModuleFunctionsToView(moduleName, ht.getModuleCategory(moduleName))
                    loadModuleUrls(moduleName)
                    if functions_not_loaded and func_call in functions_not_loaded:
                        functions_not_loaded.remove(func_call)
                    functions_not_loaded.append(func_call)
                    UtilsDjangoViewsAuto.createTemplateFunctionForModule(moduleName, ht.getModuleCategory(moduleName), func_call)

                except Exception as e:
                    ht.Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(mod_url=func_call), color=ht.Fore.YELLOW)
                    if functions_not_loaded and func_call in functions_not_loaded:
                        functions_not_loaded.remove(func_call)
                    functions_not_loaded.append(func_call)
                    UtilsDjangoViewsAuto.createTemplateFunctionForModule(moduleName, ht.getModuleCategory(moduleName), func_call)
    else:
        pass
        #Logger.printMessage(message='loadModuleUrls', description='{mod} has no functions on views config definition'.format(mod=mod), color=ht.Fore.YELLOW)

    # Review params in all functions views for reloading the json and recreating the view function
    UtilsDjangoViewsAuto.reviewChangesViewFunctionsParams()

# Automatically creates the URL's get by the modules and the configurations
try:
    for mod in ht.getModulesNames():
        #Logger.printMessage(message='Initialize', description='Loading mod \'{mod}\''.format(mod=mod))
        loadModuleUrls(mod)

    if functions_not_loaded:
        ht.Logger.printMessage(message='CORE VIEWS', description='Loaded new function{s} views: {d}'.format(s='s' if len(functions_not_loaded) > 1 else '', d=', '.join(functions_not_loaded)), color=ht.Fore.YELLOW)
        #ht.Logger.printMessage(message='RESTART SERVER', description='YOU HAVE TO RESTART EXIT AND RUN SERVER AGAIN FOR LOADING THE NEW VIEWS FOR YOUR MODULES', is_error=True)
        
        import sys
        sys.exit()

except:
    raise