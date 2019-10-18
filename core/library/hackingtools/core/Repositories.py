from . import Config, Logger, Utils
import requests, json, shutil, os

if Utils.amIdjango(__name__):
    from core.library import hackingtools as ht
else:
    import hackingtools as ht

config = Config.getConfig(parentKey='core', key='Repositories')

path = os.path.abspath(os.path.split(os.path.dirname(__file__))[0])

servers = config['servers']

def installModule(server, moduleName):
    req = requests.post('http://{ip}/category/{m}'.format(ip=server, m=moduleName))

    if req.json()['status'] == 'OK':
        category = req.json()['data']

        # Installing main files for the module

        req = requests.get('http://{ip}/module/download/files/{m}'.format(ip=server, m=moduleName), stream=True, data={'module_name' : moduleName}, headers={'Accept-Encoding' : '*/*', 'Content-Type' : 'application/zip'})

        category_folder = os.path.join(path, 'modules', category)
        if not os.path.isdir(category_folder):
            os.mkdir(category_folder)

        new_file = os.path.join(category_folder, '{m}.zip'.format(m=moduleName))
        open(new_file, 'wb').write(req.content)

        unzipper = ht.getModule('ht_unzip')
        unzipper.extractFile(new_file)

        os.remove(new_file)

        # Installing the json config
        req = requests.get('http://{ip}/module/download/config/{m}'.format(ip=server, m=moduleName), stream=True, data={'module_name' : moduleName}, headers={'Accept-Encoding' : '*/*', 'Content-Type' : 'application/json'})
        
        config_django_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config_modules_django', category))
        if not os.path.isdir(config_django_module_path):
            os.mkdir(config_django_module_path)
        
        open(os.path.join(config_django_module_path, 'ht_{m}.json'.format(m=moduleName.replace('ht_',''))), 'wb').write(req.content)


def updateModule(server, moduleName):
    removeModule(server, moduleName)
    installModule(server, moduleName)

def removeModule(server, moduleName):
    moduleName = moduleName.replace('ht_', '')
    req = requests.post('http://{ip}/category/{m}'.format(ip=server, m=moduleName))

    if req.json()['status'] == 'OK':
        category = req.json()['data']

        category_folder = os.path.join(path, 'modules', category)
        if os.path.isdir(category_folder):
            module_folder = os.path.join(category_folder, moduleName)
            if os.path.isdir(module_folder):
                shutil.rmtree(module_folder)

def uploadModule(server, category, moduleName):
    module_folder = os.path.join(path, 'modules', category, moduleName.replace('ht_', ''))
    unzipper = ht.getModule('ht_unzip')
    zipped_file = unzipper.zipDirectory(module_folder)
    req = requests.post('http://{ip}/new/module/upload/{c}'.format(ip=server, c=category), files={ "module" : (str(os.path.split(zipped_file)[1]), zipped_file)})
    if req.json()['status'] == 'OK':
        Logger.printMessage(req.json()['data'])
    Logger.printMessage(req.json()['data'], is_error=True)

def addServer(server):
    if not server in servers:
        servers.append(server)

def getOnlineServers():
    alive_servers = []
    for serv in servers:
        try:
            r = requests.post('http://{ip}/'.format(ip=serv))
            if r.ok and r.json()['status'] == 'OK':
                alive_servers.append(serv)
        except Exception as e:
            Logger.printMessage(str(e), is_error=True)
    return alive_servers
    
def getChanges(server):
    try:
        r = requests.post('http://{ip}/changes/'.format(ip=server))
        if r.ok and r.json()['status'] == 'OK':
            return r.json()['data']
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def getCategories(server):
    try:
        r = requests.post('http://{ip}/categories/'.format(ip=server))
        if r.ok and r.json()['status'] == 'OK':
            return r.json()['data']
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def getModules(server):
    try:
        r = requests.post('http://{ip}/modules/'.format(ip=server))
        if r.ok and r.json()['status'] == 'OK':
            return r.json()['data']
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def getModulesNamesByCategory(server, category):
    try:
        r = requests.post('http://{ip}/category/{cat}'.format(ip=server, cat=category))
        if r.ok and r.json()['status'] == 'OK':
            return r.json()['data']
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def downloadModuleFull(server, moduleName):
    try:
        r = requests.post('http://{ip}/download/{mod}'.format(ip=server, mod=moduleName))
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def downloadModuleFiles(server, moduleName):
    try:
        r = requests.post('http://{ip}/download/files/{mod}'.format(ip=server, mod=moduleName))
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def downloadModuleConf(server, moduleName):
    try:
        r = requests.post('http://{ip}/download/config/{mod}'.format(ip=server, mod=moduleName))
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def downloadModuleDjangoView(server, moduleName):
    try:
        r = requests.post('http://{ip}/download/views/{mod}'.format(ip=server, mod=moduleName))
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

def newModuleUpload(server, category, moduleName):
    try:
        r = requests.post('http://{ip}/new/module/upload/{cat}/{mod}/'.format(ip=server, cat=category, mod=moduleName))
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({'status':  'FAIL', 'data': str(e)})

getOnlineServers()