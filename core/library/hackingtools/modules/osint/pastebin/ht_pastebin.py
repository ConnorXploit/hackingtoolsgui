from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

import time
import requests
import datetime
from bs4 import BeautifulSoup
from io import StringIO
import gzip

config = Config.getConfig(parentKey='modules', key='ht_pastebin')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'search_pastebin'
		self.__gui_label__ = 'Pastebin Searcher'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_pastebin'), debug_module=True)

	def search_pastebin(self, keywords, run_time=0, match_total=None, crawl_total=20):
		length = 0
		time_out = False
		found_keywords = []
		paste_list = set([])
		root_url = 'http://pastebin.com'
		raw_url = 'http://pastebin.com/raw/'
		start_time = datetime.datetime.now()

		keywords = ['ssh', 'pass', 'key', 'token']

		try:
			keywords = set(keywords.split(","))
		except:
			pass
		
		try:
			run_time = int(run_time)
		except:
			pass
		
		try:
			match_total = int(match_total)
		except:
			pass
		
		try:
			crawl_total = int(crawl_total)
		except:
			pass
		
		try:
			# Continually loop until user stops execution
			while True:

				#	Get pastebin home page html
				root_html = BeautifulSoup(self.__fetch_page__(root_url), 'html.parser')
				
				#	For each paste in the public pastes section of home page
				for paste in self.__find_new_pastes__(root_html):
					
					#	look at length of paste_list prior to new element
					length = len(paste_list)
					paste_list.add(paste)

					#	If the length has increased the paste is unique since a set has no duplicate entries
					if len(paste_list) > length:
						
						#	Add the pastes url to found_keywords if it contains keywords
						raw_paste = '{r}{p}'.format(r=str(raw_url), p=str(paste))
						found_keywords = self.__find_keywords__(raw_paste, found_keywords, keywords)

					else:

						#	If keywords are not found enter time_out
						time_out = True

				# Enter the timeout if no new pastes have been found
				if time_out:
					time.sleep(2)

				Logger.printMessage("Crawled total of {n} Pastes, Keyword matches {k}".format(n=len(paste_list), k=len(found_keywords)), debug_module=True)

				if run_time and (start_time + datetime.timedelta(seconds=run_time)) < datetime.datetime.now():
					Logger.printMessage("Reached time limit, Found {n} matches.".format(n=len(found_keywords)), debug_module=True)
					return found_keywords
				# Exit if surpassed specified match timeout 
				if match_total and len(found_keywords) >= match_total:
					Logger.printMessage("Reached match limit, Found {n} matches.".format(n=len(found_keywords)), debug_module=True)
					return found_keywords

				# Exit if surpassed specified crawl total timeout 
				if crawl_total and len(paste_list) >= crawl_total:
					Logger.printMessage("Reached total crawled Pastes limit, Found {n} matches.".format(n=len(found_keywords)), debug_module=True)
					return found_keywords

		# 	On keyboard interupt
		except KeyboardInterrupt:
			return found_keywords
		#	If http request returns an error and 
		except Exception as e:
			Logger.printMessage(str(e), is_error=True)
			return found_keywords

		return found_keywords

	def __find_new_pastes__(self, root_html):
		new_pastes = []

		div = root_html.find('div', {'id': 'menu_2'})
		ul = div.find('ul', {'class': 'right_menu'})
		
		for li in ul.findChildren():
			if li.find('a'):
				new_pastes.append(str(li.find('a').get('href')).replace("/", ""))

		return new_pastes

	def __find_keywords__(self, raw_url, found_keywords, keywords):
		paste = self.__fetch_page__(raw_url)

		#	Todo: Add in functionality to rank hit based on how many of the keywords it contains
		for keyword in keywords:
			if paste.find(keyword) != -1:
				found_keywords.append(raw_url)
				break

		return found_keywords

	def __fetch_page__(self, page):
		response = requests.get(page)
		return response.content.decode()