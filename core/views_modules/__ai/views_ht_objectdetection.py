from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger, sendPool

# Create your views here.

# ht_objectdetection

@csrf_exempt
def predictImage(request):
    this_conf = config['ht_objectdetection_predictImage']
    try:
        if len(request.FILES) != 0:

            if 'image_file_test' in request.FILES:
                objectdetection = ht.getModule('ht_objectdetection')
                image_to_test = request.FILES['image_file_test']
                filename, location, uploaded_file_url = saveFileOutput(image_to_test, "objectdetection", "ai")

                first_folder_name = None
                filenameZip = None
                uploaded_file_urlZip = this_conf['default_model']
                modelfile = request.POST.get('dropdown_modelfile')
                
                if not modelfile:
                    modelfile = request.POST.get('dropdown_modelfile_main')

                if 'image_models_zip' in request.FILES:
                    zip_to_train = request.FILES['image_models_zip']
                    first_folder_name = request.POST.get('first_folder_name', None)
                    if not first_folder_name:
                        first_folder_name = zip_to_train.name.split('.')[0]
                    filenameZip, location, uploaded_file_urlZip = views.saveFileOutput(zip_to_train, "objectdetection", "ai")

                n_neighbors = int(request.POST.get('neighbors', 1))

                if filenameZip:
                    image_final = objectdetection.predictImage(
                        uploaded_file_url, 
                        model_path='{f}.clf'.format(f=filenameZip.split('.')[0]), 
                        trainZipFile=uploaded_file_urlZip, 
                        first_folder_name=first_folder_name,
                        n_neighbors=n_neighbors)
                else:
                    image_final = objectdetection.predictImage(
                        uploaded_file_url, 
                        model_path=modelfile)
                
                with open(image_final, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/{type}".format(type=filename.split('.')[1]))
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(image_final)
                    return response
            
            if request.POST.get('is_async_predictImage', False):
                data = {
                    'data' : this_conf['need_params']
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=this_conf['need_params'])
        return renderMainPanel(request=request, popup_text=this_conf['need_file'])
    except Exception as e:
        Logger.printMessage(message='predictImage', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

@csrf_exempt
def predictFromZip(request):
    this_conf = config['ht_objectdetection_predictFromZip']
    try:
        if len(request.FILES) != 0:

            if 'image_file_test_zip' in request.FILES:
                objectdetection = ht.getModule('ht_objectdetection')

                image_to_test_zip = request.FILES['image_file_test_zip']
                first_folder_name = request.POST.get('first_folder_name', None)

                filename, location, uploaded_file_url = saveFileOutput(image_to_test_zip, "objectdetection", "ai")

                if not first_folder_name:
                    first_folder_name = image_to_test_zip.split('.')[0]

                filenameZip = None
                uploaded_file_urlZip = this_conf['default_model']
                modelfile = request.POST.get('dropdown_modelfile_pred')

                if 'image_models_zip_pred' in request.FILES:
                    zip_to_train = request.FILES['image_models_zip_pred']
                    first_folder_name_zip = request.POST.get('first_folder_name_zip', None)
                    if not first_folder_name_zip:
                        first_folder_name_zip = zip_to_train.name.split('.')[0]
                    filenameZip, location, uploaded_file_urlZip = saveFileOutput(zip_to_train, "objectdetection", "ai")

                n_neighbors = int(request.POST.get('neighbors_pred', 1))

                if filenameZip:
                    image_final = objectdetection.predictFromZip(
                        uploaded_file_url, 
                        model_path='{f}.clf'.format(f=filenameZip.split('.')[0]),
                        first_folder_name=first_folder_name,
                        trainZipFile=uploaded_file_urlZip,
                        first_folder_name_training_zip=first_folder_name_zip,
                        n_neighbors=n_neighbors)
                else:
                    image_final = objectdetection.predictFromZip(
                        uploaded_file_url, 
                        model_path=modelfile,
                        first_folder_name=first_folder_name)
                
                with open(image_final, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/{type}".format(type=filename.split('.')[1]))
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(image_final)
                    return response
            if request.POST.get('is_async_predictFromZip', False):
                data = {
                    'data' : this_conf['need_params']
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=this_conf['need_params'])

    except Exception as e:
        Logger.printMessage(message='predictFromZip', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

@csrf_exempt
def trainFromZip(request):
    try:
        if len(request.FILES) != 0:
            objectdetection = ht.getModule('ht_objectdetection')
            first_folder_name = None
            filenameZip = None
            uploaded_file_urlZip = 'trained.clf'

            if 'image_models_zip' in request.FILES:
                zip_to_train = request.FILES['image_models_zip']
                first_folder_name = request.POST.get('first_folder_name', None)
                if not first_folder_name:
                    first_folder_name = zip_to_train.name.split('.')[0]
                filenameZip, location, uploaded_file_urlZip = saveFileOutput(zip_to_train, "objectdetection", "ai")

            n_neighbors = int(request.POST.get('neighbors', 1))

            if filenameZip:
                image_final = objectdetection.trainFromZip(
                    uploaded_file_urlZip, 
                    model_path='{f}.clf'.format(f=filenameZip.split('.')[0]), 
                    trainZipFile=uploaded_file_urlZip, 
                    first_folder_name=first_folder_name,
                    n_neighbors=n_neighbors)
                if request.POST.get('is_async_trainFromZip', False):
                    data = {
                        'data' : image_final
                    }
                    return JsonResponse(data)
                return renderMainPanel(request=request, popup_text=image_final)
            return renderMainPanel(request=request)

    except Exception as e:
        Logger.printMessage(message='trainFromZip', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

# Automatic view function for getTestsModelsDir
@csrf_exempt
def getTestsModelsDir(request):
	# Init of the view getTestsModelsDir
	try:
		# Pool call
		response, repool = sendPool(request, 'getTestsModelsDir')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Execute, get result and show it
			result = ht.getModule('ht_objectdetection').getTestsModelsDir()
			if request.POST.get('is_async_getTestsModelsDir', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_getTestsModelsDir', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for predict
@csrf_exempt
def predict(request):
	# Init of the view predict
	try:
		# Pool call
		response, repool = sendPool(request, 'predict')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file X_img_path
				filename_X_img_path, location_X_img_path, X_img_path = saveFileOutput(request.FILES['X_img_path'], 'objectdetection', 'ai')

			except Exception as e:
				# If not param X_img_path
				if request.POST.get('is_async_predict', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter knn_clf (Optional - Default None)
			knn_clf = request.POST.get('knn_clf', None)
			if not knn_clf:
				knn_clf = None

			try:
				# Save file model_path (Optional)
				filename_model_path, location_model_path, model_path = saveFileOutput(request.FILES['model_path'], 'objectdetection', 'ai')
			except Exception as e:
				# If not param model_path
				if request.POST.get('is_async_predict', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))

			# Parameter distance_threshold (Optional - Default 0.6)
			distance_threshold = request.POST.get('distance_threshold', 0.6)

			# Execute, get result and show it
			result = ht.getModule('ht_objectdetection').predict( X_img_path=X_img_path, knn_clf=knn_clf, model_path=model_path, distance_threshold=distance_threshold )
			if request.POST.get('is_async_predict', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_predict', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for saveCroppedImage
@csrf_exempt
def saveCroppedImage(request):
	# Init of the view saveCroppedImage
	try:
		# Pool call
		response, repool = sendPool(request, 'saveCroppedImage')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file img_path
				filename_img_path, location_img_path, img_path = saveFileOutput(request.FILES['img_path'], 'objectdetection', 'ai')

			except Exception as e:
				# If not param img_path
				if request.POST.get('is_async_saveCroppedImage', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter coords
			coords = request.POST.get('coords')

			try:
				# Save file model_path
				filename_model_path, location_model_path, model_path = saveFileOutput(request.FILES['model_path'], 'objectdetection', 'ai')

			except Exception as e:
				# If not param model_path
				if request.POST.get('is_async_saveCroppedImage', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter name
			name = request.POST.get('name')

			# Parameter counter (Optional - Default 1)
			counter = request.POST.get('counter', 1)

			# Execute the function
			ht.getModule('ht_objectdetection').saveCroppedImage( img_path=img_path, coords=coords, model_path=model_path, name=name, counter=counter )
	except Exception as e:
		if request.POST.get('is_async_saveCroppedImage', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for show_prediction_labels_on_image
@csrf_exempt
def show_prediction_labels_on_image(request):
	# Init of the view show_prediction_labels_on_image
	try:
		# Pool call
		response, repool = sendPool(request, 'show_prediction_labels_on_image')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			try:
				# Save file img_path
				filename_img_path, location_img_path, img_path = saveFileOutput(request.FILES['img_path'], 'objectdetection', 'ai')

			except Exception as e:
				# If not param img_path
				if request.POST.get('is_async_show_prediction_labels_on_image', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Parameter predictions
			predictions = request.POST.get('predictions')

			try:
				# Save file model_path
				filename_model_path, location_model_path, model_path = saveFileOutput(request.FILES['model_path'], 'objectdetection', 'ai')

			except Exception as e:
				# If not param model_path
				if request.POST.get('is_async_show_prediction_labels_on_image', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))
			# Execute, get result and show it
			result = ht.getModule('ht_objectdetection').show_prediction_labels_on_image( img_path=img_path, predictions=predictions, model_path=model_path )
			if request.POST.get('is_async_show_prediction_labels_on_image', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_show_prediction_labels_on_image', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	
# Automatic view function for train
@csrf_exempt
def train(request):
	# Init of the view train
	try:
		# Pool call
		response, repool = sendPool(request, 'train')
		if response or repool:
			if repool:
				return HttpResponse(response)
			return renderMainPanel(request=request, popup_text=response.text)
		else:
			# Parameter train_dir
			train_dir = request.POST.get('train_dir')

			try:
				# Save file model_save_path (Optional)
				filename_model_save_path, location_model_save_path, model_save_path = saveFileOutput(request.FILES['model_save_path'], 'objectdetection', 'ai')
			except Exception as e:
				# If not param model_save_path
				if request.POST.get('is_async_train', False):
					return JsonResponse({ "data" : str(e) })
				return renderMainPanel(request=request, popup_text=str(e))

			# Parameter n_neighbors (Optional - Default None)
			n_neighbors = request.POST.get('n_neighbors', None)
			if not n_neighbors:
				n_neighbors = None

			# Parameter knn_algo (Optional - Default ball_tree)
			knn_algo = request.POST.get('knn_algo', 'ball_tree')

			# Parameter verbose (Optional - Default False)
			verbose = request.POST.get('verbose', False)
			if not verbose:
				verbose = None

			# Execute, get result and show it
			result = ht.getModule('ht_objectdetection').train( train_dir=train_dir, model_save_path=model_save_path, n_neighbors=n_neighbors, knn_algo=knn_algo, verbose=verbose )
			if request.POST.get('is_async_train', False):
				return JsonResponse({ "data" : result })
			return renderMainPanel(request=request, popup_text=result)
	except Exception as e:
		if request.POST.get('is_async_train', False):
			return JsonResponse({ "data" : str(e) })
		return renderMainPanel(request=request, popup_text=str(e))
	