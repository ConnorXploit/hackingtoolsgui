from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal, sendPool, returnAsModal

# Create your views here.

# Automatic view function for get_image_exif
def get_image_exif(request):
	# Init of the view get_image_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_image_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
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
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_image_exif', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_pdf_exif
def get_pdf_exif(request):
	# Init of the view get_pdf_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_pdf_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
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
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_pdf_exif', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))

# Automatic view function for set_pdf_author
def set_pdf_author(request):
	# Init of the view set_pdf_author
	try:
		# Pool call
		response, repool = sendPool(request, 'set_pdf_author')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_metadata').set_pdf_author()
			pass
	except Exception as e:
		if request.POST.get('is_async_set_pdf_author', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for set_pdf_field_value
def set_pdf_field_value(request):
	# Init of the view set_pdf_field_value
	try:
		# Pool call
		response, repool = sendPool(request, 'set_pdf_field_value')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file pdf_file
				filename_pdf_file, location_pdf_file, pdf_file = saveFileOutput(request.FILES['pdf_file'], 'metadata', 'forensic')
			except Exception as e:
				# If not param pdf_file
				if request.POST.get('is_async_set_pdf_field_value', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter field
			field = request.POST.get('field')

			# Parameter fieldValue
			fieldValue = request.POST.get('fieldValue')

			# Execute, get result and show it
			result = ht.getModule('ht_metadata').set_pdf_field_value( pdf_file=pdf_file, field=field, fieldValue=fieldValue )
			if request.POST.get('is_async_set_pdf_field_value', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_set_pdf_field_value', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for set_pdf_metadata_to_another
def set_pdf_metadata_to_another(request):
	# Init of the view set_pdf_metadata_to_another
	try:
		# Pool call
		response, repool = sendPool(request, 'set_pdf_metadata_to_another')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file pdf_file_original
				filename_pdf_file_original, location_pdf_file_original, pdf_file_original = saveFileOutput(request.FILES['pdf_file_original'], 'metadata', 'forensic')
			except Exception as e:
				# If not param pdf_file_original
				if request.POST.get('is_async_set_pdf_metadata_to_another', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			try:
				# Save file pdf_file_fake
				filename_pdf_file_fake, location_pdf_file_fake, pdf_file_fake = saveFileOutput(request.FILES['pdf_file_fake'], 'metadata', 'forensic')
			except Exception as e:
				# If not param pdf_file_fake
				if request.POST.get('is_async_set_pdf_metadata_to_another', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_metadata').set_pdf_metadata_to_another( pdf_file_original=pdf_file_original, pdf_file_fake=pdf_file_fake )
			
			if result:
				if os.path.isfile(result):
					with open(result, 'rb') as fh:
						response = HttpResponse(fh.read(), content_type="application/{type}".format(type=os.path.split(result)[1].split('.')[1]))
						response['Content-Disposition'] = 'inline; filename=' + os.path.basename(result)
						return response

			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_set_pdf_metadata_to_another', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for get_mp3_exif
def get_mp3_exif(request):
	# Init of the view get_mp3_exif
	try:
		# Pool call
		response, repool = sendPool(request, 'get_mp3_exif')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file mp3_file
				filename_mp3_file, location_mp3_file, mp3_file = saveFileOutput(request.FILES['mp3_file'], 'metadata', 'forensic')
			except Exception as e:
				# If not param mp3_file
				if request.POST.get('is_async_get_mp3_exif', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_metadata').get_mp3_exif( mp3_file=mp3_file )
			if request.POST.get('is_async_get_mp3_exif', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_get_mp3_exif', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for set_mp3_metadata
def set_mp3_metadata(request):
	# Init of the view set_mp3_metadata
	try:
		# Pool call
		response, repool = sendPool(request, 'set_mp3_metadata')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file mp3_file
				filename_mp3_file, location_mp3_file, mp3_file = saveFileOutput(request.FILES['mp3_file'], 'metadata', 'forensic')
			except Exception as e:
				# If not param mp3_file
				if request.POST.get('is_async_set_mp3_metadata', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter title (Optional - Default None)
			title = request.POST.get('title', None)
			if not title:
				title = None

			# Parameter artist (Optional - Default None)
			artist = request.POST.get('artist', None)
			if not artist:
				artist = None

			# Parameter album (Optional - Default None)
			album = request.POST.get('album', None)
			if not album:
				album = None

			# Parameter album_artist (Optional - Default None)
			album_artist = request.POST.get('album_artist', None)
			if not album_artist:
				album_artist = None

			# Parameter track_num (Optional - Default None)
			track_num = request.POST.get('track_num', None)
			if not track_num:
				track_num = None

			# Execute, get result and show it
			result = ht.getModule('ht_metadata').set_mp3_metadata( mp3_file=mp3_file, title=title, artist=artist, album=album, album_artist=album_artist, track_num=track_num )
			if request.POST.get('is_async_set_mp3_metadata', False):
				return JsonResponse({ "data" : returnAsModal(result) })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_set_mp3_metadata', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	