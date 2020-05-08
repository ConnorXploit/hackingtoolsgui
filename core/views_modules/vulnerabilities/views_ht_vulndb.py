from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for getAPI
def getAPI(request):
	# Init of the view getAPI
	try:
		# Pool call
		response, repool = sendPool(request, 'getAPI')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter vulndb_api (Optional - Default None)
			vulndb_api = request.POST.get('vulndb_api', None)
			if not vulndb_api:
				vulndb_api = None

			# Parameter session_id (Optional - Default None)
			session_id = request.POST.get('session_id', None)
			if not session_id:
				session_id = None

			# Execute, get result and show it
			result = ht.getModule('ht_vulndb').getAPI( vulndb_api=vulndb_api, session_id=session_id )
			if request.POST.get('is_async_getAPI', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getAPI', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getCVEInfo
def getCVEInfo(request):
	# Init of the view getCVEInfo
	try:
		# Pool call
		response, repool = sendPool(request, 'getCVEInfo')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter CVE
			CVE = request.POST.get('CVE')

			# Parameter references (Optional - Default False)
			references = request.POST.get('references', False)

			# Parameter vulndb_api (Optional - Default None)
			vulndb_api = request.POST.get('vulndb_api', None)
			if not vulndb_api:
				vulndb_api = None

			# Parameter session_id (Optional - Default None)
			session_id = request.POST.get('session_id', None)
			if not session_id:
				session_id = None

			# Execute, get result and show it
			result = ht.getModule('ht_vulndb').getCVEInfo( CVE=CVE, references=references, vulndb_api=vulndb_api, session_id=session_id )
			if request.POST.get('is_async_getCVEInfo', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getCVEInfo', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getSuggestions
def getSuggestions(request):
	# Init of the view getSuggestions
	try:
		# Pool call
		response, repool = sendPool(request, 'getSuggestions')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter fieldType
			fieldType = request.POST.get('fieldType')

			# Parameter fieldName
			fieldName = request.POST.get('fieldName')

			# Parameter vulndb_api (Optional - Default None)
			vulndb_api = request.POST.get('vulndb_api', None)
			if not vulndb_api:
				vulndb_api = None

			# Parameter session_id (Optional - Default None)
			session_id = request.POST.get('session_id', None)
			if not session_id:
				session_id = None

			# Execute, get result and show it
			result = ht.getModule('ht_vulndb').getSuggestions( fieldType=fieldType, fieldName=fieldName, vulndb_api=vulndb_api, session_id=session_id )
			if request.POST.get('is_async_getSuggestions', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getSuggestions', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	