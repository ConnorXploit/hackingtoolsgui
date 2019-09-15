from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for cogerTablas
def cogerTablas(request):
	# Init of the view cogerTablas
	try:
		# Pool call
		response, repool = sendPool(request, 'cogerTablas')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').cogerTablas()
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Execute the function
			ht.getModule('ht_sqlinjection').mostrarUserPass()
	except Exception as e:
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for cantidadTuplasEnTapla
def cantidadTuplasEnTapla(request):
	# Init of the view cantidadTuplasEnTapla
	try:
		# Pool call
		response, repool = sendPool(request, 'cantidadTuplasEnTapla')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter tabla
			tabla = request.POST.get('tabla')
			
	# Parameter campo
			campo = request.POST.get('campo')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').cantidadTuplasEnTapla( tabla=tabla, campo=campo )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter tabla
			tabla = request.POST.get('tabla')
			
	# Parameter tabla_name
			tabla_name = request.POST.get('tabla_name')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').cogerColumnasTabla( tabla=tabla, tabla_name=tabla_name )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter user
			user = request.POST.get('user')
			
	# Parameter tabla
			tabla = request.POST.get('tabla')
			
	# Parameter idCampo
			idCampo = request.POST.get('idCampo')
			
	# Parameter campoConocido
			campoConocido = request.POST.get('campoConocido')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').cogerNombreDeTablaPorID( user=user, tabla=tabla, idCampo=idCampo, campoConocido=campoConocido )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter texto
			texto = request.POST.get('texto')
			
	# Parameter color
			color = request.POST.get('color')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').color( texto=texto, color=color )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter tabla_name
			tabla_name = request.POST.get('tabla_name')
			
	# Parameter table
			table = request.POST.get('table')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').compareTextExistWhereSubstringACII( tabla_name=tabla_name, table=table )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter sqli
			sqli = request.POST.get('sqli')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').ejecutarSQL( sqli=sqli )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter idCampo
			idCampo = request.POST.get('idCampo')
			
	# Parameter tabla
			tabla = request.POST.get('tabla')
			
	# Parameter campo
			campo = request.POST.get('campo')
			
	# Parameter campoConocido
			campoConocido = request.POST.get('campoConocido')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').longitudCampoIDtablaCampo( idCampo=idCampo, tabla=tabla, campo=campo, campoConocido=campoConocido )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter clave
			clave = request.POST.get('clave')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').md5_decrypt( clave=clave )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter tabla
			tabla = request.POST.get('tabla')
			
	# Parameter columna
			columna = request.POST.get('columna')
			
	# Parameter nombre_campo_id
			nombre_campo_id = request.POST.get('nombre_campo_id')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').sacarValorPorTablaColumnaID( tabla=tabla, columna=columna, nombre_campo_id=nombre_campo_id )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter url
			url = request.POST.get('url')
			
	# Parameter param_focus
			param_focus = request.POST.get('param_focus')

			# Parameter cookie (Optional - Default )
			cookie = request.POST.get('cookie', '')
			if not cookie:
				cookie = None

			# Parameter proxies (Optional - Default )
			proxies = request.POST.get('proxies', '')
			if not proxies:
				proxies = None

			# Parameter submit_name (Optional - Default )
			submit_name = request.POST.get('submit_name', '')
			if not submit_name:
				submit_name = None

			# Parameter security (Optional - Default )
			security = request.POST.get('security', '')
			if not security:
				security = None

			# Execute the function
			ht.getModule('ht_sqlinjection').setParams( url=url, param_focus=param_focus, cookie=cookie, proxies=proxies, submit_name=submit_name, security=security )
	except Exception as e:
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
			return renderMainPanel(request=request, popup_text=response.text)
		else:			
	# Parameter ascii_text
			ascii_text = request.POST.get('ascii_text')

			# Execute, get result and show it
			result = ht.getModule('ht_sqlinjection').transformAsciiToHex( ascii_text=ascii_text )
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		return renderMainPanel(request=request, popup_text=str(e))
	