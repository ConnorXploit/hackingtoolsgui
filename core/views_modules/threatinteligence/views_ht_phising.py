from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for search
def search(request):
	# Init of the view search
	try:
		# Pool call
		response, repool = sendPool(request, 'search')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter urls
			urls = request.POST.get('urls')

			# Parameter gsb_api (Optional - Default None)
			gsb_api = request.POST.get('gsb_api', None)
			if not gsb_api:
				gsb_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_phising').search( urls=urls, gsb_api=gsb_api )
			if request.POST.get('is_async_search', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_search', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))

	