from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for searchCVE
def searchCVE(request):
	# Init of the view searchCVE
	try:
		# Pool call
		response, repool = sendPool(request, 'searchCVE')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter cve_id (Optional - Default )
			cve_id = request.POST.get('cve_id', '')
			if not cve_id:
				cve_id = None

			# Execute, get result and show it
			result = ht.getModule('ht_cve').searchCVE( cve_id=cve_id )
			if request.POST.get('is_async_searchCVE', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchCVE', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	