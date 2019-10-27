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

def printMessage(message, description=None, debug_module=False, debug_core=False, is_error=False, is_warn=False, is_info=False, is_success=False, color=None):
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

    # Clear Log Starts Here
    successful_flag = '[SUCCESS]'
    error_flag = '[ERROR]'
    core_flag = '[CORE]'
    module_flag = '[MODULE]'
    warn_flag = '[WARN]'
    info_flag = '[INFO]' # Not used yet

    if description:
        msg = '{methodCalledFrom} - {message} - {description}'.format(methodCalledFrom=methodCalledFrom, message=message, description=description)
    else:
        msg = '{methodCalledFrom} - {message}'.format(methodCalledFrom=methodCalledFrom, message=message)


    if (color == Fore.YELLOW or is_warn):
        msg = '{e} - {m}'.format(e=warn_flag, m=msg)
    elif (color == Fore.GREEN or is_success):
        msg = '{e} - {m}'.format(e=successful_flag, m=msg)
    elif (color == Fore.BLUE or is_info):
        msg = '{e} - {m}'.format(e=info_flag, m=msg)
    elif is_error:
        msg = '{e} - {m}'.format(e=error_flag, m=msg)
    elif debug_module:
        msg = '{e} - {m}'.format(e=module_flag, m=msg)
    elif debug_core:
        msg = '{e} - {m}'.format(e=core_flag, m=msg)

    if description:
        logs[time_now] = msg
    else:
        logs[time_now] = msg

    temp_logs_clear = {}

    for x in logs:

        exists = False

        for temp in temp_logs_clear:
            if temp_logs_clear[temp]['msg'] == logs[x]:
                temp_logs_clear[temp]['count'] += 1
                exists = True

        if not exists:
            temp_logs_clear[x] = {}
            temp_logs_clear[x]['msg'] = logs[x]
            temp_logs_clear[x]['count'] = 1

    logs_clear = {}

    for timeLog in temp_logs_clear:
        if temp_logs_clear[timeLog]['count'] > 1:
            logs_clear[timeLog] = '({n}) - {m}'.format(n=temp_logs_clear[timeLog]['count'], m=temp_logs_clear[timeLog]['msg'])
        else:
            logs_clear[timeLog] = temp_logs_clear[timeLog]['msg']
    # Clear Log Ends Here

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