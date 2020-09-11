from django.urls import path, include
from . import views

from core.library import hackingtools as ht
from core.library.hackingtools.core import UtilsDjangoViewsAuto

import time
import os
import json
import datetime

urlpatterns = [
    path('', views.home, name="home"),
    path('documentation/<module_name>',
         views.documentation, name="documentation"),
    path('popup/<string>', views.home, name="home"),
    path('maps/', views.renderMaps, name="maps"),
    path('maps/switchFunctionMap/',
         views.switchFunctionMap, name="switchFunctionMap"),
    # Core URLs
    path('core/loadcontentfunctionparam/', views.loadcontentfunctionparam, name="loadcontentfunctionparam"),
    path('core/utils/getIPLocationGPS/', views.getIPLocationGPS, name="getIPLocationGPS"),
    path('core/module/create/', views.__createModule__, name="createmod"),
    path('core/module/remove/', views.__removeModule__, name="removeModule"),
    path('core/module/config/', views.configModule, name="configmod"),
    path('core/module/save/<string>', views.configModule, name="savemod"),
    path('core/script/save/', views.createScript, name="createscript"),
    path('core/category/create/', views.__createCategory__, name="createcat"),
    path('core/config/look_for_changes/', views.config_look_for_changes, name="config_look_for_changes"),
    path('core/config/uploadAPIFileToConf/',
         views.uploadAPIFileToConf, name="uploadAPIFileToConf"),
    path('core/config/downloadAPIFile/',
         views.downloadAPIFile, name="downloadAPIFile"),
    path('core/config/saveTemporaryAPIsOnSession/',
         views.saveTemporaryAPIsOnSession, name="saveTemporaryAPIsOnSession"),
    path('core/config/saveHostSearchedInMap/',
         views.saveHostSearchedInMap, name="saveHostSearchedInMap"),
    path('core/logger/getLogs/', views.getLogs, name="getLogs"),
    path('core/pool/getNodeId/', views.getNodeId, name="getNodeId"),
    path('core/pool/switchPool/', views.switchPool, name="switchPool"),
    path('core/pool/add_pool_node/', views.add_pool_node, name="add_pool_node"),
    path('core/connections/startNgrok/', views.startNgrok, name="startNgrok"),
    path('core/repositories/downloadInstallModule/',
         views.downloadInstallModule, name="downloadInstallModule"),
    path('core/serverDjango/restartServerDjango/',
         views.restartServerDjango, name="restartServerDjango"),
    path('pool/execute/', views.poolExecute, name="execute")
]

main_functions_not_loaded = []
functions_not_loaded = []


def loadModuleUrls(moduleName):
    main_function_config = ht.Config.getConfig(
        parentKey='modules', key=moduleName, subkey='django_form_main_function')
    functions_config = ht.Config.getConfig(
        parentKey='modules', key=moduleName, subkey='django_form_module_function')

    main_func = None
    mod = ht.getModule(moduleName)
    if hasattr(mod, '_main_gui_func_'):
        main_func = mod._main_gui_func_

    category = ht.getModuleCategory(moduleName)

    if not functions_config:
        functions = ht.getFunctionsNamesFromModule(moduleName)

        if functions and 'help' in functions:
            functions.remove('help')
        if functions:
            functions_config = {}
            for func in functions:
                new_conf = ht.DjangoFunctions.__createModuleFunctionView__(
                    category, moduleName, functionName=func)
                if new_conf:
                    functions_config[func] = new_conf[func]
    else:
        for function in ht.getFunctionsNamesFromModule(moduleName):
            if not function in functions_config and not 'help' == function:
                new_conf = ht.DjangoFunctions.__createModuleFunctionView__(
                    category, moduleName, functionName=function)
                if new_conf:
                    functions_config[function] = new_conf[function]

    if main_function_config:
        if '__function__' in main_function_config:
            try:
                func_call = main_function_config['__function__']

                url_path = 'modules/{cat}/{mod}/{func_call}/'.format(cat=ht.getModuleCategory(
                    moduleName), mod=moduleName.replace('ht_', ''), func_call=func_call)
                to_import = 'from .views_modules.{category} import views_{mod}'.format(
                    category=ht.getModuleCategory(moduleName), mod=moduleName)
                exec(to_import)
                to_execute = 'views_{mod}.{func_call}'.format(
                    mod=moduleName, func_call=func_call)
                view_object = eval(to_execute)

                urlpatterns.append(path(url_path, view_object, name=func_call))

            except ImportError:
                ht.Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(
                    to_import=to_import), is_info=True)
                UtilsDjangoViewsAuto.loadModuleFunctionsToView(
                    moduleName, ht.getModuleCategory(moduleName))
                loadModuleUrls(moduleName)
                if functions_not_loaded and func_call in functions_not_loaded:
                    functions_not_loaded.remove(func_call)
                functions_not_loaded.append(func_call)
                UtilsDjangoViewsAuto.createTemplateFunctionForModule(
                    moduleName, ht.getModuleCategory(moduleName), func_call)

            except:
                ht.Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(
                    mod_url=func_call), is_warn=True)
                if functions_not_loaded and func_call in functions_not_loaded:
                    functions_not_loaded.remove(func_call)
                functions_not_loaded.append(func_call)
                UtilsDjangoViewsAuto.createTemplateFunctionForModule(
                    moduleName, ht.getModuleCategory(moduleName), func_call)
    else:
        if main_func and not main_function_config:
            #ht.Logger.printMessage(message='loadModuleUrls', description='{mod} has no config for main function. Creating main function setted: {m}'.format(mod=moduleName, m=main_func), is_warn=True)
            if main_func in ht.getFunctionsNamesFromModule(moduleName):
                ht.DjangoFunctions.__createModuleFunctionView__(
                    category, moduleName, main_func, is_main=True)
            else:
                ht.Logger.printMessage(message='loadModuleUrls', description='Error creating main function setted: {m}. Function does not exist in module {mod}'.format(
                    m=main_func, mod=moduleName), is_error=True)
        # else:
            #ht.Logger.printMessage(message='loadModuleUrls', description='The module {mod} does not have any function defined as main for de gui'.format(mod=moduleName), is_error=True)

    if functions_config:
        for function_conf in functions_config:
            if '__function__' in functions_config[function_conf]:
                try:
                    func_call = functions_config[function_conf]["__function__"]
                    url_path = 'modules/{cat}/{mod}/{func_call}/'.format(cat=ht.getModuleCategory(
                        moduleName), mod=moduleName.replace('ht_', ''), func_call=func_call)
                    to_import = 'from .views_modules.{category} import views_{mod}'.format(
                        category=ht.getModuleCategory(moduleName), mod=moduleName)
                    exec(to_import)
                    to_execute = 'views_{mod}.{func_call}'.format(
                        mod=moduleName, func_call=func_call)
                    view_object = eval(to_execute)

                    urlpatterns.append(
                        path(url_path, view_object, name=func_call))

                except ImportError:
                    ht.Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(
                        to_import=to_import), is_info=True)
                    UtilsDjangoViewsAuto.loadModuleFunctionsToView(
                        moduleName, ht.getModuleCategory(moduleName))
                    loadModuleUrls(moduleName)
                    if functions_not_loaded and func_call in functions_not_loaded:
                        functions_not_loaded.remove(func_call)
                    functions_not_loaded.append(func_call)
                    UtilsDjangoViewsAuto.createTemplateFunctionForModule(
                        moduleName, ht.getModuleCategory(moduleName), func_call)

                except:
                    ht.Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(
                        mod_url=func_call), is_warn=True)
                    if functions_not_loaded and func_call in functions_not_loaded:
                        functions_not_loaded.remove(func_call)
                    functions_not_loaded.append(func_call)
                    UtilsDjangoViewsAuto.createTemplateFunctionForModule(
                        moduleName, ht.getModuleCategory(moduleName), func_call)
    else:
        pass
        #Logger.printMessage(message='loadModuleUrls', description='{mod} has no functions on views config definition'.format(mod=mod), is_warn=True)


# Automatically creates the URL's get by the modules and the configurations
try:
    for mod in ht.getModulesNames():
        #Logger.printMessage(message='Initialize', description='Loading mod \'{mod}\''.format(mod=mod))
        loadModuleUrls(mod)

    if functions_not_loaded or main_functions_not_loaded:
        if functions_not_loaded:
            ht.Logger.printMessage(message='CORE VIEWS', description='Loaded new function{s} views: {d}'.format(
                s='s' if len(functions_not_loaded) > 1 else '', d=', '.join(functions_not_loaded)), is_info=True)
        if main_functions_not_loaded:
            ht.Logger.printMessage(message='CORE VIEWS', description='Loaded new main function views: {d}'.format(
                d=main_functions_not_loaded[0]), is_info=True)

        #ht.Logger.printMessage(message='RESTART SERVER', description='YOU HAVE TO RESTART EXIT AND RUN SERVER AGAIN FOR LOADING THE NEW VIEWS FOR YOUR MODULES', is_error=True)

        import sys
        sys.exit()

    # try:
    #     while True:
    #         time.sleep(0.5)
    # except KeyboardInterrupt:
    #     ht.Utils.killAllWorkers([ht.threads[x] for x in ht.threads])

except:
    raise
