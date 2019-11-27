from .core import Connections
from .core import Config, Utils, Logger, Repositories
config = Config.getConfig(parentKey='core', key='import_modules')
from colorama import Fore, Back, Style

import os, time, sys, threading
from os import listdir
from os.path import isfile, join
import importlib
import types
import inspect, shutil
import ast
import progressbar
import json
import sys
import readline
readline.parse_and_bind('tab: complete')
from django.urls import resolve
from importlib import reload

# try:
#     from pip import main as pipmain
# except ImportError:
#     from pip._internal import main as pipmain

modules_loaded = {}

# If we want to be en Pool, import its Functions
global WANT_TO_BE_IN_POOL
WANT_TO_BE_IN_POOL = Config.getConfig(parentKey='core', key='WANT_TO_BE_IN_POOL')
if WANT_TO_BE_IN_POOL:
    from .core import Pool
else:
    Logger.printMessage('Pool not loaded', 'Change config or execute ht.Pool.switchPool() when you want it', is_warn=True)

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
default_class_name_for_all = config['default_class_name_for_all']

default_template_modules_ht = config['default_template_modules_ht']

package = config['package_name']

cant_install_requirements = Config.getConfig(parentKey='core', key='cant_install_requirements')

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

def getModulesFromCategory(category):
    mods = []
    for m in getModulesNames():
        if getModuleCategory(m) == category:
            mods.append(m)
    return mods

def getCategories():
    data = []
    for mods in modules_loaded:
        if mods.split('.')[1] not in data:
            data.append(mods.split('.')[1])
    return data

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
                        
def getModules():
    data = []
    for mods in modules_loaded:
        data.append('modules.{name}.{classInit}()'.format(name=mods.split('.')[-1], classInit=default_class_name_for_all))
    return data

def getModulesConfig():
    return [{m:Config.getConfig(parentKey='modules', key=m.split('.')[-1])} for m in modules_loaded]

def getModuleCategory(moduleName):
    for m in modules_loaded:
        if moduleName.replace('ht_', '') == m.split('.')[3].replace('ht_', ''):
            return m.split('.')[1]
    return None

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
    if not os.path.isdir('{dir}/core/config_modules_django/{category}/'.format(dir=dir_actual, category=category)):
        os.mkdir('{dir}/core/config_modules_django/{category}/'.format(dir=dir_actual, category=category))
    if not os.path.isfile('{dir}/core/config_modules_django/{category}/{moduleName}.json'.format(dir=dir_actual, category=category, moduleName=moduleName)):
        with open('{dir}/core/config_modules_django/{category}/ht_{moduleName}.json'.format(dir=dir_actual, category=category, moduleName=moduleName), "w") as fp:
            fp.write(json.dumps({}))
    # temp_path, hackingtools_dir = os.path.split(dir_actual)
    # temp_path, library_dir = os.path.split(temp_path)
    # urls_file = os.path.join(temp_path, 'urls.py')
    # insert_url_django(urls_file, moduleName) # TODO edit urls for auto URLs when creating module
    # print("{msg}".format(msg=urls_file))
    # Reload variables on client side
    #global hackingtools
    #reload(hackingtools)
    Config.__createModuleTemplateConfig__(moduleName, category)
    trying_something = __importModules__()
    return

def removeModule(moduleName, category):
    modulePath = os.path.join(this_dir, 'modules', category, moduleName.replace('ht_', ''))
    if os.path.isdir(modulePath):
        shutil.rmtree(modulePath)
    if os.path.isdir(modulePath):
        os.rmdir(modulePath)

def createCategory(categoryName):
    categoryName = categoryName.lower()
    categories = getCategories()
    dir_actual = os.path.dirname(__file__)
    if categoryName not in categories:
        if not os.path.isdir('{dir}/modules/{category}/'.format(dir=dir_actual, category=categoryName)):
            os.makedirs('{dir}/modules/{category}'.format(dir=dir_actual, category=categoryName))

def switchPool():
    global WANT_TO_BE_IN_POOL
    if WANT_TO_BE_IN_POOL:
        WANT_TO_BE_IN_POOL = False
    else:
        WANT_TO_BE_IN_POOL = True

def wantPool():
    global WANT_TO_BE_IN_POOL
    return WANT_TO_BE_IN_POOL

def worker(workerName, functionCall, args={}, timesleep=1, chunk=None):
    Utils.startWorker(workerName, functionCall, args, int(timesleep), chunk)

def getWorker(nameWorker):
    try:
        return Utils.getWorkers()[nameWorker]
    except:
        return None

def __cleanOutputModules__():
    for mod in getModulesNames():
        cat = getModuleCategory(mod)
        output_dir = os.path.join(os.path.dirname(__file__), 'modules', cat, mod.replace('ht_', ''), 'output')
        if os.path.isdir(output_dir):
            for temp_file in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, temp_file))

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

def __importModule__(modules, category, moduleName):
    module_import_string = 'from .{modules}.{category}.{tool} import {toolFileName}'.format(modules=modules, category=category, tool=moduleName.replace('ht_', ''), toolFileName=moduleName)
    module_import_string_no_from = '{modules}.{category}.{tool}.{toolFileName}'.format(modules=modules, category=category, tool=moduleName.replace('ht_', ''), toolFileName=moduleName)
    try:
        exec(module_import_string)
        #globals()[module_name] = importlib.import_module(module_import_string)
        module_className = __classNameFromModule__(eval(moduleName))
        module_functions = __methodsFromModule__(eval(moduleName))
        #Logger.printMessage(message='{mod} loaded'.format(mod=module_name), debug_module=True)
        if len(module_functions) > 0:
            modules_loaded[module_import_string_no_from] = {}
            for mod_func in module_functions:
                functionParams = Utils.getFunctionsParams(category=category, moduleName=moduleName, functionName=mod_func, i_want_list=True)

                modules_loaded[module_import_string_no_from][mod_func] = {}
                modules_loaded[module_import_string_no_from][mod_func]['params'] = functionParams if len(functionParams) > 0 else False

        else:
            modules_loaded[module_import_string_no_from] = 'Sin funciones...'   
    except Exception as e:
        new_module_name = str(e).split("'")[1]
        if 'No module named' in str(e):

            if not moduleName in cant_install_requirements:
                cant_install_requirements[moduleName] = []

            if not new_module_name in cant_install_requirements[moduleName]:

                try:
                    Logger.printMessage(message='__importModules__', description='Trying to install module {m}'.format(m=new_module_name), is_warn=True)
                    import subprocess
                    p = subprocess.Popen([sys.executable, '-m', 'pip', 'install', new_module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out = p.communicate()
                    if 'EnvironmentError' in out[0]:
                        Logger.printMessage(message='__importModules__', description='{moduleName} {error}'.format(moduleName=new_module_name, error='Could not install in environment'), is_error=True)
                    #pipmain([sys.executable, '-m', 'pip', 'install', '--user', new_module_name])
                except:
                    pass

                if not new_module_name in cant_install_requirements[moduleName]:
                    cant_install_requirements[moduleName].append(new_module_name)

                if not 'hackingtools' in new_module_name:
                    Config.add_requirements_ignore(moduleName, new_module_name)

                Logger.printMessage(message='__importModules__', description='{moduleName} {error}'.format(moduleName=module_import_string, error=str(e)), is_error=True)

# Core method
def __importModules__():
    """
    Método que busca dentro de las carpetas junto a este fichero (ignorando las directorios marcados anteriormente)
    y como subcarpetas tiene que haber el nombre del tipo de herramienta que es y debajo de esas carpetas
    tienen que estar los directorios individualmente por herramientas que se incorpore a la librería
    """
    Logger.printMessage(message='{meth}'.format(meth='__importModules__'), description='Loading modules...', debug_module=True)
    modules = __getModules__()
    with progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:
        for modu in modules:
            for submod in modules[modu]:
                for files in modules[modu][submod]:
                    module_name = modules[modu][submod][files][0].split(".")[0]
                    try:
                        #worker("import-module-{m}".format(m=module_name), __importModule__, args=(modu, submod, module_name, bar)) # Threaded
                        __importModule__(modules=modu, category=submod, moduleName=module_name)
                        bar.update(1)
                    except Exception as e:
                        Logger.printMessage(message='__importModules__', description='{moduleName} File not found: {error}'.format(moduleName=module_name, error=str(e)), is_error=True)
                        pass

__importModules__()

if Utils.amIdjango(__name__):
    worker('refresh-pool-servers', Pool.__checkPoolNodes__, timesleep=180)
    worker('clear-htpass-files', Config.__cleanHtPassFiles__, timesleep=100)
    worker('clear-output-modules', __cleanOutputModules__, timesleep=200)
# try:
#     for t in threads:
#         t.join()
# except:
#     pass