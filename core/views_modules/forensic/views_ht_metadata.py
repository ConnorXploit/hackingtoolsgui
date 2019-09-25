from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

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

# Automatic view function for get_image_exif
@csrf_exempt
def get_image_exif(request):
	# Init of the view get_image_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_image_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Save file filename
			filename_filename, location_filename, filename = saveFileOutput(request.FILES['filename'], 'metadata', 'forensic')

			# Execute, get result and show it
			result = ht.getModule('ht_metadata').get_image_exif( filename=filename )
			if request.POST.get('is_async', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_pdf_exif
@csrf_exempt
def get_pdf_exif(request):
	# Init of the view get_pdf_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_pdf_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Save file pdf_file
			filename_pdf_file, location_pdf_file, pdf_file = saveFileOutput(request.FILES['pdf_file'], 'metadata', 'forensic')

			# Execute, get result and show it
			result = ht.getModule('ht_metadata').get_pdf_exif( pdf_file=pdf_file )
			if request.POST.get('is_async', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		return renderMainPanel(request=request, popup_text=str(e))
	