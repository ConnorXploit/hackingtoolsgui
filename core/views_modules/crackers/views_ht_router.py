from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for getDefaultLogin
def getDefaultLogin(request):
	# Init of the view getDefaultLogin
	try:
		# Pool call
		response, repool = sendPool(request, 'getDefaultLogin')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter routerBrand (Optional - Default cisco)
			routerBrand = str(request.POST.get('routerBrand', 'cisco'))

			# Execute, get result and show it
			result = ht.getModule('ht_router').getDefaultLogin( routerBrand=routerBrand )
			if request.POST.get('is_async_getDefaultLogin', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getDefaultLogin', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getBrands
def getBrands(request):
	# Init of the view getBrands
	try:
		# Pool call
		response, repool = sendPool(request, 'getBrands')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_router').getBrands()
			if request.POST.get('is_async_getBrands', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getBrands', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	