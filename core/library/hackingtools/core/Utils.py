from . import Config, Logger

def amIdjango(fileCall):
    # Used by core on init for initialaizing Django Functions if needed
    return True if 'core.library.hackingtools' == fileCall else False

if amIdjango(__name__):
    from core.library import hackingtools as ht
else:
    import hackingtools as ht
config = Config.getConfig(parentKey='core', key='Utils')
config_logger = Config.getConfig(parentKey='core', key='Logger')
config_utils = Config.getConfig(parentKey='core', key='Utils', subkey='dictionaries')

function_param_exclude = Config.getConfig(parentKey='core', key='import_modules', subkey='function_param_exclude')
default_class_name_for_all = Config.getConfig(parentKey='core', key='import_modules', subkey='default_class_name_for_all')  

from colorama import Fore

import random
import requests
import base64
import os, inspect, ast, threading, time
from threading import Thread, Lock
import socket
import itertools
from itertools import product 

from datetime import datetime

global lock
lock = Lock()

global threads
threads = {}

def getWorkers():
    global threads
    return threads

def startWorker(workerName, functionCall, args=(), timesleep=1, chunk=None):
    t = None
    try:
        main_worker_name = 'main_{w}'.format(w=workerName)
        Logger.printMessage(main_worker_name, 'Starting thread for control threads to a functioncall', debug_core=True)
        t = Thread(target=worker, args=(workerName, functionCall, args, int(timesleep), chunk,))
        t.setDaemon(True)
        threads[main_worker_name] = t
        t.start()
    except:
        t.join()

def worker(workerName, functionCall, args=(), timesleep=1, chunk=None):
    while True:
        t = None
        try:
            Logger.printMessage(workerName, 'Calling for try in a thread')
            t = Thread(target=functionCall, args=args)
            t.setDaemon(True)
            threads[workerName] = t
            t.start()
        except:
            if t:
                t.join()
        time.sleep(timesleep)

def killAllWorkers(workers):
    for t in threads:
        threads[t].join()

# File Manipulation
def getFileContentInByteArray(filePath):
    """Function that returns a ByteArray with the data from a file
    
    Arguments:
        filePath {String} -- The Path of the file and the file name
    
    Returns:
        byteArray -- The content of the file / None
    """
    try:
        Logger.printMessage(message='{methodName}'.format(methodName='getFileInByteArray'), description='{filePath}'.format(filePath=filePath), debug_core=True)
        the_file = open(filePath, "rb")
        file_data = the_file.read()
        the_file.close()
        return file_data
    except:
        pass
    return None
        
def saveToFile(content, fileName):
    """Saves a new file with a Byte Array and a fileName
    
    Arguments:
        content {byteArray} -- The content we want to write into the file
        fileName {String} -- The file name
    
    Returns:
        boolean -- If saved True, else False
    """
    try:
        Logger.printMessage(message='{methodName}'.format(methodName='saveToFile'), description='{filename}'.format(filename=fileName), debug_core=True)
        the_file = open(fileName, "w")
        the_file.write(content)
        the_file.close()
        return True
    except:
        pass
    return False

def emptyDirectory(directory):
    """
    Cleans a directory given as param
    Be carefull with the 
    
    Arguments:
        dir : str
        
            output_dir variable in modules,
            for example, ht_crypter, it has a
            path automatically created
            for this function
    Returns:
        bool

            Returns if all was OK
    """
    try:
        #Logger.printMessage(message='emptyDirectory', description='Would empty: {path}'.format(path=directory), color=Fore.YELLOW)
        #if os.path.isdir(directory):
        #    shutil.rmtree(directory)
        #    return True
        # ! Temporary ommited
        return False
    except:
        return False

def getValidDictNoEmptyKeys(data):
    final_data = {}
    if isinstance(data, str):
        return data
    for d in data:
        if data[d]:
            if isinstance(data[d], str):
                final_data[d] = data[d]
            else:
                final_data[d] = getValidDictNoEmptyKeys(data[d])
    return final_data

def getFunctionFullCall(moduleName, category, functionName):
    return 'ht.modules.{category}.{modDir}.{module}.{callClass}().{function}'.format(category=category, modDir=moduleName.replace('ht_', ''), module=moduleName, callClass=default_class_name_for_all, function=functionName)

def getFunctionsParams(category, moduleName, functionName, i_want_list=False):
    params_func = None
    function = getFunctionFullCall(moduleName=moduleName, category=category, functionName=functionName)
    try:
        params_func = inspect.getfullargspec(eval(function))[0]
        params_func = [param for param in params_func if not param in function_param_exclude] if params_func else []

        args, varargs, keywords, defaults = inspect.getargspec(eval(function))
        args = [param for param in args if not param in function_param_exclude] if args else []

        if defaults:
            new_params_func = params_func[:-len(defaults)]
            args_defaults = dict(zip(params_func[-len(defaults):], defaults))

        if i_want_list:
            if defaults:
                # urls.py
                return new_params_func + [i for i in args_defaults.keys()]

            return {"params":params_func}

        if defaults:
            return {"params":new_params_func,"defaults": args_defaults}

        return {"params":params_func}
    except Exception as e:
        pass
    return []

def getValueType(value):
    try:
        if isinstance(eval(value), bool):
            return 'checkbox'
    except:
        pass
    try:
        if isinstance(eval(value), int):
            return 'number'
    except:
        pass
    try:
        if isinstance(eval(value), list):
            return 'select'
    except:
        pass
    try:
        if isinstance(eval(value), str):
            if '.' in value and len(value.split('.')[1] in range(1,4)):
                return 'file'
            if 'pass' in value or 'password' in value:
                return 'password'
            if 'data' in value:
                return 'textarea'
            return 'select'
    except:
        pass
    return 'text'

def doesFunctionContainsExplicitReturn(functionCall):
    try:
        return True if 'return' in inspect.getsource(eval(functionCall)) else False
    except:
        return False

# Others
def getTime():
    return datetime.utcnow().strftime(config_logger['log_print_date_format'])[:-3]

# Maths
def euclides(a, b):
    """Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
    
    Arguments:
        a {integer} -- Value 1 to use in euclides
        b {integer} -- Value 2 to use in euclides
    
    Returns:
        integer -- Euclides of a and b
    """
    Logger.printMessage(message='{methodName}'.format(methodName='euclides'), description='{a} - {b}'.format(a=a, b=b), debug_core=True)
    while b != 0:
        a, b = b, a % b
    return a

def multiplicativeInverse(e, phi):
    """Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    
    Arguments:
        e {integer} -- Euclides value
        phi {integer} -- Phi value
    
    Returns:
        integer -- The inverse multiplicative of e and phi
    """
    Logger.printMessage(message='{methodName}'.format(methodName='multiplicativeInverse'), description='{e} - {phi}'.format(e=e, phi=phi), debug_core=True)
    # See: http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    def eea(a,b):
        if b==0:return (1,0)
        (q,r) = (a//b,a%b)
        (s,t) = eea(b,r)
        return (t, s-(q*t) )

    inv = eea(e,phi)[0]
    if inv < 1: inv += phi #we only want positive values
    return inv

def isPrime(n):
    """Tests to see if a number is prime.
    
    Arguments:
        number {integer} -- The number to test if is a prime number
    
    Returns:
        boolean -- If is prime True, else False
    """
    Logger.printMessage(message='{methodName}'.format(methodName='isPrime'), description='{n}'.format(n=n), debug_core=True)
    excepted = (0, 2, 4, 5, 6, 8)
    if not int(str(n)[-1]) in excepted:
        if (n==1):
            return False
        elif (n==2):
            return True
        else:
            for x in range(2,n):
                if(n % x==0):
                    return False
            return True
    return False

def getRandomPrimeByLength(length = 8):
    """Returns a random prime number with the length you choose
    
    Keyword Arguments:
        length {integer} -- The length of the number we want (default: {8})
    
    Returns:
        integer -- A random prime number with the length you specified / -1
    """
    try:
        length = int(length)
    except:
        length = 8
    try:
        while True:
            n = int(randomText(length=length, alphabet='numeric'))
            if len(str(n)) == length and isPrime(n):
                return n
    except:
        return -1

# Text Treatment
def decimalToBinary(n):
    return bin(n).replace("0b","")

def textToAscii(content):
    """Transform text in String to ASCII Array
    
    Arguments:
        content {String} -- The String content we want to transform into ASCII Array
    
    Returns:
        Array -- The content String transformed into an Array in ASCII
    """
    Logger.printMessage(message='{methodName}'.format(methodName='textToAscii'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [ord(pal) for pal in content]

def asciiToHex(content):
    """Transform ASCII Array to Hex Array
    
    Arguments:
        content {Array} -- An Array with some content in ASCII for transforming into Hex Array
    
    Returns:
        Array -- The content ASCII Array transformed into an Hex Array
    """
    Logger.printMessage(message='{methodName}'.format(methodName='AsciiToHex'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [hex(n)[2:] for n in content]

def hexToBase64(content):
    """Transform Hex Array to Base64 Array
    
    Arguments:
        content {Array} -- An Array with some content in Hex for transforming into Base64 Array
    
    Returns:
        Array -- The content transformed into an Base64 Array
    """
    Logger.printMessage(message='{methodName}'.format(methodName='HexToBase64'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [base64.b64encode(n.encode()) for n in content]

def joinBase64(content):
    """Transform Base64 Array to String
    
    Arguments:
        content {Array} -- An Array with some content in Base64 for transforming into a String
    
    Returns:
        String -- The content Base64 Array joined and transformed from Base64 decoded and encoded to String
    """
    Logger.printMessage(message='{methodName}'.format(methodName='joinBase64'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return (''.join([content[i].decode('utf-8') for i in range(0, len(content))])).encode()

def asciiToBase64(content):
    """Transform ASCII String to Base64 Array
    
    Arguments:
        content {String} -- A String with some content in ASCII for transforming into a Base64 Array
    
    Returns:
        Array -- The content in ASCII String transformed into a Base64 Array
    """
    Logger.printMessage(message='{methodName}'.format(methodName='asciiToBase64'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [content[i:i+4] for i in range(0, len(content), 4)]

def base64ToHex(content):
    """Transform Base64 Array to Hex Array
    
    Arguments:
        content {Array} -- The content in a Base64 Array to transform into an Hex Array
    
    Returns:
        Array -- The content in Base64 Array transformed into an Hex Array
    """
    Logger.printMessage(message='{methodName}'.format(methodName='base64ToHex'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [base64.b64decode(b64) for b64 in content]

def hexToDecimal(content):
    """Transform Hex Array to Decimal Array
    
    Arguments:
        content {Array} -- The content in an Hex Array to transform to a Decimal Array
    
    Returns:
        Array -- The content in an Hex Array transformed into a Decimal Array
    """
    Logger.printMessage(message='{methodName}'.format(methodName='hexToDecimal'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [int(hexa.decode("UTF-8"), 16) for hexa in content]

def decimalToAscii(content):
    """Transform Decimal Array to ASCII String
    
    Arguments:
        content {Array} -- The content in a Decimal Array to transform to an ASCII String
    
    Returns:
        String -- The content in a Decimal Array transformed to an ASCII String
    """
    Logger.printMessage(message='{methodName}'.format(methodName='decimalToAscii'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return ''.join([chr(dec) for dec in content])

def randomText(length=8, alphabet='lalpha'):
    try:
        return ''.join(random.SystemRandom().choice(config_utils[alphabet]) for _ in range(int(length)))
    except Exception as e:
        Logger.printMessage(message=randomText, description=e, is_error=True)

def getCombinationPosibilitiesLength(alphabet, length):
    return [''.join(x) for x in product(config_utils[alphabet], repeat=int(length))]

def fromWhatDictListIsChar(char='a'):
    dictionaryOptions = Config.getConfig(parentKey='modules', key='ht_bruteforce', subkey='dictionaryOptions')
    for opt in dictionaryOptions:
        if char in config_utils[opt]:
            return opt
    return 'lalpha'

def getCombinationPosibilitiesByPattern(try_pattern=None):
    try:
        alphabets_patter = []
        create_pattern = []
        for char in try_pattern:
            char_alphabet = fromWhatDictListIsChar(char=char)

            if len(alphabets_patter) == 0 or not char_alphabet in alphabets_patter or not alphabets_patter[-1] == char_alphabet:
                alphabets_patter.append(char_alphabet)
                create_pattern.append(1)
            else:
                create_pattern[-1] += 1

        final_combinations = []

        for i_alp, alp in enumerate(alphabets_patter):
            if i_alp == 0:
                final_combinations = getCombinationPosibilitiesLength(alphabet=alp, length=create_pattern[i_alp])
            else:
                final_combinations = [r[0] + r[1] for r in itertools.product(final_combinations, getCombinationPosibilitiesLength(alphabet=alp, length=create_pattern[i_alp]))]

        return final_combinations
    except MemoryError:
        Logger.printMessage(message='Memory Error', description='There are so many combinations for this pattern', is_error=True)

def getDict(length=8, maxvalue=10000, alphabet='lalpha', try_pattern=None):
    if try_pattern and not try_pattern == '':
        return getCombinationPosibilitiesByPattern(try_pattern=try_pattern)
    else:
        res = getCombinationPosibilitiesLength(alphabet=alphabet, length=length)
        Logger.printMessage(message='getDict', description='{data} - {count}'.format(data=res[:10], count=len(res)), debug_core=True)
        return res
