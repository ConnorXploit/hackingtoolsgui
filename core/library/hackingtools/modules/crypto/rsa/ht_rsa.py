from hackingtools.core import Logger
import random
import base64

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_rsa loaded', debug_module=True)
		pass

	def generate_keypair(self, prime_a, prime_b):
		if not (self.__is_prime__(prime_a) and self.__is_prime__(prime_b)):
			raise ValueError('Both numbers must be prime.')
		elif prime_a == prime_b:
			raise ValueError('p and q cannot be equal')
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
		mensajeRecibido = self.__recibirBase64__(ciphertext)
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

	def test(self):
		message = input('Escribe tu mensaje a cifrar > ')

		prime_a, prime_b = self.getRandomKeypair()
		public, private = self.generate_keypair(prime_a, prime_b)
		print('Public key: {pub} - Private Key: {pri}'.format(pub=public, pri=private))

		encrypted_msg = self.encrypt(private, message)
		print('Mensaje cifrado: {msg}'.format(msg=encrypted_msg))

		decrypted_msg = self.decrypt(public, encrypted_msg)
		print('Mensaje descifrado: {msg}'.format(msg=decrypted_msg))