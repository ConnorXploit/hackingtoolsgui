from django.shortcuts import render
from .library import hackingtools
from importlib import reload
# Create your views here.

def home(request):
    modules_and_params = hackingtools.getModulesJSON()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[2] in categories:
            categories.append(mod.split('.')[2])
        modules_all[mod.split('.')[3]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all })

def createModule(request):
    mod_name = request.POST.get('module_name').strip().lower()
    mod_cat = request.POST.get('category_name')
    hackingtools.createModule(mod_name, mod_cat)
    reload(hackingtools) # NO SE ACTUALIZA
    modules_and_params = hackingtools.getModulesJSON()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[2] in categories:
            categories.append(mod.split('.')[2])
        modules_all[mod.split('.')[3]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all })

def createCategory(request):
    mod_cat = request.get('category')
    hackingtools.createCategory(mod_cat)
    modules_and_params = hackingtools.getModulesJSON()
    modules_all = {}
    categories = []
    for mod in modules_and_params:
        if not mod.split('.')[2] in categories:
            categories.append(mod.split('.')[2])
        modules_all[mod.split('.')[3]] = modules_and_params[mod]
    modules_names = hackingtools.getModulesNames()
    return render(request, 'core/index.html', { 'modules':modules_names, 'categories':categories, 'modules_all':modules_all })