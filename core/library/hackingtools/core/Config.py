import os

global config
config = {}

def __readConfig__():
    # Read config
    import json

    global config
    config = {}
    with open(os.path.join(os.path.dirname(__file__) , 'config.json')) as json_data_file:
        config = json.load(json_data_file)

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