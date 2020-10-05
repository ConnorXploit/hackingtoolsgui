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
		self._main_gui_func_ = 'encode'
		self.__gui_label__ = 'RSA Crypter'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_rsa'), debug_module=True)

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
			while prime_a == '' or prime_a == prime_b:
				prime_a = Utils.getRandomPrimeByLength(length)
			while prime_b == '' or prime_a == prime_b:
				prime_b = Utils.getRandomPrimeByLength(length)
		if prime_a > prime_b:
			temp = prime_b
			prime_b = prime_a
			prime_a = temp
		Logger.printMessage(message='getRandomKeypair', description=(prime_a, prime_b), debug_module=True)
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
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{msg} - Length: {l}'.format(msg=mensaje[0:10], l=len(mensaje)), debug_module=True)
			mensaje1 = [(ord(chr(char)) ** key) % n for char in mensaje]
			mensajeHex = Utils.asciiToHex(mensaje1)
			mensajeBase64 = Utils.hexToBase64(mensajeHex)
			mensajeFinalBase64 = Utils.joinBase64(mensajeBase64)
			return mensajeFinalBase64.decode("utf-8")
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='encrypt'), description='{msg}'.format(msg=e))
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

	def encode(self, password, plaintext):
		enc = []
		for i in range(len(plaintext)):
			key_c = password[i % len(password)]
			enc_c = chr((ord(plaintext[i]) + ord(key_c)) % 256)
			enc.append(enc_c)
		return base64.urlsafe_b64encode("".join(enc).encode()).decode()

	def decode(self, password, ciphertext):
		dec = []
		ciphertext = base64.urlsafe_b64decode(ciphertext).decode()
		for i in range(len(ciphertext)):
			key_c = password[i % len(password)]
			dec_c = chr((256 + ord(ciphertext[i]) - ord(key_c)) % 256)
			dec.append(dec_c)
		return "".join(dec)

	def encodeFromComplexMap(self, password, plaintext):
		data = self.encode(password, plaintext)
		complexMap = [ ht.Utils.randomText(length=16, alphabet='mixalpha-numeric-symbol14') for i in range(16) ]

		data_rss_encoded = []
		for char in data:
			char_mapped = False
			rss_appearances = ''
			for line_index, line in enumerate(complexMap):
				if not char_mapped:
					appearances = [i for i in range(len(line)) if line.startswith(char, i)]
					for app in appearances:
						if not char_mapped:
							use_this_appearance = bool(random.getrandbits(1))
							if use_this_appearance:
								rss_appearances = '{l}{s}{a}{ss}'.format( l=line_index, a=app, s=ht.Utils.getRandomCharFromDict('symbols14'), ss=ht.Utils.getRandomCharFromDict('symbols14') )
								char_mapped = True

			if not char_mapped:
				print('No mapeado: ', char)
				rss_appearances = '{l}{s}{l}{ss}'.format( l=char, a=char, s=ht.Utils.getRandomCharFromDict('symbols14'), ss=ht.Utils.getRandomCharFromDict('symbols14') )

			data_rss_encoded.append(rss_appearances)

		return ( ''.join(data_rss_encoded), ''.join(complexMap) )

	def decodeFromComplexMap(self, password, ciphertext, complexMap):
		try:
			full_data = ciphertext

			symbols14 = Config.getConfig('core', 'Utils', 'dictionaries', 'symbols14')

			full_lines = []

			if not isinstance(complexMap, list):
				complexMap = ''.join(complexMap.split('\n'))
				chunks, chunk_size = len(complexMap), len(complexMap)//16
				complexMap = [ complexMap[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

			better_decoded = full_data
			for symb in symbols14:
				better_decoded = ' '.join(better_decoded.split(symb))

			list_decoded = better_decoded.split(' ')

			count = 0
			for row in range( int(len(list_decoded)/2) ):
				full_lines.append( [ list_decoded[row + count], list_decoded[row + count + 1] ] )
				count += 1

			rss_decoded = []

			for lines in full_lines:
				row_n = lines[0]
				char_n = lines[1]
				if row_n == '':
					row_n = -1
				if char_n == '':
					char_n = -1
				try:
					row_n = int(row_n)
				except:
					pass
				try:
					char_n = int(char_n)
				except:
					pass
				if not isinstance(row_n, int) or not isinstance(char_n, int):
					rss_decoded.append(row_n)
				else:
					rss_decoded.append(complexMap[row_n][char_n])

			return self.decode(password, ''.join(rss_decoded))
		except:
			return 'Bad password'