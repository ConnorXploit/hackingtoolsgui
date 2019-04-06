import inspect
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

from . import Config
config = Config.getConfig(parentKey='core', key='Logger')

colorama.init()

global logs
logs = {}

global DEBUG_CORE_FLAG 
DEBUG_CORE_FLAG = config['DEBUG_CORE_FLAG']

global DEBUG_MODULE_FLAG 
DEBUG_MODULE_FLAG = config['DEBUG_MODULE_FLAG']

global DEBUG_USER 
DEBUG_USER = config['DEBUG_USER']

if config['clear_on_load']:
    print(colorama.ansi.clear_screen()) # Clear Screen Code

def setDebugCore(on=True):
    """
    Funcion para establecer el DEBUG_CORE_FLAG a True/False
    """
    global DEBUG_CORE_FLAG
    DEBUG_CORE_FLAG = on

def setDebugModule(on=True):
    """
    Funcion para establecer el DEBUG_MODULE_FLAG a True/False
    """
    global DEBUG_MODULE_FLAG
    DEBUG_MODULE_FLAG = on

def setDebug(on=True):
    """
    Funcion para establecer el DEBUG_USER a True/False
    """
    global DEBUG_USER
    DEBUG_USER = on

def saveLog():
    time_now = datetime.utcnow().strftime(config['log_save_date_format'])[:-3]
    with open('log-{time}.txt'.format(time=time_now), 'w') as f:
        for log in logs:
            f.write("{log}\n".format(log=log))

def printMessage(message, description=None, debug_module=False, debug_core=False, is_error=False, color=None):
    """
    Funcion para imprimir mensajes en consola con estilos, tiempo, funcion de llamada, etc.
    """
    filename = inspect.stack()[1].filename
    methodName = inspect.stack()[1].function
    
    if methodName.startswith('<'):
        methodCalledFrom = filename.split('\\')[-1]
    else:
        methodCalledFrom = '{file}.{function}()'.format(file=filename.split('\\')[-1], function=methodName)
    
    time_now = datetime.utcnow().strftime(config['log_print_date_format'])[:-3]

    colorMessage = Fore.LIGHTMAGENTA_EX

    if color:
        colorMessage = color

    if is_error:
        colorMessage = Fore.RED

    if ((not debug_module) and (not debug_core) and (DEBUG_USER)) or ((debug_module) and (DEBUG_MODULE_FLAG)) or ((debug_core) and (DEBUG_CORE_FLAG)):
        if description:
            logs[time_now] = '{methodCalledFrom} - {message} - {description}'.format(methodCalledFrom=methodCalledFrom, message=message, description=description)
            print('{timeColorStart}[{time}]{timeColorEnd} - {methodCalledFromColorStart}{methodCalledFrom}{methodCalledFromColorEnd} - {messageColorStart}{message}{messageColorEnd} - {description}'.format(
                timeColorStart=Fore.BLUE, 
                timeColorEnd=Fore.WHITE, 
                time=time_now,
                methodCalledFromColorStart=Fore.GREEN, 
                methodCalledFrom=methodCalledFrom,
                methodCalledFromColorEnd=Fore.WHITE,
                messageColorStart=colorMessage,
                message=message,
                messageColorEnd=Fore.WHITE,
                description=description))
        else:
            logs[time_now] = '{methodCalledFrom} - {message}'.format(methodCalledFrom=methodCalledFrom, message=message)
            print('{timeColorStart}[{time}]{timeColorEnd} - {methodCalledFromColorStart}{methodCalledFrom}{methodCalledFromColorEnd} - {messageColorStart}{message}{messageColorEnd}'.format(
                timeColorStart=Fore.BLUE, 
                timeColorEnd=Fore.WHITE, 
                time=time_now,
                methodCalledFromColorStart=Fore.GREEN, 
                methodCalledFrom=methodCalledFrom,
                methodCalledFromColorEnd=Fore.WHITE,
                messageColorStart=colorMessage,
                message=message,
                messageColorEnd=Fore.WHITE))