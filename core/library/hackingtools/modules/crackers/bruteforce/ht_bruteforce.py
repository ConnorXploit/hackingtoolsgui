from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

import time
import numpy

config = Config.getConfig(parentKey='modules', key='ht_bruteforce')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		Utils.emptyDirectory(output_dir)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_bruteforce'))

	def crackZip(self, zipPathName, unzipper=None, alphabet='lalpha', password_length=4, password_pattern=None, log=False):
		max_length_posibilities = int(config['max_for_chunk'])
		if not unzipper:
			unzipper = ht.getModule('ht_unzip')
		if log:
			Logger.setDebugCore(True)
		texts = Utils.getDict(length=int(password_length), alphabet=alphabet, try_pattern=password_pattern)
		if len(texts) > max_length_posibilities:
			texts_list = numpy.array_split(texts, max_length_posibilities)
		else:
			texts_list = [texts]
		for index_t_list, t_list in enumerate(texts_list):
			if len(texts) > max_length_posibilities:
				Logger.printMessage(message='crackZip', description='Chunk {n} - {word}'.format(n=index_t_list, word=t_list[1]))
			for text in t_list:
				if os.path.isfile(zipPathName):
					password = unzipper.extractFile(zipPathName, text, posible_combinations=len(texts))
				else:
					Logger.printMessage(message='crackZip', description='File doesnt exists {a}'.format(a=zipPathName), is_error=True)
					break
				if password:
					Logger.printMessage(message='crackZip', description='{msg_password_is} {a}'.format(msg_password_is=config['msg_password_is'], a=password))
					if log:
						Logger.setDebugCore(False)
					return password
		Logger.setDebugCore(False)
		return None