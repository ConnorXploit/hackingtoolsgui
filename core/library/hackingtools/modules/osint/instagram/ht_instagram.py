from hackingtools.core import Logger

class StartModule():
    
    def __init__(self):
        Logger.printMessage(message='ht_instagram loaded', debug_module=True)
        pass
        
    def getEdad(self):
        Logger.printMessage(message='{methodName}'.format(methodName='getEdad'), debug_module=True)
        return 23