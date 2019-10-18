from . import Config, Logger, Utils
config = Config.getConfig(parentKey='core', key='Connections')
import sys, requests, socket

# Connections Treatment
global services
services = []

global listening_port
listening_port = '8000'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# Main functions
def getMyServices():
    global services
    return [serv for serv in services if serv]

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

def getMyPublicIP():
    try:
        return Logger.print_and_return(msg='getMyPublicIP', value=requests.get('https://api.ipify.org').text, debug_core=True)
    except:
        return Logger.print_and_return(msg='getMyPublicIP', value='127.0.0.1', debug_core=True)

def getMyLanIP():
    for ip in socket.gethostbyname_ex(socket.gethostname())[-1]:
        if '192.168.1' in ip or '192.168.0' in ip:
            return Logger.print_and_return(msg='getMyLanIP', value=ip, debug_core=True)

def getMyLocalIP():
    return Logger.print_and_return(msg='getMyLocalIP', value='127.0.0.1', debug_core=True)

def __initServices__():
    global services

    https = '' # Anytime when adding ssl, shold be with an 's'

    loadActualPort()

    if 'ngrok' in config and config['ngrok'] and '__load_on_boot__' in config['ngrok'] and config['ngrok']['__load_on_boot__'] == True:
        startNgrok(getActualPort())

    # for service in (getMyPublicIP(), getMyLanIP(), getMyLocalIP()):
    #     services.append('http{s}://{ip}:{port}'.format(s=https, ip=service, port=getActualPort()))

    for service in (getMyLanIP(), getMyLocalIP()):
        services.append('http{s}://{ip}:{port}'.format(s=https, ip=service, port=getActualPort()))

    Logger.printMessage(message='Loaded services', description=services, color=Logger.Fore.YELLOW, debug_core=True)

# Ngrok connections
global ngrok_ip
ngrok_ip = None

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
__initServices__()