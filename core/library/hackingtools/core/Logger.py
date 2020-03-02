import inspect as __inspect
import os as __os
from datetime import datetime as __datetime
import colorama as __colorama
from colorama import Fore as __Fore

from . import Config, Utils
config = Config.getConfig(parentKey='core', key='Logger')


import logging
logger = logging.getLogger('hackingtools')
# Prevent multiple instances
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('hackingtools.log')
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)

__colorama.init()

global __logs__
__logs__ = {}

global __logs_clear__
__logs_clear__ = {}

global __DEBUG_CORE_FLAG__ 
__DEBUG_CORE_FLAG__ = config['__DEBUG_CORE_FLAG__']

global __DEBUG_MODULE_FLAG__ 
__DEBUG_MODULE_FLAG__ = config['__DEBUG_MODULE_FLAG__']

global __DEBUG_USER__ 
__DEBUG_USER__ = config['__DEBUG_USER__']

if config['clear_on_load']:
    print(__colorama.ansi.clear_screen()) # Clear Screen Code

def setDebugCore(on=True):
    """Function for establising __DEBUG_CORE_FLAG__ to True/False
    
    Keyword Arguments:
        on {boolean} -- Set's True or False the Debug messages for Core Logger calls (default: {True})
    """
    global __DEBUG_CORE_FLAG__
    __DEBUG_CORE_FLAG__ = on

def setDebugModule(on=True):
    """Function for establising __DEBUG_MODULE_FLAG__ to True/False
    
    Keyword Arguments:
        on {boolean} -- Set's True or False the Debug messages for Module Logger calls (default: {True})
    """
    global __DEBUG_MODULE_FLAG__
    __DEBUG_MODULE_FLAG__ = on

def setDebug(on=True):
    """Function for establising __DEBUG_USER__ to True/False
    
    Keyword Arguments:
        on {boolean} -- Set's True or False the Debug messages for User Logger calls (default: {True})
    """
    global __DEBUG_USER__
    __DEBUG_USER__ = on

def saveLog():
    """Creates a file with the log created by the library since loaded last time.
    Output format can be changed into config.json
    """
    global __logs__
    time_now = __datetime.utcnow().strftime(config['log_save_date_format'])[:-3]
    with open('log-{time}.txt'.format(time=time_now), 'w') as f:
        for log in getLogs():
            f.write("{log}\n".format(log=log))

def getLogs():
    global __logs__
    return __logs__

def getLogsClear():
    global __logs_clear__
    return __logs_clear__

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
    global __logs__
    global __logs_clear__
    filename = __inspect.stack()[1].filename
    methodName = __inspect.stack()[1].function
    
    if methodName.startswith('<'):
        methodCalledFrom = filename.split('\\')[-1]
    else:
        methodCalledFrom = '{file}.{function}()'.format(file=filename.split('\\')[-1], function=methodName)
    
    methodCalledFrom = str(__os.path.join(__os.path.split(__os.path.split(methodCalledFrom)[0])[1], __os.path.split(methodCalledFrom)[1]))

    time_now = Utils.getTime()

    colorMessage = __Fore.LIGHTMAGENTA_EX

    if color:
        colorMessage = color

    if is_error:
        colorMessage = __Fore.RED

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
    
    if is_error:
        logger.critical(msg)
    elif is_info:
        logger.info(msg)
    elif is_success:
        logger.debug(msg)
    elif is_warn:
        logger.warning(msg)
    else:
        logger.debug(msg)

    if (color == __Fore.YELLOW or is_warn):
        msg = '{e} - {m}'.format(e=warn_flag, m=msg)
    elif (color == __Fore.GREEN or is_success):
        msg = '{e} - {m}'.format(e=successful_flag, m=msg)
    elif (color == __Fore.BLUE or is_info):
        msg = '{e} - {m}'.format(e=info_flag, m=msg)
    elif is_error:
        msg = '{e} - {m}'.format(e=error_flag, m=msg)
    elif debug_module:
        msg = '{e} - {m}'.format(e=module_flag, m=msg)
    elif debug_core:
        msg = '{e} - {m}'.format(e=core_flag, m=msg)

    if description:
        __logs__[time_now] = msg
    else:
        __logs__[time_now] = msg

    temp_logs_clear = {}

    for x in __logs__:

        exists = False

        for temp in temp_logs_clear:
            if temp_logs_clear[temp]['msg'] == __logs__[x]:
                temp_logs_clear[temp]['count'] += 1
                exists = True

        if not exists:
            temp_logs_clear[x] = {}
            temp_logs_clear[x]['msg'] = __logs__[x]
            temp_logs_clear[x]['count'] = 1

    __logs_clear__ = {}

    for timeLog in temp_logs_clear:
        if temp_logs_clear[timeLog]['count'] > 1:
            __logs_clear__[timeLog] = '({n}) - {m}'.format(n=temp_logs_clear[timeLog]['count'], m=temp_logs_clear[timeLog]['msg'])
        else:
            __logs_clear__[timeLog] = temp_logs_clear[timeLog]['msg']
    # Clear Log Ends Here

    if ((not debug_module == True) and (not debug_core == True) and (__DEBUG_USER__ == True)) or ((debug_module == True) and (__DEBUG_MODULE_FLAG__ == True)) or ((debug_core == True) and (__DEBUG_CORE_FLAG__ == True)):
        if description:
            print('{timeColorStart}[{time}]{timeColorEnd} - {methodCalledFromColorStart}{methodCalledFrom}{methodCalledFromColorEnd} - {messageColorStart}{message}{messageColorEnd} - {description}'.format(
                timeColorStart=__Fore.BLUE, 
                timeColorEnd=__Fore.WHITE, 
                time=time_now,
                methodCalledFromColorStart=__Fore.GREEN, 
                methodCalledFrom=methodCalledFrom,
                methodCalledFromColorEnd=__Fore.WHITE,
                messageColorStart=colorMessage,
                message=message,
                messageColorEnd=__Fore.WHITE,
                description=description))
        else:
            print('{timeColorStart}[{time}]{timeColorEnd} - {methodCalledFromColorStart}{methodCalledFrom}{methodCalledFromColorEnd} - {messageColorStart}{message}{messageColorEnd}'.format(
                timeColorStart=__Fore.BLUE, 
                timeColorEnd=__Fore.WHITE, 
                time=time_now,
                methodCalledFromColorStart=__Fore.GREEN, 
                methodCalledFrom=methodCalledFrom,
                methodCalledFromColorEnd=__Fore.WHITE,
                messageColorStart=colorMessage,
                message=message,
                messageColorEnd=__Fore.WHITE))