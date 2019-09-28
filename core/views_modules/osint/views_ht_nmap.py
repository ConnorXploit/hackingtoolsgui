from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for getConnectedDevices
@csrf_exempt
def getConnectedDevices(request):
	# Init of the view getConnectedDevices
	try:
		# Pool call
		response, repool = sendPool(request, 'getConnectedDevices')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
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
@csrf_exempt
def getDevicePorts(request):
	# Init of the view getDevicePorts
	try:
		# Pool call
		response, repool = sendPool(request, 'getDevicePorts')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
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
@csrf_exempt
def hasDevicePortOpened(request):
	# Init of the view hasDevicePortOpened
	try:
		# Pool call
		response, repool = sendPool(request, 'hasDevicePortOpened')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
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
	