from . import Config, Logger, Utils, Pool

config = Config.getConfig(parentKey='core', key='Connections')
import sys, requests, socket, os

# Connections Treatment
global __services__
__services__ = []

global __listening_port__
__listening_port__ = '8000'

global __https__
__https__ = ''

__headers__ = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

__tor_proxies__ = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

# Ngrok connections
global __ngrok_ip__
__ngrok_ip__ = None

# Main functions
def getMyServices():
    global __services__
    return [serv for serv in __services__ if serv]

def addMineService(serv):
    global __services__
    Logger.printMessage('Adding service', serv, debug_core=True)
    if not serv in __services__:
        __services__.append(serv)

def getActualPort():
    global __listening_port__
    return __listening_port__

def getMyPublicIP(as_service=False):
    global __listening_port__
    global __https__
    try:
        if as_service:
            return Logger.print_and_return(msg='getMyPublicIP', value='http{s}://{i}:{p}'.format(s=__https__,
                                                                                                 i=requests.get(
                                                                                                     '__https__://api.ipify.org').text,
                                                                                                 p=__listening_port__),
                                           debug_core=True)
        return Logger.print_and_return(msg='getMyPublicIP', value=requests.get('__https__://api.ipify.org').text,
                                       debug_core=True)
    except:
        if as_service:
            return Logger.print_and_return(msg='getMyPublicIP',
                                           value='http{s}://127.0.0.1:{p}'.format(s=__https__, p=__listening_port__),
                                           debug_core=True)
        return Logger.print_and_return(msg='getMyPublicIP', value='127.0.0.1', debug_core=True)

def getMyLanIP(as_service=False):
    global __listening_port__
    global __https__
    for ip in socket.gethostbyname_ex(socket.gethostname())[-1]:
        if '192.168.1' in ip or '192.168.0' in ip:
            if as_service:
                return Logger.print_and_return(msg='getMyLanIP', value='http{s}://{i}:{p}'.format(s=__https__, i=ip,
                                                                                                  p=__listening_port__),
                                               debug_core=True)
            return Logger.print_and_return(msg='getMyLanIP', value=ip, debug_core=True)

def getMyLocalIP(as_service=False, port=True):
    global __services__
    global __listening_port__
    global __https__
    if isHeroku():
        if not __services__:
            Pool.__checkPoolNodes__()
            Config.__readConfig__()
            __services__ += Config.getConfig(parentKey='core', key='Connections', subkey='my___services__')
        if as_service:
            if port:
                return Logger.print_and_return(msg='getMyLocalIP',
                                               value='http{s}://{ss}:{p}'.format(s=__https__, ss=__services__[0],
                                                                                 p=__listening_port__), debug_core=True)
            return Logger.print_and_return(msg='getMyLocalIP', value=__services__[0], debug_core=True)
        return Logger.print_and_return(msg='getMyLocalIP', value=__services__[0], debug_core=True)
    if as_service:
        if port:
            return Logger.print_and_return(msg='getMyLocalIP',
                                           value='http{s}://127.0.0.1:{p}'.format(s=__https__, p=__listening_port__),
                                           debug_core=True)
        return Logger.print_and_return(msg='getMyLocalIP', value='http{s}://127.0.0.1'.format(s=__https__),
                                       debug_core=True)
    return Logger.print_and_return(msg='getMyLocalIP', value='127.0.0.1', debug_core=True)

def isHeroku():
    if 'DYNO' in os.environ:  # Automatically Heroku Deploy
        return True
    return False

def getNgrokServiceUrl():
    global __ngrok_ip__
    return __ngrok_ip__

def startNgrok(port=__listening_port__):
    try:
        from pyngrok import ngrok
        global __ngrok_ip__
        __ngrok_ip__ = ngrok.connect(int(port))
        if __ngrok_ip__:
            __services__.append(__ngrok_ip__)
            return Logger.print_and_return(msg='ngrok', value=__ngrok_ip__)
    except Exception as e:
        Logger.printMessage(message='Couldn\'t start ngrok service', description=str(e), is_error=True)
        return None

def stopNgrok(ngrokServiceUrl):
    try:
        from pyngrok import ngrok
        global __ngrok_ip__
        ngrok.disconnect(ngrokServiceUrl)
        __services__.remove(ngrokServiceUrl)
        return True
    except Exception as e:
        Logger.printMessage(message='Couldn\'t stop ngrok service', description=str(e), is_error=True)
        return False

def requestByTor(url):
    try:
        return requests.get(url, proxies=__tor_proxies__).text.strip()
    except Exception as e:
        Logger.printMessage( str(e), is_error=True)
        return None

def __serviceNotMine__(service):
    for serv in __services__:
        if service == serv:
            return False
    return True

def __loadActualPort__():
    global __listening_port__
    try:
        __listening_port__ = Logger.print_and_return(msg='__loadActualPort__', value=sys.argv[-1].split(':')[1],
                                                     debug_core=True)
    except:
        __listening_port__ = Logger.print_and_return(msg='__loadActualPort__', value='8000', debug_core=True)

def __initServices__():
    if not isHeroku():
        global __services__
        global __https__

        __loadActualPort__()

        if 'ngrok' in config and config['ngrok'] and '__load_on_boot__' in config['ngrok'] and config['ngrok'][
            '__load_on_boot__'] == True:
            startNgrok(getActualPort())

        # for service in (getMyPublicIP(), getMyLanIP(), getMyLocalIP()):
        #     __services__.append('http{s}://{ip}:{port}'.format(s=__https__, ip=service, port=getActualPort()))

        global __ngrok_ip__
        if __ngrok_ip__:
            __services__ = [__ngrok_ip__]
        else:
            [__services__.append(service) for service in (getMyLanIP(as_service=True), getMyLocalIP(as_service=True))]
    else:
        Pool.__checkPoolNodes__()
        Config.__readConfig__()
        __services__ += Config.getConfig(parentKey='core', key='Connections', subkey='my___services__')
    Logger.printMessage(message='Loaded __services__', description=__services__, color=Logger.__Fore.YELLOW,
                        debug_core=True)

# Init
if not isHeroku():
    __initServices__()
