from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

import requests

config = Config.getConfig(parentKey='modules', key='ht_abuseipdb')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'Abuse IP DB'
		self._funcArgFromFunc_ = {
			'_functionName_' : {
				'_functionParamName_' : {
					'_moduleName_' : '_functionName_' 
				}
			}
		}

		self.api_url = 'https://api.abuseipdb.com/api/v2/check'

		self.api = ''

		self.headers = {
			'Accept' : 'application/json',
			'Key' : self.api
		}

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_abuseipdb'), debug_module=True)
	
	def __getAbuseByAPI__(self, abuseipdb_api='', session_id=None):
		if not abuseipdb_api:
			self.api = ht.Config.getAPIKey('abuseipdb_api', session_id)
		else:
			self.api = abuseipdb_api

		self.headers = {
			'Accept' : 'application/json',
			'Key' : self.api
		}

	def checkIP(self, ip, score=False, totalReports=False, abuseipdb_api=None):
		self.__getAbuseByAPI__(abuseipdb_api)
		if not self.api:
			return 'Debes usar una API Key válida'
		response = requests.get(self.api_url, headers=self.headers, params={'ipAddress' : ip})
		if response.status_code == 200:
			data = response.json()
			if 'data' in data:
				finalData = {}
				finalData['ip'] = ip
				finalData['isPublic'] = data['data']['isPublic']
				if totalReports:
					finalData['totalReports'] = data['data']['totalReports']
				if score:
					finalData['score'] = data['data']['abuseConfidenceScore']
				return finalData
			return {}
		return {}