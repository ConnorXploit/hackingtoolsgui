from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.
	
# Automatic view function for getIPListfromServices
def getIPListfromServices(request):
	# Init of the view getIPListfromServices
	try:
		# Pool call
		response, repool = sendPool(request, 'getIPListfromServices')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter serviceName
			serviceName = request.POST.get('serviceName')

			# Parameter shodan_api (Optional - Default None)
			shodan_api = request.POST.get('shodan_api', None)
			if not shodan_api:
				shodan_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').getIPListfromServices( serviceName=serviceName, shodan_api=shodan_api )
			if request.POST.get('is_async_getIPListfromServices', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getIPListfromServices', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for search_host
def search_host(request):
	# Init of the view search_host
	try:
		# Pool call
		response, repool = sendPool(request, 'search_host')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Parameter shodan_api (Optional - Default None)
			shodan_api = request.POST.get('shodan_api', None)
			if not shodan_api:
				shodan_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').search_host( ip=ip, shodan_api=shodan_api )
			if request.POST.get('is_async_search_host', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_search_host', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getSSLCerts
def getSSLCerts(request):
	# Init of the view getSSLCerts
	try:
		# Pool call
		response, repool = sendPool(request, 'getSSLCerts')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Parameter shodan_api (Optional - Default None)
			shodan_api = request.POST.get('shodan_api', None)
			if not shodan_api:
				shodan_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').getSSLCerts( ip=ip, shodan_api=shodan_api )
			if request.POST.get('is_async_getSSLCerts', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getSSLCerts', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for queryShodan
def queryShodan(request):
	# Init of the view queryShodan
	try:
		# Pool call
		response, repool = sendPool(request, 'queryShodan')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter category (Optional - Default )
			category = request.POST.get('category', '')
			if not category:
				category = None

			# Parameter osintDays (Optional - Default 100)
			osintDays = request.POST.get('osintDays', 100)

			# Parameter shodan_api (Optional - Default None)
			shodan_api = request.POST.get('shodan_api', None)
			if not shodan_api:
				shodan_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').queryShodan( category=category, osintDays=osintDays, shodan_api=shodan_api )
			if request.POST.get('is_async_queryShodan', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_queryShodan', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for searchFromConfig
def searchFromConfig(request):
	# Init of the view searchFromConfig
	try:
		# Pool call
		response, repool = sendPool(request, 'searchFromConfig')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter search (Optional - Default )
			search = request.POST.get('search', '')
			if not search:
				search = None

			# Parameter keyword (Optional - Default )
			keyword = request.POST.get('keyword', '')
			if not keyword:
				keyword = None

			# Parameter shodan_api (Optional - Default None)
			shodan_api = request.POST.get('shodan_api', None)
			if not shodan_api:
				shodan_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').searchFromConfig( search=search, keyword=keyword, shodan_api=shodan_api )
			if request.POST.get('is_async_searchFromConfig', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchFromConfig', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for setApi
def setApi(request):
	# Init of the view setApi
	try:
		# Pool call
		response, repool = sendPool(request, 'setApi')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_shodan').setApi()
			pass
	except Exception as e:
		if request.POST.get('is_async_setApi', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	