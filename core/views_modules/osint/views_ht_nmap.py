from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

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

def getDevicePorts(request):
	ip = request.POST.get('ip')
	tcp = request.POST.get('tcp', True)
	udp = request.POST.get('udp', False)
	result = ht.getModule('ht_nmap').getDevicePorts( ip=ip, tcp=tcp, udp=udp )
	return renderMainPanel(request=request, popup_text=result)
	
def hasDevicePortOpened(request):
	ip = request.POST.get('ip')
	port = request.POST.get('port')
	result = ht.getModule('ht_nmap').hasDevicePortOpened( ip=ip, port=port )
	return renderMainPanel(request=request, popup_text=result)
	