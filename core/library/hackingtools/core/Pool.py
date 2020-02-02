from . import Config, Logger, Utils
if Utils.amIdjango(__name__):
    from core.library import hackingtools as ht
else:
    import hackingtools as ht
from django.urls import resolve
from colorama import Fore
from tempfile import TemporaryFile
import sys, requests, json, os, random, threading, time

# Nodes Pool Treatment

nodes_pool = Config.getConfig(parentKey='core', key='Pool', subkey='known_nodes')

global CHECKED_NODES
CHECKED_NODES = False
MY_NODE_ID = Utils.randomText(length=32, alphabet='mixalpha-numeric-symbol14')

def switchPool():
    ht.switchPool()

def addNodeToPool(node_ip):
    global nodes_pool
    global CHECKED_NODES
    if node_ip and not node_ip in nodes_pool:
        if Utils.amIdjango(__name__):
            Logger.printMessage(node_ip, debug_core=True)
        if not node_ip in ht.Connections.getMyServices():
            nodes_pool.append(node_ip)
            Config.add_pool_node(node_ip)
            CHECKED_NODES = False

def callNodesForInformAboutMyServices():
    global nodes_pool 
    for n in nodes_pool:
        ngrok_url = ht.Connections.getNgrokServiceUrl()
        service_for_call = '{node_ip}/core/pool/add_pool_node/'.format(node_ip=n)
        if ngrok_url:
            try:
                if ngrok_url:
                    requests.post(service_for_call, data={'pool_ip':ngrok_url , 'pooling':True},  headers=ht.Connections.headers)
            except:
                pass
        else:
            for serv in ht.Connections.getMyServices():
                try:
                    if serv:
                        requests.post(service_for_call, data={'pool_ip':serv , 'pooling':True},  headers=ht.Connections.headers)
                except:
                    pass

def send(node_request, functionName):
    creator_id = MY_NODE_ID
    pool_nodes = getPoolNodes()
    try:
        if ht.wantPool():
            function_api_call = resolve(node_request.path_info).route
            pool_it = node_request.POST.get('__pool_it_{func}__'.format(func=functionName), False)
            if pool_it:
                if pool_nodes:
                    params = dict(node_request.POST)
                    if 'pool_list' in params:
                        if not params['pool_list']:
                            params['pool_list'] = []
                    if 'creator' in params:
                        if params['creator'] == MY_NODE_ID:
                            Logger.printMessage(message='My own call', description='Discarding...', is_warn=True)
                            return (None, None)
                    if not 'creator' in params:
                        params['creator'] = creator_id

                    if params['creator'] == creator_id: # TODO This disables repooling ------ SOLVE THIS PLEASEEE WE NEED REPOOOL
                        response, creator, _ = __sendPool__(creator=params['creator'], function_api_call=function_api_call, params=dict(params), files=node_request.FILES)
                        
                        callNodesForInformAboutMyServices()
                                
                        if 'creator' in params and params['creator'] == creator_id and response:
                            if isinstance(response, str):
                                return ({ 'res' : response, 'nodes_pool' : nodes_pool }, creator_id)
                            if isinstance(response, dict):
                                return ({ 'res' : response['data'], 'nodes_pool' : nodes_pool }, creator_id)
                            try:
                                return (str(response.text), False)
                            except:
                                return (str(response), False)
                        if response:
                            return (response, creator) # Repool
                    return (None, None)
                else:
                    return (None, None)
            else:
                return (None, None)
        else:
            Logger.printMessage(message='Disabled pool', description='If want to pool, change __WANT_TO_BE_IN_POOL__ to true', is_warn=True)
            return (None, None)
    except Exception as e:
        Logger.printMessage(message='ERROR', description=str(e), is_error=True)
        return (None, None)

def sendNow(moduleName, functionName, params={}, files={}):
    global nodes_pool

    url_path = 'modules/{cat}/{mod}/{func_call}/'.format(cat=ht.getModuleCategory(moduleName), mod=moduleName.replace('ht_', ''), func_call=functionName)

    params['creator'] = MY_NODE_ID
    params['pool_list'] = []
            
    response, _, resolver = __sendPool__(MY_NODE_ID, url_path, params, files)

    while 'NoneType' in response:
        response, _, resolver = __sendPool__(MY_NODE_ID, url_path, params, files)
        
    res = {}
    res['nodes_pool'] = nodes_pool
    res['resolved_by'] = resolver

    if isinstance(response, dict):
        res['res'] = response['data']
    else:
        res['res'] = response
    
    return res

def __sendPool__(creator, function_api_call='', params={}, files=[]):
    # We have 3 diferent nodes list:
    #   1- nodes_pool : We know those nodes for any call
    #   2- pool_list : is inside params['pool_list'] and has the list of all pools that know this pool request
    #   3- nodes : Are the nodes we can call from out nodes_pool and that the aren't inside pool_list
    # Finally we add all pool_list nodes that aren't inside our nodes_pool to nodes_pool list

    global nodes_pool

    nodes = [] # Nodes to send this call. Thay have to be nodes that haven't received this yet.
    pool_list = [] # The pool_list is a list for getting all the nodes that have been notified by this call.

    mine_function_call = False

    try:
        pool_list = params['pool_list']
        for service in ht.Connections.getMyServices():
            if service in pool_list:
                mine_function_call = True
                Logger.printMessage(message=function_api_call, description='It\'s my own call', is_warn=True)
                return (None, None, None)
    except:
        pass
    
    nodes = nodes_pool
    if pool_list:
        nodes = list(set(nodes_pool) - set(pool_list))

    # Get all nodes in pool_list as known for us if we don't have any
    if not nodes_pool:
        nodes_pool = pool_list

    # I save pool_list items i don't have yet on my pools

    nodes_pool = nodes_pool + list(set(pool_list) - set(nodes_pool))

    my_own_call = False

    if pool_list:
        for service in ht.Connections.getMyServices():
            if service in pool_list:
                my_own_call = True
                pool_list.remove(service)

    # Remove any posible service with my public, local or lan IP
    if nodes_pool:
        for service in ht.Connections.getMyServices():
            removeNodeFromPool(service)

    random.shuffle(nodes)

    if len(nodes) > 0:
        if not mine_function_call and not my_own_call:
            for node in nodes:
                try:
                    if ht.Connections.__serviceNotMine__(node):

                        node_call = '{node_ip}/pool/execute/'.format(node_ip=node)

                        params['pool_list'] = pool_list

                        for serv in ht.Connections.getMyServices():
                            params['pool_list'].append(serv)
                            
                        params['is_pool'] = True

                        params['functionCall'] = function_api_call

                        if not 'creator' in params:
                            params['creator'] == MY_NODE_ID
                        
                        if node not in params['pool_list']:
                            print(files)
                            r = requests.post(node_call, files=files, data=params, headers=dict(Referer=node))
                        
                            if r.status_code == 200:
                                for n in pool_list:
                                    if ht.Connections.__serviceNotMine__(n) and not n == node:
                                        addNodeToPool(n)
                                Logger.printMessage(message='Solved by', description=(node), debug_core=True)
                                try:
                                    Logger.printMessage(json.loads(str(r.text))['data'], debug_core=True)
                                except:
                                    Logger.printMessage(r, debug_core=True)
                                return (json.loads(str(r.text))['data'], params['creator'], node) # (Data Content, Creator Call, Resolved By Node)
                except Exception as e:
                    Logger.printMessage(message='ERROR', description=str(e), is_warn=True)
        else:
            Logger.printMessage(message='ERROR', description='Returned to me my own function called into the pool', debug_core=True)
    else:
        Logger.printMessage(message='ERROR', description='There is nobody on the pool list', debug_core=True)

    return (None, None, None)

def getPoolNodes():
    global nodes_pool
    random.shuffle(nodes_pool)
    return nodes_pool

def removeNodeFromPool(node_ip):
    global nodes_pool
    if node_ip in nodes_pool:
        nodes_pool.remove(node_ip)
    Config.remove_pool_node(node_ip)

def checkNode(node):
    idnode = getNodeId(node)
    if idnode == MY_NODE_ID:
        Logger.printMessage('Removing node from nodes_pool, im this service xD', node, debug_core=True)
        removeNodeFromPool(node)
        if not node in ht.Connections.getMyServices():
            Config.add_my_service(node) 

def getNodeId(node, thread=False):
    threaded = thread

    if not thread:
        threaded = True

    while threaded:

        url = '{url}/core/pool/getNodeId/'.format(url=node)

        if thread:
            Logger.printMessage('Call to the node for not been idle in 3 minutes', url, color=Logger.Fore.YELLOW)
            time.sleep(180)

        try:
            r = requests.post(url, headers=ht.Connections.headers)
            if r.status_code == 200:
                return r.json()['data']
        except:
            Logger.printMessage('Error connecting to server, removing node from pool', url, is_error=True)
            removeNodeFromPool(node)

        if not thread:
            threaded = False

    return None

def __checkPoolNodes__(thread=False):
    global CHECKED_NODES
    changes = False
    if not CHECKED_NODES:
        for node in getPoolNodes():
            idnode = getNodeId(node, thread)
            if idnode == MY_NODE_ID:
                checkNode(node)
                changes = True
            CHECKED_NODES = True
        if not getPoolNodes():
            Config.__djangoSwitchPoolItButtons__(False)
            return False
    
    if getPoolNodes() and changes:
        Config.__djangoSwitchPoolItButtons__(True)
        return True
    return False

# t = ht.Utils.worker(functionCall=__checkPoolNodes__, args=(True,))