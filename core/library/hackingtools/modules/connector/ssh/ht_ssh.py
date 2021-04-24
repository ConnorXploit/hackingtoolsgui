from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os, sys
from paramiko import SSHClient as __SSHClient__
from paramiko import AutoAddPolicy as __AutoAddPolicy__
from paramiko import RSAKey as __RSAKey__
from paramiko.auth_handler import AuthenticationException as __AuthenticationException__
from paramiko.auth_handler import SSHException as __SSHException__
from scp import SCPClient as __SCPClient__
from scp import SCPException as __SCPException__

config = Config.getConfig(parentKey='modules', key='ht_ssh')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'connect'
		self.__gui_label__ = 'SSH Connection'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_ssh'), debug_module=True)

	 # Fetch and transfer SSH Keys.

	def connect(self, host, user, ssh_key_filepath, remote_upload_dir):
		self.host = host
		self.user = user
		self.ssh_key_filepath = ssh_key_filepath
		self.remote_path = remote_upload_dir
		self.client = None
		self.scp = None
		self.conn = None
		self.__upload_ssh_key__()

	def upload_files(self, files):
		"""Upload multiple files to a remote directory."""
		if self.client is None:
			self.client = self.__connect__()
		uploads = [self.__upload_single_file__(file) for file in files]
		Logger.printMessage(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}', debug_module=True)

	def download_file(self, file):
		"""Download file from remote host."""
		if self.conn is None:
			self.conn = self.__connect__()
		self.scp.get(file)

	def execute_commands(self, commands):
		"""Execute multiple commands in succession."""
		if self.client is None:
			self.client = self.__connect__()
		for cmd in commands:
			stdin, stdout, stderr = self.client.exec_command(cmd)
			stdout.channel.recv_exit_status()
			response = stdout.readlines()
			for line in response:
				Logger.printMessage(f'INPUT: {cmd} | OUTPUT: {line}')

	def disconnect(self):
		"""Close ssh connection."""
		self.client.close()
		self.scp.close()

	def __get_ssh_key__(self):
		"""Fetch locally stored SSH key."""
		try:
			self.ssh_key = __RSAKey__.from_private_key_file(self.ssh_key_filepath)
		except __SSHException__:
			self.ssh_key = None
		return self.ssh_key

	def __upload_ssh_key__(self):
		try:
			os.system(f'scp -i {self.ssh_key_filepath} {self.user}@{self.host}')
			os.system(f'scp -i {self.ssh_key_filepath}.pub {self.user}@{self.host}')
		except FileNotFoundError as e:
			Logger.printMessage(e, is_error=True)
		except Exception as e:
			Logger.printMessage(e, is_error=True)

	def __connect__(self):
		"""Open connection to remote host."""
		try:
			self.client = __SSHClient__()
			self.client.load_system_host_keys()
			self.client.set_missing_host_key_policy(__AutoAddPolicy__())
			self.client.connect(self.host, username=self.user, key_filename=self.ssh_key_filepath, look_for_keys=True, timeout=5000)
			self.scp = __SCPClient__(self.client.get_transport())
		except __AuthenticationException__ as e:
			Logger.printMessage('Authentication failed: did you remember to create an SSH key?', is_error=True)
			Logger.printMessage(e, is_error=True)
		except Exception as e:
			Logger.printMessage(e, is_error=True)
		finally:
			return self.client

	def __upload_single_file__(self, file):
		"""Upload a single file to a remote directory."""
		try:
			self.scp.put(file, recursive=True, remote_path=self.remote_path)
		except __SCPException__ as e:
			Logger.printMessage(e, is_error=True)
		except Exception as e:
			Logger.printMessage(e, is_error=True)
		finally:
			Logger.printMessage(f'Uploaded {file} to {self.remote_path}', debug_module=True)

