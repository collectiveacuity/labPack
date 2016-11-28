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
                {'requests': 30, 'period': 10}
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

    def handle(self, response):

    # construct default response details
        details = {
            'method': response.request.method,
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers
        }

    # rate limit headers:
        # https://www.meetup.com/meetup_api/docs/#limits
        # X-RateLimit-Limit
        # X-RateLimit-Remaining
        # X-RateLimit-Reset

    # handle different codes
        if details['code'] == 200:
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()

        return details

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
                'expires_at': 0,
                'refresh_token': ''
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
        self.service_handler = meetupHandler()
        self.requests_handler = requests_handler

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
        response_details = self.service_handler.handle(response)

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
        print(token_details)

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

    _class_fields = {
        'schema': {
            'api_endpoint': 'https://api.meetup.com',
            'access_token': '1350d78219f4dc9ded18c7fbda86a19e',
            'service_scope': ['ageless'],
            'requests_handler': 'labpack.handlers.requests.handle_requests',
            'usage_client': 'labpack.storage.appdata.appdataClient.__init__',
            'member_id': 12345678,
            'group_url': 'myfavoritegroup',
            'group_id': 23456789,
            'event_id': 23454321,
            'max_results': 4
        },
        'components': {
            '.service_scope': {
                'unique_values': True
            },
            '.service_scope[0]': {
                'discrete_values': ['ageless', 'basic', 'event_management', 'group_edit', 'group_content', 'group_join', 'profile_edit', 'reporting', 'rsvp']
            },
            '.max_results': {
                'integer_data': True
            },
            '.member_id': {
                'integer_data': True
            },
            '.event_id': {
                'integer_data': True
            },
            '.group_id': {
                'integer_data': True
            }
        }
    }

    def __init__(self, access_token, service_scope, usage_client=None, requests_handler=None):

        ''' initialization method for meetup client class

        :param access_token: string with access token for user provided by meetup oauth
        :param service_scope: dictionary with service type permissions
        :param usage_client: [optional] callable that records usage data
        :param requests_handler: [optional] callable that handles requests errors
        '''

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'access_token': access_token,
            'service_scope': service_scope
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct class properties
        self.access_token = access_token
        self.service_scope = service_scope
        self.endpoint = self.fields.schema['api_endpoint']
    
    # construct method handlers
        self.requests_handler = requests_handler
        self.service_handler = meetupHandler(usage_client)
    
    def _get_request(self, url, headers=None, params=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': {'Authorization': 'Bearer %s' % self.access_token},
            'params': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)

    # send request
        try:
            response = requests.get(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'GET'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.service_handler.handle(response)

        return response_details

    def _post_request(self, url, headers=None, params=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': {'Authorization': 'Bearer %s' % self.access_token},
            'params': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)

    # send request
        try:
            response = requests.post(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'POST'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.service_handler.handle(response)

        return response_details

    def get_member_profile(self, member_id=0):

        ''' a method to retrieve member profile info

        :param member_id: [optional] integer with member id from member profile
        :return: dictionary with member profile inside [json] key

        {
            'json': {
                'name': 'First Last'
                'photo_url': 'http://photos1.meetupstatic.com/photos/member/member_12.jpeg',
                'other_services': {},
                'lon': '-12.34567890',
                'lat': '87.65432109',
                'id': '123456789',
                'visited': '2015-10-23 13:12:44 PST',
                'city': 'Sacramento',
                'joined': 'Tue Oct 08 14:25:56 PDT 2012',
                'zip': '95660',
                'bio': 'my info',
                'link': 'http://www.meetup.com/members/12345678',
                'state': 'CA',
                'country': 'us',
                'lang': 'en_US'
            }
        }
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.get_member_profile' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/members/' % self.endpoint
        params = {
            'member_id': 'self'
        }
        if member_id:
            params['member_id'] = member_id

    # send request
        response_details = self._get_request(url, params=params)

    # construct method output dictionary
        profile_details = {
            'json': {}
        }
        for key, value in response_details.items():
            if not key == 'json':
                profile_details[key] = value

    # parse response
        if response_details['json']:
            if 'results' in response_details['json'].keys():
                if response_details['json']['results']:
                    details = response_details['json']['results'][0]
                    for key, value in details.items():
                        if key != 'topics':
                            profile_details['json'][key] = value

        return profile_details

    def get_member_settings(self, member_id):

        ''' a method to retrieve member settings details

        :param member_id: integer with member id from member profile
        :return: dictionary with member settings inside [json] key

        {
            'json': {
                'name': 'First Last',
                'status': 'active',
                'gender: 'none',
                'messaging_pref': 'all_members',
                'lon': '-12.34',
                'lat': '87.65',
                'id': '123456789',
                'city': 'Sacramento',
                'joined': 1234567890000,
                'bio': 'my info',
                'state': 'CA',
                'country': 'us',
                'localized_country_name': 'USA',
                'privacy': {
                    'bio': 'visible',
                    'groups': 'hidden',
                    'topics': 'visible'
                },
                'stats': {
                    'groups': 123,
                    'rsvps': 234,
                    'topics': 12
                },
                'photo': {
                    'type': 'member',
                    'id': 12,
                    'highres_link': 'http://photos1.meetupstatic.com/photos/member/highres_12.jpeg',
                    'photo_link': 'http://photos1.meetupstatic.com/photos/member/member_12.jpeg',
                    'thumb_link': 'http://photos1.meetupstatic.com/photos/member/thumb_12.jpeg'
                }
            }
        }
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.get_member_settings' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct member id
        if not member_id:
            raise IndexError('%s requires member id argument.' % title)

    # compose request fields
        url = '%s/members/%s' % (self.endpoint, str(member_id))
        params = {
            'fields': 'gender,birthday,messaging_pref,other_services,privacy,self,stats'
        }

    # send requests
        member_settings = self._get_request(url, params=params)

        return member_settings

    def get_member_topics(self, member_id):

        ''' a method to retrieve a list of topics member follows

        :param member_id: integer with meetup member id
        :return: dictionary with list of topics inside [json] key

        {
            'json': [
                {
                  'urlkey': 'diningout',
                  'lang': 'en_US',
                  'id': 713,
                  'name': 'Dining Out'
                }
            ]
        }
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.get_member_topics' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct member id
        if not member_id:
            raise IndexError('%s requires member id argument.' % title)

    # compose request fields
        url = '%s/members/%s' % (self.endpoint, str(member_id))
        params = {
            'fields': 'topics'
        }

    # send requests
        response_details = self._get_request(url, params=params)

    # construct method output dictionary
        member_topics = {
            'json': []
        }
        for key, value in response_details.items():
            if not key == 'json':
                member_topics[key] = value

    # parse response
        if response_details['json']:
            if 'topics' in response_details['json'].keys():
                member_topics['json'] = response_details['json']['topics']

        return member_topics

    def get_member_groups(self, member_id):

        ''' a method to retrieve a list of meetup groups member belongs to

        :param member_id: integer with meetup member id
        :return: dictionary with list of groups in [json]

        {
            'json': [
                {
                    'status': 'active',
                    'updated': 1234567891000,
                    'visited': 1234567891000,
                    'created': 1234567891000,
                    'group': {
                        'id': 12334567,
                        'join_mode': 'open',
                        'group_photo': { ... PHOTO OBJECT ... },
                        'urlname': 'myfavoritegroup',
                        'members': 123,
                        'key_photo': { ... },
                        'who': 'Team Us',
                        'name': 'My Favorite Group'
                    }
                }
            ]
        }
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.get_member_groups' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct member id
        if not member_id:
            raise IndexError('%s requires member id argument.' % title)

    # compose request fields
        url = '%s/members/%s' % (self.endpoint, str(member_id))
        params = {
            'fields': 'memberships'
        }

    # send requests
        response_details = self._get_request(url, params=params)

    # construct method output dictionary
        member_groups = {
            'json': []
        }
        for key, value in response_details.items():
            if not key == 'json':
                member_groups[key] = value

    # parse response
        if response_details['json']:
            if 'memberships' in response_details['json'].keys():
                member_groups['json'] = response_details['json']['memberships']['member']

        return member_groups

    def get_member_events(self, upcoming=True):

        ''' a method to retrieve a list of events member attended or will attend

        :param upcoming: [optional] boolean to filter list to only future events
        :return: dictionary with event list results within [json]

        {
            'json': [
                {
                    'id': '123456789',
                    'name': 'My Favorite Event',
                    'created': 1234567890000,
                    'updated': 1234567890000,
                    'visibility': 'public',
                    'status': 'upcoming',
                    'time': 1234567890000,
                    'utc_offset': -28800000,
                    'duration': 11700000,
                    'fee': {
                        'accepts': 'paypal',
                        'required': True,
                        'label': 'price',
                        'currency': 'USD',
                        'description': 'per person',
                        'amount': 5.0
                    },
                    'rsvp_rules': {
                        'close_time': 1234567890000,
                        'closed': False,
                        'guest_limit': 0,
                        'open_time': 1234567890000,
                        'refund_policy': { 'days': 3, 'notes': '', 'policies': [] },
                        'waitlisting': 'auto'
                    },
                    'survey_questions': [
                        {
                            'id': 234567890,
                            'question': 'tell me something i want to know'
                        }
                    ],
                    'rsvp_limit': 200,
                    'yes_rsvp_count': 200,
                    'waitlist_count': 123,
                    'rsvpable': True,
                    'rsvpable_after_join': True,
                    'rsvp_after_join': True,
                    'description': '<p>A long description</p>',
                    'comment_count': 1,
                    'how_to_find_us': 'open the door',
                    'group': { ... GROUP OBJECT ... },
                    'venue': { ... VENUE OBJECT ... },
                    'event_hosts': [ { ... HOST OBJECT ... }]
                    'short_link': 'http://meetu.ps/e/df6Ju/GlGy/i'
                    'link': 'https://www.meetup.com/mygroup/events/123456789/'
                }
            ]
        }
        '''

    # https://www.meetup.com/meetup_api/docs/self/events/

    # construct request fields
        url = '%s/self/events' % self.endpoint
        params = {
            'status': 'past',
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable'
        }
        if upcoming:
            params['status'] = 'upcoming'

    # send requests
        member_events = self._get_request(url, params=params)
        for event in member_events['json']:
            if not 'fee' in event.keys():
                event['fee'] = {}
            if not 'rsvpable_after_join' in event.keys():
                event['rsvpable_after_join'] = True

        return member_events

    def get_member_calendar(self, max_results=0):

        ''' a method to retrieve the upcoming events for all groups member belongs to

        :param max_results: [optional] integer with number of events to include
        :return: dictionary with event list results within [json]

        {
            'json': [
                {
                    'id': '123456789',
                    'name': 'My Favorite Event',
                    'created': 1234567890000,
                    'updated': 1234567890000,
                    'visibility': 'public',
                    'status': 'upcoming',
                    'time': 1234567890000,
                    'utc_offset': -28800000,
                    'duration': 11700000,
                    'fee': {
                        'accepts': 'paypal',
                        'required': True,
                        'label': 'price',
                        'currency': 'USD',
                        'description': 'per person',
                        'amount': 5.0
                    },
                    'rsvp_rules': {
                        'close_time': 1234567890000,
                        'closed': False,
                        'guest_limit': 0,
                        'open_time': 1234567890000,
                        'refund_policy': { 'days': 3, 'notes': '', 'policies': [] },
                        'waitlisting': 'auto'
                    },
                    'survey_questions': [
                        {
                            'id': 234567890,
                            'question': 'tell me something i want to know'
                        }
                    ],
                    'rsvp_limit': 200,
                    'yes_rsvp_count': 200,
                    'waitlist_count': 123,
                    'rsvpable': True,
                    'rsvpable_after_join': True,
                    'rsvp_after_join': True,
                    'description': '<p>A long description</p>',
                    'comment_count': 1,
                    'how_to_find_us': 'open the door',
                    'group': { ... GROUP OBJECT ... },
                    'venue': { ... VENUE OBJECT ... },
                    'event_hosts': [ { ... HOST OBJECT ... }]
                    'short_link': 'http://meetu.ps/e/df6Ju/GlGy/i'
                    'link': 'https://www.meetup.com/mygroup/events/123456789/'
                }
            ]
        }
        '''

    #
        title = '%s.get_member_calendar' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'max_results': max_results
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/self/calendar' % self.endpoint
        params = {
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable'
        }
        if max_results:
            params['page'] = str(max_results)

    # send requests
        member_calender = self._get_request(url, params=params)

    # construct method output
        for event in member_calender['json']:
            if not 'fee' in event.keys():
                event['fee'] = {}
            if not 'rsvpable_after_join' in event.keys():
                event['rsvpable_after_join'] = True

        return member_calender

    def get_group_details(self, group_url='', group_id=0):

        ''' a method to retrieve details about a meetup group

        :param group_url: string with meetup urlname of group
        :param group_id: int with meetup id for group
        :return: dictionary with group details inside [json] key

        {
            'json': {
                'category': {
                    'id': 34,
                    'name': 'Tech',
                    'shortname': 'Tech',
                    'sort_name': 'Tech'
                },
                'city': 'Sacramento',
                'country': 'US',
                'created': 1234567890000,
                'description': '',
                'id': 12345678,
                'join_mode': 'open',
                'key_photo': { ... PHOTO OBJECT ... },
                'lat': 12.34,
                'link': 'https://www.meetup.com/myfavoritegroup/',
                'localized_country_name': 'USA',
                'lon': -12.34,
                'members': 201,
                'name': 'My Favorite Group',
                'next_event': { ... EVENT OBJECT ... },
                'organizer': { ... HOST OBJECT ... },
                'photos': [ { ... PHOTO OBJECT ... } ],
                'state': 'CA',
                'timezone': 'US/Western',
                'urlname': 'myfavoritegroup',
                'visibility': 'public',
                'who': 'Team Us'
            }
        }
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/#get

        title = '%s.get_group_details' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'group_id': group_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if not group_url and not group_id:
            raise IndexError('%s requires either a group_url or group_id argument.' % title)

    # construct request fields
        if group_id:
            url = '%s/2/groups?group_id=%s' % (self.endpoint, group_id)
        else:
            url = '%s/%s' % (self.endpoint, group_url)

    # send request
        response_details = self._get_request(url)

    # cosntruct method output
        group_details = response_details
        if group_id:
            if response_details['json']:
                if 'results' in response_details['json'].keys():
                    if response_details['json']['results']:
                        group_details['json'] = response_details['json']['results'][0]

        return group_details

    def get_group_events(self, group_url):

        ''' a method to retrieve a list of upcoming events hosted by group

        :param group_url: string with meetup urlname field of group
        :return: dictionary with event list results within [json]

        {
            'json': [
                {
                    'id': '123456789',
                    'name': 'My Favorite Event',
                    'created': 1234567890000,
                    'updated': 1234567890000,
                    'visibility': 'public',
                    'status': 'upcoming',
                    'time': 1234567890000,
                    'utc_offset': -28800000,
                    'duration': 11700000,
                    'fee': {
                        'accepts': 'paypal',
                        'required': True,
                        'label': 'price',
                        'currency': 'USD',
                        'description': 'per person',
                        'amount': 5.0
                    },
                    'rsvp_rules': {
                        'close_time': 1234567890000,
                        'closed': False,
                        'guest_limit': 0,
                        'open_time': 1234567890000,
                        'refund_policy': { 'days': 3, 'notes': '', 'policies': [] },
                        'waitlisting': 'auto'
                    },
                    'survey_questions': [
                        {
                            'id': 234567890,
                            'question': 'tell me something i want to know'
                        }
                    ],
                    'rsvp_limit': 200,
                    'yes_rsvp_count': 200,
                    'waitlist_count': 123,
                    'rsvpable': True,
                    'rsvpable_after_join': True,
                    'rsvp_after_join': True,
                    'description': '<p>A long description</p>',
                    'comment_count': 1,
                    'how_to_find_us': 'open the door',
                    'group': { ... GROUP OBJECT ... },
                    'venue': { ... VENUE OBJECT ... },
                    'event_hosts': [ { ... HOST OBJECT ... }]
                    'short_link': 'http://meetu.ps/e/df6Ju/GlGy/i'
                    'link': 'https://www.meetup.com/mygroup/events/123456789/'
                }
            ]
        }
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/#list


        title = '%s.get_group_events' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events' % (self.endpoint, group_url)
        params = {
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable'
        }

    # send request
        group_events = self._get_request(url, params=params)

    # construct method output
        for event in group_events['json']:
            if not 'fee' in event.keys():
                event['fee'] = {}
            if not 'rsvpable_after_join' in event.keys():
                event['rsvpable_after_join'] = True

        return group_events

    def get_event_details(self, group_url, event_id):

        ''' a method to retrieve details for an event

        :param group_url: string with meetup urlname for host group
        :param event_id: integer with meetup id for event
        :return: dictionary with event details inside [json] key

        {
            'json': {
                'id': '123456789',
                'name': 'My Favorite Event',
                'created': 1234567890000,
                'updated': 1234567890000,
                'visibility': 'public',
                'status': 'upcoming',
                'time': 1234567890000,
                'utc_offset': -28800000,
                'duration': 11700000,
                'fee': {
                    'accepts': 'paypal',
                    'required': True,
                    'label': 'price',
                    'currency': 'USD',
                    'description': 'per person',
                    'amount': 5.0
                },
                'rsvp_rules': {
                    'close_time': 1234567890000,
                    'closed': False,
                    'guest_limit': 0,
                    'open_time': 1234567890000,
                    'refund_policy': { 'days': 3, 'notes': '', 'policies': [] },
                    'waitlisting': 'auto'
                },
                'survey_questions': [
                    {
                        'id': 234567890,
                        'question': 'tell me something i want to know'
                    }
                ],
                'rsvp_limit': 200,
                'yes_rsvp_count': 200,
                'waitlist_count': 123,
                'rsvpable': True,
                'rsvpable_after_join': True,
                'rsvp_after_join': True,
                'description': '<p>A long description</p>',
                'comment_count': 1,
                'how_to_find_us': 'open the door',
                'group': { ... GROUP OBJECT ... },
                'venue': { ... VENUE OBJECT ... },
                'event_hosts': [ { ... HOST OBJECT ... }]
                'short_link': 'http://meetu.ps/e/df6Ju/GlGy/i'
                'link': 'https://www.meetup.com/mygroup/events/123456789/'
            }
        }
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:id/#get

        title = '%s.get_event_details' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'event_id': event_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events/%s' % (self.endpoint, group_url, str(event_id))
        params = {
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable,rsvpable_after_join'
        }

    # send request
        response_details = self._get_request(url, params=params)

    # construct event details
        event_details = {
            'json': {
                'fee': {},
                'rsvpable_after_join': True
            }
        }
        for key, value in response_details.items():
            if key != 'json':
                event_details[key] = value

    # parse response
        if response_details['json']:
            event_details['json'].update(**response_details['json'])

        return event_details

    def get_event_attendees(self, group_url, event_id):

        ''' a method to retrieve attendee list for event from meetup api

        :param group_url: string with meetup urlname for host group
        :param event_id: integer with meetup id for event
        :return: dictionary with attendee list inside [json] key

        {
            'json': [
                {
                    'created': 1234567891000,
                    'updated': 1234567891000,
                    'response': 'yes',
                    'guests': 0,
                    'member': {
                        'event_context': { 'host': False },
                        'id': 12334567,
                        'name': 'First',
                        'photo': { ... PHOTO OBJECT ... }
                    },
                    'venue': { ... VENUE OBJECT ... },
                    'group': { ... GROUP OBJECT ... },
                    'event': { ... EVENT OBJECT ... }
                }
            ]
        }
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/rsvps/#list

        title = '%s.get_event_attendees' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'event_id': event_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events/%s/rsvps' % (self.endpoint, group_url, str(event_id))

    # send request
        response_details = self._get_request(url)

        return response_details

    def update_rsvp_details(self, group_url, event_id):

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/rsvps/

        url = '%s/%s/events/%s/rsvps' % (self.endpoint, group_url, event_id)
        response_details = self._post_request(url)

        return response_details

    def list_groups(self, categories=None, topics=None, text='', country='', latitude=0, longitude=0, location='', radius=10, zip_code=''):

    # https://www.meetup.com/meetup_api/docs/find/groups/

        url = '%s/find/groups' % self.endpoint
        params = {
            'category': '',
            'topic_id': '',
            'text': '',
            'country': '',
            'lat': '',
            'lon': '',
            'location': '',
            'radius': '',
            'zip': '',
            'self_groups': 'exclude'
        }

        group_list = self._get_request(url, params=params)

        return group_list

    def scan_groups(self):

        ''' a method to iterate over all ID permutations to discover meetup groups '''

        group_list = []

        return group_list

    def get_group_members(self, group_url):

    # https://www.meetup.com/meetup_api/docs/:urlname/members/#list

        group_members = []

        return group_members

    def join_group(self, group_url):

    # https://www.meetup.com/meetup_api/docs/:urlname/members/#create

        url = '%s/%s/members' % (self.endpoint, group_url)
        response_details = self._post_request(url)

        return response_details

    def list_locations(self, latitude, longitude, results=100):

        ''' a method to retrieve location names based upon latitude and longitude '''

    # https://www.meetup.com/meetup_api/docs/find/locations/

        location_list = []

        return location_list

    def get_venue_details(self, venue_id):
        venue_details = {}
        return venue_details

    def update_member_profile(self, profile_details):

        return profile_details

if __name__ == '__main__':
    from pprint import pprint
    from time import time
    from labpack.records.settings import load_settings
    meetup_config = load_settings('../../../cred/meetup.yaml')
    meetup_oauth = meetupOAuth(meetup_config['meetup_client_id'], meetup_config['meetup_client_secret'])
    auth_url = meetup_oauth.generate_url(meetup_config['meetup_redirect_uri'], service_scope=['ageless', 'profile_edit', 'basic'], state_value='unittest')
    assert auth_url.find('oauth2') > 0
    from labpack.storage.appdata import appdataClient
    log_client = appdataClient(collection_name='Logs', prod_name='Fitzroy')
    path_filters = [{0: {'discrete_values': ['knowledge']}, 1: {'discrete_values': ['tokens']}, 2: {'discrete_values':['meetup']}}]
    token_list = log_client.list(log_client.conditionalFilter(path_filters), reverse_search=True)
    token_details = log_client.read(token_list[0])
    # new_details = meetup_oauth.renew_token(token_details['refresh_token'])
    # token_details.update(**new_details['json'])
    # new_key = 'knowledge/tokens/meetup/%s/%s.yaml' % (token_details['user_id'], token_details['expires_at'])
    # log_client.create(new_key, token_details)
    meetup_client = meetupClient(token_details['access_token'], token_details['service_scope'])
    # profile_details = meetup_client.get_member_profile()
    # member_id = int(profile_details['json']['id'])
    # settings_details = meetup_client.get_member_settings(member_id)
    # topic_details = meetup_client.get_member_topics(member_id)
    # group_details = meetup_client.get_member_groups(member_id)
    # event_details = meetup_client.get_member_events()
    event_details = meetup_client.get_member_calendar(max_results=10)
    group_url = event_details['json'][0]['group']['urlname']
    event_id = int(event_details['json'][0]['id'])
    group_id = int(event_details['json'][0]['group']['id'])
    print(event_details['json'][0])
    # group_details = meetup_client.get_group_details(group_id=group_id)
    # group_events = meetup_client.get_group_events(group_url)
    # event_id = int(group_events['json'][0]['id'])
    # event_details = meetup_client.get_event_details(group_url, event_id)
    # event_attendees = meetup_client.get_event_attendees(group_url, event_id)
    # member_id = event_attendees['json'][0]['member']['id']
    # profile_details = meetup_client.get_member_profile(member_id)
    # print(profile_details)




