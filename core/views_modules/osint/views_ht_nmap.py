from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# ht_nmap

def getConnectedDevices(request):
    if request.POST.get('ip'):
        ip_to_scan = request.POST.get('ip')
        nmap = ht.getModule('ht_nmap')
        response_nmap = nmap.getConnectedDevices(ip=ip_to_scan)
        resp_text = ','.join(response_nmap)
        if request.POST.get('is_async', False):
            data = {
                'data' : resp_text
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=resp_text)
    else:
        return renderMainPanel(request=request)

# End ht_nmap

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
			if request.POST.get('is_async', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			if request.POST.get('is_async', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		return renderMainPanel(request=request, popup_text=str(e))
	