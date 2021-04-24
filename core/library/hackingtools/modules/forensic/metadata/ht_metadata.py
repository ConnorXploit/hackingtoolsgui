from hackingtools.core import Logger, Config
import hackingtools as ht
import os, json

# Image Metadata
from PIL import Image
# PDF Metadata
from PyPDF2 import PdfFileReader, PdfFileWriter
import pdfrw
from pdfrw import PdfReader, PdfWriter
# MP3
import eyed3
# import mutagen

import os

config = Config.getConfig(parentKey='modules', key='ht_metadata')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'set_pdf_metadata_to_another'
		self.__gui_label__ = 'Metadata manipulation'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_metadata'), debug_module=True)

	def get_image_exif(self, filename):
		Logger.printMessage(message='{methodName}'.format(methodName='get_image_exif'), description=filename, debug_module=True)
		try:
			img_file = Image.open(filename)
			img_file.verify()
			info = img_file._getexif()
			return info
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
			return e
		return -1

	def get_pdf_exif(self, pdf_file):
		Logger.printMessage(message='{methodName}'.format(methodName='get_pdf_exif'), description=pdf_file, debug_module=True)
		info = ''
		data = {}
		try:
			with open(pdf_file, 'rb') as f:
				pdf = PdfFileReader(f)
				info = pdf.getDocumentInfo()
				number_of_pages = pdf.getNumPages()
			if info:
				for a in info:
					data[a] = info[a]
			return data
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
			return e
		return -1
	
	def set_pdf_field_value(self, pdf_file, field, fieldValue):
		try:
			trailer = PdfReader(pdf_file)
			if trailer.Info is None:
				trailer.Info = pdfrw.objects.pdfdict.PdfDict()
			setDataQuery = 'trailer.Info.{f} = "{v}"'.format(f=field.replace('/', ''), v=fieldValue)
			exec(setDataQuery)
			new_pdf = os.path.split(pdf_file)[1]
			new_file = os.path.join( output_dir, new_pdf )
			PdfWriter(new_file, trailer=trailer).write()
			return new_file
		except:
			Logger.printMessage(pdf_file, is_error=True)
			return pdf_file

	def set_pdf_metadata_to_another(self, pdf_file_original, pdf_file_fake):
		meta = self.get_pdf_exif(pdf_file_original)
		for data, val in meta.items():
			pdf_file_fake = self.set_pdf_field_value(pdf_file_fake, data, val)
		return pdf_file_fake

	def get_mp3_exif(self, mp3_file):
		try:
			audioFile = eyed3.load(mp3_file)
			keys = [ tag for tag in dir(audioFile.tag) if not tag.startswith('_') ]
			data = {}
			for k in keys:
				temp = eval("audioFile.tag.{f}".format(f=k))
				if temp is not None and temp:
					if not isinstance(temp, str):
						subkeys = [ t for t in dir(temp) if not t.startswith('_') ]
						if subkeys:
							data[k] = {}
							for s in subkeys:
								new_temp = eval("audioFile.tag.{f}.{r}".format(f=k, r=s))
								if new_temp is not None and new_temp:
									if isinstance(new_temp, str):
										if str(new_temp) != 'None':
											data[k][s] = str(new_temp)
						if k in data and not data[k]:
							del data[k]
					else:
						data[k] = str(temp)
			return data
		except Exception as e:
			Logger.printMessage(str(e), is_error=True)
			return str(e)

	def set_mp3_metadata(self, mp3_file, title=None, artist=None, album=None, album_artist=None, track_num=None):
		try:
			new_file = "edited-{f}".format(f=os.path.split(mp3_file)[1])
			new_file = os.path.join(output_dir, new_file)
			audioFile = eyed3.load(mp3_file)
			if title:
				audioFile.tag.title = title
			if artist:
				audioFile.tag.artist = artist
			if album:
				audioFile.tag.album = album
			if album_artist:
				audioFile.tag.album_artist = album_artist
			if track_num:
				audioFile.tag.title = track_num
			audioFile.tag.save(new_file)
			return new_file
		except Exception as e:
			Logger.printMessage(str(e), is_error=True)
			return str(e)

	# def get_audio_video_exif(self, filename):
	# 	Logger.printMessage(message='{methodName}'.format(methodName='get_audio_video_exif'), description=filename, debug_module=True)
	# 	try:
	# 		my_file = mutagen.File(filename)
	# 		img_file.verify()
	# 		info = img_file._getexif()
	# 		return info
	# 	except Exception as e:
	# 		Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
	# 		return e
	# 	return -1
