from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_fuzz')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'Web Fuzzer'
		self._funcArgFromFunc_ = {
			'_functionName_' : {
				'_functionParamName_' : {
					'_moduleName_' : '_functionName_' 
				}
			}
		}

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_fuzz'), debug_module=True)