from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for traceroute
def traceroute(request):
	# Init of the view traceroute
	try:
		# Pool call
		response, repool = sendPool(request, 'traceroute')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter domain_or_ip
			domain_or_ip = request.POST.get('domain_or_ip')

			# Execute, get result and show it
			result = ht.getModule('ht_scapy').traceroute( domain_or_ip=domain_or_ip )
			if request.POST.get('is_async_traceroute', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_traceroute', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	