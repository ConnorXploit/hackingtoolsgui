from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for get_followers
def get_followers(request):
	# Init of the view get_followers
	try:
		# Pool call
		response, repool = sendPool(request, 'get_followers')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Parameter limit (Optional - Default 1000)
			limit = int(request.POST.get('limit', 1000))

			# Parameter interval (Optional - Default 0)
			interval = int(request.POST.get('interval', 0))

			# Execute, get result and show it
			result = ht.getModule('ht_twitter').get_followers( username=username, limit=limit, interval=interval )
			if request.POST.get('is_async_get_followers', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_followers', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_friends
def get_friends(request):
	# Init of the view get_friends
	try:
		# Pool call
		response, repool = sendPool(request, 'get_friends')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Parameter limit (Optional - Default 1000)
			limit = int(request.POST.get('limit', 1000))

			# Parameter interval (Optional - Default 0)
			interval = int(request.POST.get('interval', 0))

			# Execute, get result and show it
			result = ht.getModule('ht_twitter').get_friends( username=username, limit=limit, interval=interval )
			if request.POST.get('is_async_get_friends', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_friends', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_timeline
def get_timeline(request):
	# Init of the view get_timeline
	try:
		# Pool call
		response, repool = sendPool(request, 'get_timeline')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Parameter limit (Optional - Default 1000)
			limit = int(request.POST.get('limit', 1000))

			# Parameter interval (Optional - Default 0)
			interval = int(request.POST.get('interval', 0))

			# Execute, get result and show it
			result = ht.getModule('ht_twitter').get_timeline( username=username, limit=limit, interval=interval )
			if request.POST.get('is_async_get_timeline', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_timeline', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_user
def get_user(request):
	# Init of the view get_user
	try:
		# Pool call
		response, repool = sendPool(request, 'get_user')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username
			username = request.POST.get('username')

			# Execute, get result and show it
			result = ht.getModule('ht_twitter').get_user( username=username )
			if request.POST.get('is_async_get_user', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_user', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for searchTweets
def searchTweets(request):
	# Init of the view searchTweets
	try:
		# Pool call
		response, repool = sendPool(request, 'searchTweets')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter username (Optional - Default )
			username = str(request.POST.get('username', ''))
			if not username:
				username = None

			# Parameter since (Optional - Default )
			since = str(request.POST.get('since', ''))
			if not since:
				since = None

			# Parameter until (Optional - Default )
			until = str(request.POST.get('until', ''))
			if not until:
				until = None

			# Parameter query (Optional - Default )
			query = str(request.POST.get('query', ''))
			if not query:
				query = None

			# Parameter limit (Optional - Default 1000)
			limit = int(request.POST.get('limit', 1000))

			# Parameter verified (Optional - Default False)
			verified = int(request.POST.get('verified', False))

			# Parameter proxy (Optional - Default )
			proxy = str(request.POST.get('proxy', ''))
			if not proxy:
				proxy = None

			# Parameter interval (Optional - Default 0)
			interval = int(request.POST.get('interval', 0))

			# Execute, get result and show it
			result = ht.getModule('ht_twitter').searchTweets( username=username, since=since, until=until, query=query, limit=limit, verified=verified, proxy=proxy, interval=interval )
			if request.POST.get('is_async_searchTweets', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_searchTweets', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	