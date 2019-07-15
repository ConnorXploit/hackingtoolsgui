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
		try:
			img_file = Image.open(filename)
			img_file.verify()
			info = img_file._getexif()
			return info
		except:
			pass
		return

	def get_pdf_exif(self, pdf_file):
		info = ''
		data = {}
		with open(pdf_file, 'rb') as f:
			pdf = PdfFileReader(f)
			info = pdf.getDocumentInfo()
			number_of_pages = pdf.getNumPages()
		for a in info:
			data[a] = info[a]
		return data