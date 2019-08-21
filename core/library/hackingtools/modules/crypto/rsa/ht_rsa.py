from hackingtools.core import Logger, Config, Utils
import hackingtools as ht

import random
import base64
import os

config = Config.getConfig(parentKey='modules', key='ht_rsa')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
	'''How to use:

	prime_a, prime_b = self.getRandomKeypair()
	public, private = self.generate_keypair(prime_a, prime_b)

	print('Public key: {pub} - Private Key: {pri}'.format(pub=public, pri=private))

	encrypted_msg = self.encrypt(private, message)
	print('Message ciphered: {msg}'.format(msg=encrypted_msg))

	decrypted_msg = self.decrypt(public, encrypted_msg)
	print('Message deciphered: {msg}'.format(msg=decrypted_msg))
	
	'''

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_rsa'))

	def generate_keypair(self, prime_a, prime_b):
		if not (Utils.isPrime(int(prime_a)) and Utils.isPrime(int(prime_b))):
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
			g = Utils.euclides(e, phi)
			while g != 1:
				e = random.randrange(1, phi)
				g = Utils.euclides(e, phi)

			#Use Extended Euclid's Algorithm to generate the private key
			d = Utils.multiplicativeInverse(e, phi)
			
			#Return public and private keypair
			#Public key is (e, n) and private key is (d, n)
			return ((e, n), (d, n))

	def getRandomKeypair(self, length = 8):
		Logger.printMessage(message='{methodName}'.format(methodName='getRandomKeypair'), debug_module=True)
		prime_a = ''
		prime_b = ''
		while prime_a == prime_b:
			while prime_a == '':
				prime_a = Utils.getRandomPrimeByLength(length)
			while prime_b == '':
				prime_b = Utils.getRandomPrimeByLength(length)
		print(prime_a, prime_b)
		return (prime_a, prime_b)
	
	def encrypt(self, private_key, plaintext):
		try:
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{private_key} - {msg}'.format(private_key=private_key, msg=plaintext[0:10]), debug_module=True)
			#Unpack the key into it's components
			key, n = private_key
			ba64 = base64.b64encode(plaintext)
			ashex = Utils.asciiToHex(ba64)
			hexba64 = Utils.hexToBase64(ashex)
			ba64un = Utils.joinBase64(hexba64)
			decasc = Utils.decimalToAscii(ba64un)
			mensaje = Utils.textToAscii(decasc)
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{msg}'.format(msg=mensaje[0:10]), debug_module=True)
			mensaje1 = [(ord(chr(char)) ** key) % n for char in mensaje]
			mensajeHex = Utils.asciiToHex(mensaje1)
			mensajeBase64 = Utils.hexToBase64(mensajeHex)
			mensajeFinalBase64 = Utils.joinBase64(mensajeBase64)
			return mensajeFinalBase64.decode("utf-8")
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{msg}'.format(msg=e), debug_error=True)
			return

	def decrypt(self, public_key, ciphertext):
		Logger.printMessage(message='{methodName}'.format(methodName='decrypt'), description='{public_key}'.format(public_key=public_key), debug_module=True)
		#Unpack the key into its components
		key, n = public_key
		menRec = Utils.asciiToBase64(ciphertext.encode('utf-8'))
		menHex = Utils.base64ToHex(menRec)
		menDec = Utils.hexToDecimal(menHex)
		Logger.printMessage(message='{methodName}'.format(methodName='decrypt'), description='{msg}'.format(msg=menDec[0:10]), debug_module=True)
		menDesc = [((char ** key) % n) for char in menDec]
		menAscii = Utils.decimalToAscii(menDesc)
		decasc = Utils.asciiToBase64(''.join(menAscii).encode())
		hexba64 = Utils.base64ToHex(decasc)
		ashex = Utils.hexToDecimal(hexba64)
		deasc = Utils.decimalToAscii(ashex)
		ba64 = base64.b64decode(deasc.encode())
		return ba64