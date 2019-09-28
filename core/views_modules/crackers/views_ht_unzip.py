from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for extractFile
@csrf_exempt
def extractFile(request):
	# Init of the view extractFile
	try:
		# Pool call
		response, repool = sendPool(request, 'extractFile')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file zipPathName
				filename_zipPathName, location_zipPathName, zipPathName = saveFileOutput(request.FILES['zipPathName'], 'unzip', 'crackers')

			except Exception as e:
				# If not param zipPathName
				if request.POST.get('is_async_extractFile', False):
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
			result = ht.getModule('ht_unzip').extractFile( zipPathName=zipPathName, password=password, posible_combinations=posible_combinations, output_dir_new=output_dir_new )
			if request.POST.get('is_async_extractFile', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_extractFile', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for zipFiles
@csrf_exempt
def zipFiles(request):
	# Init of the view zipFiles
	try:
		# Pool call
		response, repool = sendPool(request, 'zipFiles')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file files
				filename_files, location_files, files = saveFileOutput(request.FILES['files'], 'unzip', 'crackers')

			except Exception as e:
				# If not param files
				if request.POST.get('is_async_zipFiles', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter new_folder_name
			new_folder_name = request.POST.get('new_folder_name')

			# Execute, get result and show it
			result = ht.getModule('ht_unzip').zipFiles( files=files, new_folder_name=new_folder_name )
			if request.POST.get('is_async_zipFiles', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_zipFiles', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	