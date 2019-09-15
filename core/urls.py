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

default_view_function_init = "\ndef {funcName}(request):\n"

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

def getViewTemplateByFunctionParams(moduleName, functionName):
    category = ht.getModuleCategory(moduleName)
    params = ht.Utils.getFunctionsParams(category=category, moduleName=moduleName, functionName=functionName)
    template = '\t# Init of the view {f}\n'.format(f=functionName)
    functionParamsForCallInStr = ""

    if params:

        if 'params' in params:
            for p in params['params']:
                
                if 'file' in p:
                    template = '{temp}\t\n\t# Save file {p}\n'.format(temp=template, p=p)
                    template = '{temp}\tfilename, location, {p} = saveFileOutput(request.POST.get(\'{p}\'), {mod_no_extensiom}, {category})\n'.format(temp=template, p=p, mod_no_extension=moduleName.replace('ht_', ''), category=ht.getModuleCategory(moduleName))
                else:
                    template = '{temp}\t\n\t# Parameter {p}\n'.format(temp=template, p=p)
                    template = '{temp}\t{p} = request.POST.get(\'{p}\')\n'.format(temp=template, p=p)
                functionParamsForCallInStr = '{f} {p}={p},'.format(f=functionParamsForCallInStr, p=p)

        if 'defaults' in params:
            for p in params['defaults']:

                if 'file' in p:
                    template = '{temp}\tfilename, location, {p} = saveFileOutput(request.POST.get(\'{p}\'), {mod_no_extensiom}, {category})\n'.format(temp=template, p=p, mod_no_extension=moduleName.replace('ht_', ''), category=ht.getModuleCategory(moduleName))
                else:
                    val = params['defaults'][p]
                    template = '{temp}\t\n\t# Parameter {p} (Optional - Default {v})\n'.format(temp=template, v=val, p=p)

                    if isinstance(val, str):
                        template = '{temp}\t{p} = request.POST.get(\'{p}\', \'{v}\')\n'.format(temp=template, p=p, v=val)
                    else:
                        template = '{temp}\t{p} = request.POST.get(\'{p}\', {v})\n'.format(temp=template, p=p, v=val)
                    if not val:
                        template = '{temp}\tif not {p}:\n'.format(temp=template, p=p)
                        template = '{temp}\t\t{p} = None\n'.format(temp=template, p=p)

                if not p in functionParamsForCallInStr:
                    functionParamsForCallInStr = '{f} {p}={p},'.format(f=functionParamsForCallInStr, p=p)

    functionParamsForCallInStr = functionParamsForCallInStr[:-1]

    if ht.Utils.doesFunctionContainsExplicitReturn(ht.Utils.getFunctionFullCall(moduleName, functionName)):
        
        template = '{temp}\t\n\t# Execute, get result and show it\n'.format(temp=template)
        template = '{temp}\t{r}\n'.format(temp=template, r="result = ht.getModule('{moduleName}').{functionName}({functionParamsForCallInStr} )".format(moduleName=moduleName, functionName=functionName, functionParamsForCallInStr=functionParamsForCallInStr))
        example_return = "return renderMainPanel(request=request, popup_text=result)"
        template = '{temp}\t{r}\n\t'.format(temp=template, r=example_return)

    else:
        template = '{temp}\t{r}\n'.format(temp=template, r="ht.getModule('{moduleName}').{functionName}({functionParamsForCallInStr} )".format(moduleName=moduleName, functionName=functionName, functionParamsForCallInStr=functionParamsForCallInStr))
        
    if template == "":
        template = '\tpass\n\t'

    return template

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

                f.write(getViewTemplateByFunctionParams(moduleName, functionName))

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

def regenerateModal(moduleName):
    pass

def reviewChangesViewFunctionsParams():
    pass

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
                Logger.printMessage(message='loadModuleUrls', description='Can\' load {to_import}. Creating it!'.format(to_import=to_import))
                loadModuleFunctionsToView(moduleName)
                if functions_not_loaded and func_call in functions_not_loaded:
                    functions_not_loaded.remove(func_call)
                functions_not_loaded.append(func_call)
                createTemplateFunctionForModule(moduleName, func_call)

            except Exception as e:
                Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(mod_url=func_call))
                if functions_not_loaded and func_call in functions_not_loaded:
                    functions_not_loaded.remove(func_call)
                functions_not_loaded.append(func_call)
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
                    if functions_not_loaded and func_call in functions_not_loaded:
                        functions_not_loaded.remove(func_call)
                    functions_not_loaded.append(func_call)
                    createTemplateFunctionForModule(moduleName, func_call)

                except Exception as e:
                    Logger.printMessage(message='loadModuleUrls', description='There is no View for the URL \'{mod_url}\' Creating it!'.format(mod_url=func_call))
                    if functions_not_loaded and func_call in functions_not_loaded:
                        functions_not_loaded.remove(func_call)
                    functions_not_loaded.append(func_call)
                    createTemplateFunctionForModule(moduleName, func_call)
    else:
        pass
        #Logger.printMessage(message='loadModuleUrls', description='{mod} has no functions on views config definition'.format(mod=mod), color=ht.Fore.YELLOW)

    # Review params in all functions views for reloading the json and recreating the view function
    reviewChangesViewFunctionsParams()

    if functions_not_loaded:
        Logger.printMessage(message='CORE VIEWS', description='Loaded new function{s} views: {d}'.format(s='s' if len(functions_not_loaded) > 1 else '', d=','.join(functions_not_loaded)))
        Logger.printMessage(message='CORE VIEWS', description='YOU HAVE TO RESTART EXIT AND RUN SERVER AGAIN', is_error=True)

# Automatically creates the URL's get by the modules and the configurations
try:
    for mod in ht.getModulesNames():
        #Logger.printMessage(message='Initialize', description='Loading mod \'{mod}\''.format(mod=mod))
        loadModuleUrls(mod)
except:
    raise