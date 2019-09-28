from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# ht_rsa
@csrf_exempt
def encrypt(request):
    if request.POST.get('private_key_keynumber') and request.POST.get('private_key_keymod') and request.POST.get('cipher_text'):
        priv_key_k = request.POST.get('private_key_keynumber')
        priv_key_n = request.POST.get('private_key_keymod')
        text = request.POST.get('cipher_text')
        crypter = views.ht.getModule('ht_rsa')
        crypted_text = crypter.encrypt(private_key=(int(priv_key_k), int(priv_key_n)), plaintext=text.encode())
        if request.POST.get('is_async_encrypt', False):
            data = {
                'data' : crypted_text
            }
            return JsonResponse(data)
        return views.renderMainPanel(request=request, popup_text=crypted_text)
    else:
        return views.renderMainPanel(request=request)

@csrf_exempt
def decrypt(request):
    if request.POST.get('public_key_keynumber') and request.POST.get('public_key_keymod') and request.POST.get('decipher_text'):
        pub_key_k = request.POST.get('public_key_keynumber')
        pub_key_n = request.POST.get('public_key_keymod')
        text = request.POST.get('decipher_text')
        crypter = views.ht.getModule('ht_rsa')
        decrypted_text = crypter.decrypt(public_key=(int(pub_key_k), int(pub_key_n)), ciphertext=text)
        if request.POST.get('is_async_decrypt', False):
            data = {
                'data' : decrypted_text
            }
            return JsonResponse(data)
        return views.renderMainPanel(request=request, popup_text=decrypted_text)
    else:
        return views.renderMainPanel(request=request)

@csrf_exempt
def getRandomKeypair(request):
    response, repool = views.sendPool(request, "getRandomKeypair")
    if response or repool:
        if repool:
            return HttpResponse(response)
        return views.renderMainPanel(request=request, popup_text=response.text)
    else:
        length = None
        if request.POST.get('prime_length'):
            length = request.POST.get('prime_length')
        crypter = views.ht.getModule('ht_rsa')
        keypair = (0, 0)
        if length:
            keypair = crypter.getRandomKeypair(int(length))
        else:
            keypair = crypter.getRandomKeypair()
        keypair = '({n1}, {n2})'.format(n1=keypair[0], n2=keypair[1])
        if request.POST.get('is_async_getRandomKeypair', False):
            data = {
                'data' : keypair
            }
            return JsonResponse(data)
        return views.renderMainPanel(request=request, popup_text=keypair)

@csrf_exempt
def generate_keypair(request):
    response, repool = views.sendPool(request, "generate_keypair")
    if response or repool:
        if repool:
            return HttpResponse(response)
        return views.renderMainPanel(request=request, popup_text=response.text)
    else:
        if request.POST.get('prime_a') and request.POST.get('prime_b'):
            prime_a = request.POST.get('prime_a')
            prime_b = request.POST.get('prime_b')
            crypter = views.ht.getModule('ht_rsa')
            keypair = crypter.generate_keypair(int(prime_a), int(prime_b))
            if not isinstance(keypair, str):
                try: 
                    keypair = '({n1}, {n2})'.format(n1=keypair[0], n2=keypair[1])
                except:
                    pass
            if request.POST.get('is_async_generate_keypair', False):
                data = {
                    'data' : keypair
                }
                return JsonResponse(data)
            return views.renderMainPanel(request=request, popup_text=keypair)
        else:
            return views.renderMainPanel(request=request)

# End ht_rsa
