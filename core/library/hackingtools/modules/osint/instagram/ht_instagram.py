from hackingtools.core import Logger, Config
from hackingtools.core.Objects import CookieSessionManager, InstagramEndPoints, Account, Comment, Media, Location, UserStories, Story, Tag, TwoStepConsoleVerification
from hackingtools.core.Exceptions import NotFoundException, AnyException, AuthException
import hackingtools as ht

import os
import time, requests, re, json, hashlib, random
from slugify import slugify

config = Config.getConfig(parentKey='modules', key='ht_instagram')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

HTTP_NOT_FOUND = 404
HTTP_OK = 200
HTTP_FORBIDDEN = 403
HTTP_BAD_REQUEST = 400

MAX_COMMENTS_PER_REQUEST = 300
MAX_LIKES_PER_REQUEST = 50

# 30 mins time limit on operations that require multiple self.__req
PAGING_TIME_LIMIT_SEC = 1800
PAGING_DELAY_MINIMUM_MICROSEC = 1000000  # 1 sec min delay to simulate browser
PAGING_DELAY_MAXIMUM_MICROSEC = 3000000  # 3 sec max delay to simulate browser

instance_cache = None

class StartModule():

    def __init__(self):
        self._main_gui_func_ = 'getAccountByUsername'
        self.__gui_label__ = 'Instagram Info Extractor'
        self.__req = requests.session()
        self.paging_time_limit_sec = PAGING_TIME_LIMIT_SEC
        self.paging_delay_minimum_microsec = PAGING_DELAY_MINIMUM_MICROSEC
        self.paging_delay_maximum_microsec = PAGING_DELAY_MAXIMUM_MICROSEC

        self.session_username = None
        self.session_password = None
        self.user_session = None
        self.rhx_gis = None
        self.sleep_between_requests = 0
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/66.0.3359.139 Safari/537.36'
        
    def help(self):
        return ht.getFunctionsNamesFromModule('ht_instagram')

    def getAccountByUsername(self, username):
        try:
            return self.__get_account__(username).get_data()
        except Exception as e:
            return str(e)

    def __with_credentials__(self, username, password, session_folder=None):
        """
        param string username
        param string password
        param null sessionFolder
        return Instagram
        """
        instance_cache = None

        if not session_folder:
            cwd = os.getcwd()
            session_folder = cwd + os.path.sep + 'sessions' + os.path.sep

        if isinstance(session_folder, str):

            instance_cache = CookieSessionManager(session_folder, '{n}.txt'.format(n=slugify(username)))

        else:
            instance_cache = session_folder

        instance_cache.empty_saved_cookies()


        self.session_username = username
        self.session_password = password

    def __set_proxies__(self, proxy):
        if proxy and isinstance(proxy, dict):
            self.__req.proxies = proxy

    def __disable_verify__(self):
        self.__req.verify = False

    def __disable_proxies__(self):
        self.__req.proxies = {}

    def __get_user_agent__(self):
        return self.user_agent

    def __set_user_agent__(self, user_agent):
        self.user_agent = user_agent

    @staticmethod
    def __set_account_medias_request_count__(count):
        """
        Set how many media objects should be retrieved in a single request
        param int count
        """
        InstagramEndPoints().request_media_count = count

    def __get_account_by_id__(self, id):
        """
        :param id: account id
        :return: Account
        """
        username = self.__get_username_by_id__(id)
        return self.__get_account__(username)

    def __get_username_by_id__(self, id):
        """
        :param id: account id
        :return: username string from response
        """
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(InstagramEndPoints().get_account_json_private_info_link_by_account_id(id), headers=self.__generate_headers__(self.user_session))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException('Failed to fetch account with given id')

        if HTTP_OK != response.status_code:
            raise AnyException.default(response.text, response.status_code)

        json_response = response.json()
        if not json_response:
            raise AnyException('Response does not JSON')

        if json_response['status'] != 'ok':
            message = json_response['message'] if ('message' in json_response.keys()) else 'Unknown Error'
            raise AnyException(message)

        return json_response['user']['username']

    def __generate_headers__(self, session, gis_token=None):
        """
        :param session: user session dict
        :param gis_token: a token used to be verified by instagram in header
        :return: header dict
        """
        headers = {}
        if session is not None:
            cookies = ''

            for key in session.keys():
                cookies += f"{key}={session[key]}; "

            csrf = session['x-csrftoken'] if session['csrftoken'] is None else \
                session['csrftoken']

            headers = {
                'cookie': cookies,
                'referer': InstagramEndPoints().BASE_URL + '/',
                'x-csrftoken': csrf
            }

        if self.user_agent is not None:
            headers['user-agent'] = self.user_agent

            if gis_token is not None:
                headers['x-instagram-gis'] = gis_token

        return headers

    def __generate_gis_token__(self, variables):
        """
        :param variables: a dict used to  generate_gis_token
        :return: a token used to be verified by instagram
        """
        rhx_gis = self.__get_rhx_gis__() if self.__get_rhx_gis__() is not None else 'NULL'
        string_to_hash = ':'.join([rhx_gis, json.dumps(variables, separators=(',', ':')) if isinstance(variables, dict) else variables])
        return hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()

    def __get_rhx_gis__(self):
        """
        :return: a string to generate gis_token
        """
        if self.rhx_gis is None:
            try:
                shared_data = self.__get_shared_data_from_page__()
            except Exception as _:
                raise AnyException('Could not extract gis from page')

            if 'rhx_gis' in shared_data.keys():
                self.rhx_gis = shared_data['rhx_gis']
            else:
                self.rhx_gis = None

        return self.rhx_gis

    def __get_mid__(self):
        """manually fetches the machine id from graphQL"""
        time.sleep(self.sleep_between_requests)
        response = self.__req.get('https://www.instagram.com/web/__mid/')

        if response.status_code != HTTP_OK:
            raise AnyException.default(response.text, response.status_code)

        return response.text

    def __get_shared_data_from_page__(self, url=InstagramEndPoints().BASE_URL):
        """
        :param url: the requested url
        :return: a dict extract from page
        """
        url = url.rstrip('/') + '/'
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(url, headers=self.__generate_headers__(self.user_session))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException(f"Page {url} not found")

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text, response.status_code)

        return self.__extract_shared_data_from_body__(response.text)

    @staticmethod
    def __extract_shared_data_from_body__(body):
        """
        :param body: html string from a page
        :return: a dict extract from page
        """
        array = re.findall(r'_sharedData = .*?;</script>', body)
        if len(array) > 0:
            raw_json = array[0][len("_sharedData ="):-len(";</script>")]

            return json.loads(raw_json)

        return None

    def __search_tags_by_tag_name__(self, tag):
        """
        :param tag: tag string
        :return: list of Tag
        """
        # TODO: Add tests and auth
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(InstagramEndPoints().get_general_search_json_link(tag))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException(
                'Account with given username does not exist.')

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        try:
            status = json_response['status']
            if status != 'ok':
                raise AnyException(
                    'Response code is not equal 200. '
                    'Something went wrong. Please report issue.')
        except KeyError:
            raise AnyException('Response code is not equal 200. Something went wrong. Please report issue.')

        try:
            hashtags_raw = json_response['hashtags']
            if len(hashtags_raw) == 0:
                return []
        except KeyError:
            return []

        hashtags = []
        for json_hashtag in hashtags_raw:
            hashtags.append(Tag(json_hashtag['hashtag']))

        return hashtags

    def __get_medias__(self, username, count=20, maxId=''):
        """
        :param username: instagram username
        :param count: the number of how many media you want to get
        :param maxId: used to paginate
        :return: list of Media
        """
        account = self.__get_account__(username)
        return self.__get_medias_by_user_id__(account.identifier, count, maxId)

    def __get_medias_by_code__(self, media_code):
        """
        :param media_code: media code
        :return: Media
        """
        url = InstagramEndPoints().get_media_page_link(media_code)
        return self.__get_media_by_url__(url)

    def __get_medias_by_user_id__(self, id, count=12, max_id=''):
        """
        :param id: instagram account id
        :param count: the number of how many media you want to get
        :param max_id: used to paginate
        :return: list of Media
        """
        index = 0
        medias = []
        is_more_available = True

        while index < count and is_more_available:

            variables = {
                'id': str(id),
                'first': str(count),
                'after': str(max_id)
            }

            headers = self.__generate_headers__(self.user_session,
                                            self.__generate_gis_token__(
                                                variables))

            time.sleep(self.sleep_between_requests)
            response = self.__req.get(
                InstagramEndPoints().get_account_medias_json_link(variables),
                headers=headers)

            if not HTTP_OK == response.status_code:
                raise AnyException.default(response.text,
                                                 response.status_code)

            arr = json.loads(response.text)

            try:
                nodes = arr['data']['user']['edge_owner_to_timeline_media'][
                    'edges']
            except KeyError:
                return {}

            for mediaArray in nodes:
                if index == count:
                    return medias

                media = Media(mediaArray['node'])
                medias.append(media)
                index += 1

            if not nodes or nodes == '':
                return medias

            max_id = \
                arr['data']['user']['edge_owner_to_timeline_media'][
                    'page_info'][
                    'end_cursor']
            is_more_available = \
                arr['data']['user']['edge_owner_to_timeline_media'][
                    'page_info'][
                    'has_next_page']

        return medias

    def __get_media_by_id__(self, media_id):
        """
        :param media_id: media id
        :return: list of Media
        """
        media_link = Media.get_link_from_id(media_id)
        return self.__get_media_by_url__(media_link)

    def __get_media_by_url__(self, media_url):
        """
        :param media_url: media url
        :return: Media
        """
        url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

        if len(re.findall(url_regex, media_url)) <= 0:
            raise ValueError('Malformed media url')

        url = media_url.rstrip('/') + '/?__a=1'
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(url, headers=self.__generate_headers__(
            self.user_session))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException(
                'Media with given code does not exist or account is private.')

        if HTTP_OK != response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        media_array = response.json()
        try:
            media_in_json = media_array['graphql']['shortcode_media']
        except KeyError:
            raise AnyException('Media with this code does not exist')

        return Media(media_in_json)

    def __get_medias_from_feed__(self, username, count=20):
        """
        :param username: instagram username
        :param count: the number of how many media you want to get
        :return: list of Media
        """
        medias = []
        index = 0
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(InstagramEndPoints().get_account_json_link(username),
                                  headers=self.__generate_headers__(
                                      self.user_session))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException(
                'Account with given username does not exist.')

        if HTTP_OK != response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        user_array = response.json()

        try:
            user = user_array['graphql']['user']
        except KeyError:
            raise NotFoundException(
                'Account with this username does not exist')

        try:
            nodes = user['edge_owner_to_timeline_media']['edges']
            if len(nodes) == 0:
                return []
        except Exception:
            return []

        for media_array in nodes:
            if index == count:
                return medias
            medias.append(Media(media_array['node']))
            index += 1

        return medias

    def __get_medias_by_tag__(self, tag, count=12, max_id='', min_timestamp=None):
        """
        :param tag: tag string
        :param count: the number of how many media you want to get
        :param max_id: used to paginate
        :param min_timestamp: limit the time you want to start from
        :return: list of Media
        """
        index = 0
        medias = []
        media_ids = []
        has_next_page = True
        while index < count and has_next_page:

            time.sleep(self.sleep_between_requests)
            response = self.__req.get(
                InstagramEndPoints().get_medias_json_by_tag_link(tag, max_id),
                headers=self.__generate_headers__(self.user_session))

            if response.status_code != HTTP_OK:
                raise AnyException.default(response.text,
                                                 response.status_code)

            arr = response.json()

            try:
                arr['graphql']['hashtag']['edge_hashtag_to_media']['count']
            except KeyError:
                return []

            nodes = arr['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            for media_array in nodes:
                if index == count:
                    return medias
                media = Media(media_array['node'])
                if media.identifier in media_ids:
                    return medias

                if min_timestamp is not None \
                        and media.created_time < min_timestamp:
                    return medias

                media_ids.append(media.identifier)
                medias.append(media)
                index += 1

            if len(nodes) == 0:
                return medias

            max_id = \
                arr['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                    'end_cursor']
            has_next_page = \
                arr['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                    'has_next_page']

        return medias

    def __get_medias_by_location_id__(self, facebook_location_id, count=24,
                                  max_id=''):
        """
        :param facebook_location_id: facebook location id
        :param count: the number of how many media you want to get
        :param max_id: used to paginate
        :return: list of Media
        """
        index = 0
        medias = []
        has_next_page = True

        while index < count and has_next_page:

            time.sleep(self.sleep_between_requests)
            response = self.__req.get(
                InstagramEndPoints().get_medias_json_by_location_id_link(
                    facebook_location_id, max_id),
                headers=self.__generate_headers__(self.user_session))

            if response.status_code != HTTP_OK:
                raise AnyException.default(response.text,
                                                 response.status_code)

            arr = response.json()

            nodes = arr['graphql']['location']['edge_location_to_media'][
                'edges']
            for media_array in nodes:
                if index == count:
                    return medias

                medias.append(Media(media_array['node']))
                index += 1

            if len(nodes) == 0:
                return medias

            has_next_page = \
                arr['graphql']['location']['edge_location_to_media'][
                    'page_info'][
                    'has_next_page']
            max_id = \
                arr['graphql']['location']['edge_location_to_media'][
                    'page_info'][
                    'end_cursor']

        return medias

    def __get_current_top_medias_by_tag_name__(self, tag_name):
        """
        :param tag_name: tag string
        :return: list of the top Media
        """
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(
            InstagramEndPoints().get_medias_json_by_tag_link(tag_name, ''),
            headers=self.__generate_headers__(self.user_session))

        if response.status_code == HTTP_NOT_FOUND:
            raise NotFoundException(
                'Account with given username does not exist.')

        if response.status_code is not HTTP_OK:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()
        medias = []

        nodes = \
            json_response['graphql']['hashtag']['edge_hashtag_to_top_posts'][
                'edges']

        for media_array in nodes:
            medias.append(Media(media_array['node']))

        return medias

    def __get_current_top_medias_by_location_id__(self, facebook_location_id):
        """
        :param facebook_location_id: facebook location id
        :return: list of the top Media
        """
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(
            InstagramEndPoints().get_medias_json_by_location_id_link(facebook_location_id),
            headers=self.__generate_headers__(self.user_session))
        if response.status_code == HTTP_NOT_FOUND:
            raise NotFoundException(
                "Location with this id doesn't exist")

        if response.status_code != HTTP_OK:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        nodes = \
            json_response['graphql']['location']['edge_location_to_top_posts'][
                'edges']
        medias = []

        for media_array in nodes:
            medias.append(Media(media_array['node']))

        return medias

    def __get_paginate_medias__(self, username, max_id=''):
        """
        :param username: instagram user name
        :param max_id: used to paginate next time
        :return: dict that contains Media list, maxId, hasNextPage
        """
        account = self.__get_account__(username)
        has_next_page = True
        medias = []

        to_return = {
            'medias': medias,
            'maxId': max_id,
            'hasNextPage': has_next_page,
        }

        variables = json.dumps({
            'id': str(account.identifier),
            'first': str(InstagramEndPoints().request_media_count),
            'after': str(max_id)
        }, separators=(',', ':'))

        time.sleep(self.sleep_between_requests)
        response = self.__req.get(
            InstagramEndPoints().get_account_medias_json_link(variables),
            headers=self.__generate_headers__(self.user_session,
                                          self.__generate_gis_token__(variables))
        )

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        arr = response.json()

        try:
            nodes = arr['data']['user']['edge_owner_to_timeline_media']['edges']
        except KeyError:
            return to_return

        for mediaArray in nodes:
            medias.append(Media(mediaArray['node']))

        max_id = \
            arr['data']['user']['edge_owner_to_timeline_media']['page_info'][
                'end_cursor']
        has_next_page = \
            arr['data']['user']['edge_owner_to_timeline_media']['page_info'][
                'has_next_page']

        to_return = {
            'medias': medias,
            'maxId': max_id,
            'hasNextPage': has_next_page,
        }

        return to_return

    def __get_paginate_medias_by_tag__(self, tag, max_id=''):
        """
        :param tag: tag name
        :param max_id: used to paginate next time
        :return: dict that contains Media list, maxId, hasNextPage
        """
        has_next_page = True
        medias = []

        to_return = {
            'medias': medias,
            'maxId': max_id,
            'hasNextPage': has_next_page,
        }

        time.sleep(self.sleep_between_requests)
        response = self.__req.get(
            InstagramEndPoints().get_medias_json_by_tag_link(tag, max_id),
            headers=self.__generate_headers__(self.user_session))

        if response.status_code != HTTP_OK:
            raise AnyException.default(response.text,
                                             response.status_code)

        arr = response.json()

        try:
            nodes = arr['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        except KeyError:
            return to_return

        for media_array in nodes:
            medias.append(Media(media_array['node']))

        max_id = \
            arr['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                'end_cursor']
        has_next_page = \
            arr['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                'has_next_page']
        try:
            media_count = arr['graphql']['hashtag']['edge_hashtag_to_media'][
                'count']
        except KeyError:
            return to_return

        to_return = {
            'medias': medias,
            'count': media_count,
            'maxId': max_id,
            'hasNextPage': has_next_page,
        }

        return to_return

    def __get_location_by_id__(self, facebook_location_id):
        """
        :param facebook_location_id: facebook location id
        :return: Location
        """
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(
            InstagramEndPoints().get_medias_json_by_location_id_link(facebook_location_id),
            headers=self.__generate_headers__(self.user_session))

        if response.status_code == HTTP_NOT_FOUND:
            raise NotFoundException(
                'Location with this id doesn\'t exist')

        if response.status_code != HTTP_OK:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        return Location(json_response['graphql']['location'])

    def __get_media_likes_by_code__(self, code, count=10, max_id=None):
        """
        :param code:
        :param count:
        :param max_id:
        :return:
        """

        remain = count
        likes = []
        index = 0
        has_previous = True

        #TODO: $index < $count (bug index getting to high since max_likes_per_request gets sometimes changed by instagram)

        while (has_previous and index < count):
            if (remain > MAX_LIKES_PER_REQUEST):
                number_of_likes_to_receive = MAX_LIKES_PER_REQUEST
                remain -= MAX_LIKES_PER_REQUEST
                index += MAX_LIKES_PER_REQUEST
            else:
                number_of_likes_to_receive = remain
                index += remain
                remain = 0


            variables = {
                "shortcode": str(code),
                "first": str(number_of_likes_to_receive),
                "after": '' if not max_id else max_id
            }

            time.sleep(self.sleep_between_requests)

            response = self.__req.get(
                InstagramEndPoints().get_last_likes_by_code(variables),
                headers=self.__generate_headers__(self.user_session))

            if not response.status_code == HTTP_OK:
                raise AnyException.default(response.text,response.status_code)

            jsonResponse = response.json()

            nodes = jsonResponse['data']['shortcode_media']['edge_liked_by']['edges']

            for likesArray in nodes:

                like = Account(likesArray['node'])
                likes.append(like)


            has_previous = jsonResponse['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']
            number_of_likes = jsonResponse['data']['shortcode_media']['edge_liked_by']['count']
            if count > number_of_likes:
                count = number_of_likes

            if len(nodes) == 0:
                data = {}
                data['next_page'] = max_id
                data['accounts'] = likes

                return data

            max_id = jsonResponse['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']

        data = {}
        data['next_page'] = max_id
        data['accounts'] = likes

        return data

    def __get_followers__(self, account_id, count=20, page_size=20, end_cursor='',
                      delayed=True):

        """
        :param account_id:
        :param count:
        :param page_size:
        :param end_cursor:
        :param delayed:
        :return:
        """
        # TODO set time limit
        # if ($delayed) {
        #     set_time_limit($this->pagingTimeLimitSec);
        # }

        index = 0
        accounts = []

        next_page = end_cursor

        if count < page_size:
            raise AnyException(
                'Count must be greater than or equal to page size.')

        while True:
            time.sleep(self.sleep_between_requests)

            variables = {
                'id': str(account_id),
                'first': str(count),
                'after': next_page
            }

            headers = self.__generate_headers__(self.user_session)

            response = self.__req.get(
                InstagramEndPoints().get_followers_json_link(variables),
                headers=headers)

            if not response.status_code == HTTP_OK:
                raise AnyException.default(response.text,
                                                 response.status_code)

            jsonResponse = response.json()

            if jsonResponse['data']['user']['edge_followed_by']['count'] == 0:
                return accounts

            edgesArray = jsonResponse['data']['user']['edge_followed_by'][
                'edges']
            if len(edgesArray) == 0:
                AnyException(
                    f'Failed to get followers of account id {account_id}.'
                    f' The account is private.',
                    HTTP_FORBIDDEN)

            pageInfo = jsonResponse['data']['user']['edge_followed_by'][
                'page_info']
            if pageInfo['has_next_page']:
                next_page = pageInfo['end_cursor']

            for edge in edgesArray:

                accounts.append(Account(edge['node']))
                index += 1

                if index >= count:
                    #since break 2 not in python, looking for better solution since duplicate code
                    data = {}
                    data['next_page'] = next_page
                    data['accounts'] = accounts

                    return data

            #must be below here
            if not pageInfo['has_next_page']:
                break

            if delayed != None:
                # Random wait between 1 and 3 sec to mimic browser
                microsec = random.uniform(1.0, 3.0)
                time.sleep(microsec)

        data = {}
        data['next_page'] = next_page
        data['accounts'] = accounts

        return data

    def __get_following__(self, account_id, count=20, page_size=20, end_cursor='',
                      delayed=True):
        """
        :param account_id:
        :param count:
        :param page_size:
        :param end_cursor:
        :param delayed:
        :return:
        """

        #TODO
        #     if ($delayed) {
        #         set_time_limit($this->pagingTimeLimitSec);
        #     }

        index = 0
        accounts = []

        next_page = end_cursor

        if count < page_size:
            raise AnyException('Count must be greater than or equal to page size.')

        while True:

            variables = {
                'id': str(account_id),
                'first': str(count),
                'after': next_page
            }

            headers = self.__generate_headers__(self.user_session)


            response = self.__req.get(
                InstagramEndPoints().get_following_json_link(variables),
                headers=headers)

            if not response.status_code == HTTP_OK:
                raise AnyException.default(response.text,response.status_code)

            jsonResponse = response.json()
            if jsonResponse['data']['user']['edge_follow']['count'] == 0:
                return accounts

            edgesArray = jsonResponse['data']['user']['edge_follow'][
                'edges']

            if len(edgesArray) == 0:
                raise AnyException(
                    f'Failed to get follows of account id {account_id}.'
                    f' The account is private.',
                    HTTP_FORBIDDEN)

            pageInfo = jsonResponse['data']['user']['edge_follow']['page_info']
            if pageInfo['has_next_page']:
                next_page = pageInfo['end_cursor']

            for edge in edgesArray:
                accounts.append(Account(edge['node']))
                index += 1
                if index >= count:
                    #since no break 2, looking for better solution since duplicate code
                    data = {}
                    data['next_page'] = next_page
                    data['accounts'] = accounts

                    return data

            #must be below here
            if not pageInfo['has_next_page']:
                break

            if delayed != None:
                # Random wait between 1 and 3 sec to mimic browser
                microsec = random.uniform(1.0, 3.0)
                time.sleep(microsec)

        data = {}
        data['next_page'] = next_page
        data['accounts'] = accounts

        return data

    def __get_media_comments_by_id__(self, media_id, count=10, max_id=None):
        """
        :param media_id: media id
        :param count: the number of how many comments you want to get
        :param max_id: used to paginate
        :return: Comment List
        """
        code = Media.get_code_from_id(media_id)
        return self.__get_media_comments_by_code__(code, count, max_id)

    def __get_media_comments_by_code__(self, code, count=10, max_id=''):

        """
        :param code: media code
        :param count: the number of how many comments you want to get
        :param max_id: used to paginate
        :return: Comment List
        """

        comments = []
        index = 0
        has_previous = True

        while has_previous and index < count:
            number_of_comments_to_receive = 0
            if count - index > MAX_COMMENTS_PER_REQUEST:
                number_of_comments_to_receive = MAX_COMMENTS_PER_REQUEST
            else:
                number_of_comments_to_receive = count - index

            variables = {
                "shortcode": str(code),
                "first": str(number_of_comments_to_receive),
                "after": '' if not max_id else max_id
            }

            comments_url = InstagramEndPoints().get_comments_before_comments_id_by_code(
                variables)

            time.sleep(self.sleep_between_requests)
            response = self.__req.get(comments_url,
                                      headers=self.__generate_headers__(
                                          self.user_session,
                                          self.__generate_gis_token__(variables)))

            if not response.status_code == HTTP_OK:
                raise AnyException.default(response.text,
                                                 response.status_code)

            jsonResponse = response.json()

            nodes = jsonResponse['data']['shortcode_media']['edge_media_to_parent_comment']['edges']

            for commentArray in nodes:
                comment = Comment(commentArray['node'])
                comments.append(comment)
                index += 1

            has_previous = jsonResponse['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']

            number_of_comments = jsonResponse['data']['shortcode_media']['edge_media_to_parent_comment']['count']
            if count > number_of_comments:
                count = number_of_comments

            max_id = jsonResponse['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']

            if len(nodes) == 0:
                break


        data = {}
        data['next_page'] = max_id
        data['comments'] = comments
        return data

    def __get_account__(self, username):
        """
        :param username: username
        :return: Account
        """
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(InstagramEndPoints().get_account_page_link(username), headers=self.__generate_headers__(self.user_session))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException('Account with given username does not exist.')

        if HTTP_OK != response.status_code:
            raise AnyException.default(response.text, response.status_code)

        user_array = self.__extract_shared_data_from_body__(response.text)

        if user_array['entry_data']['ProfilePage'][0]['graphql']['user'] is None:
            raise NotFoundException('Account with this username does not exist')

        return Account(user_array['entry_data']['ProfilePage'][0]['graphql']['user'])

    def __get_stories__(self, reel_ids=None):
        """
        :param reel_ids: reel ids
        :return: UserStories List
        """
        variables = {'precomposed_overlay': False, 'reel_ids': []}

        if reel_ids is None or len(reel_ids) == 0:
            time.sleep(self.sleep_between_requests)
            response = self.__req.get(InstagramEndPoints().get_user_stories_link(),
                                      headers=self.__generate_headers__(
                                          self.user_session))

            if not HTTP_OK == response.status_code:
                raise AnyException.default(response.text,
                                                 response.status_code)

            json_response = response.json()

            try:
                edges = json_response['data']['user']['feed_reels_tray'][
                    'edge_reels_tray_to_reel']['edges']
            except KeyError:
                return []

            for edge in edges:
                variables['reel_ids'].append(edge['node']['id'])

        else:
            variables['reel_ids'] = reel_ids

        time.sleep(self.sleep_between_requests)
        response = self.__req.get(InstagramEndPoints().get_stories_link(variables),
                                  headers=self.__generate_headers__(
                                      self.user_session))

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        try:
            reels_media = json_response['data']['reels_media']
            if len(reels_media) == 0:
                return []
        except KeyError:
            return []

        stories = []
        for user in reels_media:
            user_stories = UserStories()

            user_stories.owner = Account(user['user'])
            for item in user['items']:
                story = Story(item)
                user_stories.stories.append(story)

            stories.append(user_stories)
        return stories

    def __search_accounts_by_username__(self, username):
        """
        :param username: user name
        :return: Account List
        """
        time.sleep(self.sleep_between_requests)
        response = self.__req.get(
            InstagramEndPoints().get_general_search_json_link(username),
            headers=self.__generate_headers__(self.user_session))

        if HTTP_NOT_FOUND == response.status_code:
            raise NotFoundException(
                'Account with given username does not exist.')

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        try:
            status = json_response['status']
            if not status == 'ok':
                raise AnyException(
                    'Response code is not equal 200.'
                    ' Something went wrong. Please report issue.')
        except KeyError:
            raise AnyException(
                'Response code is not equal 200.'
                ' Something went wrong. Please report issue.')

        try:
            users = json_response['users']
            if len(users) == 0:
                return []
        except KeyError:
            return []

        accounts = []
        for json_account in json_response['users']:
            accounts.append(Account(json_account['user']))

        return accounts

    # TODO not optimal separate http call after getMedia
    def __get_media_tagged_users_by_code__(self, code):
        """
        :param code: media short code
        :return: list contains tagged_users dict
        """
        url = InstagramEndPoints().get_media_json_link(code)

        time.sleep(self.sleep_between_requests)
        response = self.__req.get(url, headers=self.__generate_headers__(
            self.user_session))

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        try:
            tag_data = json_response['graphql']['shortcode_media'][
                'edge_media_to_tagged_user']['edges']
        except KeyError:
            return []

        tagged_users = []

        for tag in tag_data:
            x_pos = tag['node']['x']
            y_pos = tag['node']['y']
            user = tag['node']['user']
            # TODO: add Model and add Data to it instead of Dict
            tagged_user = dict()
            tagged_user['x_pos'] = x_pos
            tagged_user['y_pos'] = y_pos
            tagged_user['user'] = user

            tagged_users.append(tagged_user)

        return tagged_users

    def __is_logged_in__(self, session):
        """
        :param session: session dict
        :return: bool
        """
        if session is None or 'sessionid' not in session.keys():
            return False

        session_id = session['sessionid']
        csrf_token = session['csrftoken']

        headers = {
            'cookie': f"ig_cb=1; csrftoken={csrf_token}; sessionid={session_id};",
            'referer': InstagramEndPoints().BASE_URL + '/',
            'x-csrftoken': csrf_token,
            'X-CSRFToken': csrf_token,
            'user-agent': self.user_agent,
        }

        time.sleep(self.sleep_between_requests)
        response = self.__req.get(InstagramEndPoints().BASE_URL, headers=headers)

        if not response.status_code == HTTP_OK:
            return False

        cookies = response.cookies.get_dict()

        if cookies is None or not 'ds_user_id' in cookies.keys():
            return False

        return True

    def __login__(self, force=False, two_step_verificator=None):
        """support_two_step_verification true works only in cli mode - just run __login__ in cli mode - save cookie to file and use in any mode
        :param force: true will refresh the session
        :param two_step_verificator: true will need to do verification when an account goes wrong
        :return: headers dict
        """
        if self.session_username is None or self.session_password is None:
            raise AuthException("User credentials not provided")

        if two_step_verificator:
            two_step_verificator = TwoStepConsoleVerification()

        session = json.loads(
            instance_cache.get_saved_cookies()) if instance_cache.get_saved_cookies() != None else None

        if force or not self.__is_logged_in__(session):
            time.sleep(self.sleep_between_requests)
            response = self.__req.get(InstagramEndPoints().BASE_URL)
            if not response.status_code == HTTP_OK:
                raise AnyException.default(response.text,
                                                 response.status_code)

            match = re.findall(r'"csrf_token":"(.*?)"', response.text)

            if len(match) > 0:
                csrfToken = match[0]

            cookies = response.cookies.get_dict()

            # cookies['mid'] doesnt work at the moment so fetch it with function
            mid = self.__get_mid__()

            headers = {
                'cookie': f"ig_cb=1; csrftoken={csrfToken}; mid={mid};",
                'referer': InstagramEndPoints().BASE_URL + '/',
                'x-csrftoken': csrfToken,
                'X-CSRFToken': csrfToken,
                'user-agent': self.user_agent,
            }
            payload = {'username': self.session_username,
                       'password': self.session_password}
            response = self.__req.post(InstagramEndPoints().LOGIN_URL, data=payload,
                                       headers=headers)

            if not response.status_code == HTTP_OK:
                if (
                        response.status_code == HTTP_BAD_REQUEST
                        and response.text is not None
                        and response.json()['message'] == 'checkpoint_required'
                        and two_step_verificator is not None):
                    response = self.__verify_two_step__(response, cookies,
                                                      two_step_verificator)
                    print('checkpoint required')

                elif response.status_code is not None and response.text is not None:
                    raise AuthException(
                        f'Response code is {response.status_code}. Body: {response.text} Something went wrong. Please report issue.',
                        response.status_code)
                else:
                    raise AuthException(
                        'Something went wrong. Please report issue.',
                        response.status_code)

            if not response.json()['authenticated']:
                raise AuthException('User credentials are wrong.')

            cookies = response.cookies.get_dict()

            cookies['mid'] = mid
            instance_cache.set_saved_cookies(json.dumps(cookies, separators=(',', ':')))

            self.user_session = cookies

        else:
            self.user_session = session

        return self.__generate_headers__(self.user_session)

    def __verify_two_step__(self, response, cookies, two_step_verificator):
        """
        :param response: Response object returned by Request
        :param cookies: user cookies
        :param two_step_verificator: two_step_verification instance
        :return: Response
        """
        new_cookies = response.cookies.get_dict()
        cookies = {**cookies, **new_cookies}

        cookie_string = ''
        for key in cookies.keys():
            cookie_string += f'{key}={cookies[key]};'

        headers = {
            'cookie': cookie_string,
            'referer': InstagramEndPoints().LOGIN_URL,
            'x-csrftoken': cookies['csrftoken'],
            'user-agent': self.user_agent,
        }

        url = InstagramEndPoints().BASE_URL + response.json()['checkpoint_url']

        time.sleep(self.sleep_between_requests)
        response = self.__req.get(url, headers=headers)
        data = self.__extract_shared_data_from_body__(response.text)

        if data is not None:
            try:
                choices = \
                    data['entry_data']['Challenge'][0]['extraData']['content'][
                        3][
                        'fields'][0]['values']
            except KeyError:
                choices = dict()
                try:
                    fields = data['entry_data']['Challenge'][0]['fields']
                    try:
                        choices.update({'label': f"Email: {fields['email']}",
                                        'value': 1})
                    except KeyError:
                        pass
                    try:
                        choices.update(
                            {'label': f"Phone: {fields['phone_number']}",
                             'value': 0})
                    except KeyError:
                        pass

                except KeyError:
                    pass

            if len(choices) > 0:
                selected_choice = two_step_verificator.get_verification_type(
                    choices)
                response = self.__req.post(url,
                                           data={'choice': selected_choice},
                                           headers=headers)

        if len(re.findall('name="security_code"', response.text)) <= 0:
            raise AuthException(
                'Something went wrong when try '
                'two step verification. Please report issue.',
                response.status_code)

        security_code = two_step_verificator.get_security_code()

        post_data = {
            'csrfmiddlewaretoken': cookies['csrftoken'],
            'verify': 'Verify Account',
            'security_code': security_code,
        }
        response = self.__req.post(url, data=post_data, headers=headers)
        if not response.status_code == HTTP_OK \
                or 'Please check the code we sent you and try again' in response.text:
            raise AuthException(
                'Something went wrong when try two step'
                ' verification and enter security code. Please report issue.',
                response.status_code)

        return response

    def __add_comment__(self, media_id, text, replied_to_comment_id=None):
        """
        :param media_id: media id
        :param text:  the content you want to post
        :param replied_to_comment_id: the id of the comment you want to reply
        :return: Comment
        """
        media_id = media_id.identifier if isinstance(media_id, Media) else media_id

        replied_to_comment_id = replied_to_comment_id._data['id'] if isinstance(replied_to_comment_id, Comment) else replied_to_comment_id

        body = {'comment_text': text,
                'replied_to_comment_id': replied_to_comment_id
                if replied_to_comment_id is not None else ''}

        response = self.__req.post(InstagramEndPoints().get_add_comment_url(media_id),
                                   data=body, headers=self.__generate_headers__(
                self.user_session))

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        if json_response['status'] != 'ok':
            status = json_response['status']
            raise AnyException(
                f'Response status is {status}. '
                f'Body: {response.text} Something went wrong.'
                f' Please report issue.',
                response.status_code)

        return Comment(json_response)

    def __delete_comment__(self, media_id, comment_id):
        """
        :param media_id: media id
        :param comment_id: the id of the comment you want to delete
        """
        media_id = media_id.identifier if isinstance(media_id,
                                                     Media) else media_id

        comment_id = comment_id._data['id'] if isinstance(comment_id,
                                                          Comment) else comment_id

        response = self.__req.post(
            InstagramEndPoints().get_delete_comment_url(media_id, comment_id),
            headers=self.__generate_headers__(self.user_session))

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        if json_response['status'] != 'ok':
            status = json_response['status']
            raise AnyException(
                f'Response status is {status}. '
                f'Body: {response.text} Something went wrong.'
                f' Please report issue.',
                response.status_code)

    def __like__(self, media_id):
        """
        :param media_id: media id
        """
        media_id = media_id.identifier if isinstance(media_id,
                                                     Media) else media_id
        response = self.__req.post(InstagramEndPoints().get_like_url(media_id),
                                   headers=self.__generate_headers__(
                                       self.user_session))

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        if json_response['status'] != 'ok':
            status = json_response['status']
            raise AnyException(
                f'Response status is {status}. '
                f'Body: {response.text} Something went wrong.'
                f' Please report issue.',
                response.status_code)

    def __unlike__(self, media_id):
        """
        :param media_id: media id
        """
        media_id = media_id.identifier if isinstance(media_id,
                                                     Media) else media_id
        response = self.__req.post(InstagramEndPoints().get_unlike_url(media_id),
                                   headers=self.__generate_headers__(
                                       self.user_session))

        if not HTTP_OK == response.status_code:
            raise AnyException.default(response.text,
                                             response.status_code)

        json_response = response.json()

        if json_response['status'] != 'ok':
            status = json_response['status']
            raise AnyException(
                f'Response status is {status}. '
                f'Body: {response.text} Something went wrong.'
                f' Please report issue.',
                response.status_code)

    def __follow__(self, user_id):
        """
        :param user_id: user id
        :return: bool
        """
        if self.__is_logged_in__(self.user_session):
            url = InstagramEndPoints().get_follow_url(user_id)

            try:
                follow = self.__req.post(url,
                                         headers=self.__generate_headers__(
                                             self.user_session))
                if follow.status_code == HTTP_OK:
                    return True
            except:
                raise AnyException("Except on follow!")
        return False

    def __unfollow__(self, user_id):
        """
        :param user_id: user id
        :return: bool
        """
        if self.__is_logged_in__(self.user_session):
            url_unfollow = InstagramEndPoints().get_unfollow_url(user_id)
            try:
                unfollow = self.__req.post(url_unfollow)
                if unfollow.status_code == HTTP_OK:
                    return unfollow
            except:
                raise AnyException("Exept on unfollow!")
        return False