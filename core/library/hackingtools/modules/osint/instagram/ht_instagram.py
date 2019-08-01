from hackingtools.core import Logger, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_instagram')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
    
    def __init__(self):
        Logger.printMessage(message='ht_instagram loaded', debug_core=True)
        pass
        
    def help(self):
        functions = ht.getFunctionsNamesFromModule('ht_instagram')
        Logger.printMessage(message=functions)
        return functions

    def getEdad(self):
        Logger.printMessage(message='{methodName}'.format(methodName='getEdad'), debug_module=True)
        return 23