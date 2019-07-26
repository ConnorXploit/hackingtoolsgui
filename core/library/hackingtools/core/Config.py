import os
import json

global config
config = {}

def __readConfig__():
    """Read's all the configuration included in your config.json file
    """
    global config
    config = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config = json.load(json_data_file)

def __save_config__(new_conf):
    """Save configuration passed as parameter to this function.
    This, writes into your config.json
    
    Arguments:
        new_conf {Array} -- The Array with the configuration you want to dump onto the file
    """
    with open(os.path.join(os.path.dirname(__file__) , 'config.json'), 'w', encoding='utf8') as outfile:  
        json.dump(new_conf, outfile, indent=4, ensure_ascii=False)

def __createModuleTemplateConfig__(module_name):
    """This function creates into config.json a template with a simple config for trying in your GUI your functions.
    You would see in configuration file a new ht_yourmodulename key with some more data inside it.
    They are necesary when using the framework GUI for trying the functions.
    
    Arguments:
        module_name {String} -- A function name in String that is loaded in your hackingtools library
    """
    global config
    config_tmp = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config_tmp = json.load(json_data_file)
    new_config = {
        "__gui_label__" : "_MODULE_GUI_LABEL_",
        "_comment" : "Rename templates if have to use: (remove underscore) 'django_form_main_function' and 'django_form_module_function'",
        "_django_form_main_function_" : {
            "_HTML_FIELD_NAME_" : {
                "__id__" : "_HTML_FIELD_NAME_",
                "__type__" : "_HTML_INPUT_TYPE_",
                "__className__" : "_HTML_INPUT_CLASS_",
                "label_desc" : "_DESCRIPTION_LABEL_",
                "required" : "_IF_REQUIRED_",
                "value" : "_INPUT_VALUE_",
                "loading_text" : "_INPUT_LOADING_TEXT_"
            }
        },
        "_django_form_module_function_" : {
            "_PUBLIC_FUNCTION_" : {
                "__function__" : "_FUNCTION_CALLABLE_NAME_",
                "__return__" : "_IF_RETURNS_LIKE_TEXT_",
                "_PARAM_TO_USE_IN_VIEWS_PY_" : {
                    "__id__" : "_HTML_FIELD_NAME_",
                    "__type__" : "_HTML_INPUT_TYPE_",
                    "__className__" : "_HTML_INPUT_CLASS_",
                    "label_desc" : "_DESCRIPTION_LABEL_",
                    "value" : "_INPUT_VALUE_",
                    "required" : "_IF_REQUIRED_",
                    "returnable_modules_functions" : {
                        "_MODULE_CALL_FOR_" : [
                            "_THAT_MODULES_FUNCTION"
                        ]
                    }
                }
            }
        }
    }
    new_key_module = 'ht_{mod}'.format(mod=module_name)
    config_tmp['modules'][new_key_module] = new_config
    __save_config__(config_tmp)

def __look_for_changes__():
    """Reloads the configuration loaded
    
    Returns:
        boolean -- Tell's if there where any changes
    """
    global config
    config_tmp = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config_tmp = json.load(json_data_file)

    if not sorted(config.items()) == sorted(config_tmp.items()):
        config = config_tmp
        return True
    return False

def getConfig(parentKey, key, subkey=None, extrasubkey=None):
    """Returns the configuration of some key values you explicitly tell on params
    
    Arguments:
        parentKey {String} -- Parent key of the config.json
        key {String} -- The String of a child into that parent key on the config.json
    
    Keyword Arguments:
        subkey {String} -- The String of a child, into that child, into that parent key on the config.json (default: {None})
        extrasubkey {String} -- The String of a child, into that child, into the other child, into that parent key on the config.json (default: {None})
    
    Returns:
        Array -- The content of the config.json you selected into an Array / None
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

def getApiKey(apiName):
    """Return an API Key registered into configuration
    
    Arguments:
        apiName {String} -- The API Key name in String that is registered into config.json
    
    Returns:
        String -- The API Key into your config.json into the apiName you selected / None
    """
    try:
        return config['core']['__API_KEY__'][apiName]
    except:
        return None

__readConfig__()