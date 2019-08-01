from hackingtools.core import Logger, Config
import hackingtools as ht

import nmap
import os

config = Config.getConfig(parentKey='modules', key='ht_nmap')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	cacheSearchInfo = []
	
	def __init__(self):
		Logger.printMessage(message='ht_nmap loaded', debug_core=True)
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_nmap'))

	def saveCacheSearchInfo(self, activate=False):
		pass

	def getConnectedDevices(self, ip):
		nm = nmap.PortScanner()
		results = nm.scan(ip, '-sP')
		hosts = []
		for host in results.all_hosts():
			if results[host].state() == 'up':
				hosts.append(host)
		return hosts

	def getDevicePorts(self, ip, tcp=True, udp=False):
		nm = nmap.PortScanner()
		results = nm.scan(ip)
		ports = []
		for host in results.all_hosts():
			if tcp:
				for port in results[host]['tcp'].keys():
					ports.append(port)
			if udp:
				for port in results[host]['udp'].keys():
					ports.append(port)
		return ports

	def hasDevicePortOpened(self, ip, port):
		nm = nmap.PortScanner()
		results = nm.scan(ip)
		exists = False
		for host in results.all_hosts():
			if exists:
				break
			if not exists:
				exists = results[host].has_tcp(port)
			if not exists:
				exists = results[host].has_udp(port)
		return exists
