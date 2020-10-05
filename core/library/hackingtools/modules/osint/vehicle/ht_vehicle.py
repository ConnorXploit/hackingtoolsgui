from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

import requests, json

config = Config.getConfig(parentKey='modules', key='ht_vehicle')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'searchIdentificationPlate'
		self.__gui_label__ = 'Vehicle Info Extractor'
		self._funcArgFromFunc_ = {
			'_functionName_' : {
				'_functionParamName_' : {
					'_moduleName_' : '_functionName_' 
				}
			}
		}
		self._mainUrl_ = 'https://motorgiga.com/personal/ajax'
		self._urlMatriculationDate_ = '{url}/getAntiguedadMatricula.php?tipo=actual&numeroMat={num}&letrasMat={chars}'
		self._urlIdentificationTag_ = '{url}/getEtiquetaEco.php?matricula={plate}'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_vehicle'), debug_module=True)
		
	def searchIdentificationPlate(self, plate):
		try:
			if len(plate) != 7:
				return { 'error' : 'The plate has to be like: 0000AAA' }
				
			num = plate[:4]
			chars = plate[-3:]
			
			response = requests.get(self._urlMatriculationDate_.format(url=self._mainUrl_, num=num, chars=chars))
			data = json.loads(response.content.decode()[1:-1])

			if 'depuracion' in data and 'mes' in data['depuracion'] and 'ano' in data['depuracion']:
				response = requests.get(self._urlIdentificationTag_.format(url=self._mainUrl_, plate=plate))
				dataIdent = json.loads(response.content.decode()[1:-1])
				
				hasTag = False
				imgUrl = ''
				tag = ''
				
				if 'caso' in dataIdent and 'con_etiqueta' in dataIdent['caso']:
					hasTag = True
					
				if 'etiqueta' in dataIdent:
					tag = dataIdent['etiqueta']
					
				if 'img' in dataIdent:
					imgUrl = dataIdent['img']
					
				finalD = {}
				
				finalD['month'] = data['depuracion']['mes']
				finalD['year'] = data['depuracion']['ano']
				finalD['plate'] = plate
				
				if hasTag:
					finalD['hasTag'] = hasTag
					
				if tag:
					finalD['tag'] = tag
				
				if imgUrl:
					finalD['img'] = imgUrl
					
				return finalD

			return { 'error' : 'The plate has to be like: 0000AAA' }
		except Exception as e:
			return { 'error' : str(e) }
