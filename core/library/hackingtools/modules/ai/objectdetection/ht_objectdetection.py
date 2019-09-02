"""

NOTE: This example requires scikit-learn to be installed! You can install it with pip:

$ pip3 install scikit-learn

Also install zlib

http://gnuwin32.sourceforge.net/packages/zlib.htm

"""
from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os
import math
from sklearn import neighbors
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder

config = Config.getConfig(parentKey='modules', key='ht_objectdetection')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
output_dir_models = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests_models'))

ALLOWED_EXTENSIONS = {}

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_objectdetection'))

	def getTestsModelsDir(self):
		models = []
		for fileName in os.listdir(output_dir_models):
			if fileName.endswith(".{clf}".format(clf=config['models_tests_extension'])):
				models.append(fileName)
		return models

	def train(self, train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
		"""
		Trains a k-nearest neighbors classifier for face recognition.

		:param train_dir: directory that contains a sub-directory for each known person, with its name.

		(View in source code to see train_dir example tree structure)

		Structure:
			<train_dir>/
			├── <person1>/
			│   ├── <somename1>.jpeg
			│   ├── <somename2>.jpeg
			│   ├── ...
			├── <person2>/
			│   ├── <somename1>.jpeg
			│   └── <somename2>.jpeg
			└── ...

		:param model_save_path: (optional) path to save model on disk
		:param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
		:param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
		:param verbose: verbosity of training
		:return: returns knn classifier that was trained on the given data.
		"""
		Logger.printMessage(message="train", description="{msg}: {d}".format(msg=config['training_log_message'], d=train_dir), debug_module=True)
		X = []
		y = []

		# Loop through each person in the training set
		for class_dir in os.listdir(train_dir):
			if not os.path.isdir(os.path.join(train_dir, class_dir)):
				continue

			# Loop through each training image for the current person
			for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
				image = face_recognition.load_image_file(img_path)
				face_bounding_boxes = face_recognition.face_locations(image)

				if len(face_bounding_boxes) != 1:
					# If there are no people (or too many people) in a training image, skip the image.
					if verbose:
						Logger.printMessage(
							message="train", 
							description="{img} {bad_image}: {msg}".format(
								img=img_path, 
								bad_image=config['training_log_bad_image'], 
								msg=config['training_log_no_recognition'] if len(face_bounding_boxes) < 1 else config['training_log_much_recognition']), 
								debug_module=True)
				else:
					# Add face encoding for current image to the training set
					X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
					y.append(class_dir)

		# Determine how many neighbors to use for weighting in the KNN classifier
		if n_neighbors is None:
			n_neighbors = int(round(math.sqrt(len(X))))
			if verbose:
				Logger.printMessage(
					message="train", 
					description="{neig}: {d}".format(neig=config['training_log_n_neighbors'], d=n_neighbors), 
					debug_module=True)
		
		# Create and train the KNN classifier
		knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
		knn_clf.fit(X, y)

		# Save the trained KNN classifier
		if model_save_path is not None:
			with open(model_save_path, 'wb') as f:
				pickle.dump(knn_clf, f)

		return knn_clf

	def predict(self, X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
		"""
		Recognizes faces in given image using a trained KNN classifier

		:param X_img_path: path to image to be recognized
		:param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
		:param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
		:param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
			of mis-classifying an unknown person as a known one.
		:return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
			For faces of unrecognized persons, the name 'unknown' will be returned.
		"""
		if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
			Logger.printMessage(message="predict", description="{invalid_path}: {im}".format(invalid_path=config['predicting_invalid_path'], im=X_img_path))
		
		if knn_clf is None and model_path is None:
			Logger.printMessage(message="predict", description=config['predicting_no_knn_or_model_path'])

		# Load a trained KNN model (if one was passed in)
		if knn_clf is None:
			with open(model_path, 'rb') as f:
				knn_clf = pickle.load(f)

		# Load image file and find face locations
		X_img = face_recognition.load_image_file(X_img_path)
		X_face_locations = face_recognition.face_locations(X_img)

		# If no faces are found in the image, return an empty result.
		if len(X_face_locations) == 0:
			return []

		# Find encodings for faces in the test iamge
		faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

		# Use the KNN model to find the best matches for the test face
		closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
		are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

		# Predict classes and remove classifications that aren't within the threshold
		return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

	def show_prediction_labels_on_image(self, img_path, predictions):
		"""
		Shows the face recognition results visually.

		:param img_path: path to image to be recognized
		:param predictions: results of the predict function
		:return:
		"""
		Logger.printMessage(message="show_prediction_labels_on_image", description="Testing: {d}".format(d=img_path), debug_module=True)
		pil_image = Image.open(img_path).convert("RGB")
		draw = ImageDraw.Draw(pil_image)

		for name, (top, right, bottom, left) in predictions:
			# Draw a box around the face using the Pillow module
			draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

			# There's a bug in Pillow where it blows up with non-UTF-8 text
			# when using the default bitmap font
			name = name.encode("UTF-8")

			# Draw a label with a name below the face
			text_width, text_height = draw.textsize(name)
			draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
			draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

		# Remove the drawing library from memory as per the Pillow docs
		del draw

		# Display the resulting image
		pil_image.save(img_path)
		return Image.open(img_path).filename

	def trainFromZip(self, zipFile, new_model_name='new_trained.clf', first_folder_name='model', n_neighbors=1):
		unzipper = ht.getModule('ht_unzip')
		unzipper.extractFile(zipFile, output_dir_new=output_dir)
		new_model = os.path.join(output_dir_models, new_model_name)
		classifier = self.train(os.path.join(output_dir, first_folder_name), model_save_path=new_model, n_neighbors=int(n_neighbors), verbose=True)
		return new_model
	
	def predictImage(self, imageFile, model_path='trained.clf', trainZipFile=None, first_folder_name=None, n_neighbors=1):
		if trainZipFile:
			if not first_folder_name:
				_, first_folder_name = os.path.split(trainZipFile.split('.')[0])
			model_path = self.trainFromZip(zipFile=trainZipFile, new_model_name='{f}.{clf}'.format(f=first_folder_name, clf=config['models_tests_extension']), first_folder_name=first_folder_name, n_neighbors=int(n_neighbors))
		else:
			model_path = os.path.join(output_dir_models, model_path)

		predictions = self.predict(imageFile, model_path=model_path)
		
		# Print results on the console
		for name, (top, right, bottom, left) in predictions:
			Logger.printMessage(message="predictImage", description="Found {} at ({}, {})".format(name, left, top), debug_module=True)

		return self.show_prediction_labels_on_image(imageFile, predictions)