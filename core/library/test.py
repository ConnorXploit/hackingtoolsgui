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

# Create a Target with an ID for later adding some hosts
target = Target(option, 1)

# Set the API for shodan
shodan.settingApi('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# Ask shodan for getting a list of IPs from a service name
for ip in shodan.getIPListfromServices(option):
    # For any IP we get, create a Host object, with the Target ID
    # Add it to target with addHost function
    target.addHost(Host(1, ip))

# For all the host we have:
for host in target.hosts:
    # Add to host's data the response of the call to the shodan function.
    # In this case, we get some public info of that IP
    host.data = shodan.shodan_search_host(host.ip)

# __str__() function is written in the Objects.py file
# ! It print in logger but only with "Logger.setDebugCore(True)" set
[host.__str__() for host in target.hosts]

