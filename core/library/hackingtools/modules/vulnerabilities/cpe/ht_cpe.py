from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_cpe')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = None
		self.__gui_label__ = 'CPE Vulnerability Info Extractor'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_cpe'), debug_module=True)