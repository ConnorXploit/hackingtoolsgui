from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.views.decorators.csrf import csrf_exempt
from .library import hackingtools as ht
from .library.hackingtools.core import Utils, Logger, Config
from importlib import reload
import os
import json
from requests import Response
from colorama import Fore

# Create your views here.

config = Config.getConfig(parentKey='django', key='views')
global ht_data
ht_data = {}

def load_data():
    global ht_data
    modules_and_params = ht.getModulesJSON()
    modules_forms = ht.__getModulesDjangoForms__()
    modules_forms_modal = ht.__getModulesDjangoFormsModal__()
    modules_config = ht.getModulesConfig()
    modules_config_treeview = ht.__getModulesConfig_treeView__()
    modules_functions_modals = ht.getModulesModalTests()
    modules_functions_calls_console_string = ht.getModulesFunctionsCalls()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[1] in categories:
            categories.append(mod.split('.')[1])
        modules_all[mod.split('.')[2]] = modules_and_params[mod]
    modules_names = ht.getModulesNames()
    pool_list = ht.getPoolNodes()
    my_node_id_pool = ht.MY_NODE_ID
    status_pool = ht.WANT_TO_BE_IN_POOL
    ht_data =  { 
        'modules':modules_names, 
        'categories':categories, 
        'modules_all':modules_all,
        'modules_forms':modules_forms, 
        'modules_forms_modal':modules_forms_modal, 
        'modules_config':modules_config, 
        'console_command':modules_functions_calls_console_string, 
        'modules_config_treeview':modules_config_treeview, 
        'modules_functions_modals':modules_functions_modals, 
        'pool_list':pool_list,
        'my_node_id_pool':my_node_id_pool,
        'status_pool':status_pool}

def renderMainPanel(request, popup_text=''):
    global ht_data
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
                doc_mod = '{documents_dir}/{c}/{b}/{a}.html'.format(documents_dir=this_conf['documents_dir'], c=mod.split('.')[-3], b=module_name.split('ht_')[1], a=module_name)
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
    response, creator = ht.send(request, functionName)
    if response:
        if creator == ht.MY_NODE_ID:
            return response, False
        return response, True
    return None, None

def switchPool(request):
    ht.switchPool()
    data = {
        'status' : ht.WANT_TO_BE_IN_POOL
    }
    return JsonResponse(data)

def createModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_cat = request.POST.get('category_name')
    created = ht.createModule(mod_name, mod_cat)
    if created:
        modules_and_params = ht.getModulesJSON()
    return renderMainPanel(request=request)

def configModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_conf = ht.getModuleConfig(mod_name)
    reload(ht)
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
    filename = fs.save(myfile.name, myfile)
    Logger.printMessage(message='saveFileOutput', description='Saving to {fi}'.format(fi=os.path.join(location,myfile.name)))
    return (filename, location, os.path.join(location, filename))

def add_pool_node(request):
    this_conf = config['add_pool_node']
    try:
        if request.POST:
            pool_node = request.POST.get('pool_ip')
        ht.addNodeToPool(pool_node)
        if request.POST.get('is_async', False):
            data = {
                'data' : ht.getPoolNodes()
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text='\n'.join(ht.getPoolNodes()))
    except:
        return renderMainPanel(request=request, popup_text=this_conf['error'])
    return renderMainPanel(request=request, popup_text='\n'.join(ht.getPoolNodes()))

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

# ht_rsa
def ht_rsa_encrypt(request):
    if request.POST.get('private_key_keynumber') and request.POST.get('private_key_keymod') and request.POST.get('cipher_text'):
        priv_key_k = request.POST.get('private_key_keynumber')
        priv_key_n = request.POST.get('private_key_keymod')
        text = request.POST.get('cipher_text')
        crypter = ht.getModule('ht_rsa')
        crypted_text = crypter.encrypt(private_key=(int(priv_key_k), int(priv_key_n)), plaintext=text.encode())
        if request.POST.get('is_async', False):
            data = {
                'data' : crypted_text
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=crypted_text)
    else:
        return renderMainPanel(request=request)

def ht_rsa_decrypt(request):
    if request.POST.get('public_key_keynumber') and request.POST.get('public_key_keymod') and request.POST.get('decipher_text'):
        pub_key_k = request.POST.get('public_key_keynumber')
        pub_key_n = request.POST.get('public_key_keymod')
        text = request.POST.get('decipher_text')
        crypter = ht.getModule('ht_rsa')
        decrypted_text = crypter.decrypt(public_key=(int(pub_key_k), int(pub_key_n)), ciphertext=text)
        if request.POST.get('is_async', False):
            data = {
                'data' : decrypted_text
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=decrypted_text)
    else:
        return renderMainPanel(request=request)

@csrf_exempt
def ht_rsa_getRandomKeypair(request):
    response, repool = sendPool(request, "getRandomKeypair")
    if response or repool:
        if repool:
            return HttpResponse(response)
        return renderMainPanel(request=request, popup_text=response.text)
    else:
        length = None
        if request.POST.get('prime_length'):
            length = request.POST.get('prime_length')
        crypter = ht.getModule('ht_rsa')
        keypair = (0, 0)
        if length:
            keypair = crypter.getRandomKeypair(int(length))
        else:
            keypair = crypter.getRandomKeypair()
        keypair = '({n1}, {n2})'.format(n1=keypair[0], n2=keypair[1])
        if request.POST.get('is_async', False):
            data = {
                'data' : keypair
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=keypair)

@csrf_exempt
def ht_rsa_generate_keypair(request):
    response, repool = sendPool(request, "generate_keypair")
    if response or repool:
        if repool:
            return HttpResponse(response)
        return renderMainPanel(request=request, popup_text=response.text)
    else:
        if request.POST.get('prime_a') and request.POST.get('prime_b'):
            prime_a = request.POST.get('prime_a')
            prime_b = request.POST.get('prime_b')
            crypter = ht.getModule('ht_rsa')
            keypair = crypter.generate_keypair(int(prime_a), int(prime_b))
            if not isinstance(keypair, str):
                try: 
                    keypair = '({n1}, {n2})'.format(n1=keypair[0], n2=keypair[1])
                except:
                    pass
            if request.POST.get('is_async', False):
                data = {
                    'data' : keypair
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=keypair)
        else:
            return renderMainPanel(request=request)

# End ht_rsa

# ht_crypter
def ht_crypter_cryptFile(request):
    this_conf = config['ht_crypter_cryptFile']
    if len(request.FILES) != 0:
        if request.FILES['filename']:
            # Get file
            myfile = request.FILES['filename']

            # Get Crypter Module
            crypter = ht.getModule('ht_crypter')

            # Save the file
            filename, location, uploaded_file_url = saveFileOutput(myfile, "crypter", "av_evasion")
            
            # Compile Exe
            compile_exe = False
            if request.POST.get('compile_exe','')=='on':
                compile_exe = True

            tmp_new_file_name = filename.split('.')[0]
            if not '.' in tmp_new_file_name:
                tmp_new_file_name = '{name}.py'.format(name=tmp_new_file_name)
            new_file_name = os.path.join(location, tmp_new_file_name)

            drop_file_name = filename
            if not '.' in drop_file_name:
                drop_file_name = '{name}.{ext}'.format(name=drop_file_name, ext=filename.split('.')[1])

            iterate_count = 1

            if request.POST.get('iteratecount'):
                try:
                    iterate_count = int(request.POST.get('iteratecount'))
                    if iterate_count < 1:
                        iterate_count = 1
                except:
                    pass

            prime_length = 2
            if request.POST.get('prime_length'):
                try:
                    prime_length = int(request.POST.get('prime_length'))
                    if prime_length < 1:
                        prime_length = 2
                except:
                    pass

            is_last = False
            if iterate_count == 1:
                is_last = True

            crypted_file = crypter.crypt_file(filename=uploaded_file_url, new_file_name=new_file_name, drop_file_name=drop_file_name, prime_length=prime_length, iterate_count=iterate_count, is_last=is_last, compile_exe=compile_exe)

            if crypted_file:
                if os.path.isfile(crypted_file):
                    with open(crypted_file, 'rb') as fh:
                        if compile_exe:
                            new_file_name = '{name}.exe'.format(name=new_file_name.split('.')[0])
                        response = HttpResponse(fh.read(), content_type="application/{type}".format(type=new_file_name.split('.')[1]))
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(crypted_file)
                        return response
                        os.remove(uploaded_file_url)
                        os.remove(crypted_file)
            else:
                Logger.printMessage(message='ht_crypter_cryptFile', description=this_conf['bad_saved'], is_error=True)
            return renderMainPanel(request=request)

    return renderMainPanel(request=request)

# End ht_crypter

# ht_shodan

def ht_shodan_getIPListfromServices(request):
    if request.POST.get('service_name'):
        service_name = request.POST.get('service_name')
        shodan_key = None
        if request.POST.get('shodanKeyString'):
            shodan_key = request.POST.get('shodanKeyString')
        shodan = ht.getModule('ht_shodan')
        response_shodan = shodan.getIPListfromServices(serviceName=service_name, shodanKeyString=shodan_key)
        resp_text = ','.join(response_shodan)
        if request.POST.get('is_async', False):
            data = {
                'data' : resp_text
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=resp_text)
    else:
        return renderMainPanel(request=request)

# End ht_shodan

# ht_nmap

def ht_nmap_getConnectedDevices(request):
    if request.POST.get('ip'):
        ip_to_scan = request.POST.get('ip')
        nmap = ht.getModule('ht_nmap')
        response_nmap = nmap.getConnectedDevices(ip=ip_to_scan)
        resp_text = ','.join(response_nmap)
        if request.POST.get('is_async', False):
            data = {
                'data' : resp_text
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=resp_text)
    else:
        return renderMainPanel(request=request)

# End ht_nmap

# ht_metadta

def ht_metadata_get_metadata_exif(request):
    if len(request.FILES) != 0:
        if request.FILES['image_file']:
            # Get file
            myfile = request.FILES['image_file']
            # Get Crypter Module
            metadata = ht.getModule('ht_metadata')
            
            # Save the file
            filename, location, uploaded_file_url = saveFileOutput(myfile, "metadata", "forensic")
            
            data = metadata.get_pdf_exif(uploaded_file_url)
            
            if request.POST.get('is_async', False):
                data = {
                    'data' : data
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=str(json.dumps(data)))
    else:
        return renderMainPanel(request=request)

# ht_bruteforce

@csrf_exempt
def ht_bruteforce_crackZip(request):
    this_conf = config['ht_bruteforce_crackZip']
    try:
        if len(request.FILES) != 0:
            if request.FILES['zipFileBruteforce']:
                # If it is a pool request... :) in config.json have to be a param to work: __pool_it_crackZip__
                response, repool = sendPool(request, "crackZip")
                if response or repool:
                    if repool:
                        return HttpResponse(response)
                    return renderMainPanel(request=request, popup_text=response.text)
                else:
                    # Get file
                    myfile = request.FILES['zipFileBruteforce']

                    async_execution = request.POST.get('async_execution', False)
                    password_length = request.POST.get('password_length', 4)

                    used_alphabet = 'numeric'

                    bruteforce_numeric = request.POST.get('bruteforce_numeric', False)
                    bruteforce_lower = request.POST.get('bruteforce_lower', False)
                    bruteforce_upper = request.POST.get('bruteforce_upper', False)
                    bruteforce_simbols = request.POST.get('bruteforce_simbols', False)
                    bruteforce_simbols_all = request.POST.get('bruteforce_simbols_all', False)

                    used_alphabet = getDictionaryAlphabet(numeric=bruteforce_numeric, lower=bruteforce_lower, upper=bruteforce_upper, simbols14=bruteforce_simbols, simbolsAll=bruteforce_simbols_all)

                    # Get Crypter Module
                    bruter = ht.getModule('ht_bruteforce')
                    unzipper = ht.getModule('ht_unzip')

                    # Save the file
                    filename, location, uploaded_file_url = saveFileOutput(myfile, "bruteforce", "crackers")
                    if uploaded_file_url:
                        password = bruter.crackZip(uploaded_file_url, unzipper=unzipper, alphabet=used_alphabet, password_length=password_length, log=False)
                    else:
                        if request.POST.get('is_async', False):
                            data = {
                                'data' : this_conf['error_see_log']
                            }
                            return JsonResponse(data)
                        return renderMainPanel(request=request, popup_text=this_conf['error_see_log'])

                    if 'is_async' in request.POST and request.POST.get('is_async') == True:
                        data = {
                            'data' : password
                        }
                        return JsonResponse(data)
                    if not password:
                        if request.POST.get('is_async', False):
                            data = {
                                'data' : this_conf['not_solved']
                            }
                            return JsonResponse(data)
                        return renderMainPanel(request=request, popup_text=this_conf['not_solved'])
                    if request.POST.get('is_async', False):
                        data = {
                            'data' : password
                        }
                        return JsonResponse(data)
                    return renderMainPanel(request=request, popup_text=password)
    except ConnectionError as conError:
        Logger.printMessage(message='ht_bruteforce_crackZip', description=this_conf['conn_closed'])
    return renderMainPanel(request=request)

# ht_unzip

def ht_unzip_extractFile(request):
    this_conf = config['ht_unzip_extractFile']
    if len(request.FILES) != 0:
        if request.FILES['zipFile']:
            # Get file
            myfile = request.FILES['zipFile']

            password = ''
            if request.POST.get('passwordFile'):
                password = request.POST.get('passwordFile')

            # Get Crypter Module
            unzipper = ht.getModule('ht_unzip')

            # Save the file
            filename, location, uploaded_file_url = saveFileOutput(myfile, "unzip", "crackers")

            if uploaded_file_url:
                password = unzipper.extractFile(uploaded_file_url, password=password)
            else:
                return renderMainPanel(request=request, popup_text=this_conf['error_see_log'])

            if password:
                if request.POST.get('is_async', False):
                    data = {
                        'data' : password
                    }
                    return JsonResponse(data)
                return renderMainPanel(request=request, popup_text=password)
            else:
                return renderMainPanel(request=request, popup_text=this_conf['bad_pass'])

    return renderMainPanel(request=request)


# ht_virustotal

def ht_virustotal_isBadFile(request):
    try:
        if len(request.FILES) != 0:
            if request.FILES['filename']:
                virustotal = ht.getModule('ht_virustotal')
                # Save the file
                filename, location, uploaded_file_url = saveFileOutput(request.FILES['filename'], "virustotal", "forensic")
                response = virustotal.isBadFile(uploaded_file_url)
                if request.POST.get('is_async', False):
                    data = {
                        'data' : response
                    }
                    return JsonResponse(data)
                return renderMainPanel(request=request, popup_text=response)
    except Exception as e:
        return renderMainPanel(request=request, popup_text=str(e))

# ht_objectdetection

def ht_objectdetection_predictImage(request):
    this_conf = config['ht_objectdetection_predictImage']
    try:
        if len(request.FILES) != 0:

            if 'image_file_test' in request.FILES:
                objectdetection = ht.getModule('ht_objectdetection')
                image_to_test = request.FILES['image_file_test']
                filename, location, uploaded_file_url = saveFileOutput(image_to_test, "objectdetection", "ai")

                first_folder_name = None
                filenameZip = None
                uploaded_file_urlZip = this_conf['default_model']
                modelfile = request.POST.get('dropdown_modelfile')
                
                if not modelfile:
                    modelfile = request.POST.get('dropdown_modelfile_main')

                if 'image_models_zip' in request.FILES:
                    zip_to_train = request.FILES['image_models_zip']
                    first_folder_name = request.POST.get('first_folder_name', None)
                    if not first_folder_name:
                        first_folder_name = zip_to_train.name.split('.')[0]
                    filenameZip, location, uploaded_file_urlZip = saveFileOutput(zip_to_train, "objectdetection", "ai")

                n_neighbors = int(request.POST.get('neighbors', 1))

                if filenameZip:
                    image_final = objectdetection.predictImage(
                        uploaded_file_url, 
                        model_path='{f}.clf'.format(f=filenameZip.split('.')[0]), 
                        trainZipFile=uploaded_file_urlZip, 
                        first_folder_name=first_folder_name,
                        n_neighbors=n_neighbors)
                else:
                    image_final = objectdetection.predictImage(
                        uploaded_file_url, 
                        model_path=modelfile)
                
                with open(image_final, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/{type}".format(type=filename.split('.')[1]))
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(image_final)
                    return response
            
            if request.POST.get('is_async', False):
                data = {
                    'data' : this_conf['need_params']
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=this_conf['need_params'])
        return renderMainPanel(request=request, popup_text=this_conf['need_file'])
    except Exception as e:
        Logger.printMessage(message='ht_objectdetection_predictImage', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

def ht_objectdetection_predictFromZip(request):
    this_conf = config['ht_objectdetection_predictFromZip']
    try:
        if len(request.FILES) != 0:

            if 'image_file_test_zip' in request.FILES:
                objectdetection = ht.getModule('ht_objectdetection')

                image_to_test_zip = request.FILES['image_file_test_zip']
                first_folder_name = request.POST.get('first_folder_name', None)

                filename, location, uploaded_file_url = saveFileOutput(image_to_test_zip, "objectdetection", "ai")

                if not first_folder_name:
                    first_folder_name = image_to_test_zip.split('.')[0]

                filenameZip = None
                uploaded_file_urlZip = this_conf['default_model']
                modelfile = request.POST.get('dropdown_modelfile_pred')

                if 'image_models_zip_pred' in request.FILES:
                    zip_to_train = request.FILES['image_models_zip_pred']
                    first_folder_name_zip = request.POST.get('first_folder_name_zip', None)
                    if not first_folder_name_zip:
                        first_folder_name_zip = zip_to_train.name.split('.')[0]
                    filenameZip, location, uploaded_file_urlZip = saveFileOutput(zip_to_train, "objectdetection", "ai")

                n_neighbors = int(request.POST.get('neighbors_pred', 1))

                if filenameZip:
                    image_final = objectdetection.predictFromZip(
                        uploaded_file_url, 
                        model_path='{f}.clf'.format(f=filenameZip.split('.')[0]),
                        first_folder_name=first_folder_name,
                        trainZipFile=uploaded_file_urlZip,
                        first_folder_name_training_zip=first_folder_name_zip,
                        n_neighbors=n_neighbors)
                else:
                    image_final = objectdetection.predictFromZip(
                        uploaded_file_url, 
                        model_path=modelfile,
                        first_folder_name=first_folder_name)
                
                with open(image_final, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/{type}".format(type=filename.split('.')[1]))
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(image_final)
                    return response
            if request.POST.get('is_async', False):
                data = {
                    'data' : this_conf['need_params']
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=this_conf['need_params'])

    except Exception as e:
        Logger.printMessage(message='ht_objectdetection_predictFromZip', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

def ht_objectdetection_trainFromZip(request):
    try:
        if len(request.FILES) != 0:
            objectdetection = ht.getModule('ht_objectdetection')
            first_folder_name = None
            filenameZip = None
            uploaded_file_urlZip = 'trained.clf'

            if 'image_models_zip' in request.FILES:
                zip_to_train = request.FILES['image_models_zip']
                first_folder_name = request.POST.get('first_folder_name', None)
                if not first_folder_name:
                    first_folder_name = zip_to_train.name.split('.')[0]
                filenameZip, location, uploaded_file_urlZip = saveFileOutput(zip_to_train, "objectdetection", "ai")

            n_neighbors = int(request.POST.get('neighbors', 1))

            if filenameZip:
                image_final = objectdetection.trainFromZip(
                    uploaded_file_urlZip, 
                    model_path='{f}.clf'.format(f=filenameZip.split('.')[0]), 
                    trainZipFile=uploaded_file_urlZip, 
                    first_folder_name=first_folder_name,
                    n_neighbors=n_neighbors)
                if request.POST.get('is_async', False):
                    data = {
                        'data' : image_final
                    }
                    return JsonResponse(data)
                return renderMainPanel(request=request, popup_text=image_final)
            return renderMainPanel(request=request)

    except Exception as e:
        Logger.printMessage(message='ht_objectdetection_trainFromZip', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))


