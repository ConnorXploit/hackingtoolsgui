from .core import Config, Utils, Logger
config = Config.getConfig(parentKey='core', key='import_modules')
from colorama import Fore, Back, Style

import os, time, sys, threading
from os import listdir
from os.path import isfile, join
import importlib
import types
import inspect
import ast
import progressbar
import requests
import sys
import readline
from django.urls import resolve
from importlib import reload

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

modules_loaded = {}

# If we want to be en Pool, import its Functions
WANT_TO_BE_IN_POOL = Config.getConfig(parentKey='core', key='WANT_TO_BE_IN_POOL')
if WANT_TO_BE_IN_POOL:
    from .core import Pool
else:
    Logger.printMessage('Pool not loaded', 'Change config or execute ht.Pool.switchPool() when you want it', color=Fore.YELLOW)

# If it's Django, import it's Functions
amidjango = Utils.amIdjango(__name__)
if amidjango:
    from .core import DjangoFunctions

this_dir = os.path.dirname(os.path.abspath(__file__))

blacklist_extensions = config['blacklist_extensions']
blacklist_directories = config['blacklist_directories']
ignore_files = config['ignore_files']
ignore_folders = config['ignore_folders']
class_name_starts_with_modules = config['class_name_starts_with_modules']
function_name_starts_with_modules = config['function_name_starts_with_modules']
function_param_exclude = config['function_param_exclude']
default_class_name_for_all = config['default_class_name_for_all']

default_template_modules_ht = config['default_template_modules_ht']

package = config['package_name']

# === getModulesJSON ===
def getModulesJSON():
    """
    Returns an Array with the modules loaded

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    conf = {}
    for mod in modules_loaded:
        if isinstance(modules_loaded[mod], str):
            conf[mod] = '1 function'
        else:
            conf[mod] = '{func} functions'.format(func=len(modules_loaded[mod]))
    #Logger.printMessage('Modules loaded as JSON automatically:', conf, debug_module=True)
    return modules_loaded

def getFunctionsNamesFromModule(module_name):
    """Returns an Array with the functions of a module you choose

    Parameters
    ----------
        module_name = String

    Return
    ----------
        Array
    """
    try:
        for mod in modules_loaded:
            if module_name in mod and not isinstance(modules_loaded[mod], str):
                return list(modules_loaded[mod].keys())
            elif module_name in mod:
                return list(modules_loaded[mod])
        return []
    except:
        return []

def getModuleCalls(module_name=None):
    """Return an Array with the modules calls you can write for importing directly a module.
    Also, it logs into your console the calls formated for well reading.

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    Logger.printMessage('Modules :', debug_module=True)
    if module_name:
        for mods in getModules():
            if module_name in mods:
                return mods
    return [mods for mods in getModules()]

def getModulesNames():
    """Return's an Array with all the modules loaded names (ht_shodan, ht_nmap, etc.)

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    modules_names = []
    for tools in modules_loaded:
        modules_names.append(tools.split('.')[-1])
    return modules_names

def getModulesFullConfig():
    """Return's an Array with all the config of all modules loaded

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    modules_conf = {}
    for module in getModulesNames():
        module_conf = Config.getConfig(parentKey='modules', key=module)
        if module_conf:
            modules_conf[module] = module_conf
    return modules_conf

def setDebugCore(on=True):
    """Set Debug Log from Core to on/off

    Parameters
    ----------
        on = boolean (True/False)

    Return
    ----------
        None
    """
    Logger.setDebugCore(on)

def setDebugModule(on=True):
    """Set Debug Log from Modules to on/off

    Parameters
    ----------
        on = boolean (True/False)

    Return
    ----------
        None
    """
    Logger.setDebugModule(on)
    
def getModule(moduleName):
    """Return's and load's a module into a variable passing a module name as parameter

    Parameters
    ----------
        moduleName = String

    Return
    ----------
        eval(module)
    """
    Logger.printMessage('Initiation of {moduleName}'.format(moduleName=moduleName), debug_module=True)
    for m in modules_loaded:
        if moduleName in m:
            if not 'ht_' in moduleName:
                moduleName = 'ht_{m}'.format(m=moduleName)
            sentence = 'modules.{category}.{mod}.{moduleName}.StartModule()'.format(category=m.split('.')[1], mod=moduleName.split('_')[1], moduleName=moduleName)
            return eval(sentence)
    Logger.printMessage('Looks like {mod} is not loaded on HackingTools. Look the first import in log. You could have some error in your code :)'.format(mod=moduleName), is_error=True)

def getModuleConfig(moduleName):
    """Return's an Array with the config of a module passed as parameter

    Parameters
    ----------
        moduleName = String

    Return
    ----------
        Array/None
    """
    if moduleName in getModulesNames():
        actualConf = getModulesJSON()
        for mod in actualConf:
            if moduleName in mod.split('.')[-1]:
                return actualConf[mod]
    return None

def getModulesConfig():
    return [{m:Config.getConfig(parentKey='modules', key=m.split('.')[-1])} for m in modules_loaded]

def getModuleCategory(moduleName):
    for m in modules_loaded:
        if moduleName.split('ht_')[1] == m.split('.')[3].split('ht_')[1]:
            return m.split('.')[1]
    return None

#TODO Continue documentation here

# Import Modules

# Core method - Usado por: __importModules__()
def __listDirectory__(directory, files=False, exclude_pattern_starts_with=None):
    """
    Devuelve las carpetas contenidas en el directorio indicado. Si se quieren listar los 
    ficheros se deberá indicar el argumento files=True. En el caso de querer excluir ficheros o carpetas
    se indicará en el argumento exclude_pattern_starts_with con el comienzo de los mismos.
    """
    mypath = os.path.join(this_dir, directory)
    data = ''

    if files:
        data = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    else:
        data = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
    
    if blacklist_extensions:
        new_data = []
        for d in data:
            has_extension = False
            for black_ext in blacklist_extensions:
                if black_ext in d:
                    has_extension = True
            if not has_extension:
                new_data.append(d)
        data = new_data

    if exclude_pattern_starts_with: 
        new_data = []
        for d in data:
            if not d.startswith(exclude_pattern_starts_with):
                new_data.append(d)
        data = new_data

    if blacklist_directories:
        new_data = []
        for d in data:
            for direc in blacklist_directories:
                if not direc in d:
                    new_data.append(d)
        data = new_data

    if ignore_folders:
        new_data = []
        for d in data:
            exists = False
            for direc in ignore_folders:
                if direc in d:
                    exists = True
            if not exists:
                new_data.append(d)
        data = new_data
    
    if files and ignore_files:
        new_data = []
        for d in data:
            for file_ign in ignore_files:
                if not file_ign in d:
                    new_data.append(d)
        data = new_data

    return data

# Core method - Usado por: __importModules__()
def __getModules__(directory='', exclude_pattern_starts_with='.'):
    """
    Devuelve las carpetas o ficheros contenidas en cada módulo del directorio actual, expluyendo de la raiz 
    los directorios que empiecen por punto. 
    """
    data = {}
    dirs = __listDirectory__(directory=directory, exclude_pattern_starts_with=exclude_pattern_starts_with)
    if dirs:
        for d in dirs:
            if not os.path.isfile(d):
                sub_dirs = __listDirectory__(directory = d) #Tengo que excluir el __pycache__
                data[d] = {}
                for sub in sub_dirs: # Tipo de Herramientas (OSINT, SQLi, etc.)
                    sub_dirs_tools = __listDirectory__(directory = '{d}/{sub}'.format(d=d, sub=sub))
                    data[d][sub] = {}
                    for tool in sub_dirs_tools:
                        sub_dirs_tool_files = __listDirectory__(directory = '{d}/{sub}/{tool}'.format(d=d, sub=sub, tool=tool), files=True)
                        data[d][sub][tool] = sub_dirs_tool_files
                subdirectorio = __listDirectory__(directory = d, files=True)
                if len(subdirectorio) > 0:
                    data[d]['files'] = subdirectorio
            else:
                try:
                    data['files'].append(d)
                except:
                    data['files'] = []
                    data['files'].append(d)
    else:
        dirs_files = __listDirectory__(directory = directory, files=True)
        data[directory] = dirs_files
    return data

# Core method - Usado por: __importModules__()
def __methodsFromModule__(cls):
    """
    Devuelve los métodos que tiene una clase pasada como parametro
    """
    return [x for x in dir(getattr(cls, default_class_name_for_all)) if not x.startswith(function_name_starts_with_modules)]

# Core method - Usado por: __importModules__()
def __classNameFromModule__(cls):
    return [x for x in dir(cls) if inspect.isclass(getattr(cls, x)) and x.startswith(class_name_starts_with_modules)]

# Core method
def __importModules__():
    """
    Método que busca dentro de las carpetas junto a este fichero (ignorando las directorios marcados anteriormente)
    y como subcarpetas tiene que haber el nombre del tipo de herramienta que es y debajo de esas carpetas
    tienen que estar los directorios individualmente por herramientas que se incorpore a la librería
    """
    modules = __getModules__()
    Logger.printMessage(message='{meth}'.format(meth='__importModules__'), description='Loading modules...', debug_module=True)
    with progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:
        for modu in modules:
            for submod in modules[modu]:
                for files in modules[modu][submod]:
                    try:
                        module_name = modules[modu][submod][files][0].split(".")[0]
                        #Logger.printMessage(message='{category}'.format(category=submod), description=module_name, debug_module=True) 
                        module_import_string = 'from .{modules}.{category}.{tool} import {toolFileName}'.format(package=package, modules=modu, category=submod, tool=files, toolFileName=module_name)
                        module_import_string_no_from = '{modules}.{category}.{tool}.{toolFileName}'.format(package=package, modules=modu, category=submod, tool=files, toolFileName=module_name)
                        try:
                            exec(module_import_string)
                            #globals()[module_name] = importlib.import_module(module_import_string)
                            module_className = __classNameFromModule__(eval(module_name))
                            module_functions = __methodsFromModule__(eval(module_name))
                            #Logger.printMessage(message='{mod} loaded'.format(mod=module_name), debug_module=True)
                            bar.update(1)
                            if len(module_functions) > 0:
                                modules_loaded[module_import_string_no_from] = {}
                                for mod_func in module_functions:
                                    function = '{module}.{callClass}().{function}'.format(module=module_name, callClass=default_class_name_for_all, function=mod_func)

                                    try:
                                        params_func = inspect.getfullargspec(eval(function))[0]
                                    except:
                                        pass

                                    clean_params = []
                                    if params_func:
                                        for param_func in params_func:
                                            if param_func not in function_param_exclude:
                                                clean_params.append(param_func)

                                    modules_loaded[module_import_string_no_from][mod_func] = {}

                                    if clean_params and len(clean_params) > 0:
                                        modules_loaded[module_import_string_no_from][mod_func]['params'] = clean_params
                                    else:
                                        modules_loaded[module_import_string_no_from][mod_func]['params'] = False
                            else:
                                modules_loaded[module_import_string_no_from] = 'Sin funciones...'   
                        except Exception as e:
                            if 'No module named' in str(e):
                                try:
                                    Logger.printMessage(message='__importModules__', description='Trying to install module {m}'.format(m=str(e).split("'")[1]), color=Fore.YELLOW)
                                    pipmain(['install', '--user', str(e).split("'")[1]])
                                except:
                                    pass

                            Logger.printMessage(message='__importModules__', description='{moduleName} [ERROR] {error}'.format(moduleName=module_import_string, error=str(e)), is_error=True)
                            raise
                    except Exception as e:
                        Logger.printMessage(message='__importModules__', description='{moduleName} [ERROR] File not found: {error}'.format(moduleName=module_import_string, error=str(e)), is_error=True)
                        
def getModules():
    data = []
    for mods in modules_loaded:
        data.append('modules.{name}.{classInit}()'.format(name=mods.split('.')[-1], classInit=default_class_name_for_all))
    return data

def createModule(moduleName, category):
    """
    Iniciamos con el comando anterior la instancia del modulo
    """
    Logger.printMessage('Creating {moduleName} on {category}'.format(moduleName=moduleName, category=category), debug_module=True)
    moduleName = moduleName.replace(" ", "_").lower()
    category = category.lower()
    categories = getCategories()
    if category not in categories:
        createCategory(category)
    dir_actual = os.path.dirname(__file__)
    if not os.path.isdir('{dir}/modules/{category}/{moduleName}'.format(dir=dir_actual, category=category, moduleName=moduleName)):
        os.makedirs('{dir}/modules/{category}/{moduleName}'.format(dir=dir_actual, category=category, moduleName=moduleName))
    if not os.path.exists('{dir}/modules/{category}/__init__.py'.format(dir=dir_actual, category=category)):
        f = open('{dir}/modules/{category}/__init__.py'.format(dir=dir_actual, category=category), "w")
        f.write('')
    if not os.path.exists('{dir}/modules/{category}/{moduleName}/ht_{moduleName}.py'.format(dir=dir_actual, category=category, moduleName=moduleName)):
        f = open('{dir}/modules/{category}/{moduleName}/ht_{moduleName}.py'.format(dir=dir_actual, category=category, moduleName=moduleName), "w")
        f.write(default_template_modules_ht.format(moduleName=moduleName))
    if not os.path.exists('{dir}/modules/{category}/{moduleName}/__init__.py'.format(dir=dir_actual, category=category, moduleName=moduleName)):
        f = open('{dir}/modules/{category}/{moduleName}/__init__.py'.format(dir=dir_actual, category=category, moduleName=moduleName), "w")
        f.write('')
    # temp_path, hackingtools_dir = os.path.split(dir_actual)
    # temp_path, library_dir = os.path.split(temp_path)
    # urls_file = os.path.join(temp_path, 'urls.py')
    # insert_url_django(urls_file, moduleName) # TODO edit urls for auto URLs when creating module
    # print("{msg}".format(msg=urls_file))
    # Reload variables on client side
    global hackingtools
    #reload(hackingtools)
    Config.__createModuleTemplateConfig__(moduleName, category)
    trying_something = __importModules__()
    return

def insert_url_django(url, name):
    print(url)
    print(name)

def createCategory(categoryName):
    categoryName = categoryName.lower()
    categories = getCategories()
    dir_actual = os.path.dirname(__file__)
    if categoryName not in categories:
        if not os.path.isdir('{dir}/modules/{category}/'.format(dir=dir_actual, category=categoryName)):
            os.makedirs('{dir}/modules/{category}'.format(dir=dir_actual, category=categoryName))

def getCategories():
    data = []
    for mods in modules_loaded:
        if mods not in data:
            data.append(mods.split('.')[3])
    return data

__importModules__()
