from django.urls import path, include
from . import views

from .library import hackingtools as ht
import os, inspect

ht.setDebugCore(True)
ht.setDebugModule(True)

from .library.hackingtools.core import Config, Logger, Utils

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

default_view_init = """from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

"""

default_view_function_init = """
def {funcName}(request):
    return renderMainPanel(request=request, popup_text='Tried and working {funcName} function. It works. Lets do something with this. Edit in "views_ht_{mod}" file')
"""

lastly_added_func = ["help"]

def getModuleViewFilePath(moduleName):
    moduleViewFile = 'views_ht_{n}.py'.format(n=moduleName.replace('ht_', ''))
    categoryDir = getModuleViewCategoryDir(moduleName)
    filePath = os.path.join(categoryDir, moduleViewFile)
    return filePath

def getModuleViewCategoryDir(moduleName):
    category = ht.getModuleCategory(moduleName)
    actualDir = os.path.join('core', 'views_modules')
    categoryDir = os.path.join(actualDir, category)
    return categoryDir

def createViewFileForModule(moduleName):
    categoryDir = getModuleViewCategoryDir(moduleName)
    fileView = getModuleViewFilePath(moduleName)
    if not os.path.isdir(categoryDir):
        os.mkdir(categoryDir)
    if not os.path.isfile(fileView):
        with open(fileView, 'w') as f:
            f.write(default_view_init)

def createTemplateFunctionForModule(moduleName, functionName):
    try:
        createViewFileForModule(moduleName)
        fileView = getModuleViewFilePath(moduleName)

        if not functionName in lastly_added_func:
            with open(fileView, 'a+') as f:
                f.write(default_view_function_init.format(funcName=functionName, mod=moduleName.replace('ht_', '')))
            lastly_added_func.append(functionName)
            Logger.printMessage(message='Added a view for the function', description=functionName, debug_core=True)
        ht.DjangoFunctions.createModuleFunctionView(moduleName, functionName)
    except:
        Logger.printMessage(message='createTemplateFunctionForModule', description='Something wen\'t wrong creating template function modal view for {m}'.format(m=moduleName))

def loadModuleFunctionsToView(moduleName):
    try:
        moduleFunctions = ht.getFunctionsNamesFromModule(moduleName).remove('help')
        createViewFileForModule(moduleName)
        loadModuleUrls(moduleName)
    except:
        Logger.printMessage(message='loadModuleFunctionsToView', description='Something wen\'t wrong creating views file for {m}'.format(m=moduleName))

def loadModuleUrls(moduleName):
    main_function_config = Config.getConfig(parentKey='modules', key=moduleName, subkey='django_form_main_function')
    functions_config = Config.getConfig(parentKey='modules', key=moduleName, subkey='django_form_module_function')

    if not functions_config:
        functions = ht.getFunctionsNamesFromModule(moduleName)
        if functions and 'help' in functions:
            functions.remove('help')
        if functions:
            functions_config = {}
            for func in functions:
                new_conf = ht.DjangoFunctions.createModuleFunctionView(moduleName, functionName=func)
                functions_config[func] = new_conf[func]

    main_not_loaded = None
    functions_not_loaded = []

    if main_function_config:
        if '__function__' in main_function_config:
            try:
                func_call = main_function_config['__function__']

                url_path = 'modules/{mod}/{func_call}/'.format(mod=moduleName, func_call=func_call)
                to_import = 'from .views_modules.{category} import views_{mod}'.format(category=ht.getModuleCategory(moduleName), mod=moduleName)
                exec(to_import)
                to_execute = 'views_{mod}.{func_call}'.format(mod=moduleName, func_call=func_call)
                view_object = eval(to_execute)

                urlpatterns.append(path(url_path, view_object, name=func_call))
            
            except ImportError as e:
                Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(to_import=to_import), is_error=True)
                loadModuleFunctionsToView(moduleName)
                createTemplateFunctionForModule(moduleName, func_call)

            except Exception as e:
                Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(mod_url=func_call), is_error=True)
                createTemplateFunctionForModule(moduleName, func_call)
    else:
        pass
        #Logger.printMessage(message='loadModuleUrls', description='{mod} has no main function'.format(mod=mod), color=ht.Fore.YELLOW)

    if functions_config:
        for function_conf in functions_config:
            if '__function__' in functions_config[function_conf]:
                try:
                    func_call = functions_config[function_conf]["__function__"]
                    url_path = 'modules/{mod}/{func_call}/'.format(mod=function_conf, func_call=func_call)
                    to_import = 'from .views_modules.{category} import views_{mod}'.format(category=ht.getModuleCategory(moduleName), mod=moduleName)
                    exec(to_import)
                    to_execute = 'views_{mod}.{func_call}'.format(mod=moduleName, func_call=func_call)
                    view_object = eval(to_execute)

                    urlpatterns.append(path(url_path, view_object, name=func_call))
            
                except ImportError as e:
                    Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(to_import=to_import), color=ht.Fore.YELLOW)
                    loadModuleFunctionsToView(moduleName)
                    createTemplateFunctionForModule(moduleName, func_call)

                except Exception as e:
                    Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(mod_url=func_call), is_error=True)
                    createTemplateFunctionForModule(moduleName, func_call)
    else:
        pass
        #Logger.printMessage(message='loadModuleUrls', description='{mod} has no functions on views config definition'.format(mod=mod), color=ht.Fore.YELLOW)

# Automatically creates the URL's get by the modules and the configurations
try:
    for mod in ht.getModulesNames():
        Logger.printMessage(message='Initialize', description='Loading mod \'{mod}\''.format(mod=mod))
        loadModuleUrls(mod)
except:
    raise