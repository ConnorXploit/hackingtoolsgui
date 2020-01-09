from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for getConnectedDevices
def getConnectedDevices(request):
	# Init of the view getConnectedDevices
	try:
		# Pool call
		response, repool = sendPool(request, 'getConnectedDevices')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Execute, get result and show it
			result = ht.getModule('ht_nmap').getConnectedDevices( ip=ip )
			if request.POST.get('is_async_getConnectedDevices', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getConnectedDevices', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getDevicePorts
def getDevicePorts(request):
	# Init of the view getDevicePorts
	try:
		# Pool call
		response, repool = sendPool(request, 'getDevicePorts')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Parameter tcp (Optional - Default True)
			tcp = request.POST.get('tcp', True)

			# Parameter udp (Optional - Default False)
			udp = request.POST.get('udp', False)
			if not udp:
				udp = None

			# Execute, get result and show it
			result = ht.getModule('ht_nmap').getDevicePorts( ip=ip, tcp=tcp, udp=udp )
			if request.POST.get('is_async_getDevicePorts', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getDevicePorts', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for hasDevicePortOpened
def hasDevicePortOpened(request):
	# Init of the view hasDevicePortOpened
	try:
		# Pool call
		response, repool = sendPool(request, 'hasDevicePortOpened')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Parameter port
			port = request.POST.get('port')

			# Execute, get result and show it
			result = ht.getModule('ht_nmap').hasDevicePortOpened( ip=ip, port=port )
			if request.POST.get('is_async_hasDevicePortOpened', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_hasDevicePortOpened', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getCVEsFromHost
def getCVEsFromHost(request):
	# Init of the view getCVEsFromHost
	try:
		# Pool call
		response, repool = sendPool(request, 'getCVEsFromHost')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Execute, get result and show it
			result = ht.getModule('ht_nmap').getCVEsFromHost( ip=ip )
			if request.POST.get('is_async_getCVEsFromHost', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getCVEsFromHost', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	