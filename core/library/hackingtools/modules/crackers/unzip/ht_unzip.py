from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

from zipfile import ZipFile

config = Config.getConfig(parentKey='modules', key='ht_unzip')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		Utils.emptyDirectory(output_dir)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_unzip'))

	def extractFile(self, zipPathName, password, posible_combinations=1):
		#ZipFile only works with 7z with ZypCrypto encryption for setting the password
		try:
			Logger.printMessage(message="extractFile", description='ZIP - {pwd} - Posible Combinations: {com}'.format(pwd=password, com=posible_combinations), debug_core=True)
			with ZipFile(zipPathName) as zf:
				zf.extractall(pwd=str.encode(password))
			return password
		except Exception as e:
			return None