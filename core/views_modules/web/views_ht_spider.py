from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for crawl
def crawl(request):
	# Init of the view crawl
	try:
		# Pool call
		response, repool = sendPool(request, 'crawl')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter url
			url = request.POST.get('url')

			# Parameter depth (Optional - Default 100)
			depth = request.POST.get('depth', 100)

			# Parameter proxies (Optional - Default None)
			proxies = request.POST.get('proxies', None)
			if not proxies:
				proxies = None

			# Parameter proxyhost (Optional - Default None)
			proxyhost = request.POST.get('proxyhost', None)
			if not proxyhost:
				proxyhost = None

			# Parameter proxyuser (Optional - Default None)
			proxyuser = request.POST.get('proxyuser', None)
			if not proxyuser:
				proxyuser = None

			# Parameter proxypassword (Optional - Default None)
			proxypassword = request.POST.get('proxypassword', None)
			if not proxypassword:
				proxypassword = None

			# Parameter proxyport (Optional - Default None)
			proxyport = request.POST.get('proxyport', None)
			if not proxyport:
				proxyport = None

			# Parameter proxysecure (Optional - Default http)
			proxysecure = request.POST.get('proxysecure', 'http')

			# Execute, get result and show it
			result = ht.getModule('ht_spider').crawl( url=url, depth=depth, proxies=proxies, proxyhost=proxyhost, proxyuser=proxyuser, proxypassword=proxypassword, proxyport=proxyport, proxysecure=proxysecure )
			if request.POST.get('is_async_crawl', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_crawl', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	