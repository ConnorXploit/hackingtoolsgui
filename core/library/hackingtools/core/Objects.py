from . import Logger
import json

class Host():

    def __init__(self, target_id, ip='', ports=[], hostnames='', city='', country_name='', org='', isp='', last_update='', asn='', os='', data=''):
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
            parameters["target_id"] = self.target_id
        if self.ip:
            parameters["ip"] = self.ip
        if self.ports:
            parameters["ports"] = self.ports
        if self.hostnames:
            parameters["hostnames"] = self.hostnames
        if self.city:
            parameters["city"] = self.city
        if self.country_name:
            parameters["country_name"] = self.country_name
        if self.org:
            parameters["org"] = self.org
        if self.isp:
            parameters["isp"] = self.isp
        if self.last_update:
            parameters["last_update"] = self.last_update
        if self.asn:
            parameters["asn"] = self.asn
        if self.os:
            parameters["os"] = self.os
        if self.data:
            parameters["data"] = self.data
        Logger.printMessage(message='{data}'.format(data=json.dumps(parameters, indent=4, sort_keys=True), debug_core=True))
        return parameters
    
        
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

    def getHostByName(self, name):
        try:
            response = []
            for host in self.hosts:
                if name in host.name:
                    response.append(name)
            return response
        except:
            return []

    def getHostByIp(self, ip):
        try:
            response = []
            for host in self.hosts:
                if ip in host.ip:
                    response.append(ip)
            return response
        except:
            return []

    def removeHost(self, host):
        try:
            if host in self.hosts:
                self.hosts.remove(host)
                return True
            return False
        except:
            return False
