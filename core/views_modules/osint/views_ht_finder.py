from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for findAll
def findAll(request):
	# Init of the view findAll
	try:
		# Pool call
		response, repool = sendPool(request, 'findAll')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Execute, get result and show it
			result = ht.getModule('ht_finder').findAll( username=username )
			if request.POST.get('is_async_findAll', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_findAll', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for checkerOnline
def checkerOnline(request):
	# Init of the view checkerOnline
	try:
		# Pool call
		response, repool = sendPool(request, 'checkerOnline')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Execute, get result and show it
			result = ht.getModule('ht_finder').checkerOnline( username=username )
			if request.POST.get('is_async_checkerOnline', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_checkerOnline', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	