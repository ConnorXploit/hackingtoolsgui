from . import Config, Logger, Utils
from .Objects import Transaction
if Utils.amIdjango(__name__):
    from core.library import hackingtools as ht
else:
    import hackingtools as ht
from django.urls import resolve as __resolve
import requests as __requests
import json as __json
import random as __random
import time as __time

import binascii
from Crypto import Random
from Crypto.PublicKey import RSA

# Nodes Pool Treatment

__nodes_pool__ = Config.getConfig(parentKey='core', key='Pool', subkey='known_nodes')

global __CHECKED_NODES__
__CHECKED_NODES__ = False
__MY_NODE_ID__ = Utils.randomText(length=32, alphabet='mixalpha-numeric-symbol14')

global __BLOCKCHAIN_MASTERNODE__
__BLOCKCHAIN_MASTERNODE__ = None

global __CURRENT_BLOCKCHAIN__
__CURRENT_BLOCKCHAIN__ = None

global __PENDING_TRANSACTIONS__
__PENDING_TRANSACTIONS__ = None

def newWallet():
	random_gen = Random.new().read
	private_key = RSA.generate(1024, random_gen)
	public_key = private_key.publickey()
	response = {
		'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
		'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
	}
	return response['private_key'], response['public_key']

def __generateWalletTransaction__(value, sent_to_wallet=''):
	transaction = Transaction(__WALLET_PUBLIC_KEY__, __WALLET_PRIVATE_KEY__, sent_to_wallet, value)
	response = {'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()}
	return response['transaction'], response['signature']

def sendTransaction(value, sent_to_wallet=''):
    global __BLOCKCHAIN_MASTERNODE__
    global __CURRENT_BLOCKCHAIN__
    if __BLOCKCHAIN_MASTERNODE__:
        if not __CURRENT_BLOCKCHAIN__:
            getBlockchain()
        transaction, signature = __generateWalletTransaction__(value, sent_to_wallet)
        url = 'http://{url}/transactions/new'.format(url=__BLOCKCHAIN_MASTERNODE__)
        data = {
            'sender_address': transaction['sender_address'], 
            'recipient_address': transaction['recipient_address'], 
            'amount': transaction['value'], 
            'signature': signature
        }
        response = __requests.post( url, data )
        return __json.loads( response.text )
    else:
        Logger.printMessage( 'There is no Master Node for the Wallet configured yet', is_error=True )

def getBlockchain():
    global __BLOCKCHAIN_MASTERNODE__
    global __CURRENT_BLOCKCHAIN__
    if __BLOCKCHAIN_MASTERNODE__:
        try:
            url = 'http://{url}/chain'.format(url=__BLOCKCHAIN_MASTERNODE__)
            response = __requests.get(url)
            if response.status_code == 200:
                __CURRENT_BLOCKCHAIN__ = __json.loads( response.text )
            else:
                Logger.printMessage( response.status_code, is_error=True )
        except Exception as e:
            Logger.printMessage( str(e), is_error=True )
    else:
        Logger.printMessage( 'There is no Master Node for the Wallet configured yet', is_error=True )

def getPendingTransactions():
    global __BLOCKCHAIN_MASTERNODE__
    global __PENDING_TRANSACTIONS__
    global __WALLET_PUBLIC_KEY__
    if __BLOCKCHAIN_MASTERNODE__:
        try:
            url = 'http://{url}/transactions/get'.format(url=__BLOCKCHAIN_MASTERNODE__)
            response = __requests.get(url)
            if response.status_code == 200:
                __PENDING_TRANSACTIONS__ = [ tran for tran in __json.loads( response.text )['transactions'] if not tran['sender_address'] == __WALLET_PUBLIC_KEY__ ]
            else:
                Logger.printMessage( response.status_code, is_error=True )
        except Exception as e:
            Logger.printMessage( str(e), is_error=True )
    else:
        Logger.printMessage( 'There is no Master Node for the Wallet configured yet', is_error=True )

def setMasterNode(nodeUrl):
    global __BLOCKCHAIN_MASTERNODE__
    __BLOCKCHAIN_MASTERNODE__ = nodeUrl.replace('http://', '').replace('https://', '').split('/')[0]

def minePendingTransaction():
    global __BLOCKCHAIN_MASTERNODE__
    global __WALLET_PUBLIC_KEY__
    if __BLOCKCHAIN_MASTERNODE__:
        url = 'http://{url}/mine'.format(url=__BLOCKCHAIN_MASTERNODE__)
        data = {
            'sender_address': __WALLET_PUBLIC_KEY__
        }
        response = __requests.post( url, data )
        return __json.loads( response.text )
    else:
        Logger.printMessage( 'There is no Master Node for the Wallet configured yet', is_error=True )

__WALLET_PRIVATE_KEY__, __WALLET_PUBLIC_KEY__ = newWallet()

def switchPool():
    ht.switchPool()

def addNodeToPool(node_ip):
    global __nodes_pool__
    global __CHECKED_NODES__
    if node_ip and not node_ip in __nodes_pool__:
        if Utils.amIdjango(__name__):
            Logger.printMessage(node_ip, debug_core=True)
        if not node_ip in ht.__Connections.getMyServices():
            __nodes_pool__.append(node_ip)
            Config.add_pool_node(node_ip)
            __CHECKED_NODES__ = False

def sendNow(moduleName, functionName, params={}, files={}):
    global __nodes_pool__

    url_path = 'modules/{cat}/{mod}/{func_call}/'.format(cat=ht.getModuleCategory(moduleName), mod=moduleName.replace('ht_', ''), func_call=functionName)

    params['creator'] = __MY_NODE_ID__
    params['pool_list'] = []
            
    response, _, resolver = __sendPool__(__MY_NODE_ID__, url_path, params, files)

    while 'NoneType' in response:
        response, _, resolver = __sendPool__(__MY_NODE_ID__, url_path, params, files)
        
    res = {}
    res['__nodes_pool__'] = __nodes_pool__
    res['resolved_by'] = resolver

    if isinstance(response, dict):
        res['res'] = response['data']
    else:
        res['res'] = response
    
    return res

def getPoolNodes():
    global __nodes_pool__
    __random.shuffle(__nodes_pool__)
    return __nodes_pool__

def removeNodeFromPool(node_ip):
    global __nodes_pool__
    if node_ip in __nodes_pool__:
        __nodes_pool__.remove(node_ip)
    Config.remove_pool_node(node_ip)

def checkNode(node):
    idnode = __getNodeId__(node)
    if idnode == __MY_NODE_ID__:
        Logger.printMessage('Removing node from __nodes_pool__, im this service xD', node, debug_core=True)
        removeNodeFromPool(node)
        if not node in ht.__Connections.getMyServices():
            Config.add_my_service(node) 

def __callNodesForInformAboutMyServices__():
    global __nodes_pool__ 
    for n in __nodes_pool__:
        ngrok_url = ht.__Connections.getNgrokServiceUrl()
        service_for_call = '{node_ip}/core/pool/add_pool_node/'.format(node_ip=n)
        if ngrok_url:
            try:
                if ngrok_url:
                    __requests.post(service_for_call, data={'pool_ip':ngrok_url , 'pooling':True},  headers=ht.__Connections.headers)
            except:
                pass
        else:
            for serv in ht.__Connections.getMyServices():
                try:
                    if serv:
                        __requests.post(service_for_call, data={'pool_ip':serv , 'pooling':True},  headers=ht.__Connections.headers)
                except:
                    pass

def __send__(node_request, functionName):
    creator_id = __MY_NODE_ID__
    pool_nodes = getPoolNodes()
    try:
        if ht.wantPool():
            function_api_call = __resolve(node_request.path_info).route
            pool_it = node_request.POST.get('__pool_it_{func}__'.format(func=functionName), False)
            if pool_it:
                if pool_nodes:
                    params = dict(node_request.POST)
                    if 'pool_list' in params:
                        if not params['pool_list']:
                            params['pool_list'] = []
                    if 'creator' in params:
                        if params['creator'] == __MY_NODE_ID__:
                            Logger.printMessage(message='My own call', description='Discarding...', is_warn=True)
                            return (None, None)
                    if not 'creator' in params:
                        params['creator'] = creator_id

                    if params['creator'] == creator_id: # TODO This disables repooling ------ SOLVE THIS PLEASEEE WE NEED REPOOOL
                        response, creator, _ = __sendPool__(creator=params['creator'], function_api_call=function_api_call, params=dict(params), files=node_request.FILES)
                        
                        __callNodesForInformAboutMyServices__()
                                
                        if 'creator' in params and params['creator'] == creator_id and response:
                            if isinstance(response, str):
                                return ({ 'res' : response, '__nodes_pool__' : __nodes_pool__ }, creator_id)
                            if isinstance(response, dict):
                                return ({ 'res' : response['data'], '__nodes_pool__' : __nodes_pool__ }, creator_id)
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

def __sendPool__(creator, function_api_call='', params={}, files=[]):
    # We have 3 diferent nodes list:
    #   1- __nodes_pool__ : We know those nodes for any call
    #   2- pool_list : is inside params['pool_list'] and has the list of all pools that know this pool request
    #   3- nodes : Are the nodes we can call from out __nodes_pool__ and that the aren't inside pool_list
    # Finally we add all pool_list nodes that aren't inside our __nodes_pool__ to __nodes_pool__ list

    global __nodes_pool__

    nodes = [] # Nodes to send this call. Thay have to be nodes that haven't received this yet.
    pool_list = [] # The pool_list is a list for getting all the nodes that have been notified by this call.

    mine_function_call = False

    try:
        pool_list = params['pool_list']
        for service in ht.__Connections.getMyServices():
            if service in pool_list:
                mine_function_call = True
                Logger.printMessage(message=function_api_call, description='It\'s my own call', is_warn=True)
                return (None, None, None)
    except:
        pass
    
    nodes = __nodes_pool__
    if pool_list:
        nodes = list(set(__nodes_pool__) - set(pool_list))

    # Get all nodes in pool_list as known for us if we don't have any
    if not __nodes_pool__:
        __nodes_pool__ = pool_list

    # I save pool_list items i don't have yet on my pools

    __nodes_pool__ = __nodes_pool__ + list(set(pool_list) - set(__nodes_pool__))

    my_own_call = False

    if pool_list:
        for service in ht.__Connections.getMyServices():
            if service in pool_list:
                my_own_call = True
                pool_list.remove(service)

    # Remove any posible service with my public, local or lan IP
    if __nodes_pool__:
        for service in ht.__Connections.getMyServices():
            removeNodeFromPool(service)

    __random.shuffle(nodes)

    if len(nodes) > 0:
        if not mine_function_call and not my_own_call:
            for node in nodes:
                try:
                    if ht.__Connections.__serviceNotMine__(node):

                        node_call = '{node_ip}/pool/execute/'.format(node_ip=node)

                        params['pool_list'] = pool_list

                        for serv in ht.__Connections.getMyServices():
                            params['pool_list'].append(serv)
                            
                        params['is_pool'] = True

                        params['functionCall'] = function_api_call

                        if not 'creator' in params:
                            params['creator'] == __MY_NODE_ID__
                        
                        if node not in params['pool_list']:
                            print(files)
                            r = __requests.post(node_call, files=files, data=params, headers=dict(Referer=node))
                        
                            if r.status_code == 200:
                                for n in pool_list:
                                    if ht.__Connections.__serviceNotMine__(n) and not n == node:
                                        addNodeToPool(n)
                                Logger.printMessage(message='Solved by', description=(node), debug_core=True)
                                try:
                                    Logger.printMessage(__json.loads(str(r.text))['data'], debug_core=True)
                                except:
                                    Logger.printMessage(r, debug_core=True)
                                return (__json.loads(str(r.text))['data'], params['creator'], node) # (Data Content, Creator Call, Resolved By Node)
                except Exception as e:
                    Logger.printMessage(message='ERROR', description=str(e), is_warn=True)
        else:
            Logger.printMessage(message='ERROR', description='Returned to me my own function called into the pool', debug_core=True)
    else:
        Logger.printMessage(message='ERROR', description='There is nobody on the pool list', debug_core=True)

    return (None, None, None)

def __getNodeId__(node, thread=False):
    threaded = thread

    if not thread:
        threaded = True

    while threaded:

        url = '{url}/core/pool/getNodeId/'.format(url=node)

        if thread:
            Logger.printMessage('Call to the node for not been idle in 3 minutes', url, color=Logger.__Fore.YELLOW)
            __time.sleep(180)

        try:
            r = __requests.post(url, headers=ht.__Connections.__headers__)
            if r.status_code == 200:
                return r.json()['data']
        except:
            Logger.printMessage('Error connecting to server, removing node from pool', url, is_error=True)
            removeNodeFromPool(node)

        if not thread:
            threaded = False

    return None

def __checkPoolNodes__(thread=False):
    global __CHECKED_NODES__
    changes = False
    if not __CHECKED_NODES__:
        for node in getPoolNodes():
            idnode = __getNodeId__(node, thread)
            if idnode == __MY_NODE_ID__:
                checkNode(node)
                changes = True
            __CHECKED_NODES__ = True
        if not getPoolNodes():
            Config.__djangoSwitchPoolItButtons__(False)
            return False
    
    if getPoolNodes() and changes:
        Config.__djangoSwitchPoolItButtons__(True)
        return True
    return False

# t = ht.Utils.worker(functionCall=__checkPoolNodes__, args=(True,))