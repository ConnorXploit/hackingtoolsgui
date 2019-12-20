from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for mensaje
def mensaje(request):
	# Init of the view mensaje
	try:
		# Pool call
		response, repool = sendPool(request, 'mensaje')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter men1
			men1 = request.POST.get('men1')

			# Parameter edad (Optional - Default 19)
			edad = int(request.POST.get('edad', 19))

			# Parameter casado (Optional - Default False)
			casado = request.POST.get('casado', False)
			if not casado:
				casado = None

			# Execute, get result and show it
			result = ht.getModule('ht_pastebin').mensaje( men1=men1, edad=edad, casado=casado )
			if request.POST.get('is_async_mensaje', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_mensaje', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	