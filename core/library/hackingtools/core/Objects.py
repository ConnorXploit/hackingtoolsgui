from . import Logger, Utils
import json

class Host():

    def __init__(self, target_id, ip=[], ports=[], hostnames=[], city='', country_name='', org='', isp='', last_update='', asn='', os='', data=''):
        self.target_id = target_id
        self.ip = ip
        self.ports = ports
        self.hostnames = hostnames
        self.city = city
        self.country_name = country_name
        self.org = org
        self.isp = isp
        self.last_update = last_update
        self.asn = asn
        self.os = os
        self.data = data

    def __str__(self):
        parameters = {}
        if self.target_id:
            parameters["target_id"] = self.getTargetId()
        if self.ip:
            parameters["ip"] = self.getIp()
        if self.ports:
            parameters["ports"] = self.getPorts()
        if self.hostnames:
            parameters["hostnames"] = self.getHostNames()
        if self.city:
            parameters["city"] = self.getCity()
        if self.country_name:
            parameters["country_name"] = self.getCountryName()
        if self.org:
            parameters["org"] = self.getOrganitation()
        if self.isp:
            parameters["isp"] = self.getISP()
        if self.last_update:
            parameters["last_update"] = self.getLastUpdate()
        if self.asn:
            parameters["asn"] = self.getASN()
        if self.os:
            parameters["os"] = self.getOS()
        if self.data:
            parameters["data"] = self.getData()
        Logger.printMessage(message='{data}'.format(data=json.dumps(parameters, indent=4, sort_keys=True), debug_core=True))
        return parameters
    
    def setTarget(self, id):
        self.target_id = id

    def addIp(self, ip):
        self.removeIp(ip)
        self.ip.append(ip)

    def removeIp(self, ip):
        self.ip.remove(ip)

    def addPort(self, port):
        self.removePort(port)
        self.ports.append(port)

    def removePort(self, port):
        self.ports.remove(port)

    def addHostName(self, hostname):
        self.removeHostName(hostname)
        self.hostnames.append(hostname)

    def removeHostName(self, hostname):
        self.hostnames.remove(hostname)

    def setCity(self, city):
        self.city = city

    def setCountryname(self, countryname):
        self.country_name = countryname

    def setOrganitation(self, organitation):
        self.org = organitation

    def setISP(self, isp):
        self.isp = isp

    def setLastUpdate(self, lastupdate):
        self.last_update = lastupdate

    def setASN(self, asn):
        self.asn = asn

    def setOS(self, os):
        self.os = os

    def setData(self, data):
        self.data = data

    def getTargetId(self):
        return self.target_id

    def getIp(self):
        return self.ip

    def getPorts(self):
        return self.ports

    def getHostNames(self):
        return self.hostnames

    def getCity(self):
        return self.city

    def getCountryName(self):
        return self.country_name

    def getOrganitation(self):
        return self.org

    def getISP(self):
        return self.isp

    def getLastUpdate(self):
        return self.last_update

    def getASN(self):
        return self.asn

    def getOS(self):
        return self.os

    def getData(self):
        return self.data

    def addScanResult(self, result):
        try:
            Logger.printMessage(message='addScanResult', description=result)
            for r in result:
                try:
                    if "ip_str" == r:
                        self.addIp(result[r])
                    if "ports" == r:
                        for p, val in result[r]:
                            self.addPort({p, val})
                    if "hostnames" == r:
                        self.addHostName(list(result[r]))
                    if "city" == r:
                        self.addCity(result[r])
                    if "country_name" == r:
                        self.addCountryName(result[r])
                    if "org" == r:
                        self.addOrganitation(result[r])
                    if "isp" == r:
                        self.addISP(result[r])
                    if "last_update" == r:
                        self.addLastUpdate(result[r])
                    if "asn" == r:
                        self.addASN(result[r])
                    if "os" == r:
                        self.addOS(result[r])
                    if "data" == r:
                        self.addData(result[r])
                except:
                    pass
        except:
            pass

class Target():

    def __init__(self, name, id, mail=[], passwords=[], hosts=[], pictures=[], social_networks=[]):
        self.name = name
        self.id = id
        self.mail = mail
        self.passwords = passwords
        self.hosts = hosts
        self.pictures = pictures
        self.social_networks = social_networks

    def renameTarget(self, name):
        try:
            self.name = name
            return True
        except:
            return False

    def addHost(self, host):
        try:
            if not host in self.hosts:
                self.hosts.append(host)
                return True
            return False
        except:
            return False

    def removeHost(self, host):
        try:
            if host in self.hosts:
                self.hosts.remove(host)
                return True
            return False
        except:
            return False

    def getHostsWithKey(self, key):
        try:
            response = []
            for host in self.hosts:
                if key in host.name:
                    response.append(host)
            return response
        except:
            return []

    def getHostByName(self, name):
        try:
            response = []
            for host in self.hosts:
                if name in host.name:
                    response.append(host)
            return response
        except:
            return []

    def getHostByCpe(self, cpe):
        try:
            response = []
            for host in self.hosts:
                if name in host.name:
                    response.append(host)
            return response
        except:
            return []

    def getHostsByIp(self, ip):
        try:
            response = []
            for host in self.hosts:
                if ip in host.ip:
                    response.append(host)
            return response
        except:
            return None

    def existsHostWithIp(self, ip):
        try:
            response = []
            for host in self.hosts:
                if ip in host.ip:
                    return True
            return False
        except:
            return None
    
class Scan():
    
    def __init__(self, name, modules=[], hosts=[]):
        self.name = name
        self.modules = set(modules)
        self.hosts = hosts

    def rename(self, newName):
        self.name = newName

    def addModule(self, module):
        self.removeModule(module) # If exists
        self.modules.append(module)

    def removeModule(self, module):
        self.modules.remove(module)

    def addHost(self, host):
        self.removeHost(host)
        self.hosts.append(host)

    def removeHost(self, host_id):
        self.hosts.remove(host)

    def getName(self):
        return self.name

    def getModules(self):
        return self.modules

    def getHosts(self):
        return self.hosts

class Historical():
    
    def __init__(self):
        self.data = {}

    def addData(self, data):
        self.data[Utils.getTime()] = data

    def getData(self):
        return self.data