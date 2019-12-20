from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_pastebin')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_pastebin'), debug_module=True)