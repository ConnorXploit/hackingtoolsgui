import inspect
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

from . import Config, Utils
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
    """Function for establising DEBUG_CORE_FLAG to True/False
    
    Keyword Arguments:
        on {boolean} -- Set's True or False the Debug messages for Core Logger calls (default: {True})
    """
    global DEBUG_CORE_FLAG
    DEBUG_CORE_FLAG = on

def setDebugModule(on=True):
    """Function for establising DEBUG_MODULE_FLAG to True/False
    
    Keyword Arguments:
        on {boolean} -- Set's True or False the Debug messages for Module Logger calls (default: {True})
    """
    global DEBUG_MODULE_FLAG
    DEBUG_MODULE_FLAG = on

def setDebug(on=True):
    """Function for establising DEBUG_USER to True/False
    
    Keyword Arguments:
        on {boolean} -- Set's True or False the Debug messages for User Logger calls (default: {True})
    """
    global DEBUG_USER
    DEBUG_USER = on

def saveLog():
    """Creates a file with the log created by the library since loaded last time.
    Output format can be changed into config.json
    """
    time_now = datetime.utcnow().strftime(config['log_save_date_format'])[:-3]
    with open('log-{time}.txt'.format(time=time_now), 'w') as f:
        for log in logs:
            f.write("{log}\n".format(log=log))


def print_and_return(msg, value, debug_module=False, debug_core=False, is_error=False):
    printMessage(message=msg, description=value, debug_core=debug_core, is_error=is_error)
    return value

def printMessage(message, description=None, debug_module=False, debug_core=False, is_error=False, color=None):
    """This function prints a pretty message in console. The colors can be changed in config.json
    
    Arguments:
        message {String} -- The main message you want to show on console log
    
    Keyword Arguments:
        description {String} -- The description of the message you are showing (default: {None})
        debug_module {bool} -- Tell's if the message is been called from a module (default: {False})
        debug_core {bool} -- Tell's if the message is been called from any core file (default: {False})
        is_error {bool} -- For showing in other color because been an error (default: {False})
        color {[type]} -- A color for showing with other color (default: {None})
    """
    filename = inspect.stack()[1].filename
    methodName = inspect.stack()[1].function
    
    if methodName.startswith('<'):
        methodCalledFrom = filename.split('\\')[-1]
    else:
        methodCalledFrom = '{file}.{function}()'.format(file=filename.split('\\')[-1], function=methodName)
    
    time_now = Utils.getTime()

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