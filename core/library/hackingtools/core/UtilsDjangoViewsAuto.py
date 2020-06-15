
from core.library.hackingtools.core import Utils
from core.library import hackingtools as ht
import os, inspect

__default_view_init__ = """from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.
"""

__default_view_function_init__ = "\n# Automatic view function for {funcName}\ndef {funcName}(request):\n"

__lastly_added_func__ = ["help"]

def createTemplateFunctionForModule(moduleName, category, functionName):
    try:
        __createViewFileForModule__(moduleName, category)
        fileView =  __getModuleViewFilePath__(moduleName, category)

        if not functionName in  __lastly_added_func__:
            with open(fileView, 'a+') as f:
                f.write( __default_view_function_init__.format(funcName=functionName, mod=moduleName.replace('ht_', '')))

                f.write( __getViewTemplateByFunctionParams__(moduleName, functionName, category))

            __lastly_added_func__.append(functionName)
            ht.Logger.printMessage(message='Added a view for the function', description=functionName, debug_core=True)

        ht.DjangoFunctions.__createModuleFunctionView__(category, moduleName, functionName)

    except Exception as e:
        ht.Logger.printMessage(message=str(e), is_error=True)
        ht.Logger.printMessage(message='createTemplateFunctionForModule', description='Something wen\'t wrong creating template function modal view for {m}'.format(m=moduleName), is_error=True)

def loadModuleFunctionsToView(moduleName, category):
    try:
        #moduleFunctions = ht.getFunctionsNamesFromModule(moduleName).remove('help')
         __createViewFileForModule__(moduleName, category)
    except:
        ht.Logger.printMessage(message='loadModuleFunctionsToView', description='Something wen\'t wrong creating views file for {m}'.format(m=moduleName), is_error=True)

def restartDjangoServer():
    wsgi_file = os.path.join(os.path.split(os.path.split(os.path.split(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])[0])[0])[0], 'hackingtoolsgui', 'wsgi.py')
    if os.path.isfile(wsgi_file):
        ht.Logger.printMessage('Restarting the server!', color=ht.Logger.__Fore.YELLOW)
        with open(wsgi_file, 'a+')as f:
            f.write('\n')
        lines = open(wsgi_file, 'r').readlines()
        del lines[-1]
        open(wsgi_file, 'w').writelines(lines)

def removeModuleView(moduleName, category):
    moduleViewPath = os.path.join(os.path.split(os.path.split(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])[0])[0], 'views_modules', category, 'views_ht_{m}.py'.format(m=moduleName.replace('ht_', '')))
    if os.path.isfile(moduleViewPath):
        os.remove(moduleViewPath)
    moduleConfPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config_modules_django', category, 'ht_{m}.py'.format(m=moduleName.replace('ht_', '')))
    if os.path.isfile(moduleConfPath):
        os.remove(moduleConfPath)

def  __getModuleViewFilePath__(moduleName, category):
    moduleViewFile = 'views_ht_{n}.py'.format(n=moduleName.replace('ht_', ''))
    categoryDir =  __getModuleViewCategoryDir__(moduleName, category)
    filePath = os.path.join(categoryDir, moduleViewFile)
    return filePath

def  __getModuleViewCategoryDir__(moduleName, category):
    actualDir = os.path.join('core', 'views_modules')
    categoryDir = os.path.join(actualDir, category)
    return categoryDir

def  __getViewTemplateByFunctionParams__(moduleName, functionName, category, params=[]):
    params = Utils.getFunctionsParams(category=category, moduleName=moduleName, functionName=functionName)
    template = '\t# Init of the view {f}\n\ttry:'.format(f=functionName)
    functionParamsForCallInStr = ""

    # Add pool condition:
    template = '{temp}\n\t\t# Pool call\n'.format(temp=template)
    template = '{temp}\t\tresponse, repool = sendPool(request, \'{f}\')\n'.format(temp=template, f=functionName)
    template = '{temp}\t\tif response or repool:\n'.format(temp=template)
    template = '{temp}\t\t\tif repool:\n'.format(temp=template)
    template = '{temp}\t\t\t\treturn HttpResponse(response)\n'.format(temp=template)
    temp = 'return JsonResponse({ "data" : str(response) })'
    template = '{temp}\t\t\t{t}\n'.format(temp=template, t=temp)
    template = '{temp}\t\telse:'.format(temp=template)

    if params:

        if 'params' in params:
            for p in params['params']:
                
                if 'file' in str(p).lower() or 'path' in str(p).lower():
                    template = '{temp}\n\t\t\ttry:\n\t\t\t\t# Save file {p}\n'.format(temp=template, p=p)
                    template = '{temp}\t\t\t\tfilename_{p}, location_{p}, {p} = saveFileOutput(request.FILES[\'{p}\'], \'{mod_no_extension}\', \'{category}\')'.format(temp=template, p=p, mod_no_extension=moduleName.replace('ht_', ''), category=ht.getModuleCategory(moduleName))
                    template = '{temp}\n\t\t\texcept Exception as e:\n\t\t\t\t# If not param {p}'.format(temp=template, p=p)
                    temp = 'return JsonResponse({ "data" : str(e) })\n\t\t\t\treturn renderMainPanel(request=request, popup_text=str(e))'
                    template = '{temp}\n\t\t\t\tif request.POST.get(\'is_async_{f}\', False):\n\t\t\t\t\t{t}'.format(temp=template, f=functionName, t=temp)
                else:
                    template = '{temp}\n\t\t\t# Parameter {p}\n'.format(temp=template, p=p)
                    template = '{temp}\t\t\t{p} = request.POST.get(\'{p}\')\n'.format(temp=template, p=p)
                functionParamsForCallInStr = '{f} {p}={p},'.format(f=functionParamsForCallInStr, p=p)

        if 'defaults' in params:
            for p in params['defaults']:

                if 'file' in str(p).lower() or 'path' in str(p).lower():
                    template = '{temp}\n\t\t\ttry:\n\t\t\t\t# Save file {p} (Optional)\n'.format(temp=template, p=p)
                    template = '{temp}\t\t\t\tfilename_{p}, location_{p}, {p} = saveFileOutput(request.FILES[\'{p}\'], \'{mod_no_extension}\', \'{category}\')'.format(temp=template, p=p, mod_no_extension=moduleName.replace('ht_', ''), category=ht.getModuleCategory(moduleName))
                    template = '{temp}\n\t\t\texcept Exception as e:\n\t\t\t\t# If not param {p}'.format(temp=template, p=p)
                    temp = 'return JsonResponse({ "data" : str(e) })\n\t\t\t\treturn renderMainPanel(request=request, popup_text=str(e))\n'
                    template = '{temp}\n\t\t\t\tif request.POST.get(\'is_async_{f}\', False):\n\t\t\t\t\t{t}'.format(temp=template, f=functionName, t=temp)
                else:
                    val = params['defaults'][p]
                    template = '{temp}\n\t\t\t# Parameter {p} (Optional - Default {v})\n'.format(temp=template, v=val, p=p)
                    
                    if isinstance(val, str):
                        template = '{temp}\t\t\t{p} = str(request.POST.get(\'{p}\', \'{v}\'))\n'.format(temp=template, p=p, v=val)
                    elif isinstance(val, bool) or val in ('True', 'False'):
                            template = '{temp}\t\t\t{p} = request.POST.get(\'{p}\', {v})\n'.format(temp=template, p=p, v=val)
                    elif isinstance(val, int):
                            template = '{temp}\t\t\t{p} = int(request.POST.get(\'{p}\', {v}))\n'.format(temp=template, p=p, v=val)
                    elif isinstance(val, float):
                            template = '{temp}\t\t\t{p} = float(request.POST.get(\'{p}\', {v}))\n'.format(temp=template, p=p, v=val)
                    elif val == 'None' or not val:
                            template = '{temp}\t\t\t{p} = request.POST.get(\'{p}\', {v})\n'.format(temp=template, p=p, v=val)
                    else:
                        template = '{temp}\t\t\t{p} = request.POST.get(\'{p}\', \'{v}\')\n'.format(temp=template, p=p, v=val)

                    if val != 0 and not val:
                        template = '{temp}\t\t\tif not {p}:\n'.format(temp=template, p=p)
                        template = '{temp}\t\t\t\t{p} = None\n'.format(temp=template, p=p)

                if not p in functionParamsForCallInStr:
                    functionParamsForCallInStr = '{f} {p}={p},'.format(f=functionParamsForCallInStr, p=p)

    functionParamsForCallInStr = functionParamsForCallInStr[:-1]

    if Utils.doesFunctionContainsExplicitReturn(Utils.getFunctionFullCall(moduleName, ht.getModuleCategory(moduleName), functionName)):
        
        template = '{temp}\n\t\t\t# Execute, get result and show it\n'.format(temp=template)
        template = '{temp}\t\t\t{r}\n'.format(temp=template, r="result = ht.getModule('{moduleName}').{functionName}({functionParamsForCallInStr}{space_if_params})".format(moduleName=moduleName, functionName=functionName, functionParamsForCallInStr=functionParamsForCallInStr, space_if_params=' ' if functionParamsForCallInStr else ''))
        
        # If async
        template = '{temp}\t\t\tif request.POST.get(\'is_async_{f}\', False):\n'.format(temp=template, f=functionName)
        template = '{temp}\t\t\t\treturn JsonResponse({res})\n'.format(temp=template, res='{ "data" : returnAsModal(result) }')
                    
        example_return = "return renderMainPanel(request=request, popup_text=result)"
        template = '{temp}\t\t\t{r}\n'.format(temp=template, r=example_return)

    else:
        template = '{temp}\n\t\t\t# Execute the function\n'.format(temp=template)
        template = '{temp}\t\t\t{r}\n'.format(temp=template, r="ht.getModule('{moduleName}').{functionName}({functionParamsForCallInStr}{space_if_params})".format(moduleName=moduleName, functionName=functionName, functionParamsForCallInStr=functionParamsForCallInStr, space_if_params=' ' if functionParamsForCallInStr else ''))
        
        if not params or ('params' in params and not params['params'] and ('defaults' in params and not params['defaults'])):
            template = '{temp}\t\t\tpass\n'.format(temp=template)

		
			
    temp = 'return JsonResponse({ "data" : str(e) })\n\t\treturn renderMainPanel(request=request, popup_text=str(e))\n\t'
    template = '{temp}\texcept Exception as e:\n\t\tif request.POST.get(\'is_async_{f}\', False):\n\t\t\t{t}'.format(temp=template, f=functionName, t=temp)
    return template

def  __createViewFileForModule__(moduleName, category):
    categoryDir =  __getModuleViewCategoryDir__(moduleName, category)
    fileView =  __getModuleViewFilePath__(moduleName, category)
    if not os.path.isdir(categoryDir):
        os.mkdir(categoryDir)
    if not os.path.isfile(fileView):
        with open(fileView, 'w') as f:
            f.write(__default_view_init__)
