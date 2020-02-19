from django.http import HttpResponse, JsonResponse
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool, returnAsModal

# Create your views here.

# Automatic view function for execute_commands
def execute_commands(request):
	# Init of the view execute_commands
	try:
		# Pool call
		response, repool = sendPool(request, 'execute_commands')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter commands
			commands = request.POST.get('commands')

			# Execute the function
			ht.getModule('ht_ssh').execute_commands( commands=commands )
	except Exception as e:
		if request.POST.get('is_async_execute_commands', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))

# Automatic view function for upload_files
def upload_files(request):
	# Init of the view upload_files
	try:
		# Pool call
		response, repool = sendPool(request, 'upload_files')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file files
				filename_files, location_files, files = saveFileOutput(request.FILES['files'], 'ssh', 'connector')
			except Exception as e:
				# If not param files
				if request.POST.get('is_async_upload_files', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute the function
			ht.getModule('ht_ssh').upload_files( files=files )
	except Exception as e:
		if request.POST.get('is_async_upload_files', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for connect
def connect(request):
	# Init of the view connect
	try:
		# Pool call
		response, repool = sendPool(request, 'connect')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Parameter host
			host = request.POST.get('host')

			# Parameter user
			user = request.POST.get('user')

			try:
				# Save file ssh_key_filepath
				filename_ssh_key_filepath, location_ssh_key_filepath, ssh_key_filepath = saveFileOutput(request.FILES['ssh_key_filepath'], 'ssh', 'connector')
			except Exception as e:
				# If not param ssh_key_filepath
				if request.POST.get('is_async_connect', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter remote_upload_dir
			remote_upload_dir = request.POST.get('remote_upload_dir')

			# Execute the function
			ht.getModule('ht_ssh').connect( host=host, user=user, ssh_key_filepath=ssh_key_filepath, remote_upload_dir=remote_upload_dir )
	except Exception as e:
		if request.POST.get('is_async_connect', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for disconnect
def disconnect(request):
	# Init of the view disconnect
	try:
		# Pool call
		response, repool = sendPool(request, 'disconnect')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			# Execute the function
			ht.getModule('ht_ssh').disconnect()
	except Exception as e:
		if request.POST.get('is_async_disconnect', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for download_file
def download_file(request):
	# Init of the view download_file
	try:
		# Pool call
		response, repool = sendPool(request, 'download_file')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return JsonResponse({ "data" : str(response) })
		else:
			try:
				# Save file file
				filename_file, location_file, file = saveFileOutput(request.FILES['file'], 'ssh', 'connector')
			except Exception as e:
				# If not param file
				if request.POST.get('is_async_download_file', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute the function
			ht.getModule('ht_ssh').download_file( file=file )
	except Exception as e:
		if request.POST.get('is_async_download_file', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	