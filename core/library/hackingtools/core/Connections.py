from . import Config, Logger, Utils, Pool
config = Config.getConfig(parentKey='core', key='Connections')
import sys, requests, socket, os

# Connections Treatment
global services
services = []

global listening_port
listening_port = '8000'

global https
https = ''

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# Ngrok connections
global ngrok_ip
ngrok_ip = None

# Main functions
def getMyServices():
    global services
    return [serv for serv in services if serv]

def addMineService(serv):
    global services
    Logger.printMessage('Adding service', serv, debug_core=True)
    if not serv in services:
        services.append(serv)

def serviceNotMine(service):
    for serv in services:
        if service == serv:
            return False
    return True

def loadActualPort():
    global listening_port
    try:
        listening_port = Logger.print_and_return(msg='loadActualPort', value=sys.argv[-1].split(':')[1], debug_core=True)
    except:
        listening_port = Logger.print_and_return(msg='loadActualPort', value='8000', debug_core=True)

def getActualPort():
    global listening_port
    return listening_port

def getMyPublicIP(as_service=False):
    global listening_port
    global https
    try:
        if as_service:
            return Logger.print_and_return(msg='getMyPublicIP', value='http{s}://{i}:{p}'.format(s=https, i=requests.get('https://api.ipify.org').text, p=listening_port), debug_core=True)
        return Logger.print_and_return(msg='getMyPublicIP', value=requests.get('https://api.ipify.org').text, debug_core=True)
    except:
        if as_service:
            return Logger.print_and_return(msg='getMyPublicIP', value='http{s}://127.0.0.1:{p}'.format(s=https, p=listening_port), debug_core=True)
        return Logger.print_and_return(msg='getMyPublicIP', value='127.0.0.1', debug_core=True)

def getMyLanIP(as_service=False):
    global listening_port
    global https
    for ip in socket.gethostbyname_ex(socket.gethostname())[-1]:
        if '192.168.1' in ip or '192.168.0' in ip:
            if as_service:
                return Logger.print_and_return(msg='getMyLanIP', value='http{s}://{i}:{p}'.format(s=https, i=ip, p=listening_port), debug_core=True)
            return Logger.print_and_return(msg='getMyLanIP', value=ip, debug_core=True)

def getMyLocalIP(as_service=False, port=True):
    global services
    global listening_port
    global https
    if isHeroku():
        if not services:
            Pool.__checkPoolNodes__()
            Config.__readConfig__()
            services += Config.getConfig(parentKey='core', key='Connections', subkey='my_services')
        if as_service:
            if port:
                return Logger.print_and_return(msg='getMyLocalIP', value='http{s}://{ss}:{p}'.format(s=https, ss=services[0], p=listening_port), debug_core=True)
            return Logger.print_and_return(msg='getMyLocalIP', value=services[0], debug_core=True)
        return Logger.print_and_return(msg='getMyLocalIP', value=services[0], debug_core=True)
    if as_service:
        if port:
            return Logger.print_and_return(msg='getMyLocalIP', value='http{s}://127.0.0.1:{p}'.format(s=https, p=listening_port), debug_core=True)
        return Logger.print_and_return(msg='getMyLocalIP', value='http{s}://127.0.0.1'.format(s=https), debug_core=True)
    return Logger.print_and_return(msg='getMyLocalIP', value='127.0.0.1', debug_core=True)

def isHeroku():
    if 'DYNO' in os.environ: # Automatically Heroku Deploy
        return True
    return False

def __initServices__():
    if not isHeroku():
        global services
        global https

        loadActualPort()

        if 'ngrok' in config and config['ngrok'] and '__load_on_boot__' in config['ngrok'] and config['ngrok']['__load_on_boot__'] == True:
            startNgrok(getActualPort())

        # for service in (getMyPublicIP(), getMyLanIP(), getMyLocalIP()):
        #     services.append('http{s}://{ip}:{port}'.format(s=https, ip=service, port=getActualPort()))

        global ngrok_ip
        if ngrok_ip:
            services = [ngrok_ip]
        else:
            [services.append(service) for service in (getMyLanIP(as_service=True), getMyLocalIP(as_service=True))]
    else:
        Pool.__checkPoolNodes__()
        Config.__readConfig__()
        services += Config.getConfig(parentKey='core', key='Connections', subkey='my_services')
    Logger.printMessage(message='Loaded services', description=services, color=Logger.Fore.YELLOW, debug_core=True)

def getNgrokServiceUrl():
    global ngrok_ip
    return ngrok_ip

def startNgrok(port=listening_port):
    try:
        from pyngrok import ngrok 
        global ngrok_ip
        ngrok_ip = ngrok.connect(int(port))
        if ngrok_ip:
            services.append(ngrok_ip)
            return Logger.print_and_return(msg='ngrok', value=ngrok_ip)
    except Exception as e:
        Logger.printMessage(message='Couldn\'t start ngrok service', description=str(e), is_error=True)
        return None

def stopNgrok(ngrokServiceUrl):
    try:
        from pyngrok import ngrok 
        global ngrok_ip
        ngrok.disconnect(ngrokServiceUrl)
        services.remove(ngrokServiceUrl)
        return True
    except Exception as e:
        Logger.printMessage(message='Couldn\'t stop ngrok service', description=str(e), is_error=True)
        return False

# Init
if not isHeroku():
    __initServices__()