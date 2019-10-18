from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

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
			# Parameter private_key
			private_key = request.POST.get('private_key')

			# Parameter plaintext
			plaintext = request.POST.get('plaintext')

			# Execute, get result and show it
			result = ht.getModule('ht_rsa').encrypt( private_key=private_key, plaintext=plaintext )
			if request.POST.get('is_async_encrypt', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_encrypt', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
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
			# Parameter public_key
			public_key = request.POST.get('public_key')

			# Parameter ciphertext
			ciphertext = request.POST.get('ciphertext')

			# Execute, get result and show it
			result = ht.getModule('ht_rsa').decrypt( public_key=public_key, ciphertext=ciphertext )
			if request.POST.get('is_async_decrypt', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_decrypt', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for generate_keypair
def generate_keypair(request):
	# Init of the view generate_keypair
	try:
		# Pool call
		response, repool = sendPool(request, 'generate_keypair')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter prime_a
			prime_a = request.POST.get('prime_a')

			# Parameter prime_b
			prime_b = request.POST.get('prime_b')

			# Execute, get result and show it
			result1, result2 = ht.getModule('ht_rsa').generate_keypair( prime_a=int(prime_a), prime_b=int(prime_b) )
			if request.POST.get('is_async_generate_keypair', False):
				return JsonResponse({ "data" : '({n1},{n2})'.format(n1=result1, n2=result2) })
			return renderMainPanel(request=request, popup_text='({n1},{n2})'.format(n1=result1, n2=result2))
	except Exception as e:
		if request.POST.get('is_async_generate_keypair', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getRandomKeypair
def getRandomKeypair(request):
	# Init of the view getRandomKeypair
	try:
		# Pool call
		response, repool = sendPool(request, 'getRandomKeypair')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter length (Optional - Default 8)
			length = request.POST.get('length', 8)

			# Execute, get result and show it
			result = ht.getModule('ht_rsa').getRandomKeypair( length=length )
			if request.POST.get('is_async_getRandomKeypair', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getRandomKeypair', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	