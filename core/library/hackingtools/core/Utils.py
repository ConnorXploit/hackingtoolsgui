from . import Config, Logger

def amIdjango(fileCall):
    # Used by core on init for initialaizing Django Functions if needed
    return True if 'core.library.hackingtools' == fileCall else False

if amIdjango(__name__):
    from core.library import hackingtools as ht
    from core.library.hackingtools.core.Objects import Worker as __Worker
else:
    import hackingtools as ht
    from hackingtools.core.Objects import Worker as __Worker
__config__ = Config.getConfig(parentKey='core', key='Utils')
__config_logger__ = Config.getConfig(parentKey='core', key='Logger')
__config_utils__ = Config.getConfig(parentKey='core', key='Utils', subkey='dictionaries')

__function_param_exclude__ = Config.getConfig(parentKey='core', key='import_modules', subkey='__function_param_exclude__')
__default_class_name_for_all__ = Config.getConfig(parentKey='core', key='import_modules', subkey='__default_class_name_for_all__')  

import random as __random
import requests as __requests
import base64 as __base64
import os as __os
import ast
import inspect
import json as __json
import shutil
from threading import Thread
from threading import Lock
from itertools import product
from functools import reduce
from datetime import datetime
import platform as __platform
try:
    import git
except:
    pass
import re
from pathlib import Path

global threads
threads = {}

__path = __os.path.abspath(__os.path.split(__os.path.dirname(__file__))[0])

def getWorkers():
    global threads
    return threads

def startWorker(workerName, functionCall, args=(), timesleep=1, loop=True, run_until_ht_stops=False, log=False, timeout=None):
    t = None
    try:
        w = __Worker()
        if log:
            Logger.printMessage('Starting Worker: {w}'.format(w=workerName))
        t = Thread(target=w.run, args=(functionCall, args, int(timesleep), loop, timeout ), daemon=run_until_ht_stops)
        if loop:
            threads[workerName] = [ w, t ]
        t.start()
    except Exception as e:
        Logger.printMessage(str(e), is_error=True)

def killAllWorkers():
    global threads
    for t in threads:
        threads[t][0].terminate()
        threads[t][1].join()

def stopWorker(workerName):
    global threads
    if workerName in threads:
        try:
            threads[workerName][0].terminate()
            threads[workerName][1].join()
        except Exception as e:
            Logger.printMessage(str(e), is_error=True)
        del threads[workerName]

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
        #Logger.printMessage(message='emptyDirectory', description='Would empty: {path}'.format(path=directory), is_warn=True)
        #if __os.path.isdir(directory):
        #    shutil.rmtree(directory)
        #    return True
        # ! Temporary ommited
        return False
    except:
        return False

def readFileAsString(filepath):
    data = ''
    try:
        f = open(filepath, 'r', encoding='utf8')
        data = f.read()
    except Exception as e:
        pass
    return data

# Data Manipulation
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
    return 'ht.modules.{category}.{modDir}.{module}.{callClass}().{function}'.format(category=category, modDir=moduleName.replace('ht_', ''), module=moduleName, callClass=__default_class_name_for_all__, function=functionName)

def getAnyFunctionParams(functionObjectStr, i_want_list=False):
    try:
        params_func = inspect.getfullargspec(eval(functionObjectStr))[0]
        params_func = [param for param in params_func if not param in __function_param_exclude__] if params_func else []

        args, _, __, defaults = inspect.getargspec(eval(functionObjectStr))
        args = [param for param in args if not param in __function_param_exclude__] if args else []

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
    except:
        pass
        #Logger.printMessage('{functionObjectStr} is not a function'.format(functionObjectStr=functionObjectStr), 'Be sure you have all your module class variables outsite the class, in the file ({functionObjectStr}.py) before the \'class StartModule:\' statement'.format(functionObjectStr='.'.join(functionObjectStr.split('.')[0:5])), is_error=True)
    return []

def getFunctionsParams(category, moduleName, functionName, i_want_list=False):
    function = getFunctionFullCall(moduleName=moduleName, category=category, functionName=functionName)
    return getAnyFunctionParams(function, i_want_list)

def getValueType(value, getResponse=False, returnLiteralType=False):
    try:
        if isinstance(value, bool) and ( str(value) == 'False' or str(value) == 'True'):
            if returnLiteralType:
                return bool
            return 'checkbox'
    except:
        pass
    try:
        if isinstance(value, int) and int(value):
            if returnLiteralType:
                return int
            return 'number'
    except:
        pass
    try:
        if isinstance(value, dict) or isinstance(eval(value), dict):
            if returnLiteralType:
                return dict
            return 'data'
    except:
        pass
    try:
        if isinstance(value, datetime) or isinstance(eval(value), datetime) or datetime.strptime(value, '%Y-%m-%d %H:%M:%S') or isinstance(value, datetime):
            if returnLiteralType:
                return datetime
            return 'time'
    except:
        pass
    try:
        if (isinstance(value, list) or isinstance(eval(value), list)) and (str(value)[0] == '[' and str(value)[-1] == ']'):
            if returnLiteralType:
                return list
            return 'select'
    except:
        pass
    if returnLiteralType:
        return str
    try:
        if isinstance(value, str) or isinstance(eval(value), str):
            if returnLiteralType:
                return str
    except:
        pass
    if not getResponse:
        try:
            if isinstance(value, str) or isinstance(eval(value), str):
                if '.' in value and len(value.split('.')[1] in range(1,4)):
                    return 'file'
        except:
            pass
        try:
            if isinstance(value, str) or isinstance(eval(value), str):
                if 'path' in value or 'file' in value:
                    return 'file'
        except:
            pass
        try:
            if isinstance(value, str) or isinstance(eval(value), str):
                if 'pass' in value or 'password' in value:
                    return 'password'
        except:
            pass
    try:
        if isinstance(value, str) or isinstance(eval(value), str):
            if 'http' in value and ('.jpg' in value or '.png' in value or '.ico' in value or '.gif' in value or ('image' in value and '.php' in value)):
                return 'image'
    except:
        pass
    try:
        if isinstance(value, str) or isinstance(eval(value), str):
            if value.startswith('http://') or value.startswith('https://'):
                return 'url'
    except:
        pass
    try:
        if isinstance(value, str) or isinstance(eval(value), str):
            if len(value) > 100:
                return 'textarea'
    except:
        pass
    return 'text'

def doesFunctionContainsExplicitReturn(functionCall):
    try:
        return True if 'return' in inspect.getsource(eval(functionCall)) else False
    except:
        return False

def downloadProjectAsModuleFromGithub(moduleName, category, githubURL):
    try:
        ht.__createModule__(moduleName, category)
        moduleDir = __os.path.join( __path, 'modules', category, moduleName.replace('ht_', '') )
        if __os.path.isdir( moduleDir ):
            # Name for the new module-git
            name_git_folder = githubURL.split('/')[-1].replace('.git', '')
            # Get the dir path
            actual_git_folder = __os.path.join( moduleDir, name_git_folder )
            # Remove if exists
            if __os.path.isdir( actual_git_folder ):
                __os.remove( actual_git_folder )
            # Git clone
            git.Git( moduleDir ).clone( githubURL )
            # Create new name
            new_git_folder = __os.path.join( moduleDir, '_'.join( [ moduleName, 'git' ] ) )
            # Rename the folder
            if __os.path.isdir( new_git_folder ):
                __os.remove( new_git_folder )
                
            __os.rename( actual_git_folder, new_git_folder )
            # Get all files in directory
            entries = __os.listdir(new_git_folder)
            for ent in entries:
                # Check files for remove not interesting ones
                if ent.endswith('.md') or ent.endswith('.jpg') or ent.endswith('.png') or ent.endswith('.txt'):
                    __os.remove( __os.path.join( new_git_folder, ent ) )

            # Search for setup.py if there is
            entries = __os.listdir(new_git_folder)
            for filen in entries:
                file_to_read = __os.path.join( new_git_folder, filen )
                setup_content = readFileAsString( file_to_read )
                commands = []
                find_for = [ '--' ]
                for finding in find_for:
                    if finding in setup_content:
                        for ind in findIndexAllOccurrencesSubstring(finding, str( setup_content )):
                            interesting_line = str(setup_content)[ind:].split('\n')[0]
                            for appearances in interesting_line.split( finding ):
                                comm = ''.join( [ finding, appearances.split('\'')[0] ] ).split(' ')[0]
                                if not comm in commands and not comm == finding:
                                    commands.append( comm )
                if commands:
                    print('Found commands:', commands)
                else:
                    print('Not commands')
        else:
            Logger.printMessage('Not exists', description=moduleDir, is_error=True)
            ht.__removeModule__(moduleName, category)
    except Exception as e:
        raise
        Logger.printMessage(str(e), is_error=True)
        ht.__removeModule__(moduleName, category)

# Others
def getTime():
    return datetime.utcnow().strftime(__config_logger__['log_print_date_format'])[:-3]

def getLocationGPS():
    ip_request = __requests.get('https://get.geojs.io/v1/ip.json')
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + ip_request.json()['ip'] + '.json'
    geo_request = __requests.get(geo_request_url)
    geo_data = geo_request.json()
    return geo_data

def getIPLocationGPS(ip, api):
    url = 'http://api.ipinfodb.com/v3/ip-city/?key={api}&ip={ip}'.format(api=api, ip=ip)
    res = __requests.get(url).content.decode()
    if len(res.split(';')) > 8:
        return {'ip' : ip, 'location' : [ res.split(';')[9], res.split(';')[8] ] }
    else:
        return {'ip' : ip, 'location' : [0, 0] }

def getIPLocationGPS_v2(ip):
    try:
        url = 'https://api.ipgeolocationapi.com/geolocate/{ip}'.format(ip=ip)
        res = __json.loads(__requests.get(url).content.decode())
        if res['geo']:
            return {'ip' : ip, 'location' : [ res['geo']['longitude'], res['geo']['latitude'] ], 'country' : res['alpha2'].lower() }
        else:
            return {'ip' : ip, 'location' : [0, 0], 'country' : 'us' }
    except:
        return {'ip' : ip, 'location' : [0, 0], 'country' : 'us' }

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
def findIndexAllOccurrencesSubstring(substring, content):
    return [m.start() for m in re.finditer( substring, str(content) )]

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
    return [__base64.b64encode(n.encode()) for n in content]

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
    return [__base64.b64decode(b64) for b64 in content]

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

def randomText(length=8, alphabet='lalpha', try_pattern=None, pattern_force_chars=None):
    try:
        if try_pattern:
            alphabets_patter = []
            for char in try_pattern:
                char_alphabet = fromWhatDictListIsChar(char=char)

                if char_alphabet and pattern_force_chars and not char in pattern_force_chars:
                    alphabets_patter.append(char_alphabet)
                else:
                    alphabets_patter.append(char)
                    
            return ''.join([ getRandomCharFromDict(alphabet=alp) if getRandomCharFromDict(alphabet=alp) else alp for alp in alphabets_patter ])

        return ''.join(__random.SystemRandom().choice(__config_utils__[alphabet]) for _ in range(int(length)))

    except Exception as e:
        Logger.printMessage(message=randomText, description=e, is_error=True)

def getRandomCharFromDict(alphabet='lalpha'):
    dictionaryOptions = Config.getConfig(parentKey='core', key='Utils', subkey='dictionaries')
    if alphabet in dictionaryOptions:
        return __random.choice(dictionaryOptions[alphabet])
    return None

def fromWhatDictListIsChar(char='a'):
    dictionaryOptions = Config.getConfig(parentKey='modules', key='ht_bruteforce', subkey='dictionaryOptions')
    for opt in dictionaryOptions:
        if char in __config_utils__[opt]:
            return opt
    return None

def getCombinationPosibilitiesLength(alphabet, length, generator=False):
    if generator:
        for x in product(__config_utils__[alphabet], repeat=int(length)):
            yield ''.join(x)
    else:
        return [ ''.join(x) for x in product(__config_utils__[alphabet], repeat=int(length)) ]

def getCombinationPosibilitiesByPattern(try_pattern=None, generator=False):
    try:
        alphabets_patter = []
        create_pattern = []
        for char in try_pattern:
            char_alphabet = fromWhatDictListIsChar(char=char)
            if char_alphabet:
                if len(alphabets_patter) == 0 or not char_alphabet in alphabets_patter or not alphabets_patter[-1] == char_alphabet:
                    alphabets_patter.append(char_alphabet)
                    create_pattern.append(1)
                else:
                    create_pattern[-1] += 1
            else:
                alphabets_patter.append(char)

        final_combinations = []
        for i_alp, alp in enumerate(alphabets_patter):
            if i_alp == 0:
                for comb in getCombinationPosibilitiesLength(alphabet=alp, length=create_pattern[i_alp], generator=generator):
                    final_combinations.append(comb)
            else:
                temp_final_combinations = final_combinations
                final_combinations = []
                for combb in getCombinationPosibilitiesLength(alphabet=alp, length=create_pattern[i_alp], generator=generator):
                    for comb in [r[0] + r[1] for r in product(temp_final_combinations, combb)]:
                        final_combinations.append(comb)

        if generator:
            for f in final_combinations:
                yield f
        else:
            return final_combinations

    except MemoryError:
        Logger.printMessage(message='Memory Error', description='There are so many combinations for this pattern', is_error=True)
    return []

def getDict(length=8, alphabet='lalpha', try_pattern=None, generator=False):
    if try_pattern and not try_pattern == '':
        if generator:
            for comb in getCombinationPosibilitiesByPattern(try_pattern=try_pattern, generator=generator):
                yield comb
        else:
            return getCombinationPosibilitiesByPattern(try_pattern=try_pattern, generator=generator)
    else:
        if generator:
            for comb in getCombinationPosibilitiesLength(alphabet=alphabet, length=length, generator=generator):
                yield comb
        else:
            return getCombinationPosibilitiesLength(alphabet=alphabet, length=length, generator=generator)

def getPosibleAlphabet():
    return list(__config_utils__.keys())

def get_from_dict(data_dict, map_list, default=None):
    def getitem(source, key):
        try:
            if isinstance(source, list):
                return source[int(key)]
            if isinstance(source, dict) and key not in source.keys():
                return default
            if not source:
                return default
        except IndexError:
            return default

        return source[key]

    if isinstance(map_list, str):
        map_list = map_list.split('.')

    return reduce(getitem, map_list, data_dict)

def groupListByLength(dataList, length):
    return [ dataList[i:i+length] for i in range(0, len(dataList), length) ]