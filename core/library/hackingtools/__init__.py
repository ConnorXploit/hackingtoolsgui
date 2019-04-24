from .core import Logger
from .core import Config
config = Config.getConfig(parentKey='core', key='import_modules')

from colorama import Fore, Back, Style

import os, time, sys
from os import listdir
from os.path import isfile, join
import importlib
import types
import inspect
import ast
from importlib import reload

modules_loaded = {}

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

def getModulesJSON():
    """
    Mostramos los modulos cargados
    """
    Logger.printMessage('Modules loaded as JSON automatically:', [{mod:'{func} functions'.format(func=len(modules_loaded[mod]))} for mod in modules_loaded], debug_module=True)
    return modules_loaded

def getModulesCalls():
    """
    Por cada modulo, muestro la llamada que pueda hacer y sale en YELLOW
    """
    Logger.printMessage('Modules :', debug_module=True)
    modulesCalls = []
    for mods in getModules():
        Logger.printMessage('\t{text}'.format(text=mods), color=Fore.YELLOW, debug_module=True)
        modulesCalls.append(mods)
    return modulesCalls

def getModulesNames():
    """
    Devuelve los nombre de todos los modulos importados (ht_shodan, etc.)
    """
    modules_names = []
    for tools in modules_loaded:
        modules_names.append(tools.split('.')[-1])
    return modules_names

def getModulesGuiNames():
    names = []
    for tool in getModulesNames():
        label = Config.getConfig(parentKey='modules', key=tool, subkey='__gui_label__')
        if label:
            names.append(label)
    return names

def setDebugCore(on=True):
    """
    Establece en True / False el Debug para el CORE
    """
    Logger.setDebugCore(on)

def setDebugModule(on=True):
    """
    Establece en True / False el Debug para el Module
    """
    Logger.setDebugModule(on)
    
def getModule(moduleName):
    """
    Iniciamos con el comando anterior la instancia del modulo
    """
    Logger.printMessage('Initiation of {moduleName}'.format(moduleName=moduleName), debug_module=True)
    for m in modules_loaded:
        if moduleName in m:
            sentence = 'modules.{category}.{mod}.{moduleName}.StartModule()'.format(category=m.split('.')[1], mod=moduleName.split('_')[1], moduleName=moduleName)
            print(sentence)
            return eval(sentence)

def createModule(moduleName, category):
    """
    Iniciamos con el comando anterior la instancia del modulo
    """
    Logger.printMessage('Creating {moduleName} on {category}'.format(moduleName=moduleName, category=category), debug_module=True)
    modules.createModule(moduleName, category)
    return 'Created'

def getModuleConfig(moduleName):
    if moduleName in getModulesNames():
        actualConf = getModulesJSON()
        for mod in actualConf:
            if moduleName in mod.split('.')[-1]:
                return actualConf[mod]
    return None

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

def __createHtmlModalForm__(mod):
    module_form = Config.getConfig(parentKey='modules', key=mod, subkey='django_form')
    if not module_form:
        return

    form_url = ''
    if 'django_url_post' in module_form:
        form_url = module_form['django_url_post']
    html = "<div class=\"modal-body\">"
    footer = '<div class="modal-footer">'
    for m in module_form:
        if '__type__' in module_form[m] and '__id__' in module_form[m] and '__className__' in module_form[m]:
            input_type = module_form[m]['__type__']
            input_id = module_form[m]['__id__']
            input_class = module_form[m]['__className__']
            input_placeholder = ''
            loading_text = ''
            if 'placeholder' in module_form[m]:
                input_placeholder = module_form[m]['placeholder']
            input_value = ''
            if 'value' in module_form[m]:
                input_value = module_form[m]['value']
            loading_text = ''
            if 'loading_text' in module_form[m]:
                loading_text = module_form[m]['loading_text']
            required = ''
            if 'required' in module_form[m]:
                required = 'required'
            if input_type == 'file':
                html += "<label class=\"btn btn-default\">{placeholder}<span class=\"name-file\"></span><input type=\"file\" name=\"{id}\" class=\"{className}\" hidden {required} /></label>".format(placeholder=input_placeholder, className=input_class, id=input_id, required=required)
            elif input_type == 'checkbox':
                html += "<div class=\"custom-control custom-checkbox\"><input type=\"checkbox\" class=\"{className}\" id=\"{id}\" name=\"{id}\" {required} ><label class=\"custom-control-label\" for=\"{id}\">{placeholder}</label></div><br />".format(id=input_id, className=input_class, placeholder=input_placeholder, required=required)
            elif input_type == 'button':
                footer += "<button type=\"button\" class=\"{className}\" data-dismiss=\"modal\">{input_value}</button>".format(className=input_class, input_value=input_value)
            elif input_type == 'submit':
                footer += "<input type=\"submit\" class=\"{className}\" value=\"{input_value}\" id=\"{id}\" />".format(className=input_class, input_value=input_value, id=input_id)
                if loading_text:
                    footer += "<script>$('#"
                    footer += input_id
                    footer += "').on('click', function(){$('#"
                    footer += input_id
                    footer += "').attr('value', '{loading_text}');".format(loading_text=loading_text)
                    footer += "});</script>"
            else:
                html += "<div class=\"form-group row\"><label for=\"{id}\" class=\"col-4 col-form-label\">{placeholder}</label><div class=\"col-4\"><input class=\"{className}\" type=\"{input_type}\" value=\"{input_value}\" name=\"{id}\" {required} /></div></div>".format(id=input_id, placeholder=input_placeholder, className=input_class, input_type=input_type, input_value=input_value, required=required)
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
    for modu in modules:
        for submod in modules[modu]:
            for files in modules[modu][submod]:
                module_name = modules[modu][submod][files][0].split(".")[0]
                module_import_string = 'from .{modules}.{category}.{tool} import {toolFileName}'.format(package=package, modules=modu, category=submod, tool=files, toolFileName=module_name)
                module_import_string_no_from = '{modules}.{category}.{tool}.{toolFileName}'.format(package=package, modules=modu, category=submod, tool=files, toolFileName=module_name)
                try:
                    exec(module_import_string)
                    #globals()[module_name] = importlib.import_module(module_import_string)
                    module_className = __classNameFromModule__(eval(module_name))
                    module_functions = __methodsFromModule__(eval(module_name))

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

def getModules():
    data = []
    for mods in modules_loaded:
        data.append('modules.{name}.{classInit}()'.format(name=mods.split('.')[-1], classInit=default_class_name_for_all))
    return data

def createModule(moduleName, category):
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
    # Reload variables on client side
    global hackingtools
    #reload(hackingtools)
    __importModules__()
    
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
