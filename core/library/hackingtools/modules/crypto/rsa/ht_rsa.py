from hackingtools.core import Logger, Config
import hackingtools as ht

import random
import base64
config = Config.getConfig(parentKey='modules', key='ht_rsa')

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_rsa loaded', debug_core=True)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_rsa'))

	def generate_keypair(self, prime_a, prime_b):
		if not (self.__is_prime__(int(prime_a)) and self.__is_prime__(int(prime_b))):
			Logger.printMessage(message='{methodName}'.format(methodName='generate_keypair'), description=config['bad_identical_prime'], debug_module=True, is_error=True)
			return config['bad_identical_prime']
		elif prime_a == prime_b:
			Logger.printMessage(message='{methodName}'.format(methodName='generate_keypair'), description=config['p_q_equal_error'], debug_module=True, is_error=True)
			return config['p_q_equal_error']
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
		try:
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{private_key} - {msg}'.format(private_key=private_key, msg=plaintext[0:10]), debug_module=True)
			#Unpack the key into it's components
			key, n = private_key
			ba64 = base64.b64encode(plaintext)
			ashex = self.__ASCII_Hex__(ba64)
			hexba64 = self.__Hex_Base64__(ashex)
			ba64un = self.__unirBase64__(hexba64)
			decasc = self.__decimal_ASCII__(ba64un)
			mensaje = self.__mensajeASCII__(decasc)
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{msg}'.format(msg=mensaje[0:10]), debug_module=True)
			mensaje1 = [(ord(chr(char)) ** key) % n for char in mensaje]
			mensajeHex = self.__ASCII_Hex__(mensaje1)
			mensajeBase64 = self.__Hex_Base64__(mensajeHex)
			mensajeFinalBase64 = self.__unirBase64__(mensajeBase64)
			return mensajeFinalBase64.decode("utf-8")
		except:
			return config['error_encrypt']

	def decrypt(self, public_key, ciphertext):
		Logger.printMessage(message='{methodName}'.format(methodName='decrypt'), description='{public_key}'.format(public_key=public_key), debug_module=True)
		#Unpack the key into its components
		key, n = public_key
		menRec = self.__recibirBase64__(ciphertext.encode('utf-8'))
		menHex = self.__Base64_Hex__(menRec)
		menDec = self.__Hex_decimal__(menHex)
		Logger.printMessage(message='{methodName}'.format(methodName='decrypt'), description='{msg}'.format(msg=menDec[0:10]), debug_module=True)
		menDesc = [((char ** key) % n) for char in menDec]
		menAscii = self.__decimal_ASCII__(menDesc)
		decasc = self.__recibirBase64__(''.join(menAscii).encode())
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
		return men

	def __ASCII_Hex__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__ASCII_Hex__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeHex = [hex(numero)[2:] for numero in mensaje]
		return mensajeHex

	def __Hex_Base64__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__Hex_Base64__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeBase64 = [base64.b64encode(numero.encode()) for numero in mensaje]
		return mensajeBase64

	def __unirBase64__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__unirBase64__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		msg_base64 = ''.join([mensaje[i].decode('utf-8') for i in range(0, len(mensaje))])
		Logger.printMessage(message='{methodName}'.format(methodName='__unirBase64__'), description='{msg_base64} ...'.format(msg_base64=msg_base64[0:10]), debug_module=True)
		return msg_base64.encode()

	def __recibirBase64__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__recibirBase64__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		msg_base64 = [mensaje[i:i+4] for i in range(0, len(mensaje), 4)]
		return msg_base64
		
	def __Base64_Hex__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__Base64_Hex__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeHex = [base64.b64decode(b64) for b64 in mensaje]
		return mensajeHex

	def __Hex_decimal__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__Hex_decimal__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensajeDecimal = [int(hexa.decode("UTF-8"), 16) for hexa in mensaje]
		return mensajeDecimal

	def __decimal_ASCII__(self, mensaje):
		Logger.printMessage(message='{methodName}'.format(methodName='__decimal_ASCII__'), description='Length: {length} - {mensaje} ...'.format(length=len(mensaje), mensaje=mensaje[0:10]), debug_module=True)
		mensaje1 = ''.join([chr(decimal) for decimal in mensaje])
		return mensaje1

	def __getRandomPrime__(self, length = 8):
		prime = 0
		while True:
			primo=random.randint(10**(length-1), 10**length)
			if self.__is_prime__(primo):
				return primo

	def test(self):
		message = input('Escribe tu mensaje a cifrar > ')

		prime_a, prime_b = self.getRandomKeypair()
		public, private = self.generate_keypair(prime_a, prime_b)
		print('Public key: {pub} - Private Key: {pri}'.format(pub=public, pri=private))

		encrypted_msg = self.encrypt(private, message)
		print('Mensaje cifrado: {msg}'.format(msg=encrypted_msg))

		decrypted_msg = self.decrypt(public, encrypted_msg)
		print('Mensaje descifrado: {msg}'.format(msg=decrypted_msg))