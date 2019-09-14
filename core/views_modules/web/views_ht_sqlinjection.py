from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

def cantidadTuplasEnTapla(request):
	tabla = request.POST.get('tabla')
	campo = request.POST.get('campo')
	result = ht.getModule('ht_sqlinjection').cantidadTuplasEnTapla( tabla=tabla, campo=campo )
	return renderMainPanel(request=request, popup_text=result)
	
def cogerColumnasTabla(request):
	tabla = request.POST.get('tabla')
	tabla_name = request.POST.get('tabla_name')
	result = ht.getModule('ht_sqlinjection').cogerColumnasTabla( tabla=tabla, tabla_name=tabla_name )
	return renderMainPanel(request=request, popup_text=result)
	
def cogerNombreDeTablaPorID(request):
	user = request.POST.get('user')
	tabla = request.POST.get('tabla')
	idCampo = request.POST.get('idCampo')
	campoConocido = request.POST.get('campoConocido')
	result = ht.getModule('ht_sqlinjection').cogerNombreDeTablaPorID( user=user, tabla=tabla, idCampo=idCampo, campoConocido=campoConocido )
	return renderMainPanel(request=request, popup_text=result)
	
def cogerTablas(request):
	ht.getModule('ht_sqlinjection').cogerTablas( )

def color(request):
	texto = request.POST.get('texto')
	color = request.POST.get('color')
	result = ht.getModule('ht_sqlinjection').color( texto=texto, color=color )
	return renderMainPanel(request=request, popup_text=result)
	
def compareTextExistWhereSubstringACII(request):
	tabla_name = request.POST.get('tabla_name')
	table = request.POST.get('table')
	result = ht.getModule('ht_sqlinjection').compareTextExistWhereSubstringACII( tabla_name=tabla_name, table=table )
	return renderMainPanel(request=request, popup_text=result)
	
def ejecutarSQL(request):
	sqli = request.POST.get('sqli')
	result = ht.getModule('ht_sqlinjection').ejecutarSQL( sqli=sqli )
	return renderMainPanel(request=request, popup_text=result)
	
def longitudCampoIDtablaCampo(request):
	idCampo = request.POST.get('idCampo')
	tabla = request.POST.get('tabla')
	campo = request.POST.get('campo')
	campoConocido = request.POST.get('campoConocido')
	result = ht.getModule('ht_sqlinjection').longitudCampoIDtablaCampo( idCampo=idCampo, tabla=tabla, campo=campo, campoConocido=campoConocido )
	return renderMainPanel(request=request, popup_text=result)
	
def md5_decrypt(request):
	clave = request.POST.get('clave')
	result = ht.getModule('ht_sqlinjection').md5_decrypt( clave=clave )
	return renderMainPanel(request=request, popup_text=result)
	
def mostrarUserPass(request):
	ht.getModule('ht_sqlinjection').mostrarUserPass( )

def sacarValorPorTablaColumnaID(request):
	tabla = request.POST.get('tabla')
	columna = request.POST.get('columna')
	nombre_campo_id = request.POST.get('nombre_campo_id')
	result = ht.getModule('ht_sqlinjection').sacarValorPorTablaColumnaID( tabla=tabla, columna=columna, nombre_campo_id=nombre_campo_id )
	return renderMainPanel(request=request, popup_text=result)
	
def setParams(request):
	url = request.POST.get('url')
	param_focus = request.POST.get('param_focus')
	cookie = request.POST.get('cookie', '')
	proxies = request.POST.get('proxies', '')
	submit_name = request.POST.get('submit_name', '')
	security = request.POST.get('security', '')
	ht.getModule('ht_sqlinjection').setParams( url=url, param_focus=param_focus, cookie=cookie, proxies=proxies, submit_name=submit_name, security=security )

def transformAsciiToHex(request):
	ascii_text = request.POST.get('ascii_text')
	result = ht.getModule('ht_sqlinjection').transformAsciiToHex( ascii_text=ascii_text )
	return renderMainPanel(request=request, popup_text=result)
	