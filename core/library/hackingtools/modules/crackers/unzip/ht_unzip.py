from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

import zipfile
from zipfile import ZipFile

config = Config.getConfig(parentKey='modules', key='ht_unzip')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		Utils.emptyDirectory(output_dir)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_unzip'))

	def extractFile(self, zipPathName, password='', posible_combinations=1, output_dir_new=None):
		#ZipFile only works with 7z with ZypCrypto encryption for setting the password
		try:
			Logger.printMessage(message="extractFile", description='ZIP - {pwd} - {msg_posible_comb}: {com}'.format(pwd=password, msg_posible_comb=config['posible_combinations'], com=posible_combinations), debug_core=True)
			with ZipFile(zipPathName) as zf:
				zf.extractall(output_dir if not output_dir_new else output_dir_new, pwd=str.encode(password))
			return password
		except Exception as e:
			Logger.printMessage(message="extractFile", description=str(e), is_error=True)
			return None
	
	def zipFiles(self, files, new_folder_name):
		# Creates a Zip File from a list of files and a foldername for the new zip file
		new_zip = os.path.join(output_dir, '{n}.zip'.format(n=new_folder_name.split('.')[0]))
		shutil.make_archive(new_zip, 'zip', dir_name)
		zipF = ZipFile(new_zip, "w")
		for fpath in files:
			fdir, fname = os.path.split(fpath)
			zip_path = os.path.join(output_dir, new_folder_name, fname)
			zipF.write(fpath, zip_path)
		zipF.close()
		return new_zip 