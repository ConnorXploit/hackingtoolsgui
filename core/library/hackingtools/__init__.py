from .core import Logger
from .core import Config, Utils
config = Config.getConfig(parentKey='core', key='import_modules')
config_locales = Config.getConfig(parentKey='core', key='locales')
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
from importlib import reload

modules_loaded = {}

nodes_pool = []
MY_NODE_ID = Utils.randomText(length=32, alphabet='mixalpha-numeric-symbol14')

https = '' # Anytime when adding ssl, shold be with an 's'

listening_port = sys.argv[-1].split(':')[1]

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
    Logger.printMessage('Modules loaded as JSON automatically:', conf, debug_module=True)
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

def getModulesCalls():
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
    modulesCalls = []
    for mods in getModules():
        Logger.printMessage('\t{text}'.format(text=mods), color=Fore.YELLOW, debug_module=True)
        modulesCalls.append(mods)
    return modulesCalls

def getModulesFunctionsCalls():
    """Return's an Array with modules name as keys and inside it's values, 
    the key are the functions call names with a value of a template for 
    initialaizing and calling that function

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    modulesCalls = {}
    header = 'import hackingtools as ht\n\nht_mod = ht.getModule("{module_name}")\nmod_result = ht_mod.{module_function}({module_function_params})\n\nprint(mod_result)'
    for module in modules_loaded:
        module_funcs = {}
        for func in modules_loaded[module]:
            try:
                for param in modules_loaded[module][func]:
                    module_funcs[func] = header.format(module_name=module.split('.')[-1], module_function=func, module_function_params=', '.join(modules_loaded[module][func][param]))
            except:
                module_funcs[func] = header.format(module_name=module.split('.')[-1], module_function=func, module_function_params='')
        modulesCalls[module.split('.')[-1]] = module_funcs
    return modulesCalls

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

def getModulesGuiNames():
    """Return's an Array with the Label for GUI for that module

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    names = []
    for tool in getModulesNames():
        label = Config.getConfig(parentKey='modules', key=tool, subkey='__gui_label__')
        if label:
            names.append(label)
    return names

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

def getModulesModalTests():
    """Return's an Array with all modules as keys and their values, the Modal GUI function forms

    Parameters
    ----------
        None

    Return
    ----------
        Array
    """
    tools_functions = {}
    for tool in getModulesNames():
        tool_functions = Config.getConfig(parentKey='modules', key=tool, subkey='django_form_module_function')
        if tool_functions:
            tools_functions[tool] = tool_functions
    return tools_functions

def __getModulesConfig_treeView__():
    """Return a String with the config for the GUI Treeview

    Parameters
    ----------
        None

    Return
    ----------
        String
    """
    count = 1
    result_text = []
    tools_config = getModulesFullConfig()
    __treeview_load_all__(config=tools_config, result_text=result_text)
    response =  ','.join(result_text)
    return response

global __treeview_counter__
__treeview_counter__ = 0

def __treeview_load_all__(config, result_text, count=0, count_pid=-1):
    """Loads the GUI Treeview with the config of all the modules loaded

    Parameters
    ----------
        config = Array
        result_text = String
        count = int
        count_pid = int

    Return
    ----------
        None
    """
    open_key = "{"
    close_key = "}"
    count += 1
    count_pid += 1
    for c in config:
        count += 1
        count = __treeview_count__(count)
        result_text.append(__treeview_createJSON__(conf_key=config[c], key=c, count=count, pid=count_pid))
        Logger.printMessage('{msg} - {key} - {n} - {m}'.format(msg='Pasando por: ', key=c, n=count, m=count_pid), color=Fore.YELLOW, debug_core=True)
        if not isinstance(config[c], str) and not isinstance(config[c], bool) and not isinstance(config[c], int) and not isinstance(config[c], float):
            try:
                __treeview_load_all__(config=config[c],result_text=result_text, count=count, count_pid=count-1)
                count += 1
            except:
                try:
                    __treeview_load_all__(config=tuple(config[c]),result_text=result_text, count=count, count_pid=count-1)
                    count += 1
                    Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=config_locales['error_json_data_loaded'], key=c, conf_key=config[c]), color=Fore.YELLOW, debug_core=True)
                except:
                    Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=config_locales['error_json_data_not_loaded'], key=c, conf_key=config[c]), color=Fore.RED, debug_core=True)
        count += 1

def __treeview_count__(count):
    global __treeview_counter__
    if count < __treeview_counter__:
        count = __treeview_counter__
    count += 1
    __treeview_counter__ = count
    return count
    
def __treeview_createJSON__(conf_key, key, count=1, pid=0):
    """Return JSON String with the config for the treeview

    Parameters
    ----------
        conf_key = String
        key = String
        count = int
        pid = int

    Return
    ----------
        String JSON Format
    """
    try:
        open_key = "{"
        close_key = "}"
        if isinstance(conf_key, str):
            return '{open_key}id:{count},name:"{name}",pid:{pid},value:"{value}"{close_key}'.format(open_key=open_key, count=count, name=key, pid=pid, value=conf_key, close_key=close_key)
        else:
            return '{open_key}id:{count},name:"{name}",pid:{pid},value:""{close_key}'.format(open_key=open_key, count=count, name=key, pid=pid, close_key=close_key)
    except:
        Logger.printMessage('{msg} - {key} - {conf_key}'.format(msg=config_locales['error_load_json_data'], key=key, conf_key=conf_key), color=Fore.RED)

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
            sentence = 'modules.{category}.{mod}.{moduleName}.StartModule()'.format(category=m.split('.')[1], mod=m.split('_')[1], moduleName=moduleName)
            return eval(sentence)
    Logger.printMessage('Looks like {mod} is not loaded on HackingTools. Look the first import in log. You could have some error in your code :)'.format(mod=moduleName), debug_module=True, is_error=True)

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

# Import Modules

#TODO Continue documentation here

def addNodeToPool(node_ip):
    if not node_ip in nodes_pool:
        nodes_pool.append(node_ip)

def sendPool(function_api_call='', params={}, files=[]):
    my_public_ip = Utils.getMyPublicIP()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    nodes = []
    pool_list=[]
    pool_counter = 0
    try:
        pool_list = params['pool_list']
    except:
        pass
    try:
        pool_counter = int(params['pool_counter'])
    except:
        pass
    # Get nodes aren't notified into nodes
    for node in nodes_pool:
        if not node in pool_list:
            nodes.append(node)
            pool_list.append(node)
    # I save pool_list items i don't have yet on my pools 
    for node in pool_list:
        if not node in nodes_pool:
            nodes.append(node)
            if not node == my_public_ip:
                nodes_pool.append(my_public_ip)
    if len(nodes) > 0:
        if not my_public_ip in pool_list:
            pool_list.append('http{s}://{ip}:{port}'.format(s=https, ip=my_public_ip, port=listening_port))
            pool_counter += 1
            for node in nodes:
                try:
                    node_call = '{node_ip}/{function_api}'.format(node_ip=node, function_api=function_api_call)

                    client = requests.Session()
                    client.get(node_call)
                    if 'csrftoken' in client.cookies:
                        params['csrfmiddlewaretoken'] = client.cookies['csrftoken']
                    else:
                        params['csrfmiddlewaretoken'] = client.cookies['csrf']

                    params['pool_list'] = pool_list
                    params['pool_counter'] = pool_counter

                    r = requests.post(node_call, files=files, data=params, headers=headers)

                    if r.status_code == 200:
                        if pool_counter == 1 and params['creator'] == MY_NODE_ID and params['creator_ip'] == my_public_ip:
                            Logger.printMessage('POOL_SOLVED', node_call, color=Fore.BLUE, debug_module=True)
                            pool_list = []
                            nodes_pool.remove(my_public_ip)
                            if r.text:
                                return (node, r.text)
                            return (node, r)
                        return (node, r)
                    if r:
                        return (node, r)
                    return (node, '')
                except Exception as e:
                    print(e)
                    raise
                    return (node, '')
        else:
            Logger.printMessage('Returned to me my own function called into the pool', debug_module=True)
    else:
        Logger.printMessage('There is nobody on the pool list', debug_module=True)

    return ('', '')

def getPoolNodes():
    return nodes_pool

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

def __methodsFromPythonFile__(obj):
    return [x for x in dir(obj) if not x.startswith(function_name_starts_with_modules)]

# Core method - Usado por: __importModules__()
def __classNameFromModule__(cls):
    return [x for x in dir(cls) if inspect.isclass(getattr(cls, x)) and x.startswith(class_name_starts_with_modules)]

def __createHtmlModalForm__(mod, config_subkey='django_form_main_function', config_extrasubkey=None):
    module_form = Config.getConfig(parentKey='modules', key=mod, subkey=config_subkey, extrasubkey=config_extrasubkey)
    if not module_form:
        return
    
    html = "<div class=\"modal-body\">"
    footer = '<div class="modal-footer">'
    m_form = module_form

    for m in m_form:
        temp_m_form = m_form
        if ('systems' in temp_m_form[m] and os.name in temp_m_form[m]['systems']) or not 'systems' in temp_m_form[m]:
            if '__type__' in temp_m_form[m] and '__id__' in temp_m_form[m] and '__className__' in temp_m_form[m]:
                input_type = temp_m_form[m]['__type__']
                input_id = temp_m_form[m]['__id__']
                input_class = temp_m_form[m]['__className__']
                input_placeholder = ''
                loading_text = ''
                if 'placeholder' in temp_m_form[m]:
                    input_placeholder = temp_m_form[m]['placeholder']
                input_label_desc = ''
                if 'label_desc' in temp_m_form[m]:
                    input_label_desc = temp_m_form[m]['label_desc']
                input_value = ''
                if 'value' in temp_m_form[m]:
                    input_value = temp_m_form[m]['value']
                checkbox_selected = False
                if 'selected' in temp_m_form[m]:
                    checkbox_selected = temp_m_form[m]['selected']
                loading_text = ''
                if 'loading_text' in temp_m_form[m]:
                    loading_text = temp_m_form[m]['loading_text']
                required = ''
                if 'required' in temp_m_form[m]:
                    required = 'required'
                if input_type == 'file':
                    html += "<label class=\"btn btn-default\">{input_label_desc}<span class=\"name-file\"></span><input type=\"file\" name=\"{id}\" class=\"{className}\" hidden {required} /></label>".format(input_label_desc=input_label_desc, className=input_class, id=input_id, required=required)
                elif input_type == 'checkbox':
                    if checkbox_selected:
                        html += "<div class=\"custom-control custom-checkbox\"><input type=\"checkbox\" class=\"{className}\" id=\"{id}\" name=\"{id}\" {required} checked><label class=\"custom-control-label\" for=\"{id}\">{input_label_desc}</label></div><br />".format(id=input_id, className=input_class, input_label_desc=input_label_desc, required=required)
                    else:
                        html += "<div class=\"custom-control custom-checkbox\"><input type=\"checkbox\" class=\"{className}\" id=\"{id}\" name=\"{id}\" {required} ><label class=\"custom-control-label\" for=\"{id}\">{input_label_desc}</label></div><br />".format(id=input_id, className=input_class, input_label_desc=input_label_desc, required=required)
                elif input_type == 'button':
                    footer += "<button type=\"button\" class=\"{className}\" data-dismiss=\"modal\">{input_value}</button>".format(className=input_class, input_value=input_value)
                elif input_type == 'submit':
                    footer += "<input type=\"submit\" class=\"{className}\" value=\"{input_value}\" id=\"{id}\" />".format(className=input_class, input_value=input_value, id=input_id)
                    if loading_text:
                        footer += "<script>$('#"
                        footer += input_id
                        footer += "').on('click', function(e){$('#"
                        footer += input_id
                        footer += "').attr('value', '{loading_text}'); e.preventDevault();".format(loading_text=loading_text)
                        footer += "});</script>"
                elif input_type == 'textarea':
                    if input_label_desc:
                        html += "<div class=\"form-group row\"><label for=\"{id}\" class=\"col-4 col-form-label\">{input_label_desc}</label><div class=\"col-4\"><textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"5\" placeholder=\"{placeholder}\"></textarea></div></div>".format(className=input_class, id=input_id, placeholder=input_placeholder, input_label_desc=input_label_desc)
                    else:
                        html += "<textarea class=\"{className}\" name=\"{id}\" id=\"{id}\" rows=\"5\" placeholder=\"{placeholder}\"></textarea>".format(className=input_class, id=input_id, placeholder=input_placeholder)
                else:
                    html += "<div class=\"form-group row\"><label for=\"{id}\" class=\"col-4 col-form-label\">{input_label_desc}</label><div class=\"col-4\"><input class=\"{className}\" type=\"{input_type}\" value=\"{input_value}\" placeholder=\"{placeholder}\" name=\"{id}\" {required}/></div></div>".format(id=input_id, placeholder=input_placeholder, input_label_desc=input_label_desc, className=input_class, input_type=input_type, input_value=input_value, required=required)
    footer += '</div>'
    html += footer
    html += '</div>'
    return html

def __getModulesDjangoForms__():
    forms = {}
    for mod in getModulesNames():
        form = __createHtmlModalForm__(mod)
        if form:
            forms[mod] = form
    return forms

def __getModulesDjangoFormsModal__():
    forms = {}
    for mod in getModulesNames():
        mod_data = {}
        functions = __getModuleFunctionNamesFromConfig__(mod)
        if functions:
            for functs in functions:
                form = __createHtmlModalForm__(mod, 'django_form_module_function', functs)
                if form:
                    mod_data[functs] = form
        if mod_data:
            forms[mod] = mod_data
    return forms

def __getModuleFunctionNamesFromConfig__(mod):
    functions = Config.getConfig(parentKey='modules', key=mod, subkey='django_form_module_function')
    if functions:
        return [func_name for func_name in functions]
    else:
        return

def getModulesConfig():
    return [{m:Config.getConfig(parentKey='modules', key=m.split('.')[-1])} for m in modules_loaded]

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

                                if params_func:
                                    clean_params = []
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
                        print("{a} - [ERROR] - {msg}".format(a=module_import_string, msg=str(e)))
    #return True

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
    Config.__createModuleTemplateConfig__(moduleName)
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
