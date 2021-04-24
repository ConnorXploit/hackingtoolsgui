from hackingtools.core import Logger, Utils, Config, Connections
import hackingtools as ht
import os

from bs4 import BeautifulSoup
import requests

config = Config.getConfig(parentKey='modules', key='ht_cve')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'searchCVE'
		self.__gui_label__ = 'CVE Vulnerability Info Extractor'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_cve'), debug_module=True)

	def searchCVE(self, cve_id):
		try:
			url = 'https://www.cvedetails.com/cve/{id}'.format(id=cve_id.strip())
			response = requests.get(url, headers=Connections.__headers__)
			soup = BeautifulSoup(response.text,"html.parser")

			data = {}
			vulnered_systems = []
			metasploit_modules = []
			table_heading_list = []

			data['CVE'] = soup.find(attrs={"name":"description"})['content'].split(':', 1)[0].lstrip().rstrip().strip()

			data['Description'] = soup.find(attrs={"name":"description"})['content'].split(':', 1)[1].strip()

			data['CVSS'] = soup.find('div', attrs={'class' : 'cvssbox'}).contents[0]

			heading_list = ["Confidentiality Impact", "Integrity Impact", "Availability Impact", "Access Complexity", "Authentication", "Gained Access", "Vulnerability Type(s)", "CWE ID"]
			for h in heading_list:
				for heading in soup.find_all("th"):
					if h == heading.text:
						data[h] = soup.find(text=h).findNext('td').text.replace('\n', ' ').strip()


			table_vulnered_systems = soup.find("table", {"id": "vulnprodstable"})
			if table_vulnered_systems:
				table_rows = table_vulnered_systems.find_all("tr")

				for h in table_rows[0].find_all("td"):
					table_heading_list.append(h.text.replace('\n', ' ').strip())

				del table_rows[0]

				for row in table_rows:
					system_found = ''
					for index_c, column in enumerate(row.find_all("td")):
						if index_c == 2:
							system_found = column.text.lstrip().rstrip().strip()
						if index_c == 3:
							system_found = '{m} {mm}'.format(m=system_found, mm=column.text.lstrip().rstrip().strip())
						if index_c == 4:
							system_found = '{m} {mm}'.format(m=system_found, mm=column.text.lstrip().rstrip().strip())
						if index_c == 5:
							system_found = '{m} {mm}'.format(m=system_found, mm=column.text.lstrip().rstrip().strip())
						if index_c == 6:
							system_found = '{m} {mm}'.format(m=system_found, mm=column.text.lstrip().rstrip().strip())
					if system_found:
						vulnered_systems.append(system_found.lstrip().rstrip().strip())

				if vulnered_systems:
					data['Products Affected'] = vulnered_systems

			table_metasploit_modules = soup.find("table", {"class": "metasploit"})
			if table_metasploit_modules:
				table_rows = table_metasploit_modules.find_all("tr")
				table_rows_grouped = ht.Utils.groupListByLength(table_rows, 2)

				for t_group in table_rows_grouped:
					d = {}
					d['link'] = t_group[0].find('a', href=True)['href'].lstrip().rstrip().strip()
					d['name'] = t_group[0].find('a').text.lstrip().rstrip().strip()
					d['description'] = t_group[1].text.lstrip().rstrip().strip()
					metasploit_modules.append(d)

				if metasploit_modules:
					data['Metasploit Modules Related'] = metasploit_modules

			return data
		except Exception as e:
			return str(e)

