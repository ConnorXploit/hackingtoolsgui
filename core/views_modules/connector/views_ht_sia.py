from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for getConsensus
def getConsensus(request):
	# Init of the view getConsensus
	try:
		# Pool call
		response, repool = sendPool(request, 'getConsensus')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getConsensus()
			if request.POST.get('is_async_getConsensus', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getConsensus', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getDaemonConstants
def getDaemonConstants(request):
	# Init of the view getDaemonConstants
	try:
		# Pool call
		response, repool = sendPool(request, 'getDaemonConstants')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getDaemonConstants()
			if request.POST.get('is_async_getDaemonConstants', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getDaemonConstants', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getDaemonVersion
def getDaemonVersion(request):
	# Init of the view getDaemonVersion
	try:
		# Pool call
		response, repool = sendPool(request, 'getDaemonVersion')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getDaemonVersion()
			if request.POST.get('is_async_getDaemonVersion', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getDaemonVersion', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getRenter
def getRenter(request):
	# Init of the view getRenter
	try:
		# Pool call
		response, repool = sendPool(request, 'getRenter')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getRenter()
			if request.POST.get('is_async_getRenter', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getRenter', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getRenterContracts
def getRenterContracts(request):
	# Init of the view getRenterContracts
	try:
		# Pool call
		response, repool = sendPool(request, 'getRenterContracts')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getRenterContracts()
			if request.POST.get('is_async_getRenterContracts', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getRenterContracts', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getRenterDownloads
def getRenterDownloads(request):
	# Init of the view getRenterDownloads
	try:
		# Pool call
		response, repool = sendPool(request, 'getRenterDownloads')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getRenterDownloads()
			if request.POST.get('is_async_getRenterDownloads', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getRenterDownloads', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getRenterFiles
def getRenterFiles(request):
	# Init of the view getRenterFiles
	try:
		# Pool call
		response, repool = sendPool(request, 'getRenterFiles')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getRenterFiles()
			if request.POST.get('is_async_getRenterFiles', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getRenterFiles', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getRenterPrices
def getRenterPrices(request):
	# Init of the view getRenterPrices
	try:
		# Pool call
		response, repool = sendPool(request, 'getRenterPrices')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getRenterPrices()
			if request.POST.get('is_async_getRenterPrices', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getRenterPrices', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getWallet
def getWallet(request):
	# Init of the view getWallet
	try:
		# Pool call
		response, repool = sendPool(request, 'getWallet')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getWallet()
			if request.POST.get('is_async_getWallet', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getWallet', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getWalletAddress
def getWalletAddress(request):
	# Init of the view getWalletAddress
	try:
		# Pool call
		response, repool = sendPool(request, 'getWalletAddress')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getWalletAddress()
			if request.POST.get('is_async_getWalletAddress', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getWalletAddress', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getWalletAddresses
def getWalletAddresses(request):
	# Init of the view getWalletAddresses
	try:
		# Pool call
		response, repool = sendPool(request, 'getWalletAddresses')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getWalletAddresses()
			if request.POST.get('is_async_getWalletAddresses', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getWalletAddresses', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getWalletBackup
def getWalletBackup(request):
	# Init of the view getWalletBackup
	try:
		# Pool call
		response, repool = sendPool(request, 'getWalletBackup')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getWalletBackup()
			if request.POST.get('is_async_getWalletBackup', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getWalletBackup', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getWalletSeeds
def getWalletSeeds(request):
	# Init of the view getWalletSeeds
	try:
		# Pool call
		response, repool = sendPool(request, 'getWalletSeeds')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getWalletSeeds()
			if request.POST.get('is_async_getWalletSeeds', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getWalletSeeds', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for getWalletTransactions
def getWalletTransactions(request):
	# Init of the view getWalletTransactions
	try:
		# Pool call
		response, repool = sendPool(request, 'getWalletTransactions')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_sia').getWalletTransactions()
			if request.POST.get('is_async_getWalletTransactions', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getWalletTransactions', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	