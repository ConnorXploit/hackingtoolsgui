from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for searchCWE
def searchCWE(request):
	# Init of the view searchCWE
	try:
		# Pool call
		response, repool = sendPool(request, 'searchCWE')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter cwe_id
			cwe_id = request.POST.get('cwe_id')

			# Execute, get result and show it
			result = ht.getModule('ht_cwe').searchCWE( cwe_id=cwe_id )
			if request.POST.get('is_async_searchCWE', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchCWE', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for searchWeakness
def searchWeakness(request):
	# Init of the view searchWeakness
	try:
		# Pool call
		response, repool = sendPool(request, 'searchWeakness')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter cwe_id
			cwe_id = request.POST.get('cwe_id')

			# Execute, get result and show it
			result = ht.getModule('ht_cwe').searchWeakness( cwe_id=cwe_id )
			if request.POST.get('is_async_searchWeakness', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchWeakness', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	