from hackingtools.core import Logger
import random

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_rsa loaded', debug_module=True)
		pass

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

	def encrypt(self, private_key, plaintext):
		#Unpack the key into it's components
		key, n = private_key
		#Convert each letter in the plaintext to numbers based on the character using a^b mod m
		cipher = [(ord(char) ** key) % n for char in plaintext]
		#Return the array of bytes
		return cipher

	def decrypt(self, public_key, ciphertext):
		#Unpack the key into its components
		key, n = public_key
		#Generate the plaintext based on the ciphertext and key using a^b mod m
		plain = [chr((char ** key) % n) for char in ciphertext]
		#Return the array of bytes as a string
		return ''.join(plain)
		
	def getRandomKeypair(self):
		prime_a = ''
		prime_b = ''
		while prime_a == '':
			num = random.randint(random.randint(0,15),random.randint(15,30))*random.randint(1,10)
			if self.__is_prime__(num):
				prime_a = num
		while prime_b == '':
			num = random.randint(random.randint(30,45),random.randint(45,60))*random.randint(1,10)
			if self.__is_prime__(num):
				prime_b = num
		return (prime_a, prime_b)

	def test(self):
		message= input('Escribe tu mensaje a cifrar > ')

		prime_a, prime_b = self.getRandomKeypair()
		public, private = self.generate_keypair(prime_a, prime_b)
		print('Public key: {pub} - Private Key: {pri}'.format(pub=public, pri=private))

		encrypted_msg = self.encrypt(private, message)
		print('Mensaje cifrado: {msg}'.format(msg=encrypted_msg))

		encrypted_msg_joined = ''.join(map(lambda x: str(x), encrypted_msg))
		print('Mensaje cifrado junto: {msg}'.format(msg=encrypted_msg_joined))

		decrypted_msg = self.decrypt(public, encrypted_msg)
		print('Mensaje descifrado: {msg}'.format(msg=decrypted_msg))