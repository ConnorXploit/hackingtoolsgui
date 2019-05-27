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
        return 'Bad key on JSON'

__readConfig__()