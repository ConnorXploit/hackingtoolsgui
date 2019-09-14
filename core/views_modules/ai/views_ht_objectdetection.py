from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

# ht_objectdetection

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
            
            if request.POST.get('is_async', False):
                data = {
                    'data' : this_conf['need_params']
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=this_conf['need_params'])
        return renderMainPanel(request=request, popup_text=this_conf['need_file'])
    except Exception as e:
        Logger.printMessage(message='predictImage', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

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
            if request.POST.get('is_async', False):
                data = {
                    'data' : this_conf['need_params']
                }
                return JsonResponse(data)
            return renderMainPanel(request=request, popup_text=this_conf['need_params'])

    except Exception as e:
        Logger.printMessage(message='predictFromZip', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))

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
                if request.POST.get('is_async', False):
                    data = {
                        'data' : image_final
                    }
                    return JsonResponse(data)
                return renderMainPanel(request=request, popup_text=image_final)
            return renderMainPanel(request=request)

    except Exception as e:
        Logger.printMessage(message='trainFromZip', description=str(e), is_error=True)
        return renderMainPanel(request=request, popup_text=str(e))


def getTestsModelsDir(request):
	result = ht.getModule('ht_objectdetection').getTestsModelsDir( )
	return renderMainPanel(request=request, popup_text=result)
	
def predict(request):
	X_img_path = request.POST.get('X_img_path')
	knn_clf = request.POST.get('knn_clf', None)
	model_path = request.POST.get('model_path', None)
	distance_threshold = request.POST.get('distance_threshold', 0.6)
	result = ht.getModule('ht_objectdetection').predict( X_img_path=X_img_path, knn_clf=knn_clf, model_path=model_path, distance_threshold=distance_threshold )
	return renderMainPanel(request=request, popup_text=result)
	
def saveCroppedImage(request):
	img_path = request.POST.get('img_path')
	coords = request.POST.get('coords')
	model_path = request.POST.get('model_path')
	name = request.POST.get('name')
	counter = request.POST.get('counter', 1)
	ht.getModule('ht_objectdetection').saveCroppedImage( img_path=img_path, coords=coords, model_path=model_path, name=name, counter=counter )

def show_prediction_labels_on_image(request):
	img_path = request.POST.get('img_path')
	predictions = request.POST.get('predictions')
	model_path = request.POST.get('model_path')
	result = ht.getModule('ht_objectdetection').show_prediction_labels_on_image( img_path=img_path, predictions=predictions, model_path=model_path )
	return renderMainPanel(request=request, popup_text=result)
	
def train(request):
	train_dir = request.POST.get('train_dir')
	model_save_path = request.POST.get('model_save_path', None)
	n_neighbors = request.POST.get('n_neighbors', None)
	knn_algo = request.POST.get('knn_algo', 'ball_tree')
	verbose = request.POST.get('verbose', False)
	result = ht.getModule('ht_objectdetection').train( train_dir=train_dir, model_save_path=model_save_path, n_neighbors=n_neighbors, knn_algo=knn_algo, verbose=verbose )
	return renderMainPanel(request=request, popup_text=result)
	