from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for hashContent
def hashContent(request):
	# Init of the view hashContent
	try:
		# Pool call
		response, repool = sendPool(request, 'hashContent')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter content
			content = request.POST.get('content')

			# Execute, get result and show it
			result = ht.getModule('ht_hash').hashContent( content=content )
			if request.POST.get('is_async_hashContent', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_hashContent', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	