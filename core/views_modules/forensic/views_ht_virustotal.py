from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for isBadFile
def isBadFile(request):
	# Init of the view isBadFile
	try:
		# Pool call
		response, repool = sendPool(request, 'isBadFile')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file filename
				filename_filename, location_filename, filename = saveFileOutput(request.FILES['filename'], 'virustotal', 'forensic')
			except Exception as e:
				# If not param filename
				if request.POST.get('is_async_isBadFile', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_virustotal').isBadFile( filename=filename )
			if request.POST.get('is_async_isBadFile', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_isBadFile', False):
			return JsonResponse({ "data" : str(e) })
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
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file fileHash
				filename_fileHash, location_fileHash, fileHash = saveFileOutput(request.FILES['fileHash'], 'virustotal', 'forensic')
			except Exception as e:
				# If not param fileHash
				if request.POST.get('is_async_isBadFileHash', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_virustotal').isBadFileHash( fileHash=fileHash )
			if request.POST.get('is_async_isBadFileHash', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_isBadFileHash', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	