__author__ = 'rcj1492'
__created__ = '2015.06'

class MeetupError(Exception):

    def __init__(self, message='', error_dict=None):

        ''' a method to raise meetup api related errors

        :param message:
        :param error_dict:
        '''

        text = '\nBad Request %s' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                for key, value in error_dict.items():
                    self.error[key] = value
        super(MeetupError, self).__init__(text)

class meetupHandler(object):

    ''' handles responses from meetup api and usage data'''

    _class_fields = {
        'schema': {
            'rate_limits': [
                {'requests': 3, 'period': 1}
            ]
        }
    }

    def __init__(self, usage_client=None):

        ''' initialization method for meetup handler class

        :param usage_client: callable that records usage data
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct initial methods
        self.rate_limits = self.fields.schema['rate_limits']
        self.usage_client = usage_client

    def handle(self, err):
        return err

class meetupRegister(object):
    ''' currently must be done manually '''
    # https://secure.meetup.com/meetup_api/oauth_consumers/
    def __init__(self, app_settings):
        pass

    def setup(self):
        return self

    def update(self):
        return self

class meetupOAuth(object):

    ''' a class of methods to handle oauth2 authentication with meetup API '''

    # https://www.meetup.com/meetup_api/auth/#oauth2

    _class_fields = {
        'schema': {
            'code_endpoint': 'https://secure.meetup.com/oauth2/authorize',
            'token_endpoint': 'https://secure.meetup.com/oauth2/access',
            'token_details': {
                'access_token': '',
                'token_type': '',
                'expires_in': 0,
                'refresh_token': '',
                'user_id': 0
            },
            'token_status': {
                'client_id': '',
                'scope': '',
                'expires_in': 0,
                'user_id': 0
            },
            'client_id': '',
            'client_secret': '',
            'device_type': '',
            'redirect_uri': '',
            'service_scope': ['ageless'],
            'state_value': '',
            'auth_code': ''
        },
        'components': {
            '.device_type': {
                'discrete_values': ['web', 'mobile']
            },
            '.redirect_uri': {
                'must_contain': ['^https://']
            },
            '.service_scope': {
                'unique_values': True
            },
            '.service_scope[0]': {
                'discrete_values': ['ageless', 'basic', 'event_management', 'group_edit', 'group_content', 'group_join', 'profile_edit', 'reporting', 'rsvp']
            }
        }
    }

    def __init__(self, client_id, client_secret, requests_handler=None):

        ''' initialization method for meetup oauth class

        :param client_id: string with client id registered for app with moves api
        :param client_secret: string with client secret registered for app with moves api
        :param requests_handler: callable that handles requests errors
        '''

        # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

        # construct client attributes
        self.client_id = self.fields.validate(client_id, '.client_id')
        self.client_secret = self.fields.validate(client_secret, '.client_secret')

        # construct handlers
        self.meetup_handler = meetupHandler()
        self.requests_handler = requests_handler

    def _get_request(self, url, params):

        import requests

    # send request
        try:
            response = requests.get(url=url, params=params)
        except Exception:
            if self.requests_handler:
                request_object = requests.Request(method='GET', url=url, params=params)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.meetup_handler.handle(response)

        return response_details

    def _post_request(self, url, data):

        import requests

    # send request
        try:
            response = requests.post(url=url, data=data)
        except Exception:
            if self.requests_handler:
                request_object = requests.Request(method='GET', url=url, data=data)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.meetup_handler.handle(response)

        return response_details

    def generate_url(self, redirect_uri, service_scope=None, state_value='', device_type=''):

        ''' a method to generate the oauth2 authorization url for client to meetup api

        :param device_type: string with type of device receiving authorization url
        :param redirect_uri: string with redirect uri registered with moves
        :param service_scope: [optional] list with service type permissions
        :param state_value: [optional] string with unique url-safe variable
        :return: string with authorization url
        '''

        title = '%s.generate_url' % self.__class__.__name__

    # validate inputs
        input_args = {
            'redirect_uri': redirect_uri,
            'state_value': state_value,
            'device_type': device_type,
            'service_scope': service_scope
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, value)
                self.fields.validate(value, '.%s' % key, object_title)

    # determine base url for device type
        url_string = self.fields.schema['code_endpoint']

    # construct query parameters
        query_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri
        }
        if state_value:
            query_params['state'] = state_value
        for item in service_scope:
            if 'scope' not in query_params.keys():
                query_params['scope'] = ''
            if query_params['scope']:
                query_params['scope'] += ' '
            query_params['scope'] += item
        if device_type == 'mobile':
            query_params['set_mobile'] = 'on'

    # encode query parameters
        from urllib.parse import urlencode
        url_string += '?%s' % urlencode(query_params)

        return url_string

    def get_token(self, auth_code, redirect_uri):

        '''
            a method to get an access token from moves api

        :param auth_code: string with authentication code received from client
        :param redirect_uri: string with redirect uri registered with moves
        :return: dictionary with token details

        {
            'json': {
                'access_token': '1j0v33o6c5b34cVPqIiB_M2LYb_iM5S9Vcy7Rx7jA2630pK7HIjEXvJoiE8V5rRF',
                'token_type': 'bearer',
                'expires_at': 1478559072,
                'refresh_token': 'A27CSzZXKf2EPB45lvLQyT56sZ80dXNtp_lA7lvZ6UIKAy94GNvW9g9aGmJtbl28'
            }
        }
        '''

        title = '%s.get_token' % self.__class__.__name__

    # validate inputs
        input_args = {
            'auth_code': auth_code,
            'redirect_uri': redirect_uri
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, value)
                self.fields.validate(value, '.%s' % key, object_title)

    # construct url string
        url_string = self.fields.schema['token_endpoint']

    # construct request params
        request_form = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri
        }

    # send request
        from time import time
        current_time = time()
        token_details = self._post_request(url_string, data=request_form)

    # convert expiration info to epoch time
        details = token_details['json']
        if details:
            details['expires_at'] = int(current_time) + details['expires_in']
            del details['expires_in']

        return token_details

    def renew_token(self, refresh_token, service_scope=None):

        '''
            a method to renew an access token with moves api

        :param refresh_token: string with refresh token value received with prior token
        :param service_scope: dictionary with service type permissions
        :return: dictionary with token details

        {
            'json': {
                'access_token': '1j0v33o6c5b34cVPqIiB_M2LYb_iM5S9Vcy7Rx7jA2630pK7HIjEXvJoiE8V5rRF',
                'token_type': 'bearer',
                'expires_at': 1478559072,
                'refresh_token': 'A27CSzZXKf2EPB45lvLQyT56sZ80dXNtp_lA7lvZ6UIKAy94GNvW9g9aGmJtbl28',
                'user_id': 23138311640030064
            }
        }
        '''

        title = '%s.renew_token' % self.__class__.__name__

    # validate inputs
        object_title = '%s(%s=%s)' % (title, 'refresh_token', refresh_token)
        self.fields.validate(refresh_token, '.token_details.refresh_token', object_title)
        if service_scope:
            object_title = '%s(%s=%s)' % (title, 'service_scope', service_scope)
            self.fields.validate(service_scope, '.service_scope', object_title)

    # construct url string
        url_string = self.fields.schema['token_endpoint']

    # construct request params
        request_form = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

    # send request
        from time import time
        current_time = time()
        token_details = self._post_request(url_string, data=request_form)

    # convert expiration info to epoch time
        details = token_details['json']
        if details:
            details['expires_at'] = int(current_time) + details['expires_in']
            del details['expires_in']

        return token_details

class meetupClient(object):

    def __init__(self, access_token):

        ''' initialization method for meetup client class

        :param: access_token
        '''

        pass

    def memberGroups(meetup_user_id, meetup_user_key):
        '''
            function to discover info about a group
            interprets JSON response to GET request to Meetup API for group info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/groups?%s'
        params = {
            'key': meetup_user_key,
            'member_id': str(meetup_user_id)
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def groupInfo(groupID, meetup_user_key):
        '''
            function to discover info about a group
            interprets JSON response to GET request to Meetup API for group info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/groups?%s'
        params = {
            'key': meetup_user_key,
            'group_id': str(groupID)
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def groupEvents(groupID, meetup_user_key):
        '''
            function to discover upcoming events for a group
            interprets JSON response to GET request to Meetup API for group's event list
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/events?%s'
        params = {
            'key': meetup_user_key,
            'group_id': groupID
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def eventInfo(eventID, meetup_user_key):
        '''
            function to discover info about a Meetup event
            interprets JSON response to GET request to Meetup API for event info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            response (mand):
            ['rsvpable'] = true # boolean
            response (optional):
            ['rsvp_rules']['guest_limit'] = 2 # int
            ['fee']['amount'] = 10 # int
            ['fee']['required'] = "1" # string
            ['survey_questions'][0]['id'] = 22529716 # int
            ['survey_guestions'][0]['required'] = false # boolean
            ['survey_questions'][0]['question'] = "What is your name?" # string
            ['yes_rsvp_count'] = 86 # int
            ['rsvp_limit'] = 150 # int
        '''
        meetup_url = 'https://api.meetup.com/2/event/' + str(eventID) + '/?%s'
        params = {
            'key': meetup_user_key,
            'fields': 'rsvpable,rsvp_rules,fee,survey_questions'
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def eventRSVPs(eventID, meetup_user_key):
        '''
            function to check info of all RSVPs to a Meetup event by eventID
            interprets JSON response to GET request to Meetup API for RSVPs status
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            returns:
            ['results'] = list of dictionaries of users
                [0]['member']['member_id'] # int
                [0]['member']['name'] # str
                [0]['rsvp_id'] # int
                [0]['response'] # yes or no
                [0]['member_photo']['highres_link'] # str
            ['meta'] = api responsiveness data
        '''
        meetup_url = 'https://api.meetup.com/2/rsvps?%s'
        params = {
            'key': meetup_user_key,
            'event_id': str(eventID)
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def memberInfo(meetup_user_id, meetup_user_key):
        '''
            function to discover info about a Meetup member
            interprets JSON response to GET request to Meetup API for member info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            response (mand):
            response (optional):
        '''
        meetup_url = 'https://api.meetup.com/2/member/' + str(meetup_user_id) + '/?%s'
        params = {
            'key': meetup_user_key
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def memberRSVPStatus(rsvpID, meetup_user_key):
        '''
            function to check status of RSVP to a Meetup event by RSVPID
            interprets JSON response to GET request to Meetup API for member RSVP status
            requires:
            RSVPID number for member from a previous event RSVP
            meetup_user_key for member
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/rsvp/' + str(rsvpID) + '?%s'
        params = {
            'key': meetup_user_key
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def RSVPYes(eventID, meetup_user_key, guests = None):
        '''
            function to RSVP to a Meetup event on behalf of member
            creates a POST to Meetup API to RSVP with member key
            requires:
            event_id of event
            user key of member
            user to be a member of the group
            optional:
            guest limit determined by meetupEventInfo ['rsvp_rules']['guest_limit']
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        params = {
            'event_id': str(eventID),
            'rsvp': 'yes',
            'key': meetup_user_key
        }
        if guests:
            params['guests'] = str(guests)
        else:
            pass
        url = 'https://api.meetup.com/2/rsvp'
        post_params = urllib.parse.urlencode(params).encode('utf-8')
        response = urllib.request.urlopen(url, post_params)
        return json.loads(response.read().decode("utf-8"))

    def RSVPNo(eventID, meetup_user_key):
        '''
            function to decline RSVP to a Meetup event on behalf of member
            creates a POST to Meetup API to RSVP with member key
            requires:
            event_id of event
            user key of member
            user to be a member of the group
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        params = {
            'event_id': str(eventID),
            'rsvp': 'no',
            'key': meetup_user_key
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        meetup_url = 'https://api.meetup.com/2/rsvp'
        post_argument = urllib.parse.urlencode(params).encode('utf-8')
        response = urllib.request.urlopen(meetup_url, post_argument)
        return json.loads(response.read().decode("utf-8"))

    def memberEventList(meetup_user_id, meetup_user_key, api_throttle, searchDepth=False):
        '''
            returns a chronological list of events in user's Meetup groups
            searchDepth default is all
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            returns list of dictionaries:
            [0]['eventID']
            [0]['eventName']
            [0]['eventURL']
            [0]['eventDT']
            [0]['groupID']
        '''
        member_groups = meetupAPI.memberGroups(meetup_user_id, meetup_user_key)
        member_events = []
        for i in range(0,len(member_groups['results'])):
            t1 = timer()
            try:
                group_events = meetupAPI.groupEvents(member_groups['results'][i]['id'], meetup_user_key)
                if group_events['results']:
                    searchLength = len(group_events['results'])
                    if searchDepth:
                        searchLength = int(searchDepth)
                    else:
                        pass
                    for j in range(0,searchLength):
                        event = {}
                        eventURL = group_events['results'][j]['event_url'].replace('\/', '/')
                        event['eventURL'] = eventURL
                        if isinstance(group_events['results'][j]['id'],int):
                            event['eventID'] = group_events['results'][j]['id']
                        else:
                            event['eventID'] = eventURL[eventURL.find('events/') + 7:\
                                eventURL.rfind('/')]
                        event['eventName'] = group_events['results'][j]['name']
                        event['groupID'] = group_events['results'][j]['group']['id']
                        event['eventDT'] = int(group_events['results'][j]['time']) / 1000
                        member_events.append(event)
                else:
                    pass
            except:
                pass
            t2 = timer()
            time_split = t2 - t1
            wait_time = api_throttle - time_split
            if wait_time > 0:
                time.sleep(wait_time)
        return sorted(member_events, key=lambda k: k['eventDT'])

    def nextRSVP(meetup_user_id, meetup_user_key, api_throttle, searchDepth=False):
        '''
            looks for the next available event in user's Meetup groups & RSVPs for it
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            returns dictionary:
            ['rsvpID']
            ['meetup_user_key']
            ['eventID']
            ['eventName']
            ['eventURL']
            ['eventDT']
            ['groupID']
        '''
        eventFound = False
        eventCounter = 0
        if searchDepth:
            searchDepth = int(searchDepth)
        else:
            searchDepth = 3
        eventList = meetupAPI.memberEventList(meetup_user_id, meetup_user_key, api_throttle, searchDepth)
        eventRSVP = {}
        while not eventFound:
            t1 = timer()
            pE = meetupAPI.eventInfo(eventList[eventCounter]['eventID'], meetup_user_key)
            if not 'rsvp_limit' in pE.keys():
                pE['rsvp_limit'] = 1000000
            if not 'yes_rsvp_count' in pE.keys():
                pE['yes_rsvp_count'] = 0
            if not 'survey_questions' in pE.keys():
                reqQ = False
            else:
                for i in range(0,len(pE['survey_questions'])):
                    if not pE['survey_questions'][i]['required']:
                        reqQ = False
                    else:
                        reqQ = True
                        i = len(pE['survey_questions'])
            if pE['rsvpable'] and pE['yes_rsvp_count'] < pE['rsvp_limit'] and \
                    not 'fees' in pE.keys() and not reqQ:
                try:
                    rsvp = meetupAPI.RSVPYes(eventList[eventCounter]['eventID'], meetup_user_key)
                    eventFound = True
                    eventRSVP['rsvpID'] = rsvp['rsvp_id']
                    eventRSVP['meetup_user_key'] = meetup_user_key
                    eventRSVP['eventID'] = eventList[eventCounter]['eventID']
                    eventRSVP['groupID'] = eventList[eventCounter]['groupID']
                    eventRSVP['eventName'] = eventList[eventCounter]['eventName']
                    eventRSVP['eventDT'] = eventList[eventCounter]['eventDT']
                    eventRSVP['eventURL'] = eventList[eventCounter]['eventURL']
                except:
                    print('RSVP failed')
                    pass
            eventCounter += 1
            t2 = timer()
            time_split = t2 - t1
            wait_time = api_throttle - time_split
            if wait_time > 0:
                time.sleep(wait_time)
        return eventRSVP

    def methodTest(meetup_user_id, meetup_user_key, api_throttle):
        '''
            unit test for the meetup methods
        '''
        urlTitle = 'Meetup API'
        t1 = timer()
        eventRSVP = meetupAPI.nextRSVP(meetup_user_id, meetup_user_key, api_throttle, 3)
        assert meetupAPI.groupInfo(eventRSVP['groupID'], meetup_user_key)
        eventAttendees = meetupAPI.eventRSVPs(eventRSVP['eventID'], meetup_user_key)
        assert meetupAPI.memberInfo(eventAttendees['results'][0]['member']['member_id'], meetup_user_key)
        rsvpStatus = meetupAPI.memberRSVPStatus(eventRSVP['rsvpID'], meetup_user_key)
        if str(rsvpStatus['response']) == 'yes':
            meetupAPI.RSVPNo(eventRSVP['eventID'], meetup_user_key)
            print('Meetup Methods Working')
        else:
            print('failure')
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return True

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    meetup_config = load_settings('../../../cred/meetup.yaml')
    meetup_oauth = meetupOAuth(meetup_config['meetup_client_id'], meetup_config['meetup_client_secret'])
    auth_url = meetup_oauth.generate_url(meetup_config['meetup_redirect_uri'], service_scope=['ageless', 'profile_edit', 'basic'], state_value='unittest')
    print(auth_url)