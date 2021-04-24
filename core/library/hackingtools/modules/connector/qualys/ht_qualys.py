from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

config = Config.getConfig(parentKey='modules', key='ht_qualys')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'Qualys Scanner'
		
		self.server = ''

		self.session = None
		self.auth = None
		self.cookies = None

		self.username = None
		self.password = None

		self.urls = {}
		self.urls['US1'] = 'https://qualysguard.com'
		self.urls['US2'] = 'https://qualysguard.qg2.apps.qualys.com'
		self.urls['US3'] = 'https://qualysguard.qg3.apps.qualys.com'
		self.urls['US4'] = 'https://qualysguard.qg4.apps.qualys.com'
		self.urls['EU1'] = 'https://qualysguard.eu'
		self.urls['EU2'] = 'https://qualysguard.qg2.apps.qualys.eu'
		self.urls['IN1'] = 'https://qualysguard.qg1.apps.qualys.in'
		self.urls['CA1'] = 'https://qualysguard.qg1.apps.qualys.ca'

		self.headers = {} 
		self.headers['X-Requested-With'] = 'ht-qualys-connector'

		self.api = {}
		self.api['session'] = '/api/2.0/fo/session/'

		self.api['common'] = {}
		self.api['common']['assets'] = '/qps/rest/2.0/search/am/hostasset/'
		self.api['common']['assets2'] = '/api/2.0/fo/asset/host/'
		self.api['common']['scan'] = '/api/2.0/fo/scan/'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_qualys'), debug_module=True)

	def __getServerUrlByUsername__(self, username):
		try:
			if '_' in username:
				self.server = self.urls['US1']
			elif '2' in username:
				self.server = self.urls['US2']
			elif '3' in username:
				self.server = self.urls['US3']
			elif '4' in username:
				self.server = self.urls['US4']
			elif '-' in username:
				self.server = self.urls['EU1']
			elif '5' in username or '!' in username:
				self.server = self.urls['EU2']
			elif '8' in username:
				self.server = self.urls['IN1']
			elif '9' in username:
				self.server = self.urls['CA1']
			else:
				self.server = self.urls['US1']
		except:
			self.server = self.urls['US1']

	def connect(self, username, password):
		try:
			# Check and set the server depending on the user
			self.__getServerUrlByUsername__(username)

			# Save credentiales temporaly
			self.username = username
			self.password = password

			# Create payload for the API
			data = {
				'username' : self.username,
				'password' : self.password,
				'action' : 'login'
			}
			
			# Join safely the server URL with the API request path
			qualys_url = urljoin(self.server, self.api['session'])

			# Start a session for getting later the cookie that we will use for login next times
			self.session = requests.Session()

			# Get the response from the POST requests
			response = self.session.post( qualys_url, data=data, headers=self.headers, auth=self.auth )

			# If all is ok
			if response.status_code == 200:
				# Save the cookies for later sessions
				self.cookies = self.session.cookies.get_dict()
				self.auth = HTTPBasicAuth( self.username, self.password )
				return self
			return None
		except:
			return None

	def disconnect(self):
		try:
			if self.session:
				# Create payload for the API
				data = {
					'action' : 'logout'
				}
				
				# Join safely the server URL with the API request path
				qualys_url = urljoin(self.server, self.api['session'])

				# Get the response from the POST requests
				response = self.session.post( qualys_url, data=data, headers=self.headers, cookies=self.cookies, auth=self.auth )

				# If all is ok
				if response.status_code == 200:
					# Empty all session params
					self.cookies, self.username, self.password, self.session = ( None, None, None, None )
					return self
			return None
		except:
			return None

	def scan(self, ips):
		try:
			if self.session:
				# Create payload for the API
				data = {
					'ips' : ips,
					'action' : 'list'
				}

				# Join safely the server URL with the API request path
				qualys_url = urljoin(self.server, self.api['common']['assets2'])

				# Get the response from the POST requests
				response = self.session.get( qualys_url, data=data, headers=self.headers, cookies=self.cookies, auth=self.auth )

				# If all is ok
				if response.status_code == 200:
					return response.text
			return None
		except:
			return None
