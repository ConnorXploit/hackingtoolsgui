from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for readFileToType
def readFileToType(request):
	# Init of the view readFileToType
	try:
		# Pool call
		response, repool = sendPool(request, 'readFileToType')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file filename
				filename_filename, location_filename, filename = saveFileOutput(request.FILES['filename'], 'parser', 'files')
			except Exception as e:
				# If not param filename
				if request.POST.get('is_async_readFileToType', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter typeToExport
			typeToExport = request.POST.get('typeToExport')

			# Parameter typeOf (Optional - Default None)
			typeOf = request.POST.get('typeOf', None)
			if not typeOf:
				typeOf = None

			# Parameter csv_headers (Optional - Default False)
			csv_headers = request.POST.get('csv_headers', False)

			# Execute, get result and show it
			result = ht.getModule('ht_parser').readFileToType( filename=filename, typeToExport=typeToExport, typeOf=typeOf, csv_headers=csv_headers )
			if request.POST.get('is_async_readFileToType', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_readFileToType', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	