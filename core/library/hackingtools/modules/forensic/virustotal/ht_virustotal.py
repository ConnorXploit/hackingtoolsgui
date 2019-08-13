from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os
import time
import json

from hashlib import md5
from virustotal_python import Virustotal

config = Config.getConfig(parentKey='modules', key='ht_virustotal')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self.vtotal = Virustotal("9334cb7d7d9807f2c508a0eb025c9e2fdaa6c9ce907ccf7326a93bee5fbef172")
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_virustotal'))

	def isBadFileHash(self, fileHash):
		try:
			resp = self.vtotal.file_report([fileHash])
			if resp["status_code"] in (200, 204):
				if resp["status_code"] == 204:
					Logger.printMessage(message="isBadFileHash", description="Testing - {hash} - Waiting 2 seconds...".format(hash=fileHash))
					time.sleep(2)
					return self.isBadFileHash(fileHash)
				while resp["json_resp"]["response_code"] == -2:
					Logger.printMessage(message="isBadFileHash", description="Testing - {hash} - Waiting 2 seconds...".format(hash=fileHash))
					time.sleep(2)
					return self.isBadFileHash(fileHash)
				no_detected_list = []
				detected_list = []
				detected_types = []
				for antivirus in resp["json_resp"]["scans"]:
					if resp["json_resp"]["scans"][antivirus]["detected"]:
						detected_list.append((antivirus, resp["json_resp"]["scans"][antivirus]["version"]))
						if not resp["json_resp"]["scans"][antivirus]["result"] in detected_types:
							detected_types.append(resp["json_resp"]["scans"][antivirus]["result"])
					else:
						no_detected_list.append((antivirus, resp["json_resp"]["scans"][antivirus]["version"]))
				if detected_list:
					data = {}
					data["detected_list"] = detected_list
					data["detected_types"] = detected_types
					data["no_detected_list"] = no_detected_list
					return json.dumps({"Detected":data}, indent=4, sort_keys=True)
				return json.dumps({"No detected":no_detected_list}, indent=4, sort_keys=True)
			return resp
		except Exception as e:
			Logger.printMessage(message="isBadFileHash", description=str(e), is_error=True)
			return str(e)

	def isBadFile(self, filename):
		try:
			Logger.printMessage(message="isBadFile", description=filename)
			response = self.vtotal.file_scan(filename)
			if response["status_code"] == 200:
				scan_id = str(response["json_resp"]["scan_id"])
				time.sleep(2)
				resp = self.isBadFileHash(scan_id)
				return resp
		except Exception as e:
			print(e)
			Logger.printMessage(message="isBadFile", description=str(e), is_error=True)
			return str(e)