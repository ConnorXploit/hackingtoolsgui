from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os, sys, requests, json

config = Config.getConfig(parentKey='modules', key='ht_finder')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'checkerOnline'
		self.__gui_label__ = 'Find an Alias Registered Anywhere'
		self.options = {
			'facebook' : self.__facebook__,
			'twitter' : self.__twitter__,
			'instagram' : self.__instagram__,
			'medium' : self.__medium__,
			'github' : self.__github__,
			'bitbucket' : self.__bitbucket__,
		}

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_finder'), debug_module=True)

	def findAll(self, username):
		data = {}
		for opt, func in self.options.items():
			value = func(username)
			if value:
				data[opt] = value
		if data:
			return data
		return None

	def checkerOnline(self, username):
		url = 'https://checkuser.org/existence.php'
		posibilities = {}
		for i in range(1, 52): # There are 52 posibilities in the website
			data = {
				'index' : i,
				'username' : username
			}
			response = json.loads(requests.post(url, data=data).text)
			if response['status'] != 400:
				posibilities[ response['domain'].split('.')[0] ] = response['url']
		
		if posibilities:
			return posibilities
		return None			

	# a function for each site, which creates the request according to the username
	def __bitbucket__(self, username):
		url = "https://bitbucket.org/" + username + "/"
		request = requests.get(url)
		data = self.__parse__(request, username, url)
		return data

	def __github__(self, username):
		url = "https://github.com/" + username + "/"
		request = requests.get(url)
		data = self.__parse__(request, username, url)
		return data

	def __twitter__(self, username):
		url = "https://twitter.com/" + username + "/"
		request = requests.get(url)
		data = self.__parse__(request, username, url)
		return data

	def __instagram__(self, username):
		url = "https://instagram.com/" + username + "/"
		request = requests.get(url)
		data = self.__parse__(request, username, url)
		return data

	def __medium__(self, username):
		url = "https://medium.com/@" + username + "/"
		# Medium requires a browser as a user agent, such as chrome
		headers = {
			"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
		}
		request = requests.get(url, headers)
		data = self.__parse__(request, username, url)
		return data
		
	def __facebook__(self, username):
		url = "http://facebook.com/" + username + "/"
		request = requests.get(url)
		data = self.__parse__(request, username, url)
		return data

	# used for generating colored responses
	def __parse__(self, request, username, url):
		if request.status_code == 200:
			return url
		return None

	