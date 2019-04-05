from django.shortcuts import render
import hackingtools
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

def module(request):
    pass