from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for checkIP
def checkIP(request):
	# Init of the view checkIP
	try:
		# Pool call
		response, repool = sendPool(request, 'checkIP')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter ip
			ip = request.POST.get('ip')

			# Parameter score (Optional - Default False)
			score = request.POST.get('score', False)

			# Parameter totalReports (Optional - Default False)
			totalReports = request.POST.get('totalReports', False)

			# Parameter abuseipdb_api (Optional - Default None)
			abuseipdb_api = request.POST.get('abuseipdb_api', None)
			if not abuseipdb_api:
				abuseipdb_api = None

			# Execute, get result and show it
			result = ht.getModule('ht_abuseipdb').checkIP( ip=ip, score=score, totalReports=totalReports, abuseipdb_api=abuseipdb_api )
			if request.POST.get('is_async_checkIP', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_checkIP', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	