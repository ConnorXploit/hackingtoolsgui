"""
This is an example for starting doing something with the Library and learning some functions
Also you could see some modules and I use shodan for testing something
"""

# Main hackingtools imports

import hackingtools as ht
from hackingtools.core import Logger, Utils
from hackingtools.core.Objects import Target, Host

import progressbar
import time
import json

# Silent the logger for not been so noisy with the next two lines
# Logger.setDebugCore(False)
# Logger.setDebugModule(False)

# Import readline for the arrowkeys helping to reexecute a command in the command line
try:
    import readline  # Linux
except:
    import pyreadline as readline  # Windows

# Necesary sia daemon loaded in the system ( SIA-UI or siad )
# sia = ht.getModule('sia')
# print(sia.getConsensus())
# print(sia.getWallet())


# par = ht.getModule('parser')

# response = par.readFileToType('C:\\Users\\Connor\\Desktop\\ejemplo.csv', typeToExport='json')

# print( json.dumps(response, indent=4) )


# ht.Utils.downloadProjectAsModuleFromGithub('nuevo', 'nu', 'https://github.com/th3unkn0n/TeleGram-Scraper')

# sca = ht.getModule('scapy')
# print(sca.traceroute('54.38.242.225'))
# print(sca.traceroute('hackingteam.space'))
# print(sca.traceroute('google.com'))

# f = open("hashes-md5.txt","w+")
# try:
#     for i in ht.Utils.getCombinationPosibilitiesLength('lalpha-numeric', 32):
#         f.write(i + '\n')
# except:
#     pass
# f.close()

# qualys = ht.getModule('qualys')
# if qualys.connect('<USERNAME>', '<PASSWORD>'):
#     print('Sesion creada :D')
#     print(qualys.scan('XXX.XXX.XXX.XXX'))
#     if qualys.disconnect():
#         print('Sesion cerrada :D')

# ht.Config.setTelegramBotToken('<TELEGRAM_TOKEN>')
# ht.startTelegramBot()

# r = ht.getModule('radare2')
# res = r.getImports('C:\\Users\\<USER>\\Downloads\\test.exe')
# print(res)
#
# # Prints the modules loaded on your hackingtools library
# # print(ht.getModulesNames())
#
# # From hackingtools, I get a module. In this case, shodan module:
# shodan = ht.getModule('ht_shodan')
#
# # I get help method from the shodan module
# # ! This returns the methods in console!
# # ! For this options, you should have: "Logger.setDebugModule(True)" set
# # shodan.help()
#
# # Ask for an option for using later in a shodan function
# option = input('Service to search (e.g: apache): ')
#
# # Create a Target with an ID for later adding some hosts
# target = Target(option, 1)
#
# # Set the API for shodan
# shodan.settingApi('<SHODAN_API>')
#
# # Ask shodan for getting a list of IPs from a service name
# for ip in shodan.getIPListfromServices(option):
#     # For any IP we get, create a Host object, with the Target ID
#     # Add it to target with addHost function
#     if not target.existsHostWithIp(ip):
#         host = Host(1, ip)
#         target.addHost(host)
#     else:
#         print('IP Repeated... Host registered yet on the Target - {i}'.format(i=ip))
#
# # For all the host we have:
# for host in target.hosts:
#     # Add to host's data the response of the call to the shodan function.
#     # In this case, we get some public info of that IP
#     host.addScanResult(shodan.search_host(host.ip))
#
# [host.__str__() for host in target.hosts]
#
# # Import nmap module
# # nmap = ht.getModule('ht_nmap')
#
# # ip = input('Introduce una IP a escanear: ')
#
# # target = Target('search', 1)
# # target.addHost(Host(1, ip))
#
# # # For all host we have:
# # with progressbar.ProgressBar(max_value=len(target.hosts)) as bar:
# #     for host in target.hosts:
# #         # Add info of the response from nmap module function
# #         host.ports = Utils.getValidDictNoEmptyKeys(nmap.getDevicePorts(host.ip))
# #         bar.update(1)
#
# # spider = ht.getModule('ht_spider')
# # links, webforms = spider.crawl(url=input('Search a web domain: '), depth=2)
#
# # print(links)
# # print(json.dumps(webforms, indent=4, sort_keys=True))
#
#
#
# # __str__() function is written in the Objects.py file
# # ! It print in logger but only with "Logger.setDebugCore(True)" set
# #[host.__str__() for host in target.hosts]
#
# # zipp = ht.getModule('unzip')
# # print(zipp.extractFile(input('File path: '), input('Password:' )))
#
# # shodan = ht.getModule('ht_shodan')
# # nmap = ht.getModule('nmap')
#
# # shodan.help()
#
# # option = input('Dame un servicio: ')
#
# # for ip in shodan.getIPListfromServices(option):
# #     print(shodan.shodan_search_host(ip))
# #     print(nmap.getDevicePorts(ip))
