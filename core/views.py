from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.urls import reverse
from .library import hackingtools
from importlib import reload
import os
# Create your views here.

def home(request, popup=''):
    modules_and_params = hackingtools.getModulesJSON()
    modules_forms = hackingtools.__getModulesDjangoForms__()
    modules_config = hackingtools.getModulesConfig()
    modules_functions_modals = hackingtools.getModulesModalTests()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[1] in categories:
            categories.append(mod.split('.')[1])
        modules_all[mod.split('.')[2]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all, 'modules_forms':modules_forms, 'modules_config':modules_config, 'modules_functions_modals':modules_functions_modals, 'popup':popup })

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
        priv_key = request.POST.get('private_key')
        text = request.POST.get('cipher_text')
        crypter = hackingtools.getModule('ht_crypter')
        crypted_text = crypter.encrypt(priv_key, text)
        return redirect(reverse('home', popup=crypted_text))
    else:
        return redirect(reverse('home'))

def ht_crypter_decrypt(request):
    if request.POST.get('public_key') and request.POST.get('cipher_text'):
        pub_key = request.POST.get('public_key')
        text = request.POST.get('cipher_text')
        crypter = hackingtools.getModule('ht_crypter')
        decrypted_text = crypter.decrypt(pub_key, text)
        return redirect(reverse('home', popup=decrypted_text))
    else:
        return redirect(reverse('home'))

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
