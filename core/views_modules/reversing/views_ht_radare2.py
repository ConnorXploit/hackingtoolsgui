from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for getImports
def getImports(request):
	# Init of the view getImports
	try:
		# Pool call
		response, repool = sendPool(request, 'getImports')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file filemon
				filename_filemon, location_filemon, filemon = saveFileOutput(request.FILES['filemon'], 'radare2', 'reversing')
			except Exception as e:
				# If not param filemon
				if request.POST.get('is_async_getImports', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_radare2').getImports( filemon=filemon )
			if request.POST.get('is_async_getImports', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getImports', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	