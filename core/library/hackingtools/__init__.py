__tool_name__ = 'hackingtools'
from .core import Connections as __Connections
from .core import Config, Utils, Logger, Repositories, Objects

__config__ = Config.getConfig(parentKey='core', key='import_modules')

import os as __os
from os import listdir as __listdir
from os.path import isfile as __isfile
from os.path import join as __join
import importlib as ____importlib
import types as __types
import inspect as __inspect
import shutil as __shutil
import ast as __ast
import json as __json
import sys as __sys
try:
    import readline as __readline
    __readline.parse_and_bind('tab: complete')
except:
    pass
from time import sleep as __sleep

# try:
#     from pip import main as pipmain
# except ImportError:
#     from pip._internal import main as pipmain

__modules_loaded__ = {}

# If we want to be en Pool, import its Functions
global __WANT_TO_BE_IN_POOL__
__WANT_TO_BE_IN_POOL__ = Config.getConfig(parentKey='core', key='__WANT_TO_BE_IN_POOL__')
if __WANT_TO_BE_IN_POOL__:
    from .core import Pool
else:
    Logger.printMessage('Pool not loaded', 'Change config or execute ht.Pool.switchPool() when you want it', is_warn=True)

# If it's Django, import it's Functions
__amidjango__ = Utils.amIdjango(__name__)
if __amidjango__:
    from .core import DjangoFunctions

__this_dir__ = __os.path.dirname(__os.path.abspath(__file__))

__blacklist_extensions__ = __config__['__blacklist_extensions__']
__blacklist_directories__ = __config__['__blacklist_directories__']
__ignore_files__ = __config__['__ignore_files__']
__ignore_folders__ = __config__['__ignore_folders__']
__class_name_starts_with_modules__ = __config__['__class_name_starts_with_modules__']
__function_name_starts_with_modules__ = __config__['__function_name_starts_with_modules__']
__default_class_name_for_all__ = __config__['__default_class_name_for_all__']

__default_template_modules_ht__ = __config__['__default_template_modules_ht__']

__cant_install_requirements__ = Config.getConfig(parentKey='core', key='__cant_install_requirements__')

__workers__ = []

__telegrambot_name__ = 'ht-bot'
__telegrambot_token__ = ''

def __checkLibraryUpdate__():
    try:
        # Check Version Update
        import pkg_resources as __pkg
        __version__ = __pkg.get_distribution(__tool_name__).version
        import requests as __req 
        from bs4 import BeautifulSoup as __bs4
        __pypipage__ = __req.get("https://pypi.org/project/hackingtools/")
        if __pypipage__.status_code == 200:
            __pageContent = __bs4(__pypipage__.content, 'html.parser')
            __pypiHeader = __pageContent.find('h1', {'class' : 'package-header__name'}).text
            __pypiVersion = __pypiHeader.replace(__tool_name__, '').replace('\n', ' ').replace('\r', '').replace(' ', '')
            if not __version__ == __pypiVersion:
                Logger.printMessage('Version outdated... Newer version available: {v}'.format(v=__pypiVersion), is_warn=True)
    except:
        pass

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
    for tools in __modules_loaded__:
        modules_names.append(tools.split('.')[-1])
    modules_names.sort()
    return modules_names

def getModulesNamesLabels():
    modules_names = {}
    for tools in __modules_loaded__:
        try:
            moduleName = tools.split('.')[-1]
            modules_names[moduleName] = getModule(moduleName).__gui_label__
        except:
            modules_names[moduleName] = ''
    return modules_names

def getModulesFromCategory(category):
    mods = []
    for m in getModulesNames():
        if getModuleCategory(m) == category:
            mods.append(m)
    return mods

def getCategories():
    data = []
    for mods in __modules_loaded__:
        if mods.split('.')[1] not in data:
            data.append(mods.split('.')[1])
    return data

def getModule(moduleName, count_try=0):
    """Return's and load's a module into a variable passing a module name as parameter

    Parameters
    ----------
        moduleName = String

    Return
    ----------
        eval(module)
    """
    #Logger.printMessage('Initiation of {moduleName}'.format(moduleName=moduleName), debug_module=True)
    
    for m in __modules_loaded__:
        if moduleName in m:
            if not 'ht_' in moduleName:
                moduleName = 'ht_{m}'.format(m=moduleName)
            sentence = 'modules.{category}.{mod}.{moduleName}.StartModule()'.format(category=m.split('.')[1], mod='_'.join(moduleName.split('_')[1:]), moduleName=moduleName)
            return eval(sentence)

    if count_try <= 4:
        __sleep(1)
        return getModule(moduleName, count_try+1)
    else:
        Logger.printMessage('Looks like {mod} is not loaded on HackingTools. Look the first import in log. You could have some error in your code :)'.format(mod=moduleName), is_error=True)

def getModules():
    data = []
    for mods in __modules_loaded__:
        data.append(
            'modules.{name}.{classInit}()'.format(name=mods.split('.')[-1], classInit=__default_class_name_for_all__))
    return data

def getModuleCategory(moduleName):
    for m in __modules_loaded__:
        if moduleName.replace('ht_', '') == m.split('.')[3].replace('ht_', ''):
            return m.split('.')[1]
    return None

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
        for mod in __modules_loaded__:
            if module_name in mod and not isinstance(__modules_loaded__[mod], str):
                return list(__modules_loaded__[mod].keys())
            elif module_name in mod:
                return list(__modules_loaded__[mod])
        return []
    except:
        return []

def getWorkers():
    return __workers__

def getWorker(nameWorker):
    try:
        return Utils.getWorkers()[nameWorker]
    except:
        return None

def getWorkerLastResponse(nameWorker):
    try:
        return Utils.getWorkers()[nameWorker][0].getLastResponse()
    except:
        return ''

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

def switchPool():
    global __WANT_TO_BE_IN_POOL__
    if __WANT_TO_BE_IN_POOL__:
        __WANT_TO_BE_IN_POOL__ = False
    else:
        __WANT_TO_BE_IN_POOL__ = True

def wantPool():
    global __WANT_TO_BE_IN_POOL__
    return __WANT_TO_BE_IN_POOL__

def worker(workerName, functionCall, args=(), timesleep=1, loop=True, run_until_ht_stops=False, log=False, timeout=None):
    Utils.startWorker(workerName, functionCall, args, int(timesleep), loop, run_until_ht_stops, log, timeout)
    if loop:
        __workers__.append(workerName)

def stopWorker(nameWorker):
    try:
        Utils.stopWorker(nameWorker)
    except Exception as e:
        Logger.printMessage(str(e), is_error=True)

def startTelegramBot():
    #setTelegramBotToken
    worker('telegram-bot', 'ht.core.Objects.TelegramBotCoreHT.run', loop=False, log=__amidjango__)

# === __getModulesJSON__ ===
def __getModulesJSON__():
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
    for mod in __modules_loaded__:
        if isinstance(__modules_loaded__[mod], str):
            conf[mod] = '1 function'
        else:
            conf[mod] = '{func} functions'.format(func=len(__modules_loaded__[mod]))
    # Logger.printMessage('Modules loaded as JSON automatically:', conf, debug_module=True)
    return __modules_loaded__

def __getModuleCalls__(module_name=None):
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

def __getModulesFullConfig__():
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

def __getModuleConfig__(moduleName):
    """Return's an Array with the config of a module passed as parameter

    Parameters
    ----------
        moduleName = String

    Return
    ----------
        Array/None
    """
    if moduleName in getModulesNames():
        actualConf = __getModulesJSON__()
        for mod in actualConf:
            if moduleName in mod.split('.')[-1]:
                return actualConf[mod]
    return None

def __getModulesConfig__():
    return [{m: Config.getConfig(parentKey='modules', key=m.split('.')[-1])} for m in __modules_loaded__]

def __createModule__(moduleName, category):
    """
    Iniciamos con el comando anterior la instancia del modulo
    """
    Logger.printMessage('Creating {moduleName} on {category}'.format(moduleName=moduleName, category=category),
                        debug_module=True)
    moduleName = moduleName.replace(" ", "_").lower()
    category = category.lower()
    categories = getCategories()
    if category not in categories:
        __createCategory__(category)
    dir_actual = __os.path.dirname(__file__)
    if not __os.path.isdir(
            '{dir}/modules/{category}/{moduleName}'.format(dir=dir_actual, category=category, moduleName=moduleName)):
        __os.makedirs(
            '{dir}/modules/{category}/{moduleName}'.format(dir=dir_actual, category=category, moduleName=moduleName))
    if not __os.path.exists('{dir}/modules/{category}/__init__.py'.format(dir=dir_actual, category=category)):
        f = open('{dir}/modules/{category}/__init__.py'.format(dir=dir_actual, category=category), "w")
        f.write('')
    if not __os.path.exists(
            '{dir}/modules/{category}/{moduleName}/ht_{moduleName}.py'.format(dir=dir_actual, category=category,
                                                                              moduleName=moduleName)):
        f = open('{dir}/modules/{category}/{moduleName}/ht_{moduleName}.py'.format(dir=dir_actual, category=category,
                                                                                   moduleName=moduleName), "w")
        f.write(__default_template_modules_ht__.replace('{moduleName}', moduleName))
    if not __os.path.exists(
            '{dir}/modules/{category}/{moduleName}/__init__.py'.format(dir=dir_actual, category=category,
                                                                       moduleName=moduleName)):
        f = open('{dir}/modules/{category}/{moduleName}/__init__.py'.format(dir=dir_actual, category=category,
                                                                            moduleName=moduleName), "w")
        f.write('')
    if not __os.path.isdir('{dir}/core/config_modules_django/{category}/'.format(dir=dir_actual, category=category)):
        __os.mkdir('{dir}/core/config_modules_django/{category}/'.format(dir=dir_actual, category=category))
    if not __isfile(
            '{dir}/core/config_modules_django/{category}/{moduleName}.json'.format(dir=dir_actual, category=category,
                                                                                   moduleName=moduleName)):
        with open('{dir}/core/config_modules_django/{category}/ht_{moduleName}.json'.format(dir=dir_actual,
                                                                                            category=category,
                                                                                            moduleName=moduleName),
                  "w") as fp:
            fp.write(__json.dumps({}))
    # temp_path, hackingtools_dir = __os.path.split(dir_actual)
    # temp_path, library_dir = __os.path.split(temp_path)
    # urls_file = __os.path.join(temp_path, 'urls.py')
    # insert_url_django(urls_file, moduleName) # TODO edit urls for auto URLs when creating module
    # print("{msg}".format(msg=urls_file))
    # Reload variables on client side
    # global hackingtools
    # reload(hackingtools)
    Config.__createModuleTemplateConfig__(moduleName, category)
    __importModules__()
    return

def __removeModule__(moduleName, category):
    modulePath = __join(__this_dir__, 'modules', category, moduleName.replace('ht_', ''))
    try:
        __os.chmod(modulePath, 777)
    except:
        pass
    try:
        if __os.path.isdir(modulePath):
            __shutil.rmtree(modulePath, ignore_errors=True)
    except:
        pass
    try:
        if __os.path.isdir(modulePath):
            __os.rmdir(modulePath)
    except:
        pass
    try:
        if __os.path.isdir(modulePath):
            __os.removedirs(modulePath)
    except:
        pass

def __createCategory__(categoryName):
    categoryName = categoryName.lower()
    categories = getCategories()
    dir_actual = __os.path.dirname(__file__)
    if categoryName not in categories:
        if not __os.path.isdir('{dir}/modules/{category}/'.format(dir=dir_actual, category=categoryName)):
            __os.makedirs('{dir}/modules/{category}'.format(dir=dir_actual, category=categoryName))

def __cleanOutputModules__():
    for mod in getModulesNames():
        cat = getModuleCategory(mod)
        output_dir = __join(__os.path.dirname(__file__), 'modules', cat, mod.replace('ht_', ''), 'output')
        if __os.path.isdir(output_dir):
            for temp_file in __listdir(output_dir):
                __os.remove(__join(output_dir, temp_file))


# TODO Continue documentation here

# Import Modules

# Core method - Usado por: __importModules__()
def __listDirectory__(directory, files=False, exclude_pattern_starts_with=None):
    """
    Devuelve las carpetas contenidas en el directorio indicado. Si se quieren listar los 
    ficheros se deberá indicar el argumento files=True. En el caso de querer excluir ficheros o carpetas
    se indicará en el argumento exclude_pattern_starts_with con el comienzo de los mism__os.
    """
    mypath = __join(__this_dir__, directory)
    data = ''

    if files:
        data = [f for f in __listdir(mypath) if __isfile(__join(mypath, f))]
    else:
        data = [f for f in __listdir(mypath) if not __isfile(__join(mypath, f))]

    if __blacklist_extensions__:
        new_data = []
        for d in data:
            has_extension = False
            for black_ext in __blacklist_extensions__:
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

    if __blacklist_directories__:
        new_data = []
        for d in data:
            for direc in __blacklist_directories__:
                if not direc in d:
                    new_data.append(d)
        data = new_data

    if __ignore_folders__:
        new_data = []
        for d in data:
            exists = False
            for direc in __ignore_folders__:
                if direc in d:
                    exists = True
            if not exists:
                new_data.append(d)
        data = new_data

    if files and __ignore_files__:
        new_data = []
        for d in data:
            for file_ign in __ignore_files__:
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
            if not __isfile(d):
                sub_dirs = __listDirectory__(directory=d)  # Tengo que excluir el __pycache__
                data[d] = {}
                for sub in sub_dirs:  # Tipo de Herramientas (OSINT, SQLi, etc.)
                    sub_dirs_tools = __listDirectory__(directory='{d}/{sub}'.format(d=d, sub=sub))
                    data[d][sub] = {}
                    for tool in sub_dirs_tools:
                        sub_dirs_tool_files = __listDirectory__(directory='{d}/{sub}/{tool}'.format(d=d, sub=sub, tool=tool), files=True)
                        data[d][sub][tool] = sub_dirs_tool_files
                subdirectorio = __listDirectory__(directory=d, files=True)
                if len(subdirectorio) > 0:
                    data[d]['files'] = subdirectorio
            else:
                try:
                    data['files'].append(d)
                except:
                    data['files'] = []
                    data['files'].append(d)
    else:
        dirs_files = __listDirectory__(directory=directory, files=True)
        data[directory] = dirs_files
    return data

# Core method - Usado por: __importModules__()
def __methodsFromModule__(cls):
    """
    Devuelve los métodos que tiene una clase pasada como parametro
    """
    return [x for x in dir(getattr(cls, __default_class_name_for_all__)) if not x.startswith(__function_name_starts_with_modules__)]

# Core method - Usado por: __importModules__()
def __classNameFromModule__(cls):
    return [x for x in dir(cls) if __inspect.isclass(getattr(cls, x)) and x.startswith(__class_name_starts_with_modules__)]

def __importModule__(modules, category, moduleName):
    module_import_string = 'from .{modules}.{category}.{tool} import {toolFileName}'.format(modules=modules, category=category, tool=moduleName.replace('ht_', ''), toolFileName=moduleName)
    module_import_string_no_from = '{modules}.{category}.{tool}.{toolFileName}'.format(modules=modules, category=category, tool=moduleName.replace('ht_', ''), toolFileName=moduleName)
    try:
        exec(module_import_string)
        # globals()[module_name] = __importlib.import_module(module_import_string)
        _ = __classNameFromModule__(eval(moduleName))
        module_functions = __methodsFromModule__(eval(moduleName))
        # Logger.printMessage(message='{mod} loaded'.format(mod=module_name), debug_module=True)
        if len(module_functions) > 0:
            __modules_loaded__[module_import_string_no_from] = {}
            for mod_func in module_functions:
                functionParams = Utils.getFunctionsParams(category=category, moduleName=moduleName, functionName=mod_func, i_want_list=True)
                original_params = Utils.getFunctionsParams(category=category, moduleName=moduleName, functionName=mod_func)

                __modules_loaded__[module_import_string_no_from][mod_func] = {}
                __modules_loaded__[module_import_string_no_from][mod_func]['params'] = functionParams if len(functionParams) > 0 else False
                __modules_loaded__[module_import_string_no_from][mod_func]['original_params'] = original_params if original_params else None
        else:
            __modules_loaded__[module_import_string_no_from] = 'Sin funciones...'

    except Exception as e:
        Logger.printMessage(str(e), is_error=True)
        if not 'inconsistent use of tabs' in str(e):
            new_module_name = str(e).split("'")[1]
            if 'No module named' in str(e):
                if not moduleName in __cant_install_requirements__:
                    __cant_install_requirements__[moduleName] = []

                if not new_module_name in __cant_install_requirements__[moduleName]:

                    try:
                        Logger.printMessage(message='__importModules__', description='Trying to install module {m}'.format(m=new_module_name), is_warn=True)
                        import subprocess
                        p = subprocess.Popen([__sys.executable, '-m', 'pip', 'install', new_module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out = p.communicate()
                        if 'EnvironmentError' in out[0]:
                            Logger.printMessage(message='__importModules__', description='{moduleName} {error}'.format(moduleName=new_module_name, error='Could not install in environment'), is_error=True)
                        # pipmain([sys.executable, '-m', 'pip', 'install', '--user', new_module_name])
                    except:
                        pass

                    if not new_module_name in __cant_install_requirements__[moduleName]:
                        __cant_install_requirements__[moduleName].append(new_module_name)

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
    for modu in modules:
        for submod in modules[modu]:
            for files in modules[modu][submod]:
                try:
                    module_name = modules[modu][submod][files][0].split(".")[0]
                    if not __amidjango__:
                        __importModule__(modu, submod, module_name)
                        #worker("import-module-{m}".format(m=module_name), 'ht.__importModule__', args=(modu, submod, module_name), loop=False, log=False) # Threaded
                    else:
                        __importModule__(modules=modu, category=submod, moduleName=module_name)
                except Exception as e:
                    Logger.printMessage(message='__importModules__', description='{moduleName} File not found: {error}'.format(moduleName=files, error=str(e)), is_error=True)
                    pass

worker('check-library-updated', 'ht.__checkLibraryUpdate__', loop=False, run_until_ht_stops=True, log=__amidjango__)
worker('refresh-pool-servers', 'ht.Pool.__checkPoolNodes__', timesleep=180, run_until_ht_stops=True, log=__amidjango__)
worker('clear-htpass-files', 'ht.Config.__cleanHtPassFiles__', timesleep=100, run_until_ht_stops=True, log=__amidjango__)
worker('clear-uploaded-modules-temp', 'ht.Repositories.clearUploadsTemp', timesleep=200, run_until_ht_stops=True, log=__amidjango__)
worker('repositories-get-online-servers', 'ht.Repositories.getOnlineServers', loop=False, run_until_ht_stops=True, log=__amidjango__)
worker('clear-output-modules', 'ht.__cleanOutputModules__', timesleep=200, run_until_ht_stops=True, log=__amidjango__)

if __telegrambot_token__:
    Config.setTelegramBotToken(__telegrambot_token__)
    startTelegramBot()

__importModules__()

# try:
#     for t in threads:
#         t.join()
# except:
#     pass
