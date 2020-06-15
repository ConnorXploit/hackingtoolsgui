from . import Logger, Utils
import json
import time
from datetime import datetime
import requests
import os as __os
import textwrap as __textwrap
import urllib.parse
import threading as __threading
from abc import ABC as __ABC
from abc import abstractmethod
from functools import wraps
import errno
from collections import OrderedDict
import binascii
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hackingtools as ht

class Host():

    def __init__(self, target_id, ip=[], ports=[], vulnerabilities=[], hostnames=[], city='', country_name='', org='', isp='', last_update='', asn='', os='', data=''):
        self.target_id = target_id
        self.ip = ip
        self.ports = ports
        self.vulnerabilities = vulnerabilities
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
        if self.vulnerabilities:
            parameters["vulnerabilities"] = self.getVulnerabilities()
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

    def addVulnerability(self, vuln):
        if not vuln in self.vulnerabilities:
            self.vulnerabilities.append(vuln)

    def removeVulnerability(self, vuln):
        if vuln in self.vulnerabilities:
            self.vulnerabilities.remove(vuln)

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

    def getVulnerabilities(self):
        return ', '.join([vuln.getCVE() for vuln in self.vulnerabilities])

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
            Logger.printMessage(message='addScanResult', description=result, debug_core=True)
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
            for host in self.hosts:
                if ip in host.ip:
                    return True
            return False
        except:
            return None
    
class Scan():
    
    def __init__(self, name, modules=[], hosts=[]):
        self.name = name
        self.modules = list(modules)
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
        self.hosts.remove(host_id)

    def getName(self):
        return self.name

    def getModules(self):
        return self.modules

    def getHosts(self):
        return self.hosts

class Vulnerability():
    
    def __init__(self, name, cve='CVE-0000-0000', cpe='', cwe='', cvss_base=0):
        self.name = name
        self.cve = cve
        self.cwe = cwe
        self.cvss_base = cvss_base

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getCVE(self):
        return self.cve

    def setCVE(self, cve):
        self.cve = cve

    def getCWE(self):
        return self.cwe

    def setCWE(self, cwe):
        self.cwe = cwe

    def getCPE(self):
        return self.cpe

    def setCPE(self, cpe):
        self.cpe = cpe

    def getCVSS(self):
        return self.cvss_base

    def setCVSS(self, cvss):
        self.cvss_base = cvss

class Historical():
    
    def __init__(self):
        self.data = {}

    def addData(self, data):
        self.data[Utils.getTime()] = data

    def getData(self):
        return self.data
        
class Worker():
    
    def __init__(self): 
        self._running = True
        self.responses = []
        self.time = None
        self.timeout = None

    def is_alive(self):
        return self._running

    def terminate(self): 
        self._running = False
        raise KeyboardInterrupt
    
    def getLastResponse(self):
        return self.responses[-1]

    def run(self, functionCall, args, timesleep, loop, timeout):
        if timeout and isinstance(timeout, int) and not self.time:
            self.time = datetime.now()
            self.timeout = int(timeout)

        if loop:

            while self._running:
                try:
                    if timeout and (datetime.now() - self.time).total_seconds() > self.timeout:
                        self.terminate()

                    else:
                        func = '{f}{a}'.format(f=functionCall, a=tuple(args, ))
                        res = eval(func)
                        self.responses.append( res )
                        time.sleep(timesleep)
                except KeyboardInterrupt:
                    pass

        else:
            try:
                if timeout and (datetime.now() - self.time).total_seconds() > self.timeout:
                    self.terminate()

                else:
                    func = '{f}{a}'.format(f=functionCall, a=tuple(args, ))
                    res = eval(func)
                    self.responses.append( res )
                    self.terminate()
            except KeyboardInterrupt:
                pass

# Instagram Module Main Utils

class RequestHandler:
	"""
	Handle all requests with specific user-agent
	"""
	def __init__(self, user_agent, ret="text"):
		self.user_agent = user_agent
		self.current_proxy = None
		self.ret = ret

	@property
	def proxy(self):
		return self.proxy

	@proxy.setter
	def proxy(self, new_proxy):
		self.current_proxy = new_proxy

	def get(self, url):
		"""
		make request
		:param url:
		:return:
		"""
		proxies = {
			"http": f"http://{self.current_proxy}",
			"https": f"https://{self.current_proxy}"
		}
		headers = {
			"User-Agent": self.header_maker(self.user_agent)
		}
		try:
			s = requests.Session()
			if self.current_proxy:
				res = s.get(url, headers=headers, proxies=proxies)
			else:
				res = s.get(url, headers=headers)
			if res.status_code == 200:
				# check return mode
				if self.ret == "text":
					return res.text
				else:
					return res.json()
			else:
				return None
		except requests.exceptions.ConnectionError:
			raise requests.exceptions.ConnectionError
		except json.decoder.JSONDecodeError:
			return None

	def header_maker(self, mode):
		"""
		make header and return as dict
		:param mode:
		:return:
		"""
		user_agents = {
			"FF": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
			"TIMELINE": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
		}

		return user_agents[mode]

class CookieSessionManager:

    def __init__(self, session_folder, filename):
        self.session_folder = session_folder
        self.filename = filename

    def get_saved_cookies(self):
        try:
            f = open(self.session_folder + self.filename, 'r') 
            return f.read()
        except FileNotFoundError:
            return None

    def set_saved_cookies(self, cookie_string):
        if not __os.path.exists(self.session_folder):
            __os.makedirs(self.session_folder)

        with open(self.session_folder + self.filename,"w+") as f:
            f.write(cookie_string)

    def empty_saved_cookies(self):
        try:
            __os.remove(self.session_folder + self.filename)
        except FileNotFoundError:
            pass

class InitializerModel:

    def __init__(self, props=None):

        self._is_new = True
        self._is_loaded = False
        """init data was empty"""
        self._is_load_empty = True
        self._is_fake = False
        self._modified = None

        """Array of initialization data"""
        self._data = {}

        self.modified = time.time()

        if props is not None and len(props) > 0:
            self._init(props)

    def _init(self, props):
        """

        :param props: props array
        :return: None
        """
        for key in props.keys():
            try:
                self._init_properties_custom(props[key], key, props)
            except AttributeError:
                # if function does not exist fill help data array
                self._data[key] = props[key]

        self._is_new = False
        self._is_loaded = True
        self._is_load_empty = False

class Account(InitializerModel):

    def __init__(self, props=None):
        self.identifier = None
        self.username = None
        self.full_name = None
        self.profile_pic_url = None
        self.profile_pic_url_hd = None
        self.biography = None
        self.external_url = None
        self.follows_count = 0
        self.followed_by_count = 0
        self.media_count = 0
        self.is_private = False
        self.is_verified = False
        self.medias = []
        self.blocked_by_viewer = False
        self.country_block = False
        self.followed_by_viewer = False
        self.follows_viewer = False
        self.has_channel = False
        self.has_blocked_viewer = False
        self.highlight_reel_count = 0
        self.has_requested_viewer = False
        self.is_business_account = False
        self.is_joined_recently = False
        self.business_category_name = None
        self.business_email = None
        self.business_phone_number = None
        self.business_address_json = None
        self.requested_by_viewer = False
        self.connected_fb_page = None

        super(Account, self).__init__(props)

    def get_profile_picture_url(self):
        try:
            if not self.profile_pic_url_hd == '':
                return self.profile_pic_url_hd
        except AttributeError:
            try:
                return self.profile_pic_url
            except AttributeError:
                return ''

    def get_data(self):
        data = {}
        values = ('identifier', 'username', 'full_name', 'biography', 'external_url', 'media_count', 'followed_by_count', 'follows_count', 'is_private', 'is_verified')
        for val in values:
            if hasattr(self, val):
                data[val] = eval('self.{val}'.format(val=val))
        data['picture'] = self.get_profile_picture_url()
        return data

    def __str__(self):
        string = f"""
        Account info:
        Id: {self.identifier}
        Username: {self.username if hasattr(self, 'username') else '-'}
        Full Name: {self.full_name if hasattr(self, 'full_name') else '-'}
        Bio: {self.biography if hasattr(self, 'biography') else '-'}
        Profile Pic Url: {self.get_profile_picture_url()}
        External url: {self.external_url if hasattr(self, 'external_url') else '-'}
        Number of published posts: {self.media_count if hasattr(self, 'media_count') else '-'}
        Number of followers: {self.followed_by_count if hasattr(self, 'followed_by_count') else '-'}
        Number of follows: {self.follows_count if hasattr(self, 'follows_count') else '-'}
        Is private: {self.is_private if hasattr(self, 'is_private') else '-'}
        Is verified: {self.is_verified if hasattr(self, 'is_verified') else '-'}
        """
        return __textwrap.dedent(string)

    """
     * @param Media $media
     * @return Account
    """
    def add_media(self, media):
        try:
            self.medias.append(media)
        except AttributeError:
            raise AttributeError

    def _init_properties_custom(self, value, prop, array):
        
        if prop == 'id':
            self.identifier = value

        standart_properties = [
            'username',
            'full_name',
            'profile_pic_url',
            'profile_pic_url_hd',
            'biography',
            'external_url',
            'is_private',
            'is_verified',
            'blocked_by_viewer',
            'country_block',
            'followed_by_viewer',
            'follows_viewer',
            'has_channel',
            'has_blocked_viewer', 
            'highlight_reel_count',
            'has_requested_viewer',
            'is_business_account',
            'is_joined_recently',
            'business_category_name',
            'business_email',
            'business_phone_number',
            'business_address_json',
            'requested_by_viewer',
            'connected_fb_page'
        ]
        if prop in standart_properties:
            self.__setattr__(prop, value)   
        
        if prop == 'edge_follow':
            self.follows_count = array[prop]['count'] \
                if array[prop]['count'] is not None  else 0

        if prop == 'edge_followed_by':
            self.followed_by_count = array[prop]['count'] \
                if array[prop]['count'] is not None else 0

        if prop == 'edge_owner_to_timeline_media':
            self._init_media(array[prop])

    def _init_media(self, array):
        self.media_count = array['count'] if 'count' in array.keys() else 0 

        try:
            nodes = array['edges']
        except:
            return

        if not self.media_count or isinstance(nodes, list):
            return

        for media_array in nodes:
            media = Media(media_array['node'])
            if isinstance(media, Media):
                self.add_media(media)

class Comment(InitializerModel):
    """
     * @param $value
     * @param $prop
     """

    def __init__(self, props=None):
        self.identifier = None
        self.text = None
        self.created_at = None
        # Account object
        self.owner = None

        super(Comment, self).__init__(props)

    def _init_properties_custom(self, value, prop, array):

        if prop == 'id':
           self.identifier = value

        standart_properties = [
            'created_at',
            'text',
        ]

        if prop in standart_properties:
            self.__setattr__(prop, value)

        if prop == 'owner':
            self.owner = Account(value)

class Media(InitializerModel):
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_SIDECAR = 'sidecar'
    TYPE_CAROUSEL = 'carousel'

    def __init__(self, props=None):
        self.identifier = None
        self.short_code = None
        self.created_time = 0
        self.type = None
        self.link = None
        self.image_low_resolution_url = None
        self.image_thumbnail_url = None
        self.image_standard_resolution_url = None
        self.image_high_resolution_url = None
        self.square_images = []
        self.carousel_media = []
        self.caption = None
        self.is_ad = False
        self.video_low_resolution_url = None
        self.video_standard_resolution_url = None
        self.video_low_bandwidth_url = None
        self.video_views = 0
        self.video_url = None
        # account object
        self.owner = None
        self.likes_count = 0
        self.location_id = None
        self.location_name = None
        self.comments_count = 0
        self.comments = []
        self.has_more_comments = False
        self.comments_next_page = None
        self.location_slug = None

        super(Media, self).__init__(props)

    @staticmethod
    def get_id_from_code(code):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        id = 0

        for i in range(len(code)):
            c = code[i]
            id = id * 64 + alphabet.index(c)

        return id

    @staticmethod
    def get_link_from_id(id):
        code = Media.get_code_from_id(id)
        return InstagramEndPoints().get_media_page_link(code)

    @staticmethod
    def get_code_from_id(id):
        parts = str(id).partition('_')
        id = int(parts[0])
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        code = ''

        while (id > 0):
            remainder = int(id) % 64
            id = (id - remainder) // 64
            code = alphabet[remainder] + code

        return code

    def __str__(self):
        string = f"""
        Media Info:
        'Id: {self.identifier}
        Shortcode: {self.short_code}
        Created at: {self.created_time}
        Caption: {self.caption}
        Number of comments: {self.comments_count if hasattr(self,
                                                            'commentsCount') else 0}
        Number of likes: {self.likes_count}
        Link: {self.link}
        Hig res image: {self.image_high_resolution_url}
        Media type: {self.type}
        """

        return __textwrap.dedent(string)

    def _init_properties_custom(self, value, prop, arr):

        if prop == 'id':
            self.identifier = value

        standart_properties = [
            'type',
            'link',
            'thumbnail_src',
            'caption',
            'video_view_count',
            'caption_is_edited',
            'is_ad'
        ]

        if prop in standart_properties:
            self.__setattr__(prop, value)

        elif prop == 'created_time' or prop == 'taken_at_timestamp' or prop == 'date':
            self.created_time = int(value)

        elif prop == 'code':
            self.short_code = value
            self.link = InstagramEndPoints().get_media_page_link(self.short_code)

        elif prop == 'comments':
            self.comments_count = arr[prop]['count']
        elif prop == 'likes':
            self.likes_count = arr[prop]['count']

        elif prop == 'display_resources':
            medias_url = []
            for media in value:
                medias_url.append(media['src'])

                if media['config_width'] == 640:
                    self.image_thumbnail_url = media['src']
                elif media['config_width'] == 750:
                    self.image_low_resolution_url = media['src']
                elif media['config_width'] == 1080:
                    self.image_standard_resolution_url = media['src']

        elif prop == 'display_src' or prop == 'display_url':
            self.image_high_resolution_url = value
            if self.type is None:
                self.type = Media.TYPE_IMAGE

        elif prop == 'thumbnail_resources':
            square_images_url = []
            for square_image in value:
                square_images_url.append(square_image['src'])
            self.square_images = square_images_url

        elif prop == 'carousel_media':
            self.type = Media.TYPE_CAROUSEL
            self.carousel_media = []
            for carousel_array in arr["carousel_media"]:
                self.set_carousel_media(arr, carousel_array)

        elif prop == 'video_views':
            self.video_views = value
            self.type = Media.TYPE_VIDEO

        elif prop == 'videos':
            self.video_low_resolution_url = arr[prop]['low_resolution']['url']
            self.video_standard_resolution_url = \
            arr[prop]['standard_resolution']['url']
            self.video_low_bandwith_url = arr[prop]['low_bandwidth']['url']

        elif prop == 'video_resources':
            for video in value:
                if video['profile'] == 'MAIN':
                    self.video_standard_resolution_url = video['src']
                elif video['profile'] == 'BASELINE':
                    self.video_low_resolution_url = video['src']
                    self.video_low_bandwith_url = video['src']

        elif prop == 'location' and value is not None:
            self.location_id = arr[prop]['id']
            self.location_name = arr[prop]['name']
            self.location_slug = arr[prop]['slug']

        elif prop == 'user' or prop == 'owner':
            self.owner = Account(arr[prop])

        elif prop == 'is_video':
            if bool(value):
                self.type = Media.TYPE_VIDEO

        elif prop == 'video_url':
            self.video_standard_resolution_url = value

        elif prop == 'shortcode':
            self.short_code = value
            self.link = InstagramEndPoints().get_media_page_link(self.short_code)

        elif prop == 'edge_media_to_comment':
            try:
                self.comments_count = int(arr[prop]['count'])
            except KeyError:
                pass
            try:
                edges = arr[prop]['edges']

                for comment_data in edges:
                    self.comments.append(Comment(comment_data['node']))
            except KeyError:
                pass
            try:
                self.has_more_comments = bool(
                    arr[prop]['page_info']['has_next_page'])
            except KeyError:
                pass
            try:
                self.comments_next_page = str(
                    arr[prop]['page_info']['end_cursor'])
            except KeyError:
                pass

        elif prop == 'edge_media_preview_like':
            self.likes_count = arr[prop]['count']
        elif prop == 'edge_liked_by':
            self.likes_count = arr[prop]['count']

        elif prop == 'edge_media_to_caption':
            try:
                self.caption = arr[prop]['edges'][0]['node']['text']
            except (KeyError, IndexError):
                pass

        elif prop == 'edge_sidecar_to_children':
            pass
            # #TODO implement
            # if (!is_array($arr[$prop]['edges'])) {
            #     break;
            # }
            # foreach ($arr[$prop]['edges'] as $edge) {
            #     if (!isset($edge['node'])) {
            #         continue;
            #     }

            #     $this->sidecarMedias[] = static::create($edge['node']);
            # }
        elif prop == '__typename':
            if value == 'GraphImage':
                self.type = Media.TYPE_IMAGE
            elif value == 'GraphVideo':
                self.type = Media.TYPE_VIDEO
            elif value == 'GraphSidecar':
                self.type = Media.TYPE_SIDECAR

        # if self.ownerId and self.owner != None:
        #     self.ownerId = self.getOwner().getId()

    @staticmethod
    def set_carousel_media(media_array, carousel_array):

        print(carousel_array)
        # TODO implement
        pass
        """
        param mediaArray
        param carouselArray
        param instance
        return mixed
        """
        # carousel_media = CarouselMedia()
        # carousel_media.type(carousel_array['type'])

        # try:
        #     images = carousel_array['images']
        # except KeyError:
        #     pass

        # carousel_images = Media.__get_image_urls(
        #     carousel_array['images']['standard_resolution']['url'])
        # carousel_media.imageLowResolutionUrl = carousel_images['low']
        # carousel_media.imageThumbnailUrl = carousel_images['thumbnail']
        # carousel_media.imageStandardResolutionUrl = carousel_images['standard']
        # carousel_media.imageHighResolutionUrl = carousel_images['high']

        # if carousel_media.type == Media.TYPE_VIDEO:
        #     try:
        #         carousel_media.video_views = carousel_array['video_views']
        #     except KeyError:
        #         pass

        #     if 'videos' in carousel_array.keys():
        #         carousel_media.videoLowResolutionUrl(
        #             carousel_array['videos']['low_resolution']['url'])
        #         carousel_media.videoStandardResolutionUrl(
        #             carousel_array['videos']['standard_resolution']['url'])
        #         carousel_media.videoLowBandwidthUrl(
        #             carousel_array['videos']['low_bandwidth']['url'])

        # media_array.append(carousel_media)
        # # array_push($instance->carouselMedia, $carouselMedia);
        # return media_array

    @staticmethod
    def __getImageUrls(image_url):
        parts = '/'.split(urllib.parse.quote_plus(image_url)['path'])
        imageName = parts[len(parts) - 1]
        urls = {
            'thumbnail': InstagramEndPoints().INSTAGRAM_CDN_URL + 't/s150x150/' + imageName,
            'low': InstagramEndPoints().INSTAGRAM_CDN_URL + 't/s320x320/' + imageName,
            'standard': InstagramEndPoints().INSTAGRAM_CDN_URL + 't/s640x640/' + imageName,
            'high': InstagramEndPoints().INSTAGRAM_CDN_URL + 't/' + imageName,
        }
        return urls

class Location(InitializerModel):

    def __init__(self, props=None):
        self.identifier = None
        self.has_public_page = None
        self.name = None
        self.slug = None
        self.lat = None
        self.lng = None
        self.modified = None
        super(Location, self).__init__(props)

    def __str__(self):
        string = f"""
        Location info:
        Id: {self.identifier}
        Name: {self.name}
        Latitude: {self.lat}
        Longitude: {self.lng}
        Slug: {self.slug}
        Is public page available: {self.has_public_page}
        """

        return __textwrap.dedent(string)

    def _init_properties_custom(self, value, prop, arr):

        if prop == 'id':
            self.identifier = value

        standart_properties = [
            'has_public_page',
            'name',
            'slug',
            'lat',
            'lng',
            'modified',
        ]

        if prop in standart_properties:
            self.__setattr__(prop, value)

class Tag(InitializerModel):

    def __init__(self, props=None):
        self._media_count = 0
        self._name = None
        self._id = None
        super(Tag, self).__init__(props)

    def _init_properties_custom(self, value, prop, arr):

        if prop == 'id':
            self.identifier = value
        
        standart_properties = [
            'media_count',
            'name',
        ]

        if prop in standart_properties:
            self.__setattr__(prop, value)

class UserStories(InitializerModel):

    def __init__(self, stories=[], owner=None):
        if stories is None:
            stories = []
        self.owner = owner
        self.stories = stories
        super().__init__()

class Story(Media):

    skip_prop = [
        'owner'
    ]

    #  We do not need some values - do not parse it for Story,
    #  for example - we do not need owner object inside story
     
    #  param value
    #  param prop
    #  param arr

    def _init_properties_custom(self, value, prop, arr):
        if prop in Story.skip_prop:
            return
        
        super()._init_properties_custom(value, prop, arr)

    def __str__(self):
        string = f"""
        Story Info:
        'Id: {self.identifier}
        Hig res image: {self.image_high_resolution_url}
        Media type: {self.type if hasattr(self, 'type') else ''}
        """
        
        return __textwrap.dedent(string)

class CarouselMedia:

    def __init__(self):
        self.__type = ''
        self.__image_low_resolution_url = ''
        self.__image_thumbnail_url = ''
        self.__image_standard_resolution_url = ''
        self.__image_high_resolution_url = ''
        self.__video_low_resolution_url = ''
        self.__video_standard_resolution_url = ''
        self.__video_low_bandwidth_url = ''
        self.__video_views = ''

class InstagramEndPoints:
    
    USER_MEDIAS = '17880160963012870'
    USER_STORIES = '17890626976041463'
    STORIES = '17873473675158481'

    BASE_URL = 'https://www.instagram.com'
    LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'
    ACCOUNT_PAGE = 'https://www.instagram.com/{s}'
    MEDIA_LINK = 'https://www.instagram.com/p/{s}'
    ACCOUNT_MEDIAS = 'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={s}'
    ACCOUNT_JSON_INFO = 'https://www.instagram.com/{s}/?__a=1'
    MEDIA_JSON_INFO = 'https://www.instagram.com/p/{s}/?__a=1'
    MEDIA_JSON_BY_LOCATION_ID = 'https://www.instagram.com/explore/locations/{s}/?__a=1&max_id={s2}'
    MEDIA_JSON_BY_TAG = 'https://www.instagram.com/explore/tags/{s}/?__a=1&max_id={s2}'
    GENERAL_SEARCH = 'https://www.instagram.com/web/search/topsearch/?query={s}'
    COMMENTS_BEFORE_COMMENT_ID_BY_CODE = 'https://www.instagram.com/graphql/query/?query_hash=97b41c52301f77ce508f55e66d17620e&variables={s}'
    LIKES_BY_SHORTCODE_OLD = 'https://www.instagram.com/graphql/query/?query_id=17864450716183058&variables={"shortcode":"{s}","first":{s2},"after":"{s3}"}'
    LIKES_BY_SHORTCODE = 'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={s}'
    FOLLOWING_URL_OLD = 'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={{accountId}}&first={{count}}&after={{after}}'
    FOLLOWING_URL = 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={s}'
    FOLLOWERS_URL_OLD = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={{accountId}}&first={{count}}&after={{after}}'
    FOLLOWERS_URL = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={s}'
    FOLLOW_URL = 'https://www.instagram.com/web/friendships/{s}/follow/'
    UNFOLLOW_URL = 'https://www.instagram.com/web/friendships/{s}/unfollow/'
    INSTAGRAM_CDN_URL = 'https://scontent.cdninstagram.com/'
    ACCOUNT_JSON_PRIVATE_INFO_BY_ID = 'https://i.instagram.com/api/v1/users/{s}/info/'
    LIKE_URL = 'https://www.instagram.com/web/likes/{s}/like/'
    UNLIKE_URL = 'https://www.instagram.com/web/likes/{s}/unlike/'
    ADD_COMMENT_URL = 'https://www.instagram.com/web/comments/{s}/add/'
    DELETE_COMMENT_URL = 'https://www.instagram.com/web/comments/{s}/delete/{s2}/'

    ACCOUNT_MEDIAS2 = 'https://www.instagram.com/graphql/query/?query_id=17880160963012870&id={{accountId}}&first=10&after='

    GRAPH_QL_QUERY_URL = 'https://www.instagram.com/graphql/query/?query_id={s}'

    request_media_count = 30

    def get_account_page_link(self, username):
        return self.ACCOUNT_PAGE.format( s=urllib.parse.quote_plus(username) )

    def get_account_json_link(self, username):
        return self.ACCOUNT_JSON_INFO.format( s=urllib.parse.quote_plus(username) )

    def get_account_json_private_info_link_by_account_id(self, account_id):
        return self.ACCOUNT_JSON_PRIVATE_INFO_BY_ID.format( s=urllib.parse.quote_plus(str(account_id)) )

    def get_account_medias_json_link(self, variables):
        return self.ACCOUNT_MEDIAS.format( s=urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))) )

    def get_media_page_link(self, code):
        return self.MEDIA_LINK.format( s=urllib.parse.quote_plus(code) )

    def get_media_json_link(self, code):
        return self.MEDIA_JSON_INFO.format( s=urllib.parse.quote_plus(code) )

    def get_medias_json_by_location_id_link(self, facebook_location_id, max_id=''):
        return self.MEDIA_JSON_BY_LOCATION_ID.format( s=urllib.parse.quote_plus(str(facebook_location_id)), s2=urllib.parse.quote_plus(max_id) )

    def get_medias_json_by_tag_link(self, tag, max_id=''):
        return self.MEDIA_JSON_BY_TAG.format( s=urllib.parse.quote_plus(str(tag)), s2=urllib.parse.quote_plus(str(max_id)) )

    def get_general_search_json_link(self, query):
        return self.GENERAL_SEARCH.format( s=urllib.parse.quote_plus(query) )

    def get_comments_before_comments_id_by_code(self, variables):
        return self.COMMENTS_BEFORE_COMMENT_ID_BY_CODE.format( s=urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))) )

    def get_last_likes_by_code_old(self, code, count, last_like_id):
        return self.LIKES_BY_SHORTCODE_OLD.format( s=urllib.parse.quote_plus(code), s2=urllib.parse.quote_plus(str(count)), s3=urllib.parse.quote_plus(str(last_like_id)) )

    def get_last_likes_by_code(self, variables):
        return self.LIKES_BY_SHORTCODE.format( s=urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))) )

    def get_follow_url(self, account_id):
        return self.FOLLOW_URL.format( s=urllib.parse.quote_plus(account_id) )

    def get_unfollow_url(self, account_id):
        return self.UNFOLLOW_URL.format( s=urllib.parse.quote_plus(account_id) )

    def get_followers_json_link_old(self, account_id, count, after=''):
        url = self.FOLLOWERS_URL_OLD.replace(
            '{{accountId}}', urllib.parse.quote_plus(account_id))
        url = url.replace('{{count}}', urllib.parse.quote_plus(str(count)))

        if after == '':
            url = url.replace('&after={{after}}', '')
        else:
            url = url.replace('{{after}}', urllib.parse.quote_plus(str(after)))

        return url

    def get_followers_json_link(self, variables):
        return self.FOLLOWERS_URL.format( s=urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))) )

    def get_following_json_link_old(self, account_id, count, after=''):
        url = self.FOLLOWING_URL_OLD.replace(
            '{{accountId}}', urllib.parse.quote_plus(account_id))
        url = url.replace('{{count}}', urllib.parse.quote_plus(count))

        if after == '':
            url = url.replace('&after={{after}}', '')
        else:
            url = url.replace('{{after}}', urllib.parse.quote_plus(after))

        return url

    def get_following_json_link(self, variables):
        return self.FOLLOWING_URL.format( s=urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))) )

    def get_user_stories_link(self, ):
        return self.get_graph_ql_url(self.USER_STORIES, {'variables': json.dumps([], separators=(',', ':'))})

    def get_graph_ql_url(self, query_id, parameters):
        url = self.GRAPH_QL_QUERY_URL.format( s=urllib.parse.quote_plus(query_id) )

        if len(parameters) > 0:
            query_string = urllib.parse.urlencode(parameters)
            url += '&' + query_string

        return url

    def get_stories_link(self, variables):
        return self.get_graph_ql_url(self.STORIES, {'variables': json.dumps(variables, separators=(',', ':'))})

    def get_like_url(self, media_id):
        return self.LIKE_URL.format( s=urllib.parse.quote_plus(str(media_id)) )

    def get_unlike_url(self, media_id):
        return self.UNLIKE_URL.format( s=urllib.parse.quote_plus(str(media_id)) )

    def get_add_comment_url(self, media_id):
        return self.ADD_COMMENT_URL.format( s=urllib.parse.quote_plus(str(media_id)) )

    def get_delete_comment_url(self, media_id, comment_id):
        return self.DELETE_COMMENT_URL.format( s=urllib.parse.quote_plus(str(media_id)), s2=urllib.parse.quote_plus(str(comment_id)) )

class TwoStepVerificationAbstractClass(__ABC):

    @abstractmethod
    def get_verification_type(self, possible_values):
        """
        :param possible_values: array of possible values
        :return: string
        """
        pass

    @abstractmethod
    def get_security_code(self):
        """

        :return: string
        """
        pass

class TwoStepConsoleVerification(TwoStepVerificationAbstractClass):

    def get_verification_type(self, choices):
        if (len(choices) > 1):
            possible_values = {}
            print('Select where to send security code')

            for choice in choices:
                print(choice['label'] + ' - ' + str(choice['value']))
                possible_values[str(choice['value'])] = True

            selected_choice = None

            while (not selected_choice in possible_values.keys()):
                if (selected_choice):
                    print('Wrong choice. Try again')

                selected_choice = input('Your choice: ').strip()
        else:
            print('Message with security code sent to: ' + choices[0]['label'])
            selected_choice = choices[0]['value']

        return selected_choice

    def get_security_code(self):
        """

        :return: string
        """
        security_code = ''
        while (len(security_code) != 6 and not security_code.isdigit()):
            if (security_code):
                print('Wrong security code')

            security_code = input('Enter security code: ').strip()

        return security_code

class Ticker(__threading.Thread):
  """A very simple thread that merely blocks for :attr:`interval` and sets a
  :class:`__threading.Event` when the :attr:`interval` has elapsed. It then waits
  for the caller to unset this event before looping again.

  Example use::

    t = Ticker(1.0) # make a ticker
    t.start() # start the ticker in a new thread
    try:
      while t.evt.wait(): # hang out til the time has elapsed
        t.evt.clear() # tell the ticker to loop again
        print time.time(), "FIRING!"
    except:
      t.stop() # tell the thread to stop
      t.join() # wait til the thread actually dies

  """
  # SIGALRM based timing proved to be unreliable on various python installs,
  # so we use a simple thread that blocks on sleep and sets a __threading.Event
  # when the timer expires, it does this forever.
  def __init__(self, interval):
    super(Ticker, self).__init__()
    self.interval = interval
    self.evt = __threading.Event()
    self.evt.clear()
    self.should_run = __threading.Event()
    self.should_run.set()

  def stop(self):
    """Stop the this thread. You probably want to call :meth:`join` immediately
    afterwards
    """
    self.should_run.clear()

  def consume(self):
    was_set = self.evt.is_set()
    if was_set:
      self.evt.clear()
    return was_set

  def run(self):
    """The internal main method of this thread. Block for :attr:`interval`
    seconds before setting :attr:`Ticker.evt`

    .. warning::
      Do not call this directly!  Instead call :meth:`start`.
    """
    while self.should_run.is_set():
      time.sleep(self.interval)
      self.evt.set()

# Telegram Bot

class TelegramBotCoreHT():

    @staticmethod
    def run():
        from . import TelegramBot


# Pool Blockchain
class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,'recipient_address': self.recipient_address,'value': self.value})

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')