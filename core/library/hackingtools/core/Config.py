# === Treats all the configuration of the app ===

"""
All the configuration is loaded from this file

Currently we support the following 2 public functions and 4 private functions:

Public:

1. **getConfig** - Returns the configuration of some key values you explicitly tell on params (jump to section in [[Config.py#getConfig]] )

2. **getApiKey** - Return an API Key registered into configuration (jump to section in [[Config.py#getApiKey]] )

Private:

1. **__readConfig__** - Read's all the configuration included in your config.json file (jump to section in [[Config.py#__readConfig__]] )

2. **__save_config__** - Save configuration passed as parameter to this function. This, writes into your config.json (jump to section in [[Config.py#__save_config__]] )

3. **__createModuleTemplateConfig__** - This function creates into config.json a template with a simple config for trying in your GUI your functions (jump to section in [[Config.py#__createModuleTemplateConfig__]] )

4. **__look_for_changes__** - Reloads the configuration loaded (jump to section in [[Config.py#__look_for_changes__]] )

"""

import os
import json

global config
config = {}

def __readFilesAuto__():
    config = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config = json.load(json_data_file)

    if config["core"]["LOAD_DJANGO_CONF"] == True:
        django = True

    if django:
        # Load the basic config for Django
        with open(os.path.join(os.path.dirname(__file__) , 'config_django.json')) as json_data_file_django:
            config['django'] = {}
            config_django = json.load(json_data_file_django)
            for conf in config_django:
                config['django'][conf] = {}
                for django_data in config_django[conf]:
                    config['django'][conf][django_data] = config_django[conf][django_data]

        # Loads the config for the modules into Django as modal forms
        categories_dir = os.path.join(os.path.dirname(__file__), 'config_modules_django')
        for mod in config['modules']:
            categories = os.listdir(categories_dir)
            for cat in categories:
                module_config_file = os.path.join(categories_dir, cat, '{mod}.json'.format(mod=mod))
                if os.path.isfile(module_config_file):
                    with open(module_config_file) as json_data_file_django:
                        if json_data_file_django:
                            config_django = json.load(json_data_file_django)
                            for conf in config_django:
                                config['modules'][mod][conf] = config_django[conf]
    return config

# === __readConfig__ ===
def __readConfig__(django=False):
    """
    Read's all the configuration included in 
    your config.json file and inside config_modules_django directory
    recursively by your loaded modules into your config.json
    """
    global config
    config = __readFilesAuto__()

# === __save_config__ ===
def __save_config__(new_conf, config_file='config.json'):
    """
    Save configuration passed as parameter
    to this function. This, writes into 
    your config.json
    
    Arguments
    ---------
        new_conf : List
            
            The List with the configuration you 
            want to dump onto the file
    """
    with open(os.path.join(os.path.dirname(__file__) , config_file), 'w', encoding='utf8') as outfile:  
        json.dump(new_conf, outfile, indent=4, ensure_ascii=False)

def add_requirements_ignore(moduleName, requirementModuleName):
    config = {}

    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config = json.load(json_data_file)

    if not 'cant_install_requirements' in dict(config['core']):
        config['core']['cant_install_requirements'] = {}

    if not moduleName in config['core']['cant_install_requirements']:
        config['core']['cant_install_requirements'][moduleName] = []

    if not str(requirementModuleName) in list(config['core']['cant_install_requirements']):
        config['core']['cant_install_requirements'][moduleName].append(str(requirementModuleName))

    __save_config__(config)

# === __save_config__ ===
def __save_django_module_config__(new_conf, category, moduleName, functionName):
    """
    Save configuration passed as parameter
    to this function. This, writes into 
    your module view config ht_moduleName.json
    
    Arguments
    ---------
        new_conf : List
            
            The List with the configuration you 
            want to dump onto the file
    """
    config_file='ht_{moduleName}.json'.format(moduleName=moduleName.replace('ht_', ''))
    module_views_config_file = os.path.join(os.path.dirname(__file__) , 'config_modules_django', category, config_file)
    
    config = {}
    config['__gui_label__'] = moduleName
    config['django_form_module_function'] = {}

    if os.path.isfile(module_views_config_file):
        with open(module_views_config_file, 'r', encoding='utf8') as outfile:
            if outfile:
                config = json.load(outfile)

    if '_django_form_module_function_' in config:
        del(config['_django_form_module_function_'])

    if not 'django_form_module_function' in config:
        config['django_form_module_function'] = {}
    config['django_form_module_function'][functionName] = new_conf

    file_path, _ = os.path.split(module_views_config_file)
    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    with open(module_views_config_file, 'w', encoding='utf8') as outfile:  
        json.dump(config, outfile, indent=4, ensure_ascii=False)

# === __createModuleTemplateConfig__ ===
def __createModuleTemplateConfig__(module_name, category):
    """
    This function creates into config.json a template
    with a simple config for trying in your GUI your 
    functions. You would see in configuration file a new 
    ht_yourmodulename key with some more data inside it.
    They are necesary when using the framework GUI for 
    trying the functions.
    
    Arguments
    ---------
        module_name : str
            
            A function name in String that is loaded 
            in your hackingtools library
    """
    module_name = 'ht_{mod}'.format(mod=module_name)

    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config_tmp = json.load(json_data_file)
        if not module_name in config_tmp['modules']:
            config_tmp['modules'][module_name] = {}
            __save_config__(config_tmp)
            
    category_dir = os.path.join(os.path.dirname(__file__), 'config_modules_django', category)
    if not os.path.isdir(category_dir):
        os.mkdir(category_dir)

    module_config_file = os.path.join(category_dir, '{mod}.json'.format(mod=module_name))

    new_conf = {
        "__gui_label__" : "_MODULE_GUI_LABEL_",
        "_comment" : "Rename templates if have to use: (remove underscore) 'django_form_main_function' and 'django_form_module_function'",
        "_django_form_main_function_" : {
            "__function__" : "_FUNCTION_NAME_",
            "_HTML_FIELD_NAME_" : {
                "__type__" : "_HTML_INPUT_TYPE_",
                "label_desc" : "_DESCRIPTION_LABEL_",
                "required" : "_IF_REQUIRED_",
                "value" : "_INPUT_VALUE_",
                "loading_text" : "_INPUT_LOADING_TEXT_",
                "returnable_modules_functions" : {
                    "_MODULE_CALL_FOR_" : [
                        "_THAT_MODULES_FUNCTION"
                    ]
                },
                "options_from_function": {
                    "__CORE_OR_MODULE_NAME__": "__FUNCTION_TO_CALL__"
                }
            }
        },
        "_django_form_module_function_" : {
            "_PUBLIC_FUNCTION_" : {
                "__function__" : "_FUNCTION_NAME_",
                "__async__" : False,
                "__return__" : "_IF_RETURNS_LIKE_TEXT_",
                "_PARAM_TO_USE_IN_VIEWS_PY_" : {
                    "__type__" : "_HTML_INPUT_TYPE_",
                    "label_desc" : "_DESCRIPTION_LABEL_",
                    "value" : "_INPUT_VALUE_",
                    "required" : "_IF_REQUIRED_",
                    "returnable_modules_functions" : {
                        "_MODULE_CALL_FOR_" : [
                            "_THAT_MODULES_FUNCTION"
                        ]
                    },
                    "options_from_function": {
                        "__CORE_OR_MODULE_NAME__": "__FUNCTION_TO_CALL__"
                    }
                }
            }
        }
    }
    with open(module_config_file, 'w', encoding='utf8') as outfile:  
        json.dump(new_conf, outfile, indent=4, ensure_ascii=False)

# === __look_for_changes__ ===
def __look_for_changes__(django=False):
    """
    Reloads the configuration loaded
    
    Returns
    -------
        boolean
            
            Tell's if there where any changes
    """
    config_tmp = __readFilesAuto__()

    global config
    if not sorted(config.items()) == sorted(config_tmp.items()):
        config = config_tmp
        return True
    return False

# === getConfig ===
def getConfig(parentKey, key, subkey=None, extrasubkey=None):
    """
    Returns the configuration of some key values
    you explicitly tell on params
    
    Arguments
    ---------
        parentKey : str
            
            Parent key of the config.json
        key : str
            
            The String of a child into that parent 
            key on the config.json
    
    Keyword Arguments
    -----------------
        subkey : str
            
            The String of a child, into that child, 
            into that parent key on the config.json 
            (default: {None})
        extrasubkey : str
            
            The String of a child, into that child, 
            into the other child, into that parent 
            key on the config.json (default: {None})
    
    Returns
    -------
        List
            
            The content of the config.json you selected 
            into an List / None
    """
    try:
        if extrasubkey:
            try:
                if subkey:
                    try:
                        return config[parentKey][key][subkey][extrasubkey]
                    except:
                        return
            except:
                return
        else:
            try:
                if subkey:
                    try:
                        return config[parentKey][key][subkey]
                    except:
                        return
            except:
                return
        return config[parentKey][key]
    except:
        return None

# === getApiKey ===
def getApiKey(apiName):
    """
    Return an API Key registered into configuration
    
    Arguments
    ---------
        apiName : str
            
            The API Key name in String that is 
            registered into config.json
    
    Returns
    -------
        str
            
            The API Key into your config.json into 
            the apiName you selected / None
    """
    try:
        return config['core']['__API_KEY__'][apiName]
    except:
        return None

__readConfig__()