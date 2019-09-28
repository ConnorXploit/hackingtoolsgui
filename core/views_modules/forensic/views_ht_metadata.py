from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, sendPool

# Create your views here.

# Automatic view function for get_image_exif
@csrf_exempt
def get_image_exif(request):
	# Init of the view get_image_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_image_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file filename
				filename_filename, location_filename, filename = saveFileOutput(request.FILES['filename'], 'metadata', 'forensic')

			except Exception as e:
				# If not param filename
				if request.POST.get('is_async_get_image_exif', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_metadata').get_image_exif( filename=filename )
			if request.POST.get('is_async_get_image_exif', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_image_exif', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_pdf_exif
@csrf_exempt
def get_pdf_exif(request):
	# Init of the view get_pdf_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_pdf_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file pdf_file
				filename_pdf_file, location_pdf_file, pdf_file = saveFileOutput(request.FILES['pdf_file'], 'metadata', 'forensic')

			except Exception as e:
				# If not param pdf_file
				if request.POST.get('is_async_get_pdf_exif', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_metadata').get_pdf_exif( pdf_file=pdf_file )
			if request.POST.get('is_async_get_pdf_exif', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_pdf_exif', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	