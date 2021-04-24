from hackingtools.core import Logger, Utils, Config
from hackingtools.core.Objects import RequestHandler
from hackingtools.core.Exceptions import IndexError, ConnectionTimeout, InvalidValue, QueryError, ParameterRequired
import hackingtools as ht
import os, requests, json, time, re
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

config = Config.getConfig(parentKey='modules', key='ht_twitter')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

BASE_URL = "https://twitter.com/"
MOBILE_URL = "https://mobile.twitter.com/"
TIMELINE_WITH_TOKEN_QUERY = "i/search/timeline?vertical=default&src=unkn&include_available_features=1&include_entities=1&max_position=%TOKEN%&reset_error_state=false&f=tweets&q="

class StartModule():

	class __FFClass__:
		def __init__(self, username, avatar, fullname):
			"""Data model for followers/followings
			
			Arguments:
				username {str} -- [description]
				user_id {int} -- [description]
				avatar {str} -- [description]
				fullname {str} -- [description]
			"""
			self.username = username
			self.avatar = avatar
			self.fullname = fullname

		def __str__(self):
			return str(self.__dict__)

	class __TimelineClass__:
		def __init__(self, tweet_id, tweet_link, conversation_id, is_reply, has_parent, screen_name, name, user_id, user_mentions, content, reply_count, retweet_count, likes_count, created_at):
			"""
			:param tweet_id:
			:param tweet_link:
			:param conversation_id:
			:param is_reply:
			:param has_parent:
			:param screen_name:
			:param name:
			:param user_id:
			:param user_mentions:
			:param content:
			:param reply_count:
			:param retweet_count:
			:param likes_count:
			"""
			self.tweet_id = tweet_id
			self.tweet_link = tweet_link
			self.conversation_id = conversation_id
			self.is_reply = is_reply
			self.has_parent = has_parent
			self.screen_name = screen_name
			self.name = name
			self.user_id = user_id
			self.user_mentions = user_mentions
			self.content = content
			self.reply_count = reply_count
			self.retweet_count = retweet_count
			self.likes_count = likes_count
			self.created_at = created_at

		def __str__(self):
			return str(self.__dict__)

	class __ProfileClass__:
		def __init__(self, name, verified, protected, username, bio, location, url, joined_date, birthday, user_id, tweet_count, following_count, follower_count, like_count):
			"""
			User profile data model
			"""
			self.name = name
			self.verified = verified
			self.protected = protected
			self.username = username
			self.bio = bio
			self.location = location
			self.url = url
			self.joined_date = joined_date
			self.birthday = birthday
			self.user_id = user_id
			self.tweet_count = tweet_count
			self.following_count = following_count
			self.follower_count = follower_count
			self.like_count = like_count

		def __str__(self):
			return str(self.__dict__)

	def __init__(self):
		self._main_gui_func_ = 'get_user'
		self.__gui_label__ = 'Twitter Info Extractor'
		self.proxy = ''

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_twitter'))

	def searchTweets(self, username="", since="", until="", query="", limit=1000, verified=False, proxy="", interval=0):
		"""Advanced search engine"""

		cursor = "-1"
		has_more: bool = True
		result: list = []
		req = RequestHandler(user_agent="TIMELINE", ret="json")
		if proxy:
			req.proxy = proxy

		if since:
			since = int(time.mktime(datetime.strptime(since, "%Y-%m-%d").timetuple()))

		if until:
			if len(until) == 4:
				until = f"{until}-01-01"

		query_structure = {
			"from": f"+from:{username}",
			"since": f"+since:{since}",
			"verified": ":verified",
			"until": f"+until:{until}",
			"query": f"+{query}"
		}

		if username and query:
			""" not allowed """
			raise QueryError("`username` and `query` parameter not allowed together.")

		if since and until:
			""" not allowed """
			raise QueryError("`since` and `until` parameter not allowed together.")

		url = BASE_URL+TIMELINE_WITH_TOKEN_QUERY
		url = url.replace("%TOKEN%", cursor)

		# if there was username or query
		if username or query:
			if username:
				url += query_structure['from']
			else:
				url += query_structure['query']

		# if username and query aren't set properly raise error
		else:
			raise ParameterRequired("`username` or `query` required for search.")

		if since or until:
			if since:
				url += query_structure['since']
			elif until:
				url += query_structure['until']

		if verified:
			url += query_structure['verified']

		while has_more:
			res = req.get(url=url)
			if res:
				cursor, has_more = self.__extract_timeline_cursor__(response=res)
				if cursor:
					extracted_tweets = self.__extract_timeline__(res['items_html'])
					result.extend(extracted_tweets)
					url = url.replace("%TOKEN%", cursor)
					# check limitation
					if int(limit) > 0:
						if len(result) > int(limit):
							return result[:int(limit)]
					else:
						sleep(interval)
						continue
				else:
					break
				sleep(interval)
			else:
				return result

		return result

	def get_followers(self, username, limit=1000, interval=0):
		"""
		get user followers
		:param username:
		:param interval:
		:param limit:
		:return:
		"""
		return self.__follower_following__(username=username, limit=limit, proxy=self.proxy, interval=interval)

	def get_friends(self, username, limit=1000, interval=0):
		"""
		get user friends
		:param username:
		:param limit:
		:param interval:
		:return:
		"""
		return self.__follower_following__(username=username, limit=limit, proxy=self.proxy, type_="followings", interval=interval)

	def get_timeline(self, username, limit=1000, interval=0):
		"""
		get user timeline
		:param username:
		:param limit:
		:param interval:
		:return:
		"""
		return self.__timeline__(username=username, limit=limit, proxy=self.proxy, interval=interval)

	def get_user(self, username):
		"""
		get user profile info
		:param username:
		:return:
		"""
		return self.__profile__(username=username, proxy=self.proxy)

	def __follower_following__(self, username, limit=1000, type_="followers", proxy=None, interval=0):
		"""
		Followers/Followings scraper
		:param username:
		:param limit:
		:param type_:
		:param proxy:
		:param interval:
		:return:
		"""
		result = []
		cursor = str()
		first_request: bool = True
		has_more: bool = True
		# mode = FF -> followers/followings user-agent
		req = RequestHandler(user_agent="FF")
		# if proxy enabled set it
		if proxy:
			req.proxy = proxy
		while has_more:
			if first_request:
				url = MOBILE_URL + f"/{username}/{type_}/?lang=en"
				res = req.get(url)
				first_request = False
			else:
				url = MOBILE_URL + f"/{username}/{type_}/?lang=en&cursor={cursor}"
				res = req.get(url)
			if res:
				# extract cursor
				cursor = self.__extract_cursor__(res)
				if cursor:
					has_more = True
				else:
					has_more = False

				# parse followers/followings
				extracted_ff = self.__extract_ff__(res)
				result.extend(extracted_ff)
				# if there was limit
				if int(limit) > 0:
					if len(result) > int(limit):
						return result[:int(limit)]
				else:
					sleep(interval)
					continue

			else:
				return result
			# interval
			sleep(interval)

		return result

	def __timeline__(self, username, limit=1000, proxy=None, interval=0):
		"""
		timeline scraper
		:param username:
		:param limit:
		:param proxy:
		:param interval:
		:return:
		"""
		result: list = []
		cursor = "-1"
		has_more = True
		req = RequestHandler(user_agent="TIMELINE", ret="json")
		if proxy:
			req.proxy = proxy

		while has_more:

			url = BASE_URL+TIMELINE_WITH_TOKEN_QUERY+f"+from:{username}"
			url = url.replace("%TOKEN%", cursor)
			res = req.get(url)
			if res:
				cursor, has_more = self.__extract_timeline_cursor__(response=res)
				extracted_tweets = self.__extract_timeline__(res['items_html'])
				result.extend(extracted_tweets)
				# check limitation
				if int(limit) > 0:
					if len(result) > int(limit):
						return result[:int(limit)]
				else:
					sleep(interval)
					continue
			else:
				return result

			sleep(interval)

		return result

	def __profile__(self, username, proxy):
		"""
		get user profile
		"""
		
		req = RequestHandler(user_agent="TIMELINE")
		if proxy:
			req.proxy = proxy
		url = BASE_URL+username+"/?lang=en"
		res = req.get(url=url)
		if res:
			return self.__extract_profile__(res)
		else:
			return None

	def __extract_cursor__(self, html):
		"""
		extract token for next page
		:param html:
		:return:
		"""
		cursor = re.findall('cursor=(\d+)', html)
		if len(cursor) > 0:
			return cursor[0]
		else:
			return ""

	def __extract_timeline_cursor__(self, response):
		"""
		Extract cursor from json
		:param response:
		:return:
		"""
		return response['min_position'], response['has_more_items']

	def __extract_ff__(self, html):
		"""
		Extract followers/followings data from html
		:param html:
		:return:
		"""
		result = []
		soup = BeautifulSoup(html, 'html.parser')
		user_tables = soup.find_all('table', attrs={"class": "user-item"})
		if user_tables:
			for user in user_tables:
				avatar = user.find("img", attrs={"class": "profile-image"})['src'].replace('_normal','')
				if 'default_profile.png' in avatar:
					avatar = ''
				username = user.find("span", attrs={"class": "username"}).text.strip("@")
				fullname = user.find("strong", attrs={"class": "fullname"}).text
				# append to result list
				result.append(self.__FFClass__(username=username, avatar=avatar, fullname=fullname).__str__())
		return result

	def __extract_timeline__(self, html):
		"""
		Extract tweets from timeline data
		:param html:
		:return:
		"""
		result: list = []
		soup = BeautifulSoup(html, 'html.parser')

		for li in soup.find_all('li', attrs={'class': 'js-stream-item stream-item stream-item'}):
			# find first div
			first_div = li.find('div')
			# user and tweet info
			tweet_id = first_div['data-tweet-id']
			tweet_link = first_div['data-permalink-path']
			conversation_id = first_div['data-conversation-id']
			is_reply = first_div.get('data-is-reply-to', "false")
			has_parent = first_div.get('data-has-parent-tweet', "false")
			screen_name = first_div['data-screen-name']
			name = first_div['data-name']
			user_id = first_div['data-user-id']
			user_mentions = first_div.get('data-mentions', 'false')
			if ' ' in user_mentions:
				user_mentions = [user for user in user_mentions.split(" ")]
			# get content info
			content = li.find('div', attrs={'class': 'js-tweet-text-container'}).text
			# tweet statistics
			reply_count = li.find('span', attrs={'class': 'ProfileTweet-action--reply u-hiddenVisually'}).text
			reply_count = reply_count.split(" ")[0].strip()
			retweet_count = li.find('span', attrs={'class': 'ProfileTweet-action--retweet u-hiddenVisually'}).text
			retweet_count = retweet_count.split(" ")[0].strip()
			likes_count = li.find('span', attrs={'class': 'ProfileTweet-action--favorite u-hiddenVisually'}).text
			likes_count = likes_count.split(" ")[0].strip()
			# time
			created_at = li.find('a', attrs={'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})['title']
			#
			# add data to result
			result.append(self.__TimelineClass__(
				tweet_id=tweet_id,
				tweet_link=tweet_link,
				conversation_id=conversation_id,
				is_reply=is_reply,
				has_parent=has_parent,
				screen_name=screen_name,
				name=name,
				user_id=user_id,
				user_mentions=user_mentions,
				content=content,
				reply_count=reply_count,
				retweet_count=retweet_count,
				likes_count=likes_count,
				created_at=created_at
			).__str__())
		return result

	def __extract_profile__(self, html):
		"""
		extract profile data
		:param html:
		:return:
		"""
		result = []

		soup = BeautifulSoup(html, 'html.parser')
		left_side = soup.find('div', attrs={'class': 'ProfileHeaderCard'})
		# get name
		name = left_side.find('a', attrs={'class': 'ProfileHeaderCard-nameLink u-textInheritColor js-nav'}).text
		# verified account
		verified = left_side.find('span', attrs={'class': 'Icon Icon--verified'})
		if verified:
			verified = "true"
		else:
			verified = "false"
		# protected account
		protected = left_side.find('span', attrs={'class': 'Icon Icon--protected'})
		if protected:
			protected = "true"
		else:
			protected = "false"
		# screen name
		username = left_side.find('b', attrs={'class': 'u-linkComplex-target'}).text
		# bio
		bio = left_side.find('p', attrs={'class': 'ProfileHeaderCard-bio u-dir'}).text
		# location
		location = left_side.find('div', attrs={'class': 'ProfileHeaderCard-location'}).text.strip()
		# url
		url = left_side.find('span', attrs={'class': 'ProfileHeaderCard-urlText u-dir'}).text.strip()
		# joined date
		joined_date = left_side.find('span', attrs={'class': 'ProfileHeaderCard-joinDateText js-tooltip u-dir'})['title']
		# birthday
		birthday = left_side.find('span', attrs={'class': 'ProfileHeaderCard-birthdateText u-dir'}).text.strip()

		# navbar
		navbar = soup.find('div', attrs={'class': 'ProfileCanopy-nav'})
		# get user id
		user_id = navbar.find('div', attrs={'class': 'ProfileNav'})["data-user-id"]
		# find tweets count
		try:
			li_ = navbar.find('li', attrs={'class': 'ProfileNav-item ProfileNav-item--tweets is-active'})
			tweet_count = li_.find('span', attrs={'class': 'ProfileNav-value'}).text.strip()
		except AttributeError:
			tweet_count = 0

		# find followings
		try:
			li_ = navbar.find('li', attrs={'class': 'ProfileNav-item ProfileNav-item--following'})
			following_count = li_.find('span', attrs={'class': 'ProfileNav-value'}).text.strip()
		except AttributeError:
			following_count = 0

		# find followers
		try:
			li_ = navbar.find('li', attrs={'class': 'ProfileNav-item ProfileNav-item--followers'})
			follower_count = li_.find('span', attrs={'class': 'ProfileNav-value'}).text.strip()
		except AttributeError:
			follower_count = 0

		# find likes
		try:
			li_ = navbar.find('li', attrs={'class': 'ProfileNav-item ProfileNav-item--favorites'})
			like_count = li_.find('span', attrs={'class': 'ProfileNav-value'}).text.strip()
		except AttributeError:
			like_count = 0
		#
		result.append(self.__ProfileClass__(
			name=name,
			verified=verified,
			protected=protected,
			username=username,
			bio=bio,
			location=location,
			url=url,
			joined_date=joined_date,
			birthday=birthday,
			user_id=user_id,
			tweet_count=tweet_count,
			following_count=following_count,
			follower_count=follower_count,
			like_count=like_count
		).__str__())
		return result

	def __to_json__(self, objects_list):
		"""
		Get objects and convert it to json
		:param objects_list:
		:return:
		"""
		try:
			if objects_list[0].__class__.__name__ == "FF":
				return [obj.__dict__ for obj in objects_list]

			elif objects_list[0].__class__.__name__ == "Timeline":
				return [obj.__dict__ for obj in objects_list]
			elif objects_list[0].__class__.__name__ == "Profile":
				return [obj.__dict__ for obj in objects_list]
		except IndexError:
			return []

	def __to_list__(self, objects_list):
		"""
		Get objects and convert it to list
		:param objects_list:
		:return:
		"""
		try:
			if objects_list[0].__class__.__name__ == "FF":
				return [[obj.username, obj.avatar, obj.fullname] for obj in objects_list]

			elif objects_list[0].__class__.__name__ == "Timeline":
				return [[
					obj.tweet_id,
					obj.tweet_link,
					obj.conversation_id,
					obj.is_reply,
					obj.has_parent,
					obj.screen_name,
					obj.user_id,
					obj.user_mentions,
					obj.content,
					obj.reply_count,
					obj.retweet_count,
					obj.likes_count,
					obj.created_at] for obj in objects_list]
			elif objects_list[0].__class__.__name__ == "Profile":
				return [[
					obj.name,
					obj.verified,
					obj.protected,
					obj.username,
					obj.bio,
					obj.location,
					obj.url,
					obj.joined_date,
					obj.birthday,
					obj.user_id,
					obj.tweet_count,
					obj.following_count,
					obj.follower_count,
					obj.likes_count
				] for obj in objects_list]
		except IndexError:
			return []

	def __to_pandas__(self, objects_list):
		"""
		Get objects and convert it pandas DataFrame
		:param objects_list:
		:return:
		"""
		try:
			if objects_list[0].__class__.__name__ == "FF":
				return pd.DataFrame(self.__to_json__(objects_list))
			elif objects_list[0].__class__.__name__ == "Timeline":
				return pd.DataFrame(self.__to_json__(objects_list))
			elif objects_list[0].__class__.__name__ == "Profile":
				return pd.DataFrame(self.__to_json__(objects_list))
		except IndexError:
			return pd.DataFrame()

	