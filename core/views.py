from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .library import hackingtools
from importlib import reload
import os
# Create your views here.

def home(request):
    modules_and_params = hackingtools.getModulesJSON()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[1] in categories:
            categories.append(mod.split('.')[1])
        modules_all[mod.split('.')[2]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all })

def createModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_cat = request.POST.get('category_name')
    hackingtools.createModule(mod_name, mod_cat)
    #reload(hackingtools) # NO SE ACTUALIZA
    modules_and_params = hackingtools.getModulesJSON()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[1] in categories:
            categories.append(mod.split('.')[1])
        modules_all[mod.split('.')[2]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all })

def configModule(request):
    mod_name = request.POST.get('module_name').replace(" ", "_").lower()
    mod_conf = hackingtools.getModuleConfig(mod_name)
    reload(hackingtools)
    return redirect('home')

def createCategory(request):
    mod_cat = request.POST.get('category_name').replace(" ", "_").lower()
    hackingtools.createCategory(mod_cat)
    return redirect('home')

def cryptFile(request):
    if request.FILES['filename']:
        if request.POST.get('new_file_name') and request.POST.get('drop_file_name'):
            # Get file
            myfile = request.FILES['filename']

            location = os.path.join("core", "library", "hackingtools", "modules", "av_evasion", "crypter", "output")
            fs = FileSystemStorage(location=location)

            # Save file
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = os.path.join(location, filename)
            # Compile Exe
            compile_exe = False
            if request.POST.get('compile_exe','')=='on':
                compile_exe = True

            # Get Crypter Module
            crypter = hackingtools.getModule('ht_crypter')

            tmp_new_file_name = request.POST.get('new_file_name')
            if not '.' in tmp_new_file_name:
                tmp_new_file_name = '{name}.py'.format(name=tmp_new_file_name)
            new_file_name = os.path.join(location, tmp_new_file_name)

            drop_file_name = request.POST.get('drop_file_name')

            crypted_file = crypter.crypt_file(filename=uploaded_file_url, new_file_name=new_file_name, drop_file_name=drop_file_name, compile_exe=compile_exe)
            if crypted_file:
                with open(crypted_file, 'rb') as fh:
                    if compile_exe:
                        new_file_name = '{name}.exe'.format(name=new_file_name.split('.')[0])
                    response = HttpResponse(fh.read(), content_type="application/{type}".format(type=new_file_name.split('.')[1]))
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(crypted_file)
                    os.remove(uploaded_file_url)
                    return response
            else:
                print('No se ha guardado correctamente')

    return redirect('home')
