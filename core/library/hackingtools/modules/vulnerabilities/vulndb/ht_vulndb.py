from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os, requests

config = Config.getConfig(parentKey='modules', key='ht_vulndb')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'VulnDB Vulnerability Info Extractor'
		self.headers = {
			'X-VulDB-ApiKey' : ht.Config.getAPIKey('vulndb_api')
		}
		self.url = 'https://vulners.com/api/v3'
		self.options = {
			'suggest' : '/search/suggest/',
			'search-cve' : '/search/id/'
		}

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_vulndb'), debug_module=True)

	def getAPI(self, vulndb_api=None, session_id=None):
		if not vulndb_api:
			return ht.Config.getAPIKey('vulndb_api', session_id)
		return vulndb_api

	def getSuggestions(self, fieldType, fieldName, vulndb_api=None, session_id=None):
		self.headers = {
			'X-VulDB-ApiKey' : self.getAPI(vulndb_api, session_id)
		}
		params = {
			'type' : fieldType,
			'fieldName' : fieldName
		}
		suggest_url = '{h}{u}'.format(h=self.url, u=self.options['suggest'])
		response = requests.get(suggest_url, headers=self.headers, params=params)
		return response.text

	def getCVEInfo(self, CVE, references=False, vulndb_api=None, session_id=None):
		self.headers = {
			'X-VulDB-ApiKey' : self.getAPI(vulndb_api, session_id)
		}
		params = {
			'id' : CVE,
			'references' : references
		}
		suggest_url = '{h}{u}'.format(h=self.url, u=self.options['search-cve'])
		response = requests.get(suggest_url, headers=self.headers, params=params)
		return response.text

	