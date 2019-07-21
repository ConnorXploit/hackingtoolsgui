from hackingtools.core import Logger
import hackingtools as ht

from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_metadata loaded', debug_core=True)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_metadata'))

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
			for a in info:
				data[a] = info[a]
			return data
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
			return e
		return -1
