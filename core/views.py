from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.urls import reverse
from .library import hackingtools as ht
from importlib import reload
import os
# Create your views here.

def home(request, popup_text=''):
    modules_and_params = ht.getModulesJSON()
    modules_forms = ht.__getModulesDjangoForms__() # Corregir template config vacios
    modules_forms_modal = ht.__getModulesDjangoFormsModal__() # Corregir template config vacios
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
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all, 'modules_forms':modules_forms, 'modules_forms_modal':modules_forms_modal, 'modules_config':modules_config, 'console_command':modules_functions_calls_console_string, 'modules_config_treeview':modules_config_treeview, 'modules_functions_modals':modules_functions_modals, 'popup_text':popup_text })

def createModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_cat = request.POST.get('category_name')
    created = ht.createModule(mod_name, mod_cat)
    #reload(ht) # NO SE ACTUALIZA
    if created:
        modules_and_params = ht.getModulesJSON()
    return redirect(reverse('home'))

def configModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_conf = ht.getModuleConfig(mod_name)
    reload(ht)
    return redirect('home')

def createCategory(request):
    mod_cat = request.POST.get('category_name').replace(" ", "_").lower()
    ht.createCategory(mod_cat)
    return redirect('home')

def createScript(request):
    return redirect('home')

def config_look_for_changes(request):
    ht.Config.__look_for_changes__()
    return redirect('home')

# ht_rsa
def ht_rsa_encrypt(request):
    if request.POST.get('private_key_keynumber') and request.POST.get('private_key_keymod') and request.POST.get('cipher_text'):
        priv_key_k = request.POST.get('private_key_keynumber')
        priv_key_n = request.POST.get('private_key_keymod')
        text = request.POST.get('cipher_text')
        crypter = ht.getModule('ht_rsa')
        crypted_text = crypter.encrypt(private_key=(int(priv_key_k), int(priv_key_n)), plaintext=text.encode())
        return home(request=request, popup_text=crypted_text)
    else:
        return home(request=request)

def ht_rsa_decrypt(request):
    if request.POST.get('public_key_keynumber') and request.POST.get('public_key_keymod') and request.POST.get('cipher_text'):
        pub_key_k = request.POST.get('public_key_keynumber')
        pub_key_n = request.POST.get('public_key_keymod')
        text = request.POST.get('cipher_text')
        crypter = ht.getModule('ht_rsa')
        decrypted_text = crypter.decrypt(public_key=(int(pub_key_k), int(pub_key_n)), ciphertext=text)
        return home(request=request, popup_text=decrypted_text)
    else:
        return home(request=request)

def ht_rsa_getRandomKeypair(request):
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
    return home(request=request, popup_text=keypair)

def ht_rsa_generate_keypair(request):
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
        return home(request=request, popup_text=keypair)
    else:
        return home(request=request)

# End ht_rsa

# ht_crypter
def ht_crypter_cryptFile(request):
    if len(request.FILES) != 0:
        if request.FILES['filename']:
            # Get file
            myfile = request.FILES['filename']

            # Get Crypter Module
            crypter = ht.getModule('ht_crypter')
            crypter.clean_output_dir()
            
            location = os.path.join("core", "library", "hackingtools", "modules", "av_evasion", "crypter", "output")
            fs = FileSystemStorage(location=location)

            # Save file
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = os.path.join(location, filename)
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
                print('No se ha guardado correctamente')
            return redirect(reverse('home'))

    return redirect(reverse('home'))

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
        return home(request=request, popup_text=resp_text)
    else:
        return home(request=request)

# End ht_shodan

# ht_nmap

def ht_nmap_getConnectedDevices(request):
    if request.POST.get('ip'):
        ip_to_scan = request.POST.get('ip')
        nmap = ht.getModule('ht_nmap')
        response_nmap = nmap.getConnectedDevices(ip=ip_to_scan)
        resp_text = ','.join(response_nmap)
        return home(request=request, popup_text=resp_text)
    else:
        return home(request=request)

# End ht_nmap