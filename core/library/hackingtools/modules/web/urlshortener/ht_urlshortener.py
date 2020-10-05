from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

from pyshorteners import Shortener

config = Config.getConfig(parentKey='modules', key='ht_urlshortener')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'createShortcut'
		self.__gui_label__ = 'URL Shortener'
		self._funcArgFromFunc_ = {
			'createShortcut' : {
				'domainShortener' : {
					'urlshortener' : 'getShortDomains' 
				}
			}
		}

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_urlshortener'), debug_module=True)

	def createShortcut(self, url, fakeUrl, fakeText, domainShortener='tinyurl', api_key=None, user_id=None):
		try:
			short = Shortener(api_key=api_key, user_id=user_id)
			if domainShortener in short.available_shorteners:
				sh = eval( 'short.{do}'.format(do=domainShortener) )
				endLink = sh.short(url)
				withouthttp = endLink[7:]
				if withouthttp.startswith('/'):
					withouthttp = withouthttp[1:]
				fakeUrl = fakeUrl.replace('http://', '').replace('https://', '').replace('www.', '')
				fakeText = '-'.join( fakeText.split(' ') )
				return "https://www.{dom}-{post}@{withouthttp}".format(dom=fakeUrl, post=fakeText, withouthttp=withouthttp)
			return ""
		except Exception as e:
			Logger.printMessage(str(e), is_warn=True)
			return ""

	def getShortDomains(self):
		return Shortener().available_shorteners