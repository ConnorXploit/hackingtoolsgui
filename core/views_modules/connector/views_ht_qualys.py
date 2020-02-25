from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for connect
def connect(request):
	# Init of the view connect
	try:
		# Pool call
		response, repool = sendPool(request, 'connect')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Parameter password
			password = request.POST.get('password')

			# Execute, get result and show it
			result = ht.getModule('ht_qualys').connect( username=username, password=password )
			if request.POST.get('is_async_connect', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_connect', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for disconnect
def disconnect(request):
	# Init of the view disconnect
	try:
		# Pool call
		response, repool = sendPool(request, 'disconnect')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_qualys').disconnect()
			if request.POST.get('is_async_disconnect', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_disconnect', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for scan
def scan(request):
	# Init of the view scan
	try:
		# Pool call
		response, repool = sendPool(request, 'scan')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ips
			ips = request.POST.get('ips')

			# Execute, get result and show it
			result = ht.getModule('ht_qualys').scan( ips=ips )
			if request.POST.get('is_async_scan', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_scan', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	