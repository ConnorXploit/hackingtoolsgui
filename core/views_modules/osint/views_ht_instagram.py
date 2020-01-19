from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for getAccountByUsername
def getAccountByUsername(request):
	# Init of the view getAccountByUsername
	try:
		# Pool call
		response, repool = sendPool(request, 'getAccountByUsername')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Execute, get result and show it
			result = ht.getModule('ht_instagram').getAccountByUsername( username=username )
			if request.POST.get('is_async_getAccountByUsername', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getAccountByUsername', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	