"""
This is an example for starting doing something with the Library and learning some functions 
Also you could see some modules and I use shodan for testing something
"""

# Main hackingtools imports

import hackingtools as ht
from hackingtools.core import Logger
from hackingtools.core.Objects import Target, Host

# Silent the logger for not been so noisy with the next two lines
# Logger.setDebugCore(False)
# Logger.setDebugModule(False)

# Import readline for the arrowkeys helping to reexecute a command in the command line
try:
    import readline # Linux
except:
    import pyreadline as readline # Windows

# Prints the modules loaded on your hackingtools library
print(ht.getModulesNames())

# From hackingtools, I get a module. In this case, shodan module:
shodan = ht.getModule('ht_shodan')

# I get help method from the shodan module
# ! This returns the methods in console!
# ! For this options, you should have: "Logger.setDebugModule(True)" set
shodan.help()

# Ask for an option for using later in a shodan function
option = input('Service to search (e.g: apache): ')
try:
    count = int(input('How many hosts minimum are you searching for? (minimum and default: 100): '))
except:
    count = 100
    print('You entered bad chars... Taking default value (100)')

# Create a Target with an ID for later adding some hosts
target = Target(option, 1)

# Set the API for shodan
shodan.settingApi('lO6PkeAYJIp9w3N33ri0Rm2DM3WeWbhl')

# Ask shodan for getting a list of IPs from a service name
discarded = 0
while len(target.hosts) < count and discarded < count:
    for ip in shodan.getIPListfromServices(option):
        # For any IP we get, create a Host object, with the Target ID
        # Add it to target with addHost function
        if not target.getHostByIp(ip):
            target.addHost(Host(1, ip))
        else:
            discarded += 1

if discarded >= count:
    print('You arrived yo a bucle of IPs on getIPListfromServices function and they where repeated')

# For all the host we have:
for host in target.hosts:
    # Add to host's data the response of the call to the shodan function.
    # In this case, we get some public info of that IP
    host.data = shodan.shodan_search_host(host.ip)

# Import nmap module
nmap = ht.getModule('ht_nmap')

# For all host we have:
for host in target.hosts:
    # Add info of the response from nmap module function
    host.ports = nmap.getDevicePorts(host.ip)

# __str__() function is written in the Objects.py file
# ! It print in logger but only with "Logger.setDebugCore(True)" set
[host.__str__() for host in target.hosts]