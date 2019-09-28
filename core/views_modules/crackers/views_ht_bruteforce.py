from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool, getDictionaryAlphabet

# Create your views here.

# Automatic view function for crackZip
@csrf_exempt
def crackZip(request):
	# Init of the view crackZip
	try:
		# Pool call
		response, repool = sendPool(request, 'crackZip')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file zipPathName
				filename_zipPathName, location_zipPathName, zipPathName = saveFileOutput(request.FILES['zipPathName'], 'bruteforce', 'crackers')
			except Exception as e:
				# If not param zipPathName
				if request.POST.get('is_async_crackZip', False):
					return JsonResponse({ "error" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))

			# Parameter unzipper (Optional - Default None)
			unzipper = request.POST.get('unzipper', None)
			if not unzipper:
				unzipper = None

			# Parameter alphabet (Optional - Default lalpha)
			used_alphabet = 'lalpha'
			bruteforce_numeric = request.POST.get('bruteforce_numeric', False)
			bruteforce_lower = request.POST.get('bruteforce_lower', False)
			bruteforce_upper = request.POST.get('bruteforce_upper', False)
			bruteforce_simbols = request.POST.get('bruteforce_simbols', False)
			bruteforce_simbols_all = request.POST.get('bruteforce_simbols_all', False)

			used_alphabet = getDictionaryAlphabet(numeric=bruteforce_numeric, lower=bruteforce_lower, upper=bruteforce_upper, simbols14=bruteforce_simbols, simbolsAll=bruteforce_simbols_all)

			# Parameter password_length (Optional - Default 4)
			password_length = request.POST.get('password_length', 4)

			# Parameter password_pattern (Optional - Default None)
			password_pattern = request.POST.get('password_pattern', None)
			if not password_pattern:
				password_pattern = None

			# Parameter log (Optional - Default False)
			log = request.POST.get('log', False)
			if not log:
				log = None

			# Execute, get result and show it
			result = ht.getModule('ht_bruteforce').crackZip( zipPathName=zipPathName, unzipper=unzipper, alphabet=used_alphabet, password_length=password_length, password_pattern=password_pattern, log=log )
			if request.POST.get('is_async_crackZip', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_crackZip', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	