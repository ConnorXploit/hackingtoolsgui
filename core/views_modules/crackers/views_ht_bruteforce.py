from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, getDictionaryAlphabet
from core.views import sendPool

# Create your views here.

# ht_bruteforce

@csrf_exempt
def crackZip(request):
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
        Logger.printMessage(message='crackZip', description=this_conf['conn_closed'])
    return renderMainPanel(request=request)
