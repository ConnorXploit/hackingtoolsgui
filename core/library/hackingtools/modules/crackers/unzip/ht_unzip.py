from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

import shutil
from zipfile import ZipFile

config = Config.getConfig(parentKey='modules', key='ht_unzip')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		Utils.emptyDirectory(output_dir)
		self._main_gui_func_ = 'extractFilePassword'
		self.__gui_label__ = 'Extract ZIP File'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_unzip'), debug_module=True)

	def extractFilePassword(self, zipPathName, password='', posible_combinations=1, output_dir_new=None):
		#ZipFile only works with 7z with ZypCrypto encryption for setting the password
		try:
			Logger.printMessage(message="extractFilePassword", description='ZIP - {pwd} - {msg_posible_comb}: {com}'.format(pwd=password, msg_posible_comb=config['posible_combinations'], com=posible_combinations), debug_module=True)
			with ZipFile(zipPathName) as zf:
				zf.extractall(output_dir if not output_dir_new else output_dir_new, pwd=str.encode(password))
			return password
		except Exception as e:
			Logger.printMessage(message="extractFilePassword", description='{e} - {p}'.format(e=str(e), p=password), is_error=True)
			return None

	def extractFile(self, zipPathName, password=None):
		#ZipFile only works with 7z with ZypCrypto encryption for setting the password
		try:
			with ZipFile(zipPathName) as zf:
				return zf.extractall(password) if password else zf.extractall(os.path.split(zipPathName)[0])
		except Exception as e:
			Logger.printMessage(message="extractFile", description=str(e), is_error=True)
			return None
	
	def zipDirectory(self, new_folder_name):
		# Creates a Zip File from a directory
		return shutil.make_archive(new_folder_name, 'zip', new_folder_name)