from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# Automatic view function for cantidadTuplasEnTapla
def cantidadTuplasEnTapla(request):
	# Init of the view cantidadTuplasEnTapla
	try:
		# Pool call
		response, repool = sendPool(request, 'cantidadTuplasEnTapla')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').cantidadTuplasEnTapla()
			pass
	except Exception as e:
		if request.POST.get('is_async_cantidadTuplasEnTapla', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for cogerColumnasTabla
def cogerColumnasTabla(request):
	# Init of the view cogerColumnasTabla
	try:
		# Pool call
		response, repool = sendPool(request, 'cogerColumnasTabla')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').cogerColumnasTabla()
			pass
	except Exception as e:
		if request.POST.get('is_async_cogerColumnasTabla', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for cogerNombreDeTablaPorID
def cogerNombreDeTablaPorID(request):
	# Init of the view cogerNombreDeTablaPorID
	try:
		# Pool call
		response, repool = sendPool(request, 'cogerNombreDeTablaPorID')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').cogerNombreDeTablaPorID()
			pass
	except Exception as e:
		if request.POST.get('is_async_cogerNombreDeTablaPorID', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for cogerTablas
def cogerTablas(request):
	# Init of the view cogerTablas
	try:
		# Pool call
		response, repool = sendPool(request, 'cogerTablas')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').cogerTablas()
			pass
	except Exception as e:
		if request.POST.get('is_async_cogerTablas', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for color
def color(request):
	# Init of the view color
	try:
		# Pool call
		response, repool = sendPool(request, 'color')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').color()
			pass
	except Exception as e:
		if request.POST.get('is_async_color', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for compareTextExistWhereSubstringACII
def compareTextExistWhereSubstringACII(request):
	# Init of the view compareTextExistWhereSubstringACII
	try:
		# Pool call
		response, repool = sendPool(request, 'compareTextExistWhereSubstringACII')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').compareTextExistWhereSubstringACII()
			pass
	except Exception as e:
		if request.POST.get('is_async_compareTextExistWhereSubstringACII', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for ejecutarSQL
def ejecutarSQL(request):
	# Init of the view ejecutarSQL
	try:
		# Pool call
		response, repool = sendPool(request, 'ejecutarSQL')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').ejecutarSQL()
			pass
	except Exception as e:
		if request.POST.get('is_async_ejecutarSQL', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for longitudCampoIDtablaCampo
def longitudCampoIDtablaCampo(request):
	# Init of the view longitudCampoIDtablaCampo
	try:
		# Pool call
		response, repool = sendPool(request, 'longitudCampoIDtablaCampo')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').longitudCampoIDtablaCampo()
			pass
	except Exception as e:
		if request.POST.get('is_async_longitudCampoIDtablaCampo', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for md5_decrypt
def md5_decrypt(request):
	# Init of the view md5_decrypt
	try:
		# Pool call
		response, repool = sendPool(request, 'md5_decrypt')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').md5_decrypt()
			pass
	except Exception as e:
		if request.POST.get('is_async_md5_decrypt', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for mostrarUserPass
def mostrarUserPass(request):
	# Init of the view mostrarUserPass
	try:
		# Pool call
		response, repool = sendPool(request, 'mostrarUserPass')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').mostrarUserPass()
			pass
	except Exception as e:
		if request.POST.get('is_async_mostrarUserPass', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for sacarValorPorTablaColumnaID
def sacarValorPorTablaColumnaID(request):
	# Init of the view sacarValorPorTablaColumnaID
	try:
		# Pool call
		response, repool = sendPool(request, 'sacarValorPorTablaColumnaID')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').sacarValorPorTablaColumnaID()
			pass
	except Exception as e:
		if request.POST.get('is_async_sacarValorPorTablaColumnaID', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for setParams
def setParams(request):
	# Init of the view setParams
	try:
		# Pool call
		response, repool = sendPool(request, 'setParams')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').setParams()
			pass
	except Exception as e:
		if request.POST.get('is_async_setParams', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for transformAsciiToHex
def transformAsciiToHex(request):
	# Init of the view transformAsciiToHex
	try:
		# Pool call
		response, repool = sendPool(request, 'transformAsciiToHex')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').transformAsciiToHex()
			pass
	except Exception as e:
		if request.POST.get('is_async_transformAsciiToHex', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	