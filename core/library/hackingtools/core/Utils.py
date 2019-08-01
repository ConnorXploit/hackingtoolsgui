from . import Config, Logger
config = Config.getConfig(parentKey='core', key='Utils')

import random
import base64
import os

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

def emptyDirectory(dir):
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
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            return True
        return False
    except:
        return False

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

def isPrime(number):
    """Tests to see if a number is prime.
    
    Arguments:
        number {integer} -- The number to test if is a prime number
    
    Returns:
        boolean -- If is prime True, else False
    """
    Logger.printMessage(message='{methodName}'.format(methodName='isPrime'), description='{n}'.format(n=number), debug_core=True)
    excepted = (0, 2, 4, 5, 6, 8)
    if not int(str(number)[-1]) in excepted:
        division = 0
        try:
            half = number/2
            if not isinstance(half, float):
                return False
        except:
            return False
        fibo_1 = 0
        fibo_2 = 1
        fibo_temp = fibo_1 + fibo_2
        while fibo_temp < int(number/2):
            if number % fibo_temp == 0:
                division += 1
            fibo_1 = fibo_2
            fibo_2 = fibo_temp
            fibo_temp = fibo_1 + fibo_2
            if division == 2:
                return False
        if division == 1:
            return True

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
            n=random.randint(10**(length-1), 10**length)
            if isPrime(n):
                return n
    except:
        return -1

# Text Treatment
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


