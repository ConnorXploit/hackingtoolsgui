from . import Logger
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
    
    def addScanResult(self, result):
        try:
            print(result)
            for r in result:
                try:
                    if "ip_str" == r:
                        if not result[r] in self.ip:
                            self.ip.append(result[r])
                    if "ports" == r:
                        for p, val in result[r]:
                            if not p in self.ports:
                                self.ports.append({p, val})
                    if "hostnames" == r:
                        self.hostnames += list(result[r])
                    if "city" == r:
                        self.city = result[r]
                    if "country_name" == r:
                        self.country_name = result[r]
                    if "org" == r:
                        self.org = result[r]
                    if "isp" == r:
                        self.isp = result[r]
                    if "last_update" == r:
                        self.last_update = result[r]
                    if "asn" == r:
                        self.asn = result[r]
                    if "os" == r:
                        self.os = result[r]
                    if "data" == r:
                        self.data = result[r]
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
    
    def removeHost(self, host):
        try:
            if host in self.hosts:
                self.hosts.remove(host)
                return True
            return False
        except:
            return False
