from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

# ht_virustotal

def isBadFile(request):
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


def isBadFileHash(request):
	fileHash = request.POST.get('fileHash')
	result = ht.getModule('ht_virustotal').isBadFileHash( fileHash=fileHash )
	return renderMainPanel(request=request, popup_text=result)
	