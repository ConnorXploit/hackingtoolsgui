import inspect, os
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

from . import Config, Utils
config = Config.getConfig(parentKey='core', key='Logger')

colorama.init()

global logs
logs = {}

global logs_clear
logs_clear = {}

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
    global logs
    time_now = datetime.utcnow().strftime(config['log_save_date_format'])[:-3]
    with open('log-{time}.txt'.format(time=time_now), 'w') as f:
        for log in getLogs():
            f.write("{log}\n".format(log=log))

def getLogs():
    global logs
    return logs

def getLogsClear():
    global logs_clear
    return logs_clear

def print_and_return(msg, value, debug_module=False, debug_core=False, is_error=False, color=None):
    printMessage(message=msg, description=value, debug_core=debug_core, is_error=is_error, color=color)
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
    global logs
    global logs_clear
    filename = inspect.stack()[1].filename
    methodName = inspect.stack()[1].function
    
    if methodName.startswith('<'):
        methodCalledFrom = filename.split('\\')[-1]
    else:
        methodCalledFrom = '{file}.{function}()'.format(file=filename.split('\\')[-1], function=methodName)
    
    methodCalledFrom = str(os.path.join(os.path.split(os.path.split(methodCalledFrom)[0])[1], os.path.split(methodCalledFrom)[1]))

    time_now = Utils.getTime()

    colorMessage = Fore.LIGHTMAGENTA_EX

    if color:
        colorMessage = color

    if is_error:
        colorMessage = Fore.RED

    #if not debug_module and not debug_core:
    if description:
        msg = '{methodCalledFrom} - {message} - {description}'.format(methodCalledFrom=methodCalledFrom, message=message, description=description)
    else:
        msg = '{methodCalledFrom} - {message}'.format(methodCalledFrom=methodCalledFrom, message=message)

    appears = 0
    temp_logs_clear = {}

    for l in logs_clear:
        log_line = str(logs_clear[l])
        if msg != log_line:
            temp_logs_clear[l] = log_line
        else:
            appears += 1

    if appears > 0:
        temp_logs_clear[time_now] = '({n}) - {m}'.format(n=appears+1, m=msg)
    else:
        temp_logs_clear[time_now] = msg

    logs_clear = temp_logs_clear

    if description:
        logs[time_now] = '{methodCalledFrom} - {message} - {description}'.format(methodCalledFrom=methodCalledFrom, message=message, description=description)
    else:
        logs[time_now] = '{methodCalledFrom} - {message}'.format(methodCalledFrom=methodCalledFrom, message=message)

    if ((not debug_module == True) and (not debug_core == True) and (DEBUG_USER == True)) or ((debug_module == True) and (DEBUG_MODULE_FLAG == True)) or ((debug_core == True) and (DEBUG_CORE_FLAG == True)):
        if description:
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