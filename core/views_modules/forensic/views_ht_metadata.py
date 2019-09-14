from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

# ht_metadta

def get_metadata_exif(request):
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

def get_pdf_exif(request):
	pdf_file = request.POST.get('pdf_file')
	result = ht.getModule('ht_metadata').get_pdf_exif( pdf_file=pdf_file )
	return renderMainPanel(request=request, popup_text=result)

def get_image_exif(request):
    f = request.POST.get('filename')
    filename, location, uploaded_file_url = saveFileOutput(f, "metadata", "forensic")
    result = ht.getModule('ht_metadata').get_image_exif( filename=uploaded_file_url )
    return renderMainPanel(request=request, popup_text=result)