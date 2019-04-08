from .core import Logger
from . import import_modules as modules
from colorama import Fore, Back, Style

def getModulesJSON():
    """
    Mostramos los modulos cargados
    """
    Logger.printMessage('Modules loaded as JSON automatically:', modules.modules_loaded, debug_module=True)
    return modules.modules_loaded

def getModulesCalls():
    """
    Por cada modulo, muestro la llamada que pueda hacer y sale en YELLOW
    """
    Logger.printMessage('Modules :', debug_module=True)
    modulesCalls = []
    for mods in modules.getModules():
        Logger.printMessage('\t{text}'.format(text=mods), color=Fore.YELLOW, debug_module=True)
        modulesCalls.append(mods)
    return modulesCalls

def getModulesNames():
    """
    Devuelve los nombre de todos los modulos importados (ht_shodan, etc.)
    """
    modules_names = []
    for tools in modules.modules_loaded:
        modules_names.append(tools.split('.')[-1])
    return modules_names

def setDebugCore(on=True):
    """
    Establece en True / False el Debug para el CORE
    """
    Logger.setDebugCore(on)

def setDebugModule(on=True):
    """
    Establece en True / False el Debug para el Module
    """
    Logger.setDebugModule(on)
    
def getModule(moduleName):
    """
    Iniciamos con el comando anterior la instancia del modulo
    """
    Logger.printMessage('Initiation of {moduleName}'.format(moduleName=moduleName), debug_module=True)
    return eval('modules.{moduleName}.StartModule()'.format(moduleName=moduleName))

def createModule(moduleName, category):
    """
    Iniciamos con el comando anterior la instancia del modulo
    """
    Logger.printMessage('Creating {moduleName} on {category}'.format(moduleName=moduleName, category=category), debug_module=True)
    modules.createModule(moduleName, category)
    return 'Created'

def getModuleConfig(moduleName):
    if moduleName in getModulesNames():
        actualConf = getModulesJSON()
        for mod in actualConf:
            if moduleName in mod.split('.')[-1]:
                return actualConf[mod]
    return None