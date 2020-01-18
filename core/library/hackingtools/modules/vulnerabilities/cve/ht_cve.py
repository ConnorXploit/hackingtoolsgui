from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

from bs4 import BeautifulSoup
import urllib.request as urllib3

config = Config.getConfig(parentKey='modules', key='ht_cve')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_cve'), debug_module=True)

	def searchCVE(self, cve_id=''):
		try:
			url = 'https://www.cvedetails.com/cve/{id}'.format(id=cve_id.strip())
			soup = BeautifulSoup(urllib3.urlopen(url).read())
			CVE = soup.find(attrs={"name":"description"})['content'].split(':', 1)
			CVSS = soup.find('div', attrs={'class' : 'cvssbox'})
			return (CVE[0].strip(), CVE[1].lstrip(), CVSS.contents[0])
		except Exception as e:
			return (cve_id.strip(), e)