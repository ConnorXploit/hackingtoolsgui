from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# ht_shodan

@csrf_exempt
def getIPListfromServices(request):
    if request.POST.get('service_name'):
        service_name = request.POST.get('service_name')
        shodan_key = None
        if request.POST.get('shodanKeyString'):
            shodan_key = request.POST.get('shodanKeyString')
        shodan = ht.getModule('ht_shodan')
        response_shodan = shodan.getIPListfromServices(serviceName=service_name, shodanKeyString=shodan_key)
        resp_text = ','.join(response_shodan)
        if request.POST.get('is_async_getIPListfromServices', False):
            data = {
                'data' : resp_text
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=resp_text)
    else:
        return renderMainPanel(request=request)

@csrf_exempt
def search_host(request):
    if request.POST.get('service_ip'):
        service_ip = request.POST.get('service_ip')
        shodan = ht.getModule('ht_shodan')
        response_shodan = shodan.search_host(service_ip)
        if request.POST.get('is_async_search_host', False):
            data = {
                'data' : response_shodan
            }
            return JsonResponse(data)
        return renderMainPanel(request=request, popup_text=response_shodan)
    else:
        return renderMainPanel(request=request)

# End ht_shodan

# Automatic view function for getSSLCerts
@csrf_exempt
def getSSLCerts(request):
	# Init of the view getSSLCerts
	try:
		# Pool call
		response, repool = sendPool(request, 'getSSLCerts')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').getSSLCerts( ip=ip )
			if request.POST.get('is_async_getSSLCerts', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getSSLCerts', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for queryShodan
@csrf_exempt
def queryShodan(request):
	# Init of the view queryShodan
	try:
		# Pool call
		response, repool = sendPool(request, 'queryShodan')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter category (Optional - Default )
			category = request.POST.get('category', '')
			if not category:
				category = None

			# Parameter osintDays (Optional - Default 100)
			osintDays = request.POST.get('osintDays', 100)

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').queryShodan( category=category, osintDays=osintDays )
			if request.POST.get('is_async_queryShodan', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_queryShodan', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for searchFromConfig
@csrf_exempt
def searchFromConfig(request):
	# Init of the view searchFromConfig
	try:
		# Pool call
		response, repool = sendPool(request, 'searchFromConfig')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter search (Optional - Default )
			search = request.POST.get('search', '')
			if not search:
				search = None

			# Parameter keyword (Optional - Default )
			keyword = request.POST.get('keyword', '')
			if not keyword:
				keyword = None

			# Execute, get result and show it
			result = ht.getModule('ht_shodan').searchFromConfig( search=search, keyword=keyword )
			if request.POST.get('is_async_searchFromConfig', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchFromConfig', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for setApi
@csrf_exempt
def setApi(request):
	# Init of the view setApi
	try:
		# Pool call
		response, repool = sendPool(request, 'setApi')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter shodanKeyString (Optional - Default None)
			shodanKeyString = request.POST.get('shodanKeyString', None)
			if not shodanKeyString:
				shodanKeyString = None

			# Execute the function
			ht.getModule('ht_shodan').setApi( shodanKeyString=shodanKeyString )
	except Exception as e:
		if request.POST.get('is_async_setApi', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	