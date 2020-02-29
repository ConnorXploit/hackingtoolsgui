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

import os as __os
import json as __json

global __config__
__config__ = {}

global __api_keys_sessions__
__api_keys_sessions__ = False

global __switching_to_map__
__switching_to_map__ = False

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
                        return __config__[parentKey][key][subkey][extrasubkey]
                    except:
                        return
            except:
                return
        else:
            try:
                if subkey:
                    try:
                        return __config__[parentKey][key][subkey]
                    except:
                        return
            except:
                return
        return __config__[parentKey][key]
    except:
        return None

def add_pool_node(node):
    __config__ = {}
    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        __config__ = __json.load(json_data_file)

    if not 'known_nodes' in __config__['core']['Pool']:
        __config__['core']['Pool']['known_nodes'] = []

    __config__['core']['Pool']['known_nodes'].append(node)

    __save_config__(__config__)

def remove_pool_node(node):
    __config__ = {}
    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        __config__ = __json.load(json_data_file)

    if not 'known_nodes' in __config__['core']['Pool']:
        __config__['core']['Pool']['known_nodes'] = []
    
    if node in __config__['core']['Pool']['known_nodes']:
        __config__['core']['Pool']['known_nodes'].remove(node)

    __save_config__(__config__)

def add_my_service(node): # Used by Heroku
    __config__ = {}
    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        __config__ = __json.load(json_data_file)

    if not 'my_services' in __config__['core']['Connections']:
        __config__['core']['Connections']['my_services'] = []

    __config__['core']['Connections']['my_services'].append(node)

    __save_config__(__config__)

def remove_my_service(node):
    __config__ = {}
    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        __config__ = __json.load(json_data_file)

    if not 'my_services' in __config__['core']['Connections']:
        __config__['core']['Connections']['my_services'] = []
    
    if node in __config__['core']['Connections']['my_services']:
        __config__['core']['Connections']['my_services'].remove(node)

    __save_config__(__config__)

def switch_function_for_map(category, moduleName, functionName):
    global __switching_to_map__
    __switching_to_map__ = True
    mod_config_file = __os.path.join(__os.path.dirname(__file__), 'config_django.json')
    
    conf = {}

    conf = __config__['django']

    if conf:
        if not 'maps' in conf:
            conf['maps'] = {}
        in_map = '__in_map_{f}__'.format(f=functionName)

        if not moduleName in conf['maps']:
            conf['maps'][moduleName] = {}

        if not functionName in conf['maps'][moduleName]:
            conf['maps'][moduleName][functionName] = {}

        if not in_map in conf['maps'][moduleName][functionName]:
            conf['maps'][moduleName][functionName][in_map] = False
        else:
            conf['maps'][moduleName][functionName][in_map] = not conf['maps'][moduleName][functionName][in_map]

        with open(mod_config_file, 'w', encoding='utf8') as outfile:  
            __json.dump(conf, outfile, indent=4, ensure_ascii=False)

    __switching_to_map__ = False

def add_requirements_ignore(moduleName, requirementModuleName):
    __config__ = {}

    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        __config__ = __json.load(json_data_file)

    if not '__cant_install_requirements__' in dict(__config__['core']):
        __config__['core']['__cant_install_requirements__'] = {}

    if not moduleName in __config__['core']['__cant_install_requirements__']:
        __config__['core']['__cant_install_requirements__'][moduleName] = []

    if not str(requirementModuleName) in list(__config__['core']['__cant_install_requirements__']):
        __config__['core']['__cant_install_requirements__'][moduleName].append(str(requirementModuleName))

    __save_config__(__config__)

# API Keys

def getAPIsNames(session_id=None):
    if session_id:
        try:
            __config__['core']['__API_KEY_{sess}__'.format(sess=session_id)].keys()
        except:
            pass
    return list(__config__['core']['__API_KEY__'].keys())

# === getAPIKey ===
def getAPIKey(api_name, session_id=None):
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
        if session_id:
            try:
                sess_key = '__API_KEY_{sess}__'.format(sess=session_id)
                return __config__['core'][sess_key][api_name]
            except:
                pass
        return __config__['core']['__API_KEY__'][api_name]
    except:
        return None

# === setAPIKey ===
def setAPIKey(api_name, api_key, session_id=None):
    if session_id:
        try:
            sess_key = '__API_KEY_{sess}__'.format(sess=session_id)
            if not sess_key in __config__['core']:
                __config__['core'][sess_key] = {}
            __config__['core'][sess_key][api_name] = api_key
        except:
            __config__['core']['__API_KEY__'][api_name] = api_key
    else:
        __config__['core']['__API_KEY__'][api_name] = api_key

def loadRestAPIsFile(rest_api_file, password, session_id=None):
    with open(rest_api_file, 'r') as res:
        from hackingtools.modules.crypto.rsa import ht_rsa as r
        mod_rsa = r.StartModule()
        import hashlib
        deciphered = mod_rsa.decode(hashlib.md5(password.encode()).hexdigest(), res.read().replace('\n', ''))
        api_keys = __json.loads(deciphered)
        if session_id:
            try:
                sess_key = '__API_KEY_{sess}__'.format(sess=session_id)
                if not sess_key in __config__['core']:
                    __config__['core'][sess_key] = {}
                for k in __config__['core'][sess_key]:
                    if not k in api_keys:
                        api_keys[k] = __config__['core'][sess_key][k]
                __config__['core'][sess_key] = api_keys
            except:
                __config__['core']['__API_KEY__'] = api_keys
        else:
            __config__['core']['__API_KEY__'] = api_keys

def saveRestAPIsFile(rest_api_file, password, session_id=None):
    try:
        if session_id:
            try:
                sess_key = '__API_KEY_{sess}__'.format(sess=session_id)
                api_keys = __config__['core'][sess_key]
            except:
                api_keys = __config__['core']['__API_KEY__']
        else:
            api_keys = __config__['core']['__API_KEY__']
        data = __json.dumps(api_keys)
        from hackingtools.modules.crypto.rsa import ht_rsa as r
        mod_rsa = r.StartModule()
        import hashlib
        ciphered = mod_rsa.encode(hashlib.md5(password.encode()).hexdigest(), data)
        max_width = 64
        ciphered = '\n'.join([ciphered[y-max_width:y] for y in range(max_width, len(ciphered)+max_width,max_width)])
        with open(__os.path.join(__os.path.dirname(__file__), 'apis_files', rest_api_file), 'w') as n:
            n.write(ciphered)
        return __os.path.join(__os.path.dirname(__file__), 'apis_files', rest_api_file)
    except Exception as e:
        return str(e)

def setTelegramBotToken(token):
    __config__['core']['TelegramBot']['bot-token'] = token

# End API Keys

# Maps

def saveHostSearchedInMap(ip, location, country, info, searched_term, session_id=None):
    config_root = __config__['core']

    if session_id:
        if not session_id in config_root:
            config_root[session_id] = {}
        config_root = config_root[session_id]

    if not 'map_search' in config_root:
        config_root['map_search'] = {}

    config_root = config_root['map_search']

    config_root[ip] = {}
    
    config_root[ip]['longitude'] = location[0]
    config_root[ip]['latitude'] = location[1]

    config_root[ip]['country'] = country
    
    config_root[ip]['info'] = info
    config_root[ip]['searched_term'] = searched_term

def getSearchedHostsInMap(session_id=None):
    try:
        if session_id:
            return __config__['core'][session_id]['map_search']
        return __config__['core']['map_search']
    except:
        return {}

# End Maps

def __readFilesAuto__(djangoButtonsPool=False):
    __config__ = {}
    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        __config__ = __json.load(json_data_file)

    if __config__["core"]["LOAD_DJANGO_CONF"] == True:
        django = True

    if django:
        # Load the basic config for Django
        global __switching_to_map__
        if not __switching_to_map__:
            with open(__os.path.join(__os.path.dirname(__file__) , 'config_django.json')) as json_data_file_django:
                __config__['django'] = {}
                config_django = __json.load(json_data_file_django)
                for conf in config_django:
                    __config__['django'][conf] = {}
                    for django_data in config_django[conf]:
                        __config__['django'][conf][django_data] = config_django[conf][django_data] 

            # Loads the config for the modules into Django as modal forms
            categories_dir = __os.path.join(__os.path.dirname(__file__), 'config_modules_django')
            for mod in __config__['modules']:
                categories = __os.listdir(categories_dir)
                for cat in categories:
                    module_config_file = __os.path.join(categories_dir, cat, '{mod}.json'.format(mod=mod))
                    if __os.path.isfile(module_config_file):
                        with open(module_config_file) as json_data_file_django:
                            if json_data_file_django:
                                config_django = __json.load(json_data_file_django)
                                for conf in config_django:
                                    __config__['modules'][mod][conf] = config_django[conf]
                                    if djangoButtonsPool:
                                        if isinstance(__config__['modules'][mod][conf], dict):
                                            for f in __config__['modules'][mod][conf]:
                                                if '__pool_it_' in f:
                                                    __config__['modules'][mod][conf][f]['selected'] = True
    return __config__

def __djangoSwitchPoolItButtons__(checked=False):
    global __config__
    __config__ = __readFilesAuto__(djangoButtonsPool=checked)
    return __config__

# === __readConfig__ ===
def __readConfig__(django=False):
    """
    Read's all the configuration included in 
    your config.json file and inside config_modules_django directory
    recursively by your loaded modules into your config.json
    """
    global __config__
    __config__ = __readFilesAuto__()

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
    for api_name in new_conf['core']['__API_KEY__']:
        new_conf['core']['__API_KEY__'][api_name] = ''
    with open(__os.path.join(__os.path.dirname(__file__) , config_file), 'w', encoding='utf8') as outfile:  
        __json.dump(new_conf, outfile, indent=4, ensure_ascii=False)

def __cleanHtPassFiles__():
    if 'apis_files' in __os.listdir(__os.path.dirname(__file__)):
        for htpass_file in __os.listdir(__os.path.join(__os.path.dirname(__file__), 'apis_files')):
            __os.remove(__os.path.join(__os.path.dirname(__file__), 'apis_files', htpass_file))

# === __save_config__ ===
def __save_django_module_config__(new_conf, category, moduleName, functionName, is_main=True):
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
    module_views_config_file = __os.path.join(__os.path.dirname(__file__) , 'config_modules_django', category, config_file)
    
    add_django_modal_to = 'django_form_module_function'
    if is_main:
        add_django_modal_to = 'django_form_main_function'

    __config__ = {}
    __config__['__gui_label__'] = moduleName
    __config__[add_django_modal_to] = {}

    if __os.path.isfile(module_views_config_file):
        with open(module_views_config_file, 'r', encoding='utf8') as outfile:
            if outfile:
                __config__ = __json.load(outfile)

    if not add_django_modal_to in __config__:
        __config__[add_django_modal_to] = {}
    else: # is_main - not deleted in last line
        if '_django_form_main_function_' in __config__:
            del(__config__['_django_form_main_function_'])
        if not add_django_modal_to in __config__:
            __config__[add_django_modal_to] = {}
        if '__function__' in __config__[add_django_modal_to]:
            if __config__[add_django_modal_to]['__function__'] != new_conf['__function__']:
                __config__[add_django_modal_to] = {}

    if is_main and not __config__[add_django_modal_to]:
        __config__[add_django_modal_to] = new_conf
    elif add_django_modal_to == 'django_form_module_function':
        __config__[add_django_modal_to][functionName] = new_conf

    file_path, _ = __os.path.split(module_views_config_file)
    if not __os.path.isdir(file_path):
        __os.mkdir(file_path)

    with open(module_views_config_file, 'w', encoding='utf8') as outfile:  
        __json.dump(__config__, outfile, indent=4, ensure_ascii=False)

def __regenerateConfigModulesDjango__(new_conf, category, moduleName):
    config_file='ht_{moduleName}.json'.format(moduleName=moduleName.replace('ht_', ''))
    module_views_config_file = __os.path.join(__os.path.dirname(__file__) , 'config_modules_django', category, config_file)

    __config__ = {}

    if __os.path.isfile(module_views_config_file):
        with open(module_views_config_file, 'r', encoding='utf8') as outfile:
            if outfile:
                __config__ = __json.load(outfile)

    __config__['django_form_module_function'] = new_conf
    
    with open(module_views_config_file, 'w', encoding='utf8') as outfile:  
        __json.dump(__config__, outfile, indent=4, ensure_ascii=False)

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

    with open(__os.path.join(__os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config_tmp = __json.load(json_data_file)
        if not module_name in config_tmp['modules']:
            config_tmp['modules'][module_name] = {}
            __save_config__(config_tmp)
            
    category_dir = __os.path.join(__os.path.dirname(__file__), 'config_modules_django', category)
    if not __os.path.isdir(category_dir):
        __os.mkdir(category_dir)

    module_config_file = __os.path.join(category_dir, '{mod}.json'.format(mod=module_name))

    d = {}
    with open(module_config_file, 'r', encoding='utf8') as outfile:  
        d = __json.load(outfile)

    if not d:
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
            __json.dump(new_conf, outfile, indent=4, ensure_ascii=False)

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

    global __config__
    if not sorted(__config__.items()) == sorted(config_tmp.items()):
        __config__ = config_tmp
        return True
    return False

__readConfig__()