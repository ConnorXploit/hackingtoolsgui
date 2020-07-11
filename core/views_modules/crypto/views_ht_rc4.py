from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for decrypt
def decrypt(request):
	# Init of the view decrypt
	try:
		# Pool call
		response, repool = sendPool(request, 'decrypt')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter password
			password = request.POST.get('password')

			# Parameter text
			text = request.POST.get('text')

			# Execute, get result and show it
			result = ht.getModule('ht_rc4').decrypt( password=password, text=text )
			if request.POST.get('is_async_decrypt', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_decrypt', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for encrypt
def encrypt(request):
	# Init of the view encrypt
	try:
		# Pool call
		response, repool = sendPool(request, 'encrypt')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter password
			password = request.POST.get('password')

			# Parameter text
			text = request.POST.get('text')

			# Execute, get result and show it
			result = ht.getModule('ht_rc4').encrypt( password=password, text=text )
			if request.POST.get('is_async_encrypt', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_encrypt', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	