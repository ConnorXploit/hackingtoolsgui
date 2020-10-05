from hackingtools.core import Logger, Config, Utils
import hackingtools as ht

import nmap
import os

config = Config.getConfig(parentKey='modules', key='ht_nmap')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
	
	def __init__(self):
		self._main_gui_func_ = 'getCVEsFromHost'
		self.__gui_label__ = 'Nmap'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_nmap'), debug_module=True)

	def getConnectedDevices(self, ip):
		Logger.printMessage(message='{methodName}'.format(methodName='getConnectedDevices'), description='{param}'.format(param=ip), debug_module=True)
		nm = nmap.PortScanner()
		results = nm.scan(hosts=ip, arguments='-n -sP -PE -PA21,23,80,3389')
		if 'scan' in results: 
			hosts = {}
			for host in results['scan']:
				if results['scan'][host]['status']['state'] == 'up':
					mac_address = None

					if 'mac' in results['scan'][host]['addresses']:
						mac_address = results['scan'][host]['addresses']['mac']

					hosts[host] = '' if not mac_address else results['scan'][host]['vendor'][ mac_address ]
					
			return hosts
		return []

	def executeScan(self, ip, params=''):
		Logger.printMessage(message='{methodName}'.format(methodName='executeScan'), description='{param}'.format(param=ip), debug_module=True)
		nm = nmap.PortScanner()
		try:
			return dict( nm.scan(hosts=ip, arguments=params) )
		except:
			return {}

	def getCVEsFromHost(self, ip):
		Logger.printMessage(message='{methodName}'.format(methodName='getConnectedDevices'), description='{param}'.format(param=ip), debug_module=True)
		nm = nmap.PortScanner()
		results = nm.scan(hosts=ip, arguments='-Pn --script vuln')
		protocols = ('tcp', 'udp')
		discard_vuln_by_description = ('ERROR:', 'Couldn\'t', '\n  /jmx-console/: Authentication was not required\n')
		res = {}
		for p in protocols:
			if 'scan' in results and ip in results['scan']:
				if p in results['scan'][ip]:
					for port in results['scan'][ip][p]:
						res[port] = []
						if 'script' in results['scan'][ip][p][port]:
							for vuln in results['scan'][ip][p][port]['script']:
								discard = False
								for dis in discard_vuln_by_description:
									if results['scan'][ip][p][port]['script'][vuln].startswith(dis):
										discard = True
								if not discard:
									if not results['scan'][ip][p][port]['script'][vuln] == '\n':
										if 'CVE:' in results['scan'][ip][p][port]['script'][vuln]:
											res[port].append( { vuln : results['scan'][ip][p][port]['script'][vuln].split('CVE:')[1].split('\n')[0].split(' ')[0] } )
										else:
											res[port].append( { vuln : results['scan'][ip][p][port]['script'][vuln] } )
						if len(res[port]) == 0:
							del res[port]
		
		return res

	def getDevicePorts(self, ip, tcp=True, udp=False):
		Logger.printMessage(message='{methodName}'.format(methodName='getDevicePorts'), description='{param} - TCP {tcp} - UDP {udp}'.format(param=ip, tcp=tcp, udp=udp), debug_module=True)
		nm = nmap.PortScanner()
		results = nm.scan(ip)
		try:
			if tcp and not udp:
				return Utils.getValidDictNoEmptyKeys(results["scan"][ip]["tcp"])
			if udp and not tcp:
				return Utils.getValidDictNoEmptyKeys(results["scan"][ip]["udp"])
			if tcp and udp:
				return Utils.getValidDictNoEmptyKeys([results["scan"][ip]["tcp"],results["scan"][ip]["udp"]])
			return Utils.getValidDictNoEmptyKeys(results["scan"][ip]["tcp"])
		except:
			return []

	def hasDevicePortOpened(self, ip, port):
		Logger.printMessage(message='{methodName}'.format(methodName='hasDevicePortOpened'), description='{param}:{param2}'.format(param=ip, param2=port), debug_module=True)
		nm = nmap.PortScanner()
		results = nm.scan(ip)
		exists = False
		try:
			for host in results.all_hosts():
				if exists:
					break
				if not exists:
					exists = results[host].has_tcp(port)
				if not exists:
					exists = results[host].has_udp(port)
		except:
			Logger.printMessage(message="isBadFile", description=results, is_error=True)
			raise
		return exists
