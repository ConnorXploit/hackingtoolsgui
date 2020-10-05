from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os
import csv
import json
import xlsxwriter
import xmltodict
import xml.etree.ElementTree as ET
import pandas as pd
from pandas.io.json import json_normalize

config = Config.getConfig(parentKey='modules', key='ht_parser')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'File Parser'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_parser'), debug_module=True)

	def readFileToType(self, filename, typeToExport, typeOf=None, csv_headers=False):
		# Recogemos la extensión
		extension_file = filename.split('.')[-1]

		# Validamos parametros de filename y typeOf
		is_parseable = False
		if not extension_file.lower() in ('csv', 'html', 'json', 'xml'):
			if typeOf and typeOf.lower() in ('csv', 'html', 'json', 'xml'):
				is_parseable = True
		else:
			is_parseable = True

		# Si podemos parsearlo
		if is_parseable:
			# Transformar CSV a X
			if (extension_file or typeOf) == 'csv' and typeToExport == 'json':
				datos = self.__readCSVFile__(filename)
				return self.__csvToJSON__( datos, csv_headers )

			if (extension_file or typeOf) == 'csv' and typeToExport == 'xml':
				self.__csvToXML__()

			if (extension_file or typeOf) == 'csv' and typeToExport == 'html':
				self.__csvToHTML__()

			# Transformar JSON a X
			if (extension_file or typeOf) == 'json' and typeToExport == 'csv':
				datos = self.__readJSONFile__(filename)
				return self.__jsonToCSV__( datos )

			if (extension_file or typeOf) == 'json' and typeToExport == 'xml':
				self.__jsonToXML__()

			if (extension_file or typeOf) == 'json' and typeToExport == 'html':
				self.__jsonToHTML__()

			# Transformar XML a X
			if (extension_file or typeOf) == 'xml' and typeToExport == 'json':
				datos = self.__readXMLFile__(filename)
				return self.__xmlToJSON__( datos )

			if (extension_file or typeOf) == 'xml' and typeToExport == 'csv':
				self.__xmlToCSV__()

			if (extension_file or typeOf) == 'xml' and typeToExport == 'html':
				self.__xmlToHTML__()

			# Transformar HTML a X
			if (extension_file or typeOf) == 'html' and typeToExport == 'csv':
				self.__htmlToCSV__()

			if (extension_file or typeOf) == 'html' and typeToExport == 'xml':
				self.__htmlToXML__()

			if (extension_file or typeOf) == 'html' and typeToExport == 'json':
				self.__htmlToJSON__()

		else:
			return None
		
	def __readCSVFile__(self, filename):
		try:
			csvfile = open(filename, 'r')
			reader = csv.reader(csvfile)
			return reader
		except:
			return None

	def __readXMLFile__(self, filename):
		try:
			xmlfile = open(filename, 'r')
			datos = ET.parse(xmlfile).getroot()
			return datos
		except Exception as e:
			return str( e )

	def __readJSONFile__(self, filename):
		try:
			jsonfile = open(filename, 'r')
			datos = json.load( jsonfile )
			return datos
		except Exception as e:
			return str( e )

	def __csvToJSON__(self, fileData, csv_headers=False):
		data = {}

		headers = None

		temp_data = []

		for row in fileData:
			temp_data.append(row)

		if csv_headers:
			headers = temp_data[0]
			del temp_data[0]

		for i_row, row in enumerate(temp_data):
			
			if headers:
				data[ str( i_row ) ] = {}

				for i_col, col in enumerate(row):
					
					data[ str( i_row ) ][ headers[ i_col ] ] = col
			else:
				data[ str( i_row ) ] = row

		return data

	def __csvToXML__(self):
		pass
	
	def __csvToHTML__(self):
		pass

	def __jsonToCSV__(self, fileData):
		return json_normalize(fileData).to_csv( encoding='utf-8' )

	def __jsonToXML__(self):
		pass
	
	def __jsonToHTML__(self):
		pass

	def __xmlToCSV__(self):
		pass

	def __xmlToJSON__(self, fileData):
		try:
			parsedString = ET.tostring( fileData, encoding='unicode' )
			return json.dumps( xmltodict.parse(parsedString) )
		except Exception as e:
			return str( e )
	
	def __xmlToHTML__(self):
		pass

	def __htmlToCSV__(self):
		pass

	def __htmlToJSON__(self):
		pass
	
	def __htmlToXML__(self):
		pass
