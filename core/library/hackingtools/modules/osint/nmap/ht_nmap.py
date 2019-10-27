from hackingtools.core import Logger, Config, Utils
import hackingtools as ht

import nmap
import os

config = Config.getConfig(parentKey='modules', key='ht_nmap')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
	
	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_nmap'), debug_module=True)

	def getConnectedDevices(self, ip):
		Logger.printMessage(message='{methodName}'.format(methodName='getConnectedDevices'), description='{param}'.format(param=ip), debug_module=True)
		nm = nmap.PortScanner()
		results = nm.scan(ip, '-sP')
		hosts = []
		for host in results.all_hosts():
			if results[host].state() == 'up':
				hosts.append(host)
		return hosts

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
