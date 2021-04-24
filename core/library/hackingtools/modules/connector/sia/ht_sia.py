from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os
from pysia import Sia

config = Config.getConfig(parentKey='modules', key='ht_sia')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
	
	def __init__(self):
		self._main_gui_func_ = ''
		self.__gui_label__ = 'SIA Blockchain'
		self.sc = None

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_sia'), debug_module=True)

	def getDaemonConstants(self):
		self.__startSIA__()
		return self.sc.get_daemon_constants()

	def getDaemonVersion(self):
		self.__startSIA__()
		return self.sc.get_daemon_version()

	def getConsensus(self):
		self.__startSIA__()
		return self.sc.get_consensus()

	def getRenter(self):
		self.__startSIA__()
		return self.sc.get_renter()

	def getRenterContracts(self):
		self.__startSIA__()
		return self.sc.get_renter_contracts()

	def getRenterDownloads(self):
		self.__startSIA__()
		return self.sc.get_renter_downloads()

	def getRenterFiles(self):
		self.__startSIA__()
		return self.sc.get_renter_files()

	def getRenterPrices(self):
		self.__startSIA__()
		return self.sc.get_renter_prices()

	def getWalletTransactions(self):
		self.__startSIA__()
		return self.sc.get_wallet_transactions()

	def getWalletSeeds(self):
		self.__startSIA__()
		return self.sc.get_wallet_seeds()

	def getWalletBackup(self):
		self.__startSIA__()
		return self.sc.get_wallet_backup()

	def getWallet(self):
		self.__startSIA__()
		return self.sc.get_wallet()

	def getWalletAddress(self):
		self.__startSIA__()
		return self.sc.get_wallet_address()

	def getWalletAddresses(self):
		self.__startSIA__()
		return self.sc.get_wallet_addresses()

	def __startSIA__(self):
		if not self.sc:
			try:
				self.sc = Sia()
			except:
				return None
		return self.sc

	def __stopSIA__(self):
		if self.sc:
			return self.sc.get_daemon_stop()
		return None
