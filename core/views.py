from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.urls import reverse
from .library import hackingtools
from importlib import reload
import os
# Create your views here.

def home(request, popup_text=''):
    print(popup_text)
    modules_and_params = hackingtools.getModulesJSON()
    modules_forms = hackingtools.__getModulesDjangoForms__()
    modules_forms_modal = hackingtools.__getModulesDjangoFormsModal__()
    modules_config = hackingtools.getModulesConfig()
    modules_functions_modals = hackingtools.getModulesModalTests()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[1] in categories:
            categories.append(mod.split('.')[1])
        modules_all[mod.split('.')[2]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all, 'modules_forms':modules_forms, 'modules_forms_modal':modules_forms_modal, 'modules_config':modules_config, 'modules_functions_modals':modules_functions_modals, 'popup_text':popup_text })

def createModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_cat = request.POST.get('category_name')
    hackingtools.createModule(mod_name, mod_cat)
    #reload(hackingtools) # NO SE ACTUALIZA
    modules_and_params = hackingtools.getModulesJSON()
    return redirect(reverse('home'))

def configModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_conf = hackingtools.getModuleConfig(mod_name)
    reload(hackingtools)
    return redirect('home')

def createCategory(request):
    mod_cat = request.POST.get('category_name').replace(" ", "_").lower()
    hackingtools.createCategory(mod_cat)
    return redirect('home')

def createScript(request):
    return redirect('home')

# Crypter
def ht_crypter_encrypt(request):
    if request.POST.get('private_key') and request.POST.get('cipher_text'):
        return_type = None
        if request.POST.get('return-type'):
            return_type = request.POST.get('return-type')
        priv_key_k = request.POST.get('private_key_keynumber')
        priv_key_n = request.POST.get('private_key_keymod')
        text = request.POST.get('cipher_text')
        print(text)
        crypter = hackingtools.getModule('ht_crypter')
        crypted_text = crypter.encrypt((priv_key_k, priv_key_n), text)
        return home(request=request, popup_text=crypted_text)
    else:
        return home(request=request)

def ht_crypter_decrypt(request):
    if request.POST.get('public_key') and request.POST.get('cipher_text'):
        return_type = None
        if request.POST.get('return-type'):
            return_type = request.POST.get('return-type')
        pub_key = request.POST.get('public_key')
        text = request.POST.get('cipher_text')
        crypter = hackingtools.getModule('ht_crypter')
        decrypted_text = crypter.decrypt(pub_key, text)
        return home(request=request, popup_text=decrypted_text)
    else:
        return home(request=request)

def ht_crypter_getRandomKeypair(request):
    length = None
    if request.POST.get('prime_length'):
        length = request.POST.get('prime_length')
    crypter = hackingtools.getModule('ht_crypter')
    keypair = (0, 0)
    if length:
        keypair = crypter.getRandomKeypair(int(length))
    else:
        keypair = crypter.getRandomKeypair()
    keypair = '({n1}, {n2})'.format(n1=keypair[0], n2=keypair[1])
    return home(request=request, popup_text=keypair)

def ht_crypter_generate_keypair(request):
    if request.POST.get('prime_a') and request.POST.get('prime_b'):
        prime_a = request.POST.get('prime_a')
        prime_b = request.POST.get('prime_b')
        crypter = hackingtools.getModule('ht_crypter')
        keypair = crypter.generate_keypair(int(prime_a), int(prime_b))
        if not isinstance(keypair, str):
            try: 
                keypair = '({n1}, {n2})'.format(n1=keypair[0], n2=keypair[1])
            except:
                pass
        return home(request=request, popup_text=keypair)
    else:
        return home(request=request)

def ht_crypter_cryptFile(request):
    if len(request.FILES) != 0:
        if request.FILES['filename']:
            # Get file
            myfile = request.FILES['filename']

            # Get Crypter Module
            crypter = hackingtools.getModule('ht_crypter')
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

# End Crypter
