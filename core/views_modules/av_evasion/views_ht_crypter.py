from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# ht_crypter

@csrf_exempt
def crypt_file(request):
    this_conf = config['ht_crypter_crypt_file']
    if len(request.FILES) != 0:
        if request.FILES['filename']:
            # Get file
            myfile = request.FILES['filename']

            # Get Crypter Module
            crypter = ht.getModule('ht_crypter')

            # Save the file
            filename, location, uploaded_file_url = saveFileOutput(myfile, "crypter", "av_evasion")
            
            # Compile Exe
            compile_exe = False
            if request.POST.get('compile_exe','')=='on':
                compile_exe = True

            tmp_new_file_name = filename.split('.')[0]
            if not '.' in tmp_new_file_name:
                tmp_new_file_name = '{name}.py'.format(name=tmp_new_file_name)
            new_file_name = os.path.join(location, tmp_new_file_name)

            drop_file_name = filename
            if not '.' in drop_file_name:
                drop_file_name = '{name}.{ext}'.format(name=drop_file_name, ext=filename.split('.')[1])

            iterate_count = 1

            if request.POST.get('iteratecount'):
                try:
                    iterate_count = int(request.POST.get('iteratecount'))
                    if iterate_count < 1:
                        iterate_count = 1
                except:
                    pass

            prime_length = 2
            if request.POST.get('prime_length'):
                try:
                    prime_length = int(request.POST.get('prime_length'))
                    if prime_length < 1:
                        prime_length = 2
                except:
                    pass

            is_last = False
            if iterate_count == 1:
                is_last = True

            crypted_file = crypter.crypt_file(filename=uploaded_file_url, new_file_name=new_file_name, drop_file_name=drop_file_name, prime_length=prime_length, iterate_count=iterate_count, is_last=is_last, compile_exe=compile_exe)

            if crypted_file:
                if os.path.isfile(crypted_file):
                    with open(crypted_file, 'rb') as fh:
                        if compile_exe:
                            new_file_name = '{name}.exe'.format(name=new_file_name.split('.')[0])
                        response = HttpResponse(fh.read(), content_type="application/{type}".format(type=new_file_name.split('.')[1]))
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(crypted_file)
                        return response
                        os.remove(uploaded_file_url)
                        os.remove(crypted_file)
            else:
                Logger.printMessage(message='crypt_file', description=this_conf['bad_saved'], is_error=True)
            return renderMainPanel(request=request)

    return renderMainPanel(request=request)

# Automatic view function for convertToExe
@csrf_exempt
def convertToExe(request):
	# Init of the view convertToExe
	try:
		# Pool call
		response, repool = sendPool(request, 'convertToExe')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter stub_name
			stub_name = request.POST.get('stub_name')

			# Execute the function
			ht.getModule('ht_crypter').convertToExe( stub_name=stub_name )
	except Exception as e:
		if request.POST.get('is_async_convertToExe', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for createStub
@csrf_exempt
def createStub(request):
	# Init of the view createStub
	try:
		# Pool call
		response, repool = sendPool(request, 'createStub')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter crypto_data_hex
			crypto_data_hex = request.POST.get('crypto_data_hex')

			# Parameter public_key
			public_key = request.POST.get('public_key')

			try:
				# Save file drop_file_name
				filename_drop_file_name, location_drop_file_name, drop_file_name = saveFileOutput(request.FILES['drop_file_name'], 'crypter', 'av_evasion')

			except Exception as e:
				# If not param drop_file_name
				if request.POST.get('is_async_createStub', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter save_name
			save_name = request.POST.get('save_name')

			# Parameter is_iterating (Optional - Default False)
			is_iterating = request.POST.get('is_iterating', False)
			if not is_iterating:
				is_iterating = None

			# Parameter is_last (Optional - Default False)
			is_last = request.POST.get('is_last', False)
			if not is_last:
				is_last = None

			# Parameter convert (Optional - Default False)
			convert = request.POST.get('convert', False)
			if not convert:
				convert = None

			# Execute, get result and show it
			result = ht.getModule('ht_crypter').createStub( crypto_data_hex=crypto_data_hex, public_key=public_key, drop_file_name=drop_file_name, save_name=save_name, is_iterating=is_iterating, is_last=is_last, convert=convert )
			if request.POST.get('is_async_createStub', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_createStub', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	