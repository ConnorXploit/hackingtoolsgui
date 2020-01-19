from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for get_posts
def get_posts(request):
	# Init of the view get_posts
	try:
		# Pool call
		response, repool = sendPool(request, 'get_posts')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter account (Optional - Default None)
			account = request.POST.get('account', None)
			if not account:
				account = None

			# Parameter group (Optional - Default None)
			group = request.POST.get('group', None)
			if not group:
				group = None

			# Parameter pages (Optional - Default 10)
			pages = int(request.POST.get('pages', 10))

			# Parameter timeout (Optional - Default 5)
			timeout = int(request.POST.get('timeout', 5))

			# Parameter sleep (Optional - Default 0)
			sleep = int(request.POST.get('sleep', 0))

			# Parameter credentials (Optional - Default None)
			credentials = request.POST.get('credentials', None)
			if not credentials:
				credentials = None

			# Execute, get result and show it
			result = ht.getModule('ht_facebook').get_posts( account=account, group=group, pages=pages, timeout=timeout, sleep=sleep, credentials=credentials )
			if request.POST.get('is_async_get_posts', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_posts', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	