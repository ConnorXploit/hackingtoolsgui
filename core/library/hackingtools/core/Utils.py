from . import Config, Logger
config = Config.getConfig(parentKey='core', key='Utils')

import random
import base64

# File Manipulation
def getFileContentInByteArray(filePath):
    """Function that returns a ByteArray with the data from a file

    Parameters
    ----------
        filePath = String

    Return
    ----------
        ByteArray/None
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

    Parameters
    ----------
        content = ByteArray
        fileName = String

    Return
    ----------
        boolean (True/False)
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

# Maths
def euclides(a, b):
    '''Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers

    Parameters
    ----------
        a = int
        b = int

    Return
    ----------
        int
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='euclides'), description='{a} - {b}'.format(a=a, b=b), debug_core=True)
    while b != 0:
        a, b = b, a % b
    return a

def multiplicativeInverse(e, phi):
    '''Euclid's extended algorithm for finding the multiplicative inverse of two numbers

    Parameters
    ----------
        e = int
        phi = int

    Return
    ----------
        int
    '''
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
    '''Tests to see if a number is prime.

    Parameters
    ----------
        e = int
        phi = int

    Return
    ----------
        boolean (True/False)
    '''
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
    '''Returns a random prime number with the length you choose

    Parameters
    ----------
        length = int

    Return
    ----------
        int (-1 if error)
    '''
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
    '''Transform text in String to ASCII Array

    Parameters
    ----------
        content = String

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='textToAscii'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [ord(pal) for pal in content]

def asciiToHex(content):
    '''Transform ASCII Array to Hex Array

    Parameters
    ----------
        content = Array

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='AsciiToHex'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [hex(n)[2:] for n in content]

def hexToBase64(content):
    '''Transform Hex Array to Base64 Array

    Parameters
    ----------
        content = Array

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='HexToBase64'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [base64.b64encode(n.encode()) for n in content]

def joinBase64(content):
    '''Transform Base64 Array to String

    Parameters
    ----------
        content = Array

    Return
    ----------
        String
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='joinBase64'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return (''.join([content[i].decode('utf-8') for i in range(0, len(content))])).encode()

def asciiToBase64(content):
    '''Transform ASCII String to Base64 Array

    Parameters
    ----------
        content = String

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='asciiToBase64'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [content[i:i+4] for i in range(0, len(content), 4)]

def base64ToHex(content):
    '''Transform Base64 Array to Hex Array

    Parameters
    ----------
        content = Array

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='base64ToHex'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [base64.b64decode(b64) for b64 in content]

def hexToDecimal(content):
    '''Transform Hex Array to Decimal Array

    Parameters
    ----------
        content = Array

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='hexToDecimal'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return [int(hexa.decode("UTF-8"), 16) for hexa in content]

def decimalToAscii(content):
    '''Transform Decimal Array to ASCII String

    Parameters
    ----------
        content = Array

    Return
    ----------
        Array
    '''
    Logger.printMessage(message='{methodName}'.format(methodName='decimalToAscii'), description='Length: {length} - {content} ...'.format(length=len(content), content=content[0:10]), debug_core=True)
    return ''.join([chr(dec) for dec in content])


