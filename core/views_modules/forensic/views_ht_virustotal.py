from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

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

# Automatic view function for isBadFileHash
def isBadFileHash(request):
	# Init of the view isBadFileHash
	try:
		# Pool call
		response, repool = sendPool(request, 'isBadFileHash')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Save file fileHash
			filename_fileHash, location_fileHash, fileHash = saveFileOutput(request.POST.get('fileHash'), 'virustotal', 'forensic')

			# Execute, get result and show it
			result = ht.getModule('ht_virustotal').isBadFileHash( fileHash=fileHash )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		return renderMainPanel(request=request, popup_text=str(e))
	