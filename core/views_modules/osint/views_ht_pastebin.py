from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for search_pastebin
def search_pastebin(request):
	# Init of the view search_pastebin
	try:
		# Pool call
		response, repool = sendPool(request, 'search_pastebin')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter keywords
			keywords = request.POST.get('keywords')

			# Parameter run_time (Optional - Default 0)
			run_time = request.POST.get('run_time', 0)
			if not run_time:
				run_time = None

			# Parameter match_total (Optional - Default None)
			match_total = request.POST.get('match_total', None)
			if not match_total:
				match_total = None

			# Parameter crawl_total (Optional - Default None)
			crawl_total = request.POST.get('crawl_total', None)
			if not crawl_total:
				crawl_total = None

			# Execute, get result and show it
			result = ht.getModule('ht_pastebin').search_pastebin( keywords=keywords, run_time=run_time, match_total=match_total, crawl_total=crawl_total )
			if request.POST.get('is_async_search_pastebin', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_search_pastebin', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	