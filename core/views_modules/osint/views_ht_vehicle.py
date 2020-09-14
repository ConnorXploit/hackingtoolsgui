from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for searchIdentificationPlate
def searchIdentificationPlate(request):
	# Init of the view searchIdentificationPlate
	try:
		# Pool call
		response, repool = sendPool(request, 'searchIdentificationPlate')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter plate
			plate = request.POST.get('plate')

			# Execute, get result and show it
			result = ht.getModule('ht_vehicle').searchIdentificationPlate( plate=plate )
			if request.POST.get('is_async_searchIdentificationPlate', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchIdentificationPlate', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	