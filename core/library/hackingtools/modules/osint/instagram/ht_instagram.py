from hackingtools.core import Logger, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_instagram')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
    
    def __init__(self):
        pass
        
    def help(self):
        return ht.getFunctionsNamesFromModule('ht_instagram')