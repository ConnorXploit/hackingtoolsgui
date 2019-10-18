from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for extractFile
def extractFile(request):
	# Init of the view extractFile
	try:
		# Pool call
		response, repool = sendPool(request, 'extractFile')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file zipPathName
				filename_zipPathName, location_zipPathName, zipPathName = saveFileOutput(request.FILES['zipPathName'], 'unzip', 'crackers')
			except Exception as e:
				# If not param zipPathName
				if request.POST.get('is_async_extractFile', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter password (Optional - Default None)
			password = request.POST.get('password', None)
			if not password:
				password = None

			# Execute, get result and show it
			result = ht.getModule('ht_unzip').extractFile( zipPathName=zipPathName, password=password )
			if request.POST.get('is_async_extractFile', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_extractFile', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for extractFilePassword
def extractFilePassword(request):
	# Init of the view extractFilePassword
	try:
		# Pool call
		response, repool = sendPool(request, 'extractFilePassword')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file zipPathName
				filename_zipPathName, location_zipPathName, zipPathName = saveFileOutput(request.FILES['zipPathName'], 'unzip', 'crackers')
			except Exception as e:
				# If not param zipPathName
				if request.POST.get('is_async_extractFilePassword', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter password (Optional - Default )
			password = request.POST.get('password', '')
			if not password:
				password = None

			# Parameter posible_combinations (Optional - Default 1)
			posible_combinations = request.POST.get('posible_combinations', 1)

			# Parameter output_dir_new (Optional - Default None)
			output_dir_new = request.POST.get('output_dir_new', None)
			if not output_dir_new:
				output_dir_new = None

			# Execute, get result and show it
			result = ht.getModule('ht_unzip').extractFilePassword( zipPathName=zipPathName, password=password, posible_combinations=posible_combinations, output_dir_new=output_dir_new )
			if request.POST.get('is_async_extractFilePassword', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_extractFilePassword', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for zipDirectory
def zipDirectory(request):
	# Init of the view zipDirectory
	try:
		# Pool call
		response, repool = sendPool(request, 'zipDirectory')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter new_folder_name
			new_folder_name = request.POST.get('new_folder_name')

			# Execute, get result and show it
			result = ht.getModule('ht_unzip').zipDirectory( new_folder_name=new_folder_name )
			if request.POST.get('is_async_zipDirectory', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_zipDirectory', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	