from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os
from requests_html import HTMLSession
import json, time, sys

config = Config.getConfig(parentKey='modules', key='ht_cwe')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

URL = 'https://cwe.mitre.org/data/definitions/{cwe_id}.html'

BAD_CODE = True
ATTACK_CODE = True
GOOD_CODE = True

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'searchCWE'
		self.__gui_label__ = 'CWE Vulnerability Info Extractor'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_cwe'), debug_module=True)

	def searchCWE(self, cwe_id):
		try:
			data = {}
			vuln_name = ''
			vuln_summary = ''
			vuln_extended = ''
			vuln_status = ''
			
			session = HTMLSession()
			r = session.get(url = URL.format(cwe_id=cwe_id))

			if r.status_code == 200:

				if r.html.find('#Contentpane', first=True) and r.html.find('#Contentpane', first=True).find('.noprint', first=True) and r.html.find('#Contentpane', first=True).find('.noprint', first=True).find('h2', first=True):
					vuln_name = r.html.find('#Contentpane', first=True).find('.noprint', first=True).find('h2', first=True).text.split(': ')[1]

				if r.html.find('#Description', first=True):
					vuln_summary = r.html.find('#Description', first=True).text.replace('Description\n', '')

				if r.html.find('#Extended_Description', first=True):
					vuln_extended = r.html.find('#Extended_Description', first=True).text.replace('Extended Description\n', '')

				if r.html.find('.title', first=True) and r.html.find('.title', first=True).find('.status', first=True) and r.html.find('.title', first=True).find('.status', first=True).find('div', first=True):
					status_titlebar = r.html.find('.title', first=True).find('.status', first=True).find('div', first=True).text

				if r.html.find('.title', first=True) and r.html.find('.title', first=True).find('.status', first=True) and r.html.find('.title', first=True).find('.status', first=True).find('div', first=True):
					status_titlebar = r.html.find('.title', first=True).find('.status', first=True).find('div', first=True).text

				if 'Status' in status_titlebar:
					vuln_status = status_titlebar.split('Status: ')[1].split('\n')[0]

				if not 'View ID:' in status_titlebar:
					data["name"] = vuln_name
					data["lang"] = "en"
					if vuln_summary or vuln_extended:
						data["description"] = {}
					if vuln_summary:
						data["description"]["summary"] = vuln_summary
					if vuln_extended:
						try:
							vuln_extended = vuln_extended.replace('“', '"').replace('”', '"')
							data["description"]["extended"] = vuln_extended.encode('utf-8').decode('cp1252')
						except:
							print(vuln_extended)

					if vuln_status:
						data['status'] = vuln_status

					data["idCwe"] = int(cwe_id)

					if 'Category ID:' in status_titlebar:
						data["type"] = "Category"

					elif 'Weakness ID:' in status_titlebar:

						if 'Abstraction: ' in status_titlebar:
							status_titlebar = status_titlebar.split('Abstraction: ')[1].split('\n')[0]
								
							if status_titlebar in ('Base'):
								status_titlebar = 'Weakness'

							if status_titlebar in ('Compound'):
								status_titlebar = 'CompoundElement'

						else:
							status_titlebar = 'Weakness'

						data["type"] = status_titlebar

					elif 'Type:' in status_titlebar:
						data["type"] = status_titlebar.replace('Type: ', '').split('\n')[0]

					else:
						data["type"] = "Weakness"
						
			return data

		except Exception as e:
			return {}

	def searchWeakness(self, cwe_id):
		data = self.searchCWE(cwe_id)

		common_consequences = ''
		applicable_platforms = ''
		codeExamples = ''

		last_language = ''

		if data and 'description' in data and 'extended' in data['description']:
			
			if data['description']['extended']:
				data['otherNotes'] = []
				data['otherNotes'].append(str(data['description']['extended'].replace('“', '"').replace('”', '"').encode('cp1252').decode('utf-8')))

			del data['description']['extended']

			try:
				session = HTMLSession()
				r = session.get(url = URL.format(cwe_id=cwe_id))

				if r and r.status_code and r.status_code == 200:

					if r.html.find('#Common_Consequences', first=True):
						common_consequences = r.html.find('#oc_{cwe}_Common_Consequences'.format(cwe=cwe_id), first=True).find('table', first=True).find('tr')[1].find('td', first=True).text

					if r.html.find('#Applicable_Platforms'.format(cwe=cwe_id), first=True):
						data_applicable = r.html.find('#oc_{cwe}_Applicable_Platforms'.format(cwe=cwe_id), first=True).find('div')[1].text
						if '\nLanguages\n' in data_applicable:
							applicable_platforms = data_applicable.split('\nLanguages\n')[1].split(' (')[0]
						if '\nTechnologies\n' in data_applicable:
							applicable_platforms = data_applicable.split('\nTechnologies\n')[1].split(' (')[0]
					
					if r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id)) and r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id))[0].find('.indent') and r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id))[0].find('.indent')[0].find('#ExampleCode'):
						divs = r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id))[0].find('.indent')[0].find('#ExampleCode')

						if divs:
							data["codeExamples"] = []

						for div in divs:
							if '(bad code)' in div.text and BAD_CODE:
								d = {}
								d["nature"] = 'Bad_Code'
								if 'Example Language:' in div.text:
									d["languages"] = [div.text.split('Example Language: ')[1].split('\n')[0]]
									last_language = d["languages"]
									d["snippet"] = ' '.join(div.text.split('Example Language: ')[1].split('\n')[1:]).replace('\"', '')
								else:
									d["languages"] = last_language
									d["snippet"] = ' '.join(r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id))[0].find('.indent')[0].find('#ExampleCode')[0].find('.top')[0].text.replace('\"', '').split('\n'))
								data["codeExamples"].append(d)
								
							if '(attack code)' in div.text and ATTACK_CODE:
								d = {}
								d["nature"] = 'Attack_Code'
								if 'Example Language:' in div.text:
									d["languages"] = [div.text.split('Example Language: ')[1].split('\n')[0]]
									last_language = d["languages"]
									d["snippet"] = ' '.join(div.text.split('Example Language: ')[1].split('\n')[1:]).replace('\"', '')
								else:
									d["languages"] = last_language
									d["snippet"] = ' '.join(r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id))[0].find('.indent')[0].find('#ExampleCode')[0].find('.top')[0].text.replace('\"', '').split('\n'))
								data["codeExamples"].append(d)
								
							if '(good code)' in div.text and GOOD_CODE:
								d = {}
								d["nature"] = 'Good_Code'
								if 'Example Language:' in div.text:
									d["languages"] = [div.text.split('Example Language: ')[1].split('\n')[0]]
									last_language = d["languages"]
									d["snippet"] = ' '.join(div.text.split('Example Language: ')[1].split('\n')[1:]).replace('\"', '')
								else:
									d["languages"] = last_language
									d["snippet"] = ' '.join(r.html.find('#oc_{cwe}_Demonstrative_Examples'.format(cwe=cwe_id))[0].find('.indent')[0].find('#ExampleCode')[0].find('.top')[0].text.replace('\"', '').split('\n'))
								data["codeExamples"].append(d)
								
					data['references'] = []
					data['relatedAttackPatterns'] = []

					if common_consequences:
						data["commonConsequences"] = []
						scopes = { "scopes" : common_consequences.split('\n') }
						data["commonConsequences"].append(scopes)

					if applicable_platforms:
						data["applicablePlatforms"] = {}
						data["applicablePlatforms"]["languageClasses"] = {}
						data["applicablePlatforms"]["languageClasses"]["description"] = applicable_platforms.replace('Class: ', '')

					if codeExamples:
						data["codeExamples"] = {}

					if 'type' in data:
						data['weaknessAbstraction'] = data['type']
						del data['type']
							
				return data

			except Exception as e:
				return {}

