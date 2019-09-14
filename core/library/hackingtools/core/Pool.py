from .. import __init__ as ht
from . import Config, Logger, Utils
from django.urls import resolve
from colorama import Fore
import sys, requests

# Nodes Pool Treatment

nodes_pool = []
MY_NODE_ID = Utils.randomText(length=32, alphabet='mixalpha-numeric-symbol14')

https = '' # Anytime when adding ssl, shold be with an 's'

public_ip = Utils.getMyPublicIP()
lan_ip = Utils.getMyLanIP()
local_ip = Utils.getMyLocalIP()

try:
    listening_port = sys.argv[-1].split(':')[1]
except:
    listening_port = '8000'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

my_service_api = 'http{s}://{ip}:{port}'.format(s=https, ip=local_ip, port=listening_port)

public_ip_full = 'http{s}://{ip}:{port}'.format(s=https, ip=public_ip, port=listening_port)
lan_ip_full = 'http{s}://{ip}:{port}'.format(s=https, ip=lan_ip, port=listening_port)
local_ip_full = 'http{s}://{ip}:{port}'.format(s=https, ip=local_ip, port=listening_port)

def switchPool():
    ht.switchPool()

def addNodeToPool(node_ip):
    global nodes_pool
    if not node_ip in nodes_pool:
        nodes_pool.append(node_ip)

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
                    if not 'creator' in params:
                        params['creator'] = creator_id
                    response, creator = __sendPool__(creator=params['creator'], function_api_call=function_api_call, params=dict(params), files=node_request.FILES)
                    
                    global nodes_pool
                    for n in nodes_pool:
                        # Call to inform about my services
                        for serv in (public_ip_full, lan_ip_full, local_ip_full, my_service_api):
                            service_for_call = '{node_ip}/core/pool/add_pool_node/'.format(node_ip=n)
                            add_me_to_theis_pool = requests.post(service_for_call, data={'pool_ip':serv},  headers=headers)
                            if add_me_to_theis_pool.status_code == 200:
                                Logger.printMessage(message="send", description='Saving my service API REST into {n} - {s} '.format(n=n, s=serv), color=Fore.YELLOW)

                    if 'creator' in params and params['creator'] == creator_id and response:
                        return (str(response.text), False)
                    if response:
                        return (response, creator)
                    return (None, None)
                else:
                    return (None, None)
            else:
                Logger.printMessage(message='send', description='{n} - {f} - Your config should have activated "__pool_it_{f}__" for pooling the function to other nodes'.format(n=node_request, f=functionName), color=Fore.YELLOW, debug_core=True)
                return (None, None)
        else:
            Logger.printMessage(message='send', description='Disabled pool... If want to pool, change WANT_TO_BE_IN_POOL to true', color=Fore.YELLOW)
            return (None, None)
    except Exception as e:
        raise
        Logger.printMessage(message='send', description=str(e), is_error=True)
        return (None, None)

def __sendPool__(creator, function_api_call='', params={}, files=[]):
    # We have 3 diferent nodes list:
    #   1- nodes_pool : We know those nodes for any call
    #   2- pool_list : is inside params['pool_list'] and has the list of all pools that know this pool request
    #   3- nodes : Are the nodes we can call from out nodes_pool and that the aren't inside pool_list
    # Finally we add all pool_list nodes that aren't inside our nodes_pool to nodes_pool list

    global nodes_pool

    nodes = [] # Nodes to send this call. Thay have to be nodes that haven't received this yet.
    pool_list=[] # The pool_list is a list for getting all the nodes that have been notified by this call.

    mine_function_call = False

    try:
        pool_list = params['pool_list']
        for service in (public_ip_full, lan_ip_full, local_ip_full, my_service_api):
            if service in pool_list:
                mine_function_call = True
                Logger.printMessage(message='__sendPool__', description='It\'s my own call', color=Fore.YELLOW)
                return (None, None)
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

    if pool_list:
        for service in (public_ip_full, lan_ip_full, local_ip_full, my_service_api):
            if service in pool_list:
                pool_list.remove(service)

    # Remove any posible service with my public, local or lan IP
    if nodes_pool:
        for service in (public_ip_full, lan_ip_full, local_ip_full, my_service_api):
            removeNodeFromPool(service)

    if len(nodes) > 0:
        if not mine_function_call and (not my_service_api in pool_list and not public_ip_full in pool_list and not lan_ip_full in pool_list and not local_ip_full in pool_list):
            for node in nodes:
                try:
                    if not node in (public_ip_full, lan_ip_full, local_ip_full):
                        node_call = '{node_ip}/{function_api}'.format(node_ip=node, function_api=function_api_call)

                        params['pool_list'] = pool_list
                        try:
                            params['pool_list'].append(public_ip_full)
                            params['pool_list'].append(lan_ip_full)
                            params['pool_list'].append(local_ip_full)
                            params['pool_list'].append(my_service_api)
                            params['pool_list'].remove(node)
                        except:
                            pass
                            
                        params['is_pool'] = True

                        r = requests.post(node_call, files=files, data=params, headers=headers)

                        if r.status_code == 200:
                            for n in pool_list:
                                if not n in (public_ip_full, lan_ip_full, local_ip_full, my_service_api):
                                    addNodeToPool(n)
                            Logger.printMessage(message='__sendPool__', description=('Solved by {n}'.format(n=node)))
                            return (r, params['creator'])

                except Exception as e:
                    Logger.printMessage(message='__sendPool__', description=str(e), color=Fore.YELLOW)
        else:
            Logger.printMessage(message='__sendPool__', description='Returned to me my own function called into the pool', debug_module=True)
    else:
        Logger.printMessage(message='__sendPool__', description='There is nobody on the pool list', debug_module=True)

    return (None, None)

def getPoolNodes():
    global nodes_pool
    return nodes_pool

def removeNodeFromPool(node_ip):
    global nodes_pool
    if node_ip in nodes_pool:
        nodes_pool.remove(node_ip)
