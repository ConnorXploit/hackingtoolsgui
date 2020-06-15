from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for createShortcut
def createShortcut(request):
	# Init of the view createShortcut
	try:
		# Pool call
		response, repool = sendPool(request, 'createShortcut')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter url
			url = request.POST.get('url')

			# Parameter fakeUrl
			fakeUrl = request.POST.get('fakeUrl')

			# Parameter fakeText
			fakeText = request.POST.get('fakeText')

			# Parameter domainShortener (Optional - Default tinyurl)
			domainShortener = str(request.POST.get('domainShortener', 'tinyurl'))

			# Parameter api_key (Optional - Default None)
			api_key = request.POST.get('api_key', None)
			if not api_key:
				api_key = None

			# Parameter user_id (Optional - Default None)
			user_id = request.POST.get('user_id', None)
			if not user_id:
				user_id = None

			# Execute, get result and show it
			result = ht.getModule('ht_urlshortener').createShortcut( url=url, fakeUrl=fakeUrl, fakeText=fakeText, domainShortener=domainShortener, api_key=api_key, user_id=user_id )
			if request.POST.get('is_async_createShortcut', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_createShortcut', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getShortDomains
def getShortDomains(request):
	# Init of the view getShortDomains
	try:
		# Pool call
		response, repool = sendPool(request, 'getShortDomains')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_urlshortener').getShortDomains()
			if request.POST.get('is_async_getShortDomains', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getShortDomains', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	