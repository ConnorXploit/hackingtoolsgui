import os
import json

global config
config = {}

def __readConfig__():
    global config
    config = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config = json.load(json_data_file)

def __save_config__(new_conf):
    with open(os.path.join(os.path.dirname(__file__) , 'config.json'), 'w') as outfile:  
        json.dump(new_conf, outfile, indent=4)

def __createModuleTemplateConfig__(module_name):
    global config
    config_tmp = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config_tmp = json.load(json_data_file)
    new_config = {
        "__gui_label__" : "_MODULE_GUI_LABEL_",
        "django_form_main_function" : {
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
        "django_form_module_function" : {
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
    import json

    global config
    config_tmp = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config_tmp = json.load(json_data_file)

    if not sorted(config.items()) == sorted(config_tmp.items()):
        config = config_tmp
        return True
    return False

def getConfig(parentKey, key, subkey=None, extrasubkey=None):
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
        return

def getApiKey(apiName):
    try:
        return config['core']['__API_KEY__'][apiName]
    except:
        return 'API {n} not found'.format(n=apiName)

__readConfig__()