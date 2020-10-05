from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

import binascii, base64

config = Config.getConfig(parentKey='modules', key='ht_rc4')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'RC4 Crypter'
		self._funcArgFromFunc_ = {
			'_functionName_' : {
				'_functionParamName_' : {
					'_moduleName_' : '_functionName_' 
				}
			}
		}
		self.state = [None] * 256
		self.p = None
		self.q = None

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_rc4'), debug_module=True)
	
	def encrypt(self, password, text):
		try:
			S = list(range(256))
			j = 0

			for i in list(range(256)):
				j = (j + S[i] + ord(password[i % len(password)])) % 256
				S[i], S[j] = S[j], S[i]

			j = 0
			y = 0
			out = []

			for char in text:
				j = (j + 1) % 256
				y = (y + S[j]) % 256
				S[j], S[y] = S[y], S[j]

				out.append(chr(ord(char) ^ S[(S[j] + S[y]) % 256]))

			return ''.join(out)
		except Exception as e:
			Logger.printMessage(str(e), is_error=True)
			return ''

	def decrypt(self, password, text):
		return self.encrypt(password, text)
