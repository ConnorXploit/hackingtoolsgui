from hackingtools.core import Logger
import hackingtools as ht

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