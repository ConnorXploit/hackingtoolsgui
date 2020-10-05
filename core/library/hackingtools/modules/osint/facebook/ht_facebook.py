from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

import codecs
import itertools
import json
import re
import time
import warnings
from datetime import datetime
from urllib import parse as urlparse

from requests import RequestException
from requests_html import HTML, HTMLSession

config = Config.getConfig(parentKey='modules', key='ht_facebook')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

__base_url__ = 'https://m.facebook.com'
__user_agent__ = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/76.0.3809.87 Safari/537.36")
__headers__ = {'User-Agent': __user_agent__, 'Accept-Language': 'en-US,en;q=0.5'}

__session__ = None
__timeout__ = None

__likes_regex__ = re.compile(r'like_def[^>]*>([0-9,.]+)')
__comments_regex__ = re.compile(r'cmt_def[^>]*>([0-9,.]+)')
__shares_regex__ = re.compile(r'([0-9,.]+)\s+Shares')
__link_regex__ = re.compile(r"href=\"https:\/\/lm\.facebook\.com\/l\.php\?u=(.+?)\&amp;h=")

__cursor_regex__ = re.compile(r'href:"(/page_content[^"]+)"')  # First request
__cursor_regex_2__ = re.compile(r'href":"(\\/page_content[^"]+)"')  # Other requests

__photo_link__ = re.compile(r"href=\"(/[^\"]+/photos/[^\"]+?)\"")
__image_regex__ = re.compile(r"<a href=\"([^\"]+?)\" target=\"_blank\" class=\"sec\">View Full Size<\/a>")
__image_regex_lq__ = re.compile(r"background-image: url\('(.+)'\)")
__post_url_regex__ = re.compile(r'/story.php\?story_fbid=')

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'get_posts'
		self.__gui_label__ = 'Facebook Info Extractor'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_facebook'), debug_module=True)

	def get_posts(self, account=None, group=None, pages=10, timeout=5, sleep=0, credentials=None):
		valid_args = sum(arg is not None for arg in (account, group))
		if valid_args != 1:
			raise ValueError("You need to specify either account or group")

		if account is not None:
			path = f'{account}/posts/'
		elif group is not None:
			path = f'groups/{group}/'

		return self.__get_posts__(path, pages=pages, timeout=timeout, sleep=sleep, credentials=credentials)

	def __get_posts__(self, path, pages=10, timeout=5, sleep=0, credentials=None):
		"""Gets posts for a given account."""
		global __session__, __timeout__

		url = f'{__base_url__}/{path}'

		__session__ = HTMLSession()
		__session__.headers.update(__headers__)

		if credentials:
			self.__login_user__(*credentials)

		__timeout__ = timeout
		response = __session__.get(url, timeout=__timeout__)
		html = response.html
		cursor_blob = html.html

		articles = []
		while True:
			for article in html.find('article'):
				articles.append(self.__extract_post__(article))

			pages -= 1
			if pages == 0:
				return articles

			cursor =  self.__find_cursor__(cursor_blob)
			next_url = f'{__base_url__}{cursor}'

			if sleep:
				time.sleep(sleep)

			try:
				response = __session__.get(next_url, timeout=timeout)
				response.raise_for_status()
				data = json.loads(response.text.replace('for (;;);', '', 1))
			except (RequestException, ValueError):
				return articles

			for action in data['payload']['actions']:
				if action['cmd'] == 'replace':
					html = HTML(html=action['html'], url=__base_url__)
				elif action['cmd'] == 'script':
					cursor_blob = action['code']

	def __extract_post__(self, article):
		text, post_text, shared_text =  self.__extract_text__(article)
		return {
			'post_id':  self.__extract_post_id__(article),
			'text': text,
			'post_text': post_text,
			'shared_text': shared_text,
			'time':  self.__extract_time__(article),
			'image':  self.__extract_image__(article),
			'likes':  self.__find_and_search__(article, 'footer', __likes_regex__,  self.__parse_int__) or 0,
			'comments':  self.__find_and_search__(article, 'footer', __comments_regex__,  self.__parse_int__) or 0,
			'shares':   self.__find_and_search__(article, 'footer', __shares_regex__,  self.__parse_int__) or 0,
			'post_url':  self.__extract_post_url__(article),
			'link':  self.__extract_link__(article),
		}

	def __extract_post_id__(self, article):
		try:
			data_ft = json.loads(article.attrs['data-ft'])
			return data_ft['mf_story_key']
		except (KeyError, ValueError):
			return None

	def __extract_text__(self, article):
		nodes = article.find('p, header')
		if nodes:
			post_text = []
			shared_text = []
			ended = False
			for node in nodes[1:]:
				if node.tag == "header":
					ended = True
				if not ended:
					post_text.append(node.text)
				else:
					shared_text.append(node.text)

			text = '\n'.join(itertools.chain(post_text, shared_text))
			post_text = '\n'.join(post_text)
			shared_text = '\n'.join(shared_text)

			return text, post_text, shared_text

		return None

	def __extract_time__(self, article):
		try:
			data_ft = json.loads(article.attrs['data-ft'])
			page_insights = data_ft['page_insights']
		except (KeyError, ValueError):
			return None

		for page in page_insights.values():
			try:
				timestamp = page['post_context']['publish_time']
				return datetime.fromtimestamp(timestamp)
			except (KeyError, ValueError):
				continue
		return None

	def __extract_photo_link__(self, article):
		match = __photo_link__.search(article.html)
		if not match:
			return None

		url = f"{__base_url__}{match.groups()[0]}"

		response = __session__.get(url, timeout=__timeout__)
		html = response.html.html
		match = __image_regex__.search(html)
		if match:
			return match.groups()[0].replace("&amp;", "&")
		return None

	def __extract_image__(self, article):
		image_link =  self.__extract_photo_link__(article)
		if image_link is not None:
			return image_link
		return  self.__extract_image_lq__(article)

	def __extract_image_lq__(self, article):
		story_container = article.find('div.story_body_container', first=True)
		other_containers = story_container.xpath('div/div')

		for container in other_containers:
			image_container = container.find('.img', first=True)
			if image_container is None:
				continue

			style = image_container.attrs.get('style', '')
			match = __image_regex_lq__.search(style)
			if match:
				return  self.__decode_css_url__(match.groups()[0])

		return None

	def __extract_link__(self, article):
		html = article.html
		match = __link_regex__.search(html)
		if match:
			return urlparse.unquote(match.groups()[0])
		return None

	def __extract_post_url__(self, article):
		query_params = ('story_fbid', 'id')

		elements = article.find('header a')
		for element in elements:
			href = element.attrs.get('href', '')
			match = __post_url_regex__.match(href)
			if match:
				path =  self.__filter_query_params__(href, whitelist=query_params)
				return f'{__base_url__}{path}'

		return None

	def __find_and_search__(self, article, selector, pattern, cast=str):
		container = article.find(selector, first=True)
		match = container and pattern.search(container.html)
		return match and cast(match.groups()[0])

	def __find_cursor__(self, text):
		match = __cursor_regex__.search(text)
		if match:
			return match.groups()[0]

		match = __cursor_regex_2__.search(text)
		if match:
			value = match.groups()[0]
			return value.encode('utf-8').decode('unicode_escape').replace('\\/', '/')

		return None

	def __parse_int__(self, value):
		return int(''.join(filter(lambda c: c.isdigit(), value)))

	def __decode_css_url__(self, url):
		url = re.sub(r'\\(..) ', r'\\x\g<1>', url)
		url, _ = codecs.unicode_escape_decode(url)
		return url

	def __filter_query_params__(self, url, whitelist=None, blacklist=None):
		def is_valid_param(param):
			if whitelist is not None:
				return param in whitelist
			if blacklist is not None:
				return param not in blacklist
			return True  # Do nothing

		parsed_url = urlparse.urlparse(url)
		query_params = urlparse.parse_qsl(parsed_url.query)
		query_string = urlparse.urlencode(
			[(k, v) for k, v in query_params if is_valid_param(k)]
		)
		return urlparse.urlunparse(parsed_url._replace(query=query_string))

	def __login_user__(self, email, password):
		login_page = __session__.get(__base_url__)
		login_action = login_page.html.find('#login_form', first=True).attrs.get('action')
		__session__.post(__base_url__ + login_action, data={'email': email, 'pass': password})
		if 'c_user' not in __session__.cookies:
			warnings.warn('login unsuccessful')