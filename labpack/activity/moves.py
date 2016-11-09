__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

class MovesError(Exception):

    def __init__(self, message='', error_dict=None):

    # TODO create bad connection diagnostics methods

        text = '\nBad Request %s' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                for key, value in error_dict.items():
                    self.error[key] = value
        super(MovesError, self).__init__(text)

class movesHandler(object):

    ''' handles responses from moves api and usage data'''

    _class_fields = {
        'schema': {
            'rate_limits': [
                {'requests': 60, 'period': 60},
                {'requests': 2000, 'period': 3600}
            ]
        }
    }

    def __init__(self, usage_client=None):

        '''
            initialization method for moves client class
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
            'code': 200,
            'msg': 'ok',
            'content': {},
            'headers': response.headers
        }
        status = response.status_code

    # handle different codes
        if status == 401:
            details['code'] = 401
            details['msg'] = 'Unauthorized'
        else:
            details['content'] = response.json()

        return details

class movesRegister(object):
    ''' currently must be done manually '''
    ''' https://dev.moves-app.com/ '''
    def __init__(self):
        pass

class movesOAuth(object):

    ''' a class of methods to handle oauth2 authentication with moves API '''

    # https://dev.moves-app.com/docs/authentication

    _class_fields = {
        'schema': {
            'oauth_endpoint': {
                'web': 'https://api.moves-app.com/oauth/v1',
                'mobile': 'moves://app'
            },
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
            'service_scope': [ 'location' ],
            'state_value': '',
            'access_code': ''
        },
        'components': {
            '.device_type': {
                'discrete_values': [ 'web', 'mobile' ]
            },
            '.redirect_uri': {
                'must_contain': [ '^https://' ]
            },
            '.service_scope': {
                'unique_values': True,
                'max_size': 2
            },
            '.service_scope[0]': {
                'discrete_values': [ 'location', 'activity' ]
            }
        }
    }

    def __init__(self, client_id, client_secret, requests_handler=None):

        '''
            initialization method for moves oauth class

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
        self.moves_handler = movesHandler()
        self.requests_handler = requests_handler

    def _get_request(self, url, params):

        import requests

    # send request
        try:
            response = requests.get(url=url, params=params)
        except Exception as err:
            if self.requests_handler:
                return self.requests_handler(err)
            else:
                raise

    # handle response
        response_details = self.moves_handler.handle(response)

        return response_details

    def _post_request(self, url, params):

        import requests

    # send request
        try:
            response = requests.post(url=url, params=params)
        except Exception as err:
            if self.requests_handler:
                return self.requests_handler(err)
            else:
                raise

    # handle response
        response_details = self.moves_handler.handle(response)

        return response_details

    def generate_url(self, device_type, redirect_uri, service_scope, state_value=''):

        '''
            a method to generate the oauth2 authorization url for client to moves api

        :param device_type: string with type of device receiving authorization url
        :param redirect_uri: string with redirect uri registered with moves
        :param service_scope: dictionary with service type permissions
        :param state_value: [optional] string with unique url-safe variable
        :return: string with authorization url
        '''

        title = '%s.generate_url' % self.__class__.__name__

    # validate inputs
        input_args = {
            'device_type': device_type,
            'redirect_uri': redirect_uri,
            'service_scope': service_scope,
            'state_value': state_value
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, value)
                self.fields.validate(value, '.%s' % key, object_title)

    # determine base url for device type
        url_string = self.fields.schema['oauth_endpoint'][device_type]

    # construct query parameters
        query_params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': ''
        }
        for item in service_scope:
            if query_params['scope']:
                query_params['scope'] += ' '
            query_params['scope'] += item
        if device_type == 'web':
            query_params['response_type'] = 'code'
        if state_value:
            query_params['state'] = state_value

    # encode query parameters
        from urllib.parse import urlencode
        url_string += '/authorize?%s' % urlencode(query_params)

        return url_string

    def get_token(self, access_code, redirect_uri):

        '''
            a method to get an access token from moves api

        :param access_code: string with authentication code received from client
        :param redirect_uri: string with redirect uri registered with moves
        :return: dictionary with token details

        {
            'content': {
                "access_token": "1j0v33o6c5b34cVPqIiB_M2LYb_iM5S9Vcy7Rx7jA2630pK7HIjEXvJoiE8V5rRF",
                "token_type": "bearer",
                "expires_at": 1478559072,
                "refresh_token": "A27CSzZXKf2EPB45lvLQyT56sZ80dXNtp_lA7lvZ6UIKAy94GNvW9g9aGmJtbl28",
                "user_id": 23138311640030064
            }
        }
        '''

        title = '%s.get_token' % self.__class__.__name__

    # validate inputs
        input_args = {
            'access_code': access_code,
            'redirect_uri': redirect_uri
        }
        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, value)
                self.fields.validate(value, '.%s' % key, object_title)

    # construct url string
        url_string = '%s/access_token' % self.fields.schema['oauth_endpoint']['web']

    # construct request params
        request_params = {
            'grant_type': 'authorization_code',
            'code': access_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri
        }

    # send request
        from time import time
        current_time = time()
        token_details = self._post_request(url_string, params=request_params)

    # convert expiration info to epoch time
        details = token_details['content']
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
            'content': {
                "access_token": "1j0v33o6c5b34cVPqIiB_M2LYb_iM5S9Vcy7Rx7jA2630pK7HIjEXvJoiE8V5rRF",
                "token_type": "bearer",
                "expires_at": 1478559072,
                "refresh_token": "A27CSzZXKf2EPB45lvLQyT56sZ80dXNtp_lA7lvZ6UIKAy94GNvW9g9aGmJtbl28",
                "user_id": 23138311640030064
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
        url_string = '%s/access_token' % self.fields.schema['oauth_endpoint']['web']

    # construct request params
        request_params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        if service_scope:
            for item in service_scope:
                if request_params['scope']:
                    request_params['scope'] += ' '
                request_params['scope'] += item

    # send request
        from time import time
        current_time = time()
        token_details = self._post_request(url_string, params=request_params)

    # convert expiration info to epoch time
        details = token_details['content']
        if details:
            details['expires_at'] = int(current_time) + details['expires_in']
            del details['expires_in']

        return token_details

    def validate_token(self, access_token):

        '''
            a method to retrieve status of an access token with moves api

        :param access_token: string with access token value received from prior request
        :return: dictionary with status details

        {
            'content': {
                "client_id": "4j_HGYX1K166lC7Q83m5w0MYXYl45Aj6",
                "service_scope": [ 'activity' ],
                "expires_in": 4468335,
                "user_id": 23138311640030064
            }
        }
        '''

        title = '%s.validate_token' % self.__class__.__name__

    # validate inputs
        object_title = '%s(%s=%s)' % (title, 'access_token', access_token)
        self.fields.validate(access_token, '.token_details.access_token', object_title)

    # construct url string
        url_string = '%s/tokeninfo' % self.fields.schema['oauth_endpoint']['web']

    # construct request params
        request_params = {
            'access_token': access_token
        }

    # send request
        from time import time
        current_time = time()
        status_details = self._get_request(url_string, params=request_params)

    # convert expiration info to epoch time
        details = status_details['content']
        if details:
            details['expires_at'] = int(current_time) + details['expires_in']
            del details['expires_in']

    # convert service scope info to class format
            details['service_scope'] = details['scope'].split()
            del details['scope']

        return status_details

class movesClient(object):

    ''' a class of methods for retrieving user data from moves api'''

    # https://dev.moves-app.com/docs/api

    # TODO: incorporate ETags & LastModified headers

    _class_fields = {
        'schema': {
            'api_endpoint': 'https://api.moves-app.com/api/1.1',
            'access_token': 'I6oW3Jd53enK2bQhlQ36o92rgb_tUZtZsClFggwqsrejLyCIB4ihj6A7ewz_m0r0',
            'service_scope': ['location'],
            'start': 1478638948.310107,
            'end': 1478638949.310107,
            'first_date': '20160101',
            'timezone_offset': -180000,
        },
        '.service_scope': {
            'unique_values': True,
            'max_size': 2
        },
        '.service_scope[0]': {
            'discrete_values': ['location', 'activity']
        },
        '.first_date': {
            'must_contain': [ '\d{8}' ]
        },
        '.timezone_offset': {
            'integer_data': True
        }
    }

    def __init__(self, access_token, service_scope, usage_client=None, requests_handler=None):

        '''
            initialization method for moves client class

        :param access_token: string with access token for user provided by moves oauth
        :param service_scope: dictionary with service type permissions
        :param usage_client: callable that records usage data
        :param requests_handler: callable that handles requests errors
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct client attributes
        object_title = '%s.__init__(access_token=%s)' % (self.__class__.__name__, str(access_token))
        self.access_token = self.fields.validate(access_token, '.access_token', object_title)
        object_title = '%s.__init__(service_scope=[...])' % self.__class__.__name__
        self.service_scope = self.fields.validate(service_scope, '.service_scope', object_title)
        self.url = self.fields.schema['api_endpoint']

    # construct handlers
        self.moves_handler = movesHandler(usage_client)
        self.requests_handler = requests_handler

    def _get_request(self, url, headers=None, params=None):

        import requests

    # construct headers
        header_fields = {'Authorization': 'Bearer %s' % self.access_token}
        if headers:
            header_fields.update(headers)
        parameter_fields = {}
        if params:
            parameter_fields.update(params)

    # send request
        try:
            response = requests.get(url=url, headers=header_fields, params=parameter_fields)
        except Exception as err:
            if self.requests_handler:
                return self.requests_handler(err)
            else:
                raise

    # handle response
        response_details = self.moves_handler.handle(response)

        return response_details

    def _convert_dt(self, dt, timezone_offset):
        from datetime import datetime
        time_stamp = dt + timezone_offset
        calender_date = datetime.utcfromtimestamp(time_stamp).isoformat().replace('-','')[0:8]
        return calender_date

    def _process_dates(self, timezone_offset, first_date, start, end, title, track_points=False):

        ''' a helper method to process datetime information for other requests

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: float with starting datetime for daily summaries
        :param end: float with ending datetime for daily summaries
        :param title: string with request method name
        :param track_points: [optional] boolean to provide detailed tracking of user movement
        :return: dictionary of parameters to add to request
        '''

    # validate inputs
        input_fields = {
            'timezone_offset': timezone_offset,
            'first_date': first_date,
            'start': start,
            'end': end
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # validate datetimes
        max_time = 30 * 24 * 60 * 60 + 1
        max_days = '31'
        if track_points:
            max_days = '7'
            max_time = 6 * 24 * 60 * 60 + 1
        from time import time
        end_ISO = ''
        start_ISO = ''
        if end:
            if end > time():
                raise ValueError('%s(end=%s) datetime must not be in the future.' % (title, end))
            end_ISO = self._convert_dt(end, timezone_offset)
        if start:
            start_ISO = self._convert_dt(start, timezone_offset)
            if start_ISO < first_date:
                raise ValueError("%s(start=%s) datetime must not precede user signup first date." % (title, start))
        if start and end:
            if start > end:
                raise ValueError('%s(start=%s) must be a datetime before end=%s.' % (title, start, end))
            if end - start > max_time:
                raise ValueError('%s(start=%s, end=%s) must not be more than %s days apart.' % (title, start, end, max_days))

    # construct request parameters
        request_parameters = {}
        if not start_ISO and not end_ISO:
            request_parameters['pastDays'] = max_days
        else:
            if start_ISO and not end_ISO:
                end_dt = start + max_time
                current_ISO = self._convert_dt(time(), timezone_offset)
                end_ISO = self._convert_dt(end_dt, timezone_offset)
                if current_ISO < end_ISO:
                    end_ISO = current_ISO
            elif end_ISO and not start_ISO:
                start_dt = end - max_time
                start_ISO = self._convert_dt(start_dt, timezone_offset)
                if start_ISO < first_date:
                    start_ISO = first_date
            request_parameters['from'] = start_ISO
            request_parameters['to'] = end_ISO

        return request_parameters

    def list_activities(self):

        ''' a method to retrieve the details for all activities currently supported

        :return: list of dictionaries with activities details

        {
            'content': [
                {
                    "activity": "aerobics",
                    "geo": false,
                    "place": true,
                    "color": "bc4fff",
                    "units": "duration,calories"
                },
                ...
            ]
        }
        '''

        title = '%s.list_activities' % self.__class__.__name__

    # construct request parameters
        url_string = '%s/activities' % self.url

    # send request
        activities_list = self._get_request(url_string)

        return activities_list

    def get_profile(self):

        ''' a method to retrieve profile details of user

        :return: dictionary with profile details

        {
            'content': {
                "userId": 23138311640030064,
                "profile": {
                    "firstDate": "20121211",
                    "currentTimeZone": {
                        "id": "Europe/Helsinki",
                        "offset": 10800
                    },
                    "localization": {
                        "language": "en",
                        "locale": "fi_FI",
                        "firstWeekDay": 2,
                        "metric": true
                    },
                    "caloriesAvailable": true,
                    "platform": "ios"
                }
            }
        }
        '''

        title = '%s.get_profile' % self.__class__.__name__

    # construct request parameters
        url_string = '%s/user/profile' % self.url

    # send request
        profile_details = self._get_request(url_string)

        return profile_details

    def get_summary(self, timezone_offset, first_date, start=0.0, end=0.0):

        ''' a method to retrieve summary details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :return: dictionary with list of daily summary dictionaries inside content key

         { 'content':  [ SEE RESPONSE in https://dev.moves-app.com/docs/api_summaries ] }
        '''

        title = '%s.get_summary' % self.__class__.__name__

    # validate scope
        if 'activity' not in self.service_scope:
            raise ValueError('%s requires service scope to contain "activity".' % title)

    # construct request fields
        url_string = '%s/user/summary/daily' % self.url
        parameters = self._process_dates(timezone_offset, first_date, start, end, title)

    # send request
        summary_details = self._get_request(url_string, params=parameters)

        return summary_details

    def get_activities(self, timezone_offset, first_date, start=0.0, end=0.0):

        ''' a method to retrieve activity details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :return: dictionary with list of daily activities dictionaries inside content key

        { 'content':  [ SEE RESPONSE in https://dev.moves-app.com/docs/api_activities ] }

        '''

        title = '%s.get_activities' % self.__class__.__name__

    # validate scope
        if 'activity' not in self.service_scope:
            raise ValueError('%s requires service scope to contain "activity".' % title)

    # construct request fields
        url_string = '%s/user/activities/daily' % self.url
        parameters = self._process_dates(timezone_offset, first_date, start, end, title)

    # send request
        activities_details = self._get_request(url_string, params=parameters)

        return activities_details

    def get_places(self, timezone_offset, first_date, start=0.0, end=0.0):

        ''' a method to retrieve place details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :return: dictionary with list of daily places dictionaries inside content key

        { 'content':  [ SEE RESPONSE in https://dev.moves-app.com/docs/api_places ] }
        '''

        title = '%s.get_places' % self.__class__.__name__

    # validate scope
        if 'location' not in self.service_scope:
            raise ValueError('%s requires service scope to contain "location".' % title)

    # construct request fields
        url_string = '%s/user/places/daily' % self.url
        parameters = self._process_dates(timezone_offset, first_date, start, end, title)

    # send request
        places_details = self._get_request(url_string, params=parameters)

        return places_details

    def get_storyline(self, timezone_offset, first_date, start=0.0, end=0.0, track_points=False):

        ''' a method to retrieve storyline details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        NOTE: if track_points=True, start and end must be no more than 6 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :param track_points: [optional] boolean to provide detailed tracking of user movement
        :return: dictionary with list of daily places dictionaries inside content key

        { 'content':  [ SEE RESPONSE in https://dev.moves-app.com/docs/api_storyline ] }
        '''

        title = '%s.get_storyline' % self.__class__.__name__

    # validate scope
        if {'location', 'activity'} - set(self.service_scope):
            raise ValueError('%s requires service scope to contain "location" and "activity".' % title)

    # construct request fields
        url_string = '%s/user/storyline/daily' % self.url
        parameters = self._process_dates(timezone_offset, first_date, start, end, title, track_points)
        if track_points:
            parameters['trackPoints'] = 'true'

    # send request
        storyline_details = self._get_request(url_string, params=parameters)

        return storyline_details



