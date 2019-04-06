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

def getConfig(parentKey, key, subkey=None):
    try:
        if subkey:
            return config[parentKey][key][subkey]
        return config[parentKey][key]
    except:
        return 'Bad key on JSON'

__readConfig__()