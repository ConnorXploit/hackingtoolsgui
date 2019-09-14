from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, getDictionaryAlphabet
from core.views import sendPool

# Create your views here.

# ht_unzip

def extractFile(request):
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


def zipFiles(request):
	files = request.POST.get('files')
	new_folder_name = request.POST.get('new_folder_name')
	result = ht.getModule('ht_unzip').zipFiles( files=files, new_folder_name=new_folder_name )
	return renderMainPanel(request=request, popup_text=result)
	