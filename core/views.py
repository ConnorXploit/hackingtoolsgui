from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.views.decorators.csrf import csrf_exempt
from .library import hackingtools as ht
from .library.hackingtools.core import Utils, Logger, Config, Connections, UtilsDjangoViewsAuto, DjangoFunctions
from .library.hackingtools.core.DjangoFunctions import __getReturnAsModalHTML__ as returnAsModal
from importlib import reload
import os
import sys
import requests
import json
import collections
from requests import Response
from colorama import Fore

from bs4 import BeautifulSoup

from .views_modules import *

# Create your views here.

config = Config.getConfig(parentKey='django', key='views')

global ht_data
ht_data = {}

global ht_data_maps
ht_data_maps = {}

global apis_config
apis_config = ht.Config


def load_data(session_id=None):
    global ht_data
    modules_and_params = ht.__getModulesJSON__()
    modules_forms = ht.DjangoFunctions.__getModulesDjangoForms__()
    not_async_form = ht.Config.getConfig('core', 'not_async_function')
    modules_forms_modal = DjangoFunctions.__getModulesDjangoFormsModal__(
        session_id=session_id)
    modules_config = ht.__getModulesConfig__()
    # ! Slows down a lot the charge of Django home view
    #modules_config_treeview = ht.DjangoFunctions.__getModulesConfig_treeView__()
    modules_config_treeview = {}
    # TODO
    modules_functions_modals = ht.DjangoFunctions.__getModulesModalTests__()
    modules_functions_calls_console_string = ht.DjangoFunctions.__getModulesFunctionsCalls__()
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
        modules_names_repo = ['ht_{m}'.format(m=mod.replace(
            'ht_', '')) for mod in ht.Repositories.getModules(server_repo)]
        categories_names_repo = ht.Repositories.getCategories(server_repo)
    pool_list = ht.Pool.getPoolNodes()
    my_services = ht.__Connections.getMyServices()
    ngrokService = ht.__Connections.getNgrokServiceUrl()
    is_heroku = True if 'DYNO' in os.environ else False
    my_node_id_pool = ht.Pool.__MY_NODE_ID__
    status_pool = ht.__WANT_TO_BE_IN_POOL__
    funcs_map = ht.DjangoFunctions.__getModulesFunctionsForMap__()

    if session_id:
        sess_key = '__API_KEY_{sess}__'.format(sess=session_id)
        if sess_key in ht.Config.__config__['core']:
            api_keys = ht.Config.__config__['core'][sess_key]
        else:
            api_keys = {}

    else:
        api_keys = ht.Config.__config__['core']['__API_KEY__']
    ht_data = {
        'modules': modules_names,
        'modules_names_repo': modules_names_repo,
        'categories_names_repo': categories_names_repo,
        'categories': categories,
        'modules_all': modules_all,
        'modules_forms': modules_forms,
        'not_async_form': not_async_form,
        'modules_forms_modal': modules_forms_modal,
        'modules_config': modules_config,
        'console_command': modules_functions_calls_console_string,
        'modules_config_treeview': modules_config_treeview,
        'modules_functions_modals': modules_functions_modals,
        'pool_list': pool_list,
        'my_services': my_services,
        'is_heroku': is_heroku,
        'ngrokService': ngrokService,
        'my_node_id_pool': my_node_id_pool,
        'status_pool': status_pool,
        'funcs_map': funcs_map,
        'api_keys': collections.OrderedDict(sorted(api_keys.items()))}


def load_data_maps(session_id=None):
    global ht_data_maps
    if ht_data_maps:
        ht_data_maps = {}
    ht_data_maps['gps'] = ht.Utils.getLocationGPS()
    try:
        ht_data_maps['funcs_map'] = ht.DjangoFunctions.__getModulesFunctionsForMap__()
    except:
        pass
    if session_id:
        sess_key = '__API_KEY_{sess}__'.format(sess=session_id)
        if sess_key in ht.Config.__config__['core']:
            ht_data_maps['api_keys'] = ht.Config.__config__['core'][sess_key]
        else:
            ht_data_maps['api_keys'] = {}
    else:
        ht_data_maps['api_keys'] = ht.Config.__config__['core']['__API_KEY__']

    ht_data_maps['api_keys'] = collections.OrderedDict(
        sorted(ht_data_maps['api_keys'].items()))

    ht_data_maps['map_search'] = ht.Config.getSearchedHostsInMap(
        session_id=session_id)


def renderMainPanel(request, popup_text=''):
    if not 'htpass' in request.COOKIES:
        session_id = ht.Utils.randomText(40, 'mixalpha-numeric-symbol14')
    else:
        session_id = request.COOKIES['htpass']
    global ht_data
    if not ht_data:
        load_data(session_id)
    if popup_text != '':
        ht_data['popup_text'] = popup_text

    response = render(request, 'core/index.html', dict(ht_data))
    response.set_cookie('htpass', session_id)
    return response


def renderMaps(request):
    if not 'htpass' in request.COOKIES:
        session_id = ht.Utils.randomText(40, 'mixalpha-numeric-symbol14')
    else:
        session_id = request.COOKIES['htpass']
    global ht_data_maps

    load_data_maps(session_id)

    response = render(request, 'core/maps.html', dict(ht_data_maps))
    response.set_cookie('htpass', session_id)
    return response


def switchFunctionMap(request):
    mod = request.POST.get('module')
    cat = ht.getModuleCategory(mod)
    fun = request.POST.get('functionName')
    Config.switch_function_for_map(cat, mod, fun)
    return JsonResponse({'data': 'Ok'})

# Start API Keys


def uploadAPIFileToConf(request):
    session_id = request.COOKIES['htpass']
    if len(request.FILES) != 0:
        if request.FILES['api_keys_file']:
            # Get file
            myfile = request.FILES['api_keys_file']

            # Save the file
            filename, location, uploaded_file_url = saveFileOutput(
                myfile, "rsa", "crypto")

            password = request.POST.get('password_apis')

            if password:
                try:
                    apis_config.loadRestAPIsFile(
                        uploaded_file_url, password, session_id)
                    load_data(session_id=session_id)
                    load_data_maps(session_id=session_id)
                    return JsonResponse({"data": 'Imported successfully', 'status': 'OK'})
                except:
                    return JsonResponse({"data": 'Bad password', 'status': 'FAILURE'})

            return JsonResponse({"data": 'You have to insert a password', 'status': 'FAILURE'})

    return JsonResponse({"data": 'Not file uploaded', 'status': 'FAILURE'})


def downloadAPIFile(request):
    session_id = request.COOKIES['htpass']
    try:
        password = request.GET.get('password_apis')

        if password:
            try:
                file_apis = apis_config.saveRestAPIsFile('{n}.htpass'.format(
                    n=ht.Utils.randomText(32, 'mixalpha-numeric')), password, session_id)

                if os.path.exists(file_apis):
                    with open(file_apis, 'rb') as fh:

                        response = HttpResponse(
                            fh.read(), content_type="application/x-www-form-urlencoded")
                        response['Content-Disposition'] = 'inline; filename=' + \
                            os.path.basename(file_apis)
                        return response
                else:
                    return JsonResponse({"data": 'Seem\'s that the file {n} doesn\'t exist'.format(n=file_apis)})
                return JsonResponse({"data": 'Something wen\'t wrong creating the pass file... {n}'.format(n=file_apis)})

            except Exception as e:
                return JsonResponse({"data": str(e)})

        return JsonResponse({"data": 'You have to insert a password'})
    except Exception as e:
        return JsonResponse({"data": str(e)})


def saveTemporaryAPIsOnSession(request):
    session_id = request.COOKIES['htpass']
    api_keys = request.POST.get('api_keys')
    if not api_keys or not json.loads(api_keys):
        for api in apis_config.getAPIsNames():
            apis_config.setAPIKey(api, '', session_id)
        return JsonResponse({"data": api_keys})
    else:
        apis = json.loads(api_keys)
        for api in apis:
            apis_config.setAPIKey(api, apis[api], session_id)
    return JsonResponse({"data": 'Changed successfully'})

# End API Keys


def home(request, popup_text=''):
    if not 'htpass' in request.COOKIES:
        session_id = ht.Utils.randomText(40, 'mixalpha-numeric-symbol14')
    else:
        session_id = request.COOKIES['htpass']
    global ht_data
    load_data(session_id)
    if popup_text != '':
        ht_data['popup_text'] = popup_text
    return renderMainPanel(request=request)


def documentation(request, module_name=''):
    this_conf = config['documentation']
    if module_name:
        for mod in ht.__modules_loaded__:
            if module_name == mod.split('.')[-1]:
                doc_mod = '{documents_dir}/{c}/{b}/{a}.html'.format(documents_dir=this_conf['documents_dir'], c=mod.split(
                    '.')[-3], b=module_name.replace('ht_', ''), a=module_name)
                print(doc_mod)
                categories = []
                for mod in ht.__getModulesJSON__():
                    if not mod.split('.')[1] in categories:
                        categories.append(mod.split('.')[1])
                modules_names = ht.getModulesNames()
                return render(request, this_conf['html_template'], {'doc_mod': doc_mod, 'categories': categories, 'modules': modules_names})
        return renderMainPanel(request=request, popup_text=this_conf['bad_module'])
    else:
        return renderMainPanel(request=request, popup_text=this_conf['no_module_selected'])


def sendPool(request, functionName):
    # ! changes here affect all nodes on the network, so should be careful with this
    # ! It loop inside all nodes's known nodes
    if ht.wantPool():
        response, creator = ht.Pool.__send__(request, functionName)
        if response:
            if creator == ht.Pool.__MY_NODE_ID__:
                if 'nodes_pool' in response:
                    for n in response['nodes_pool']:
                        ht.Pool.addNodeToPool(n)
                return response['res'], False  # Yes, mine
            return response['res'], True  # Repool, not mine
    return None, None


def switchPool(request):
    ht.switchPool()
    data = {
        'status': ht.wantPool()
    }
    return JsonResponse(data)


def __createModule__(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_cat = request.POST.get('category_name')
    created = ht.__createModule__(mod_name, mod_cat)
    if created:
        modules_and_params = ht.__getModulesJSON__()
        load_data()
        UtilsDjangoViewsAuto.loadModuleFunctionsToView(mod_name, mod_cat)
    # ! Tengo que hacer que llame a las funciones de crear views y json con la config...
    # ! Aprovechar para solucionar los params que no cogia (es porque tira del inspect y como no está guardado en pypi esa versión, no coge esa versión y devuelve 0 params)
    # ! Creo que se puede solucionar con la Util amIDjango al inicio de los import
    # * Hay que sacar las funciones de las urls.py que sirve para ello, a un UtilsDjango.py para ciertas funciones
    # ! De esta forma, desde aqui, podemos llamar a esas funciones y cargar todo de una sola vez y avisar que las funciones
    # ! solo serán funcionales una vez se reinicie o intentar hacer que se virtualice de alguna forma esa url y se resuelva sola sin tener que recargar
    return renderMainPanel(request=request)


def __removeModule__(request):
    try:
        mod_name = request.POST.get('module_name').replace(" ", "_").lower()
        category = ht.getModuleCategory(mod_name)
        ht.__removeModule__(mod_name, category)
        UtilsDjangoViewsAuto.removeModuleView(mod_name, category)
        data = {
            'data': 'Removed successfully'
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'data': str(e)
        }
        return JsonResponse(data)


def downloadInstallModule(request):
    try:
        mod_name = request.POST.get('module_name').replace('ht_', '').lower()
        ht.Repositories.installModule(
            ht.Repositories.getOnlineServers()[0], mod_name)
        UtilsDjangoViewsAuto.restartDjangoServer()
        data = {
            'data': 'Installed successfully'
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'data': str(e)
        }
        return JsonResponse(data)


def restartServerDjango(request):
    try:
        UtilsDjangoViewsAuto.restartDjangoServer()
        data = {
            'data': 'Reloading... Please wait at least 1 minute for saving changes'
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'data': str(e)
        }
        return JsonResponse(data)


def configModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    # mod_conf = ht.__getModuleConfig__(mod_name)
    # reload(ht)
    return renderMainPanel(request=request)


def __createCategory__(request):
    mod_cat = request.POST.get('category_name').replace(" ", "_").lower()
    ht.__createCategory__(mod_cat)
    return renderMainPanel(request=request)


def createScript(request):
    return renderMainPanel(request=request)


def config_look_for_changes(request):
    if not 'htpass' in request.COOKIES:
        session_id = ht.Utils.randomText(40, 'mixalpha-numeric-symbol14')
    else:
        session_id = request.COOKIES['htpass']
    ht.Config.__look_for_changes__()
    load_data(session_id)
    return renderMainPanel(request=request)


def saveFileOutput(myfile, module_name, category):
    location = os.path.join("core", "library", "hackingtools",
                            "modules", category, module_name.split('ht_')[0], "output")
    fs = FileSystemStorage(location=location)
    if not os.path.isdir(location):
        os.mkdir(location)
    try:
        filename = fs.save(myfile.name, myfile)
    except Exception as e:
        Logger.printMessage(message='saveFileOutput',
                            description=str(e), debug_core=True)
        return (None, None, None)
    Logger.printMessage(message='saveFileOutput', description='Saving to {fi}'.format(
        fi=os.path.join(location, myfile.name)), is_success=True, debug_core=True)
    return (filename, location, os.path.join(location, filename))


def getLogs(request):
    data = {
        'data': ht.Logger.getLogsClear(),
        'buttonsPool': ht.Pool.__checkPoolNodes__()
    }

    return JsonResponse(data)


def getIPLocationGPS(request):
    ip = request.POST.get('ip', None)
    #api = request.POST.get('api', None)
    data = {
        'data': ht.Utils.getIPLocationGPS_v2(ip),
        'status': 'OK'
    }

    return JsonResponse(data)


@csrf_exempt
def saveHostSearchedInMap(request):
    if not 'htpass' in request.COOKIES:
        session_id = ht.Utils.randomText(40, 'mixalpha-numeric-symbol14')
    else:
        session_id = request.COOKIES['htpass']
    try:
        ip = request.POST.get('ip')
        location = [request.POST.get(
            'longitude', 0), request.POST.get('latitude', 0)]
        info = request.POST.get('info')
        country = request.POST.get('country')
        searched_term = request.POST.get('searched_term')
        ht.Config.saveHostSearchedInMap(
            ip, location, country, info, searched_term, session_id=session_id)
        return JsonResponse({'data': 'Saved Successfuly'})
    except Exception as e:
        print(str(e))
        return JsonResponse({'data': str(e)})


@csrf_exempt
def add_pool_node(request):
    this_conf = config['add_pool_node']
    try:
        if request.POST:
            pool_node = request.POST.get('pool_ip', None)
            if not pool_node or pool_node not in ht.Pool.getPoolNodes():
                if pool_node not in (ht.__Connections.getMyPublicIP(as_service=True), ht.__Connections.getMyLocalIP(as_service=True), ht.__Connections.getMyLanIP(as_service=True)):
                    ht.Pool.addNodeToPool(pool_node)
                    if not request.POST.get('pooling', False):
                        for serv in ht.__Connections.getMyServices():
                            service_for_call = '{node_ip}/core/pool/add_pool_node/'.format(
                                node_ip=pool_node)
                            add_me_to_theis_pool = requests.post(
                                service_for_call, data={'pool_ip': serv},  headers=ht.__Connections.__headers__)
                            if add_me_to_theis_pool.status_code == 200:
                                Logger.printMessage(message="send", description='Saving my service API REST to {n} - {s} '.format(
                                    n=pool_node, s=serv), is_info=True, debug_core=True)
                else:
                    return renderMainPanel(request=request, popup_text='Could not add my own service to my pool nodes')
            return renderMainPanel(request=request, popup_text='\n'.join(ht.Pool.getPoolNodes()))
        return renderMainPanel(request=request, popup_text='Only POST is available')
    except Exception as e:
        return renderMainPanel(request=request, popup_text='{m}\n{e}'.format(m=this_conf['error'], e=str(e)))
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

        creator = request.POST.get('creator_id', None)
        if creator != ht.Pool.__MY_NODE_ID__:

            files = None
            if request.FILES and len(request.FILES) > 0:
                files = request.FILES

            params = {}
            for key, value in request.POST.items():
                params[key] = value

            ht.Pool.__checkPoolNodes__()
            if ht.__Connections.isHeroku():
                me = ht.__Connections.getMyLocalIP(as_service=True, port=False)
            else:
                me = 'http://{url}:{port}/'.format(
                    url=Connections.getMyLocalIP(), port=Connections.getActualPort())

            if functionCall:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                client = requests.session()
                soup = BeautifulSoup(client.get(me).text, "html.parser")
                csrftoken = soup.find(
                    'input', {'name': 'csrfmiddlewaretoken'})['value']
                Logger.printMessage(csrftoken, is_info=True, debug_core=True)
                if 'csrfmiddlewaretoken' in params:
                    del params['csrfmiddlewaretoken']
                params['csrfmiddlewaretoken'] = csrftoken
                is_async = 'is_async_{fu}'.format(
                    fu=functionCall.split('/')[-2])
                params[is_async] = True
                call_url = '{me}{slash}{call}'.format(
                    me=me, slash='/' if me[-1] != '/' else '', call=functionCall)
                print(call_url)
                r = client.post(call_url, files=files,
                                data=params, headers=headers)
                Logger.printMessage(r, is_info=True, debug_core=True)
                Logger.printMessage(r.text, is_info=True, debug_core=True)
                client.close()
                return JsonResponse({'data': json.loads(r.text)['data']})
            else:
                return JsonResponse({'data': 'No function to call'})
        return JsonResponse({'fail': 'My own call'})
    except Exception as e:
        return JsonResponse({'data': str(e)})


@csrf_exempt
def getNodeId(request):
    return JsonResponse({'data': ht.Pool.__MY_NODE_ID__})

# Connections


def startNgrok(request):
    ngrok = ht.__Connections.startNgrok(Connections.getActualPort())
    if ngrok:
        ht.Pool.__callNodesForInformAboutMyServices__()
        return renderMainPanel(request=request, popup_text=ngrok)
    return renderMainPanel(request=request)
