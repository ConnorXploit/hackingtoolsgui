from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.views.decorators.csrf import csrf_exempt
from .library import hackingtools as ht
from .library.hackingtools.core import Utils, Logger, Config, Connections, UtilsDjangoViewsAuto
from importlib import reload
import os, sys, requests
import json
from requests import Response
from colorama import Fore

from bs4 import BeautifulSoup

from .views_modules import *

# Create your views here.

config = Config.getConfig(parentKey='django', key='views')
global ht_data
ht_data = {}

def load_data():
    global ht_data
    modules_and_params = ht.getModulesJSON()
    modules_forms = ht.DjangoFunctions.__getModulesDjangoForms__()
    modules_forms_modal = ht.DjangoFunctions.__getModulesDjangoFormsModal__()
    modules_config = ht.getModulesConfig()
    # ! Slows down a lot the charge of Django home view
    #modules_config_treeview = ht.DjangoFunctions.__getModulesConfig_treeView__()
    modules_config_treeview = {}
    # TODO 
    modules_functions_modals = ht.DjangoFunctions.getModulesModalTests()
    modules_functions_calls_console_string = ht.DjangoFunctions.getModulesFunctionsCalls()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[1] in categories:
            categories.append(mod.split('.')[1])
        modules_all[mod.split('.')[2]] = modules_and_params[mod]
    modules_names = ht.getModulesNames()
    server_repo = ht.Repositories.getOnlineServers()[0]
    modules_names_repo = []
    categories_names_repo = []
    if server_repo:
        modules_names_repo = ['ht_{m}'.format(m=mod.replace('ht_', '')) for mod in ht.Repositories.getModules(server_repo)]
        categories_names_repo = ht.Repositories.getCategories(server_repo)
    pool_list = ht.Pool.getPoolNodes()
    my_services = ht.Connections.getMyServices()
    ngrokService = ht.Connections.getNgrokServiceUrl()
    is_heroku = True if 'DYNO' in os.environ else False
    my_node_id_pool = ht.Pool.MY_NODE_ID
    status_pool = ht.WANT_TO_BE_IN_POOL
    ht_data =  { 
        'modules':modules_names, 
        'modules_names_repo':modules_names_repo,
        'categories_names_repo':categories_names_repo,
        'categories':categories, 
        'modules_all':modules_all,
        'modules_forms':modules_forms, 
        'modules_forms_modal':modules_forms_modal, 
        'modules_config':modules_config, 
        'console_command':modules_functions_calls_console_string, 
        'modules_config_treeview':modules_config_treeview, 
        'modules_functions_modals':modules_functions_modals, 
        'pool_list':pool_list,
        'my_services':my_services,
        'is_heroku':is_heroku,
        'ngrokService':ngrokService,
        'my_node_id_pool':my_node_id_pool,
        'status_pool':status_pool}

def renderMainPanel(request, popup_text=''):
    global ht_data
    if not ht_data:
        load_data()
    if popup_text != '':
        ht_data['popup_text'] = popup_text
    return render(request, 'core/index.html', dict(ht_data))

def home(request, popup_text=''):
    global ht_data
    load_data()
    if popup_text != '':
        ht_data['popup_text'] = popup_text
    return renderMainPanel(request=request)

def documentation(request, module_name=''):
    this_conf = config['documentation']
    if module_name:
        for mod in ht.modules_loaded:
            if module_name == mod.split('.')[-1]:
                doc_mod = '{documents_dir}/{c}/{b}/{a}.html'.format(documents_dir=this_conf['documents_dir'], c=mod.split('.')[-3], b=module_name.replace('ht_', ''), a=module_name)
                print(doc_mod)
                categories = [] 
                for mod in ht.getModulesJSON():
                    if not mod.split('.')[1] in categories:
                        categories.append(mod.split('.')[1])
                modules_names = ht.getModulesNames()
                return render(request, this_conf['html_template'], { 'doc_mod' : doc_mod, 'categories' : categories, 'modules' : modules_names })
        return renderMainPanel(request=request, popup_text=this_conf['bad_module'])
    else:
        return renderMainPanel(request=request, popup_text=this_conf['no_module_selected'])

def sendPool(request, functionName):
    # ! changes here affect all nodes on the network, so should be careful with this
    # ! It loop inside all nodes's known nodes
    if ht.wantPool():
        response, creator = ht.Pool.send(request, functionName)
        if response:
            if creator == ht.Pool.MY_NODE_ID:
                if 'nodes_pool' in response:
                    for n in response['nodes_pool']:
                        ht.Pool.addNodeToPool(n)
                return response['res'], False # Yes, mine
            return response['res'], True # Repool, not mine
    return None, None

def switchPool(request):
    ht.switchPool()
    data = {
        'status' : ht.wantPool()
    }
    return JsonResponse(data)

def createModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_cat = request.POST.get('category_name')
    created = ht.createModule(mod_name, mod_cat)
    if created:
        modules_and_params = ht.getModulesJSON()
        load_data()
        UtilsDjangoViewsAuto.loadModuleFunctionsToView(mod_name, mod_cat)
    # ! Tengo que hacer que llame a las funciones de crear views y json con la config...
    # ! Aprovechar para solucionar los params que no cogia (es porque tira del inspect y como no está guardado en pypi esa versión, no coge esa versión y devuelve 0 params)
    # ! Creo que se puede solucionar con la Util amIDjango al inicio de los import
    # * Hay que sacar las funciones de las urls.py que sirve para ello, a un UtilsDjango.py para ciertas funciones
    # ! De esta forma, desde aqui, podemos llamar a esas funciones y cargar todo de una sola vez y avisar que las funciones
    # ! solo serán funcionales una vez se reinicie o intentar hacer que se virtualice de alguna forma esa url y se resuelva sola sin tener que recargar
    return renderMainPanel(request=request)
    
def removeModule(request):
    try:
        mod_name = request.POST.get('module_name').replace(" ", "_").lower()
        category = ht.getModuleCategory(mod_name)
        ht.removeModule(mod_name, category)
        UtilsDjangoViewsAuto.removeModuleView(mod_name, category)
        data = {
            'data' : 'Removed successfully'
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'data' : str(e)
        }
        return JsonResponse(data)

def downloadInstallModule(request):
    try:
        mod_name = request.POST.get('module_name').replace('ht_', '').lower()
        ht.Repositories.installModule(ht.Repositories.getOnlineServers()[0], mod_name)
        UtilsDjangoViewsAuto.restartDjangoServer()
        data = {
            'data' : 'Installed successfully'
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'data' : str(e)
        }
        return JsonResponse(data)

def restartServerDjango(request):
    try:
        UtilsDjangoViewsAuto.restartDjangoServer()
        data = {
            'data' : 'Reloading... Please wait at least 1 minute for saving changes'
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'data' : str(e)
        }
        return JsonResponse(data)

def configModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    # mod_conf = ht.getModuleConfig(mod_name)
    # reload(ht)
    return renderMainPanel(request=request)

def createCategory(request):
    mod_cat = request.POST.get('category_name').replace(" ", "_").lower()
    ht.createCategory(mod_cat)
    return renderMainPanel(request=request)

def createScript(request):
    return renderMainPanel(request=request)

def config_look_for_changes(request):
    ht.Config.__look_for_changes__()
    load_data()
    return renderMainPanel(request=request)

def saveFileOutput(myfile, module_name, category):
    location = os.path.join("core", "library", "hackingtools", "modules", category, module_name.split('ht_')[0], "output")
    fs = FileSystemStorage(location=location)
    if not os.path.isdir(location):
        os.mkdir(location)
    try:
        filename = fs.save(myfile.name, myfile)
    except Exception as e:
        Logger.printMessage(message='saveFileOutput', description=str(e))
        return (None, None, None)
    Logger.printMessage(message='saveFileOutput', description='Saving to {fi}'.format(fi=os.path.join(location,myfile.name)))
    return (filename, location, os.path.join(location, filename))

def getLogs(request):
    data = {
        'data' : ht.Logger.getLogsClear(),
        'buttonsPool' : ht.Pool.__checkPoolNodes__()
    }
    
    return JsonResponse(data)

@csrf_exempt
def add_pool_node(request):
    this_conf = config['add_pool_node']
    try:
        if request.POST:
            pool_node = request.POST.get('pool_ip', None)
            if not pool_node in ht.Pool.getPoolNodes():
                ht.Pool.addNodeToPool(pool_node)
                if not request.POST.get('pooling', False):
                    for serv in ht.Connections.getMyServices():
                        service_for_call = '{node_ip}/core/pool/add_pool_node/'.format(node_ip=pool_node)
                        add_me_to_theis_pool = requests.post(service_for_call, data={'pool_ip':serv},  headers=ht.Connections.headers)
                        if add_me_to_theis_pool.status_code == 200:
                            Logger.printMessage(message="send", description='Saving my service API REST to {n} - {s} '.format(n=pool_node, s=serv), color=Fore.YELLOW, debug_core=True)
            return renderMainPanel(request=request, popup_text='\n'.join(ht.Pool.getPoolNodes()))
        return renderMainPanel(request=request, popup_text='Only POST is available')
    except:
        return renderMainPanel(request=request, popup_text=this_conf['error'])
    return renderMainPanel(request=request, popup_text='\n'.join(ht.Pool.getPoolNodes()))

def getDictionaryAlphabet(numeric=True, lower=False, upper=False, simbols14=False, simbolsAll=False):
    used_alphabet = 'numeric'
    if numeric and not lower and not upper and not simbols14 and not simbolsAll:
        used_alphabet = 'numeric'
    if not numeric and lower and not upper and not simbols14 and not simbolsAll:
        used_alphabet = 'lalpha'
    if not numeric and not lower and upper and not simbols14 and not simbolsAll:
        used_alphabet = 'ualpha'
    if not numeric and lower and upper and not simbols14 and not simbolsAll:
        used_alphabet = 'mixalpha'
    if not numeric and not lower and not upper and simbols14 and not simbolsAll:
        used_alphabet = 'symbols14'
    if not numeric and not lower and not upper and not simbols14 and simbolsAll:
        used_alphabet = 'symbols-all'

    if not numeric and lower and not upper and simbols14 and not simbolsAll:
        used_alphabet = 'lalpha-symbol14'
    if not numeric and lower and not upper and not simbols14 and simbolsAll:
        used_alphabet = 'lalpha-all'
    if numeric and lower and not upper and not simbols14 and not simbolsAll:
        used_alphabet = 'lalpha-numeric'
    if numeric and lower and not upper and simbols14 and not simbolsAll:
        used_alphabet = 'lalpha-numeric-symbol14'
    if numeric and lower and not upper and not simbols14 and simbolsAll:
        used_alphabet = 'lalpha-numeric-all'

    if not numeric and not lower and upper and simbols14 and not simbolsAll:
        used_alphabet = 'ualpha-symbol14'
    if not numeric and not lower and upper and not simbols14 and simbolsAll:
        used_alphabet = 'ualpha-all'
    if numeric and not lower and upper and not simbols14 and not simbolsAll:
        used_alphabet = 'ualpha-numeric'
    if numeric and not lower and upper and simbols14 and not simbolsAll:
        used_alphabet = 'ualpha-numeric-symbol14'
    if numeric and not lower and upper and not simbols14 and simbolsAll:
        used_alphabet = 'ualpha-numeric-all'

    if not numeric and lower and upper and simbols14 and not simbolsAll:
        used_alphabet = 'mixalpha-symbol14'
    if not numeric and lower and upper and not simbols14 and simbolsAll:
        used_alphabet = 'mixalpha-all'
    if numeric and lower and upper and not simbols14 and not simbolsAll:
        used_alphabet = 'mixalpha-numeric'
    if numeric and lower and upper and simbols14 and not simbolsAll:
        used_alphabet = 'mixalpha-numeric-symbol14'
    if numeric and lower and upper and not simbols14 and simbolsAll:
        used_alphabet = 'mixalpha-numeric-all'

    return used_alphabet

@csrf_exempt
def poolExecute(request):
    try:
        functionCall = request.POST.get('functionCall', None)

        files = None
        if request.FILES and len(request.FILES) > 0:
            files = request.FILES

        params = {}
        for key, value in request.POST.items():
            params[key] = value

        if ht.Connections.isHeroku():
            me = 'http://{url}/'.format(url=ht.Connections.getMyLocalIP())
        else:
            me = 'http://{url}:{port}/'.format(url=ht.Connections.getMyLocalIP(), port=Connections.getActualPort())
        print(me)

        if functionCall:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }
            client = requests.session()
            soup = BeautifulSoup(client.get(me).content, features="lxml")
            csrftoken = soup.find('input', dict(name='csrfmiddlewaretoken'))['value']
            if 'csrfmiddlewaretoken' in params:
                del params['csrfmiddlewaretoken']
            params['csrfmiddlewaretoken'] = csrftoken
            is_async = 'is_async_{fu}'.format(fu=functionCall.split('/')[-2])
            params[is_async] = True
            r = client.post('{me}{call}'.format(me=me, call=functionCall), files=files, data=params, headers=headers)
            return JsonResponse({'data' : json.loads(r.text)['data']})
        else:
            return JsonResponse({'data' : 'No function to call'})
    except Exception as e:
        return JsonResponse({'data' : me})

@csrf_exempt
def getNodeId(request):
    return JsonResponse({ 'data' : ht.Pool.MY_NODE_ID })

# Connections

def startNgrok(request):
    ngrok = ht.Connections.startNgrok(Connections.getActualPort())
    if ngrok:
        ht.Pool.callNodesForInformAboutMyServices()
        return renderMainPanel(request=request, popup_text=ngrok)
    return renderMainPanel(request=request)