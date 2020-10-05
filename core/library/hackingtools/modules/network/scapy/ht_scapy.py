from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os, time

from scapy.all import IP, TCP, UDP, sr, RandShort

config = Config.getConfig(parentKey='modules', key='ht_scapy')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'Scapy for Network Manipulation'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_scapy'), debug_module=True)

	def __trace__(self, domain_or_ip):
		return sr( IP( dst=domain_or_ip, ttl=(1,6),id=RandShort() ) / TCP(flags=0x2), verbose=True )

	def traceroute(self, domain_or_ip):
		data = []
		
		ht.worker('scapy-traceroute', 'ht.getModule("scapy").__trace__', args=((domain_or_ip),), loop=False, timeout=5)

		wor = ht.getWorker('scapy-traceroute')[0]

		while wor.is_alive():
			time.sleep(1)

		ans, _ = wor.getLastResponse()

		for snd, rcv in ans:
			data.append( { 'ttl-sent' : snd.ttl, 'rcv-src' : rcv.src, 'tcp' : isinstance(rcv.payload, TCP) } )


		return data