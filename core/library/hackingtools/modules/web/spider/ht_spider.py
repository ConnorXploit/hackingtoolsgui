from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os
from colorama import Fore

import multiprocessing
import sys
from bs4 import BeautifulSoup
import urllib.request as urllib3
import time
import mechanize
import inspect

config = Config.getConfig(parentKey='modules', key='ht_spider')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'crawl'
		self.__gui_label__ = 'Web Spider'
	
	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_spider'), debug_module=True)

	def crawl(self, url, depth=100, proxies=None, proxyhost=None, proxyuser=None, proxypassword=None, proxyport=None, proxysecure="http"):
		Logger.printMessage(message='{methodName}'.format(methodName='crawl'), debug_module=True)
		try:
			depth = int(depth)
			totalDeepCrawled = 0
			linksVisited = [url]
			totalProfundity = 0
			webForms = {}
			proxyhost = proxyhost
			proxyuser = proxyuser
			proxypassword = proxypassword
			proxysecure = proxysecure
			proxyport = proxyport
			proxies = proxies

			if proxyhost != None and proxyport != None:
				if proxyuser != None and proxypassword != None: 
					proxies = urllib3.ProxyHandler({proxysecure: proxysecure+"://"+proxyuser+":"+proxypassword+"@"+proxyhost+":"+proxyport})
				else:
					proxies = urllib3.ProxyHandler({proxysecure: proxysecure+"://"+proxyhost+":"+proxyport})
			
			if proxies:
				urlRootSite = urllib3.urlopen(url, proxies=proxies)
			else:
				urlRootSite = urllib3.urlopen(url)

			contents = urlRootSite.read()
			rootSite = BeautifulSoup(contents, features="html5lib")
			links = rootSite.find_all("a")
			webForms[url] = self.__storeWebSiteForms__(url=url, proxies=proxies, forms=webForms)

			try:
				for link in links:
					#process = multiprocessing.Process(target=__handleLink__, args=[link])
					#process.daemon = True
					#process.start()	
					#process.join()
					if not "http" in link["href"]:
						link["href"] = '{url}{subdomain}'.format(url=url, subdomain=link["href"])
					self.__handleLink__(link=link, depth=depth, webForms=webForms, proxies=proxies, linksVisited=linksVisited, totalProfundity=totalProfundity)				
					totalProfundity = 0
			finally:
				pass
			return (linksVisited, webForms)
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='crawl'), description='{param}'.format(param=e), is_error=True, is_warn=True)
			raise
		
	def __handleLink__(self, link, depth=100, webForms={}, proxies=None, linksVisited=[], totalProfundity=0):
		Logger.printMessage(message='{methodName}'.format(methodName='__handleLink__'), description='{param}'.format(param=link), debug_module=True)
		totalProfundity += 1	
		if ('href' in dict(link.attrs) and "http" in link['href']):
			try:
				href = link["href"]
				if href in linksVisited:
					return
				if proxies:
					urlLink = urllib3.urlopen(href, proxies=proxies)
				else:
					urlLink = urllib3.urlopen(href)
				linksVisited.append(link['href'])
				#Extract info about the link, before to get links in this page.
				if totalProfundity <= depth:
					linkSite = BeautifulSoup(urlLink, "lxml")
					depthLinks = linkSite.find_all("a")				
					webForms[link['href']] = self.__storeWebSiteForms__(url=link['href'], proxies=proxies, forms=webForms)
					for sublink in depthLinks:
						#processLink = multiprocessing.Process(target=self.__handleLink__, args=[sublink])
						#processLink.daemon = True
						#processLink.start()
						self.__handleLink__(link=sublink, depth=depth, webForms=webForms, proxies=proxies, linksVisited=linksVisited, totalProfundity=totalProfundity)
				else:
					totalProfundity -= 1
					return
			except:
				pass
	
	def __storeWebSiteForms__(self, url, proxies=None, forms={}):
		Logger.printMessage(message='{methodName}'.format(methodName='__storeWebSiteForms__'), description='{param}'.format(param=url), debug_module=True)
		browser = mechanize.Browser()		
		if proxies:
			browser.set_proxies(proxies)
		browser.open(url)
		try:
			for form_id, form in enumerate(browser.forms()):
				forms[str(form_id)] = {}
				if not forms[str(form_id)][form.action]:
					forms[str(form_id)][form.action] = {}
				forms[str(form_id)][form.action][form.method] = {}
				if not forms[str(form_id)][form.action][form.method][form.name]:
					forms[str(form_id)][form.action][form.method][form.name] = {}
				for control in form.controls:
					forms[str(form_id)][form.action][form.method][form.name][control] = {}
					if control.name:
						forms[str(form_id)][form.action][form.method][form.name][control]["name"] = control.name
					if control.type:
						forms[str(form_id)][form.action][form.method][form.name][control]["type"] = control.type
					if control.value:
						forms[str(form_id)][form.action][form.method][form.name][control]["value"] = control.value
		except AttributeError:
			pass
		except:
			pass
		return forms