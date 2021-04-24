from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os
import r2pipe

config = Config.getConfig(parentKey='modules', key='ht_radare2')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():


	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'Radare2 for Reversing Apps'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_radare2'), debug_module=True)

	def getImports(self, filemon):
		try:
			r = r2pipe.open(filemon)
			# saca la tabla de dll importadas en json
			return r.cmd('iij')
		except Exception as e:
			return str(e)