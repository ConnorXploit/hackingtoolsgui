from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

	
# Automatic view function for grabPortBanner
def grabPortBanner(request):
	# Init of the view grabPortBanner
	try:
		# Pool call
		response, repool = sendPool(request, 'grabPortBanner')
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
			result = ht.getModule('ht_bannergrabber').grabPortBanner( ip=ip, port=port )
			if request.POST.get('is_async_grabPortBanner', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_grabPortBanner', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	