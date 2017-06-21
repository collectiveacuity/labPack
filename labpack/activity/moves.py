__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

# TODO: incorporate rate limiting logic
class movesHandler(object):

    ''' handles responses from moves api and usage data '''

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
            'method': response.request.method,
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers
        }

    # handle different codes
        if details['code'] == 200:
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()

        return details

# TODO: use webscraper to interact with registration
class movesRegister(object):
    ''' currently must be done manually '''
    ''' https://dev.moves-app.com/ '''
    def __init__(self):
        pass

# TODO: incorporate ETags & LastModified headers
class movesClient(object):

    ''' a class of methods for retrieving user data from moves api'''

    # use labpack.authentication.oauth2.oauth2Client to obtain access token
    # https://dev.moves-app.com/docs/api

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

        ''' initialization method for moves client class

        :param access_token: string with access token for user provided by moves oauth
        :param service_scope: dictionary with service type permissions
        :param usage_client: callable that records usage data
        :param requests_handler: callable that handles requests errors
        '''
        
        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct client attributes
        object_title = '%s(access_token=%s)' % (title, str(access_token))
        self.access_token = self.fields.validate(access_token, '.access_token', object_title)
        object_title = '%s(service_scope=[...])' % title
        self.service_scope = self.fields.validate(service_scope, '.service_scope', object_title)
        self.endpoint = self.fields.schema['api_endpoint']

    # construct handlers
        self.moves_handler = movesHandler(usage_client)
        self.requests_handler = requests_handler

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

        :return: dictionary of response details with activities list inside json key

         {
            'headers': { ... },
            'code': 200,
            'error': '',
            'url': 'https://api.moves-app.com/api/1.1/activities'
            'json': [
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
        url_string = '%s/activities' % self.endpoint

    # send request
        response_details = self._get_request(url_string)

        return response_details

    def get_profile(self):

        ''' a method to retrieve profile details of user

        :return: dictionary of response details with profile details inside json key

         {
            'headers': { ... },
            'code': 200,
            'error': '',
            'url': 'https://api.moves-app.com/api/1.1/user/profile'
            'json': {
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
        url_string = '%s/user/profile' % self.endpoint

    # send request
        response_details = self._get_request(url_string)

        return response_details

    def get_summary(self, timezone_offset, first_date, start=0.0, end=0.0):

        ''' a method to retrieve summary details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :return: dictionary of response details with summary list inside json key

         {
            'headers': { ... },
            'code': 200,
            'error': '',
            'url': 'https://api.moves-app.com/api/1.1/user/summary/daily'
            'json': [ SEE RESPONSE in https://dev.moves-app.com/docs/api_summaries ]
        }
        '''

        title = '%s.get_summary' % self.__class__.__name__

    # validate scope
        if 'activity' not in self.service_scope:
            raise ValueError('%s requires service scope to contain "activity".' % title)

    # construct request fields
        url_string = '%s/user/summary/daily' % self.endpoint
        parameters = self._process_dates(timezone_offset, first_date, start, end, title)

    # send request
        response_details = self._get_request(url_string, params=parameters)

        return response_details

    def get_activities(self, timezone_offset, first_date, start=0.0, end=0.0):

        ''' a method to retrieve activity details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :return: dictionary of response details with user activities list inside json key

         {
            'headers': { ... },
            'code': 200,
            'error': '',
            'url': 'https://api.moves-app.com/api/1.1/user/activities/daily'
            'json': [ SEE RESPONSE in https://dev.moves-app.com/docs/api_activities ]
        }
        '''

        title = '%s.get_activities' % self.__class__.__name__

    # validate scope
        if 'activity' not in self.service_scope:
            raise ValueError('%s requires service scope to contain "activity".' % title)

    # construct request fields
        url_string = '%s/user/activities/daily' % self.endpoint
        parameters = self._process_dates(timezone_offset, first_date, start, end, title)

    # send request
        response_details = self._get_request(url_string, params=parameters)

        return response_details

    def get_places(self, timezone_offset, first_date, start=0.0, end=0.0):

        ''' a method to retrieve place details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :return: dictionary of response details with places list inside json key

         {
            'headers': { ... },
            'code': 200,
            'error': '',
            'url': 'https://api.moves-app.com/api/1.1/user/places/daily'
            'json': [ SEE RESPONSE in https://dev.moves-app.com/docs/api_places ]
        }
        '''

        title = '%s.get_places' % self.__class__.__name__

    # validate scope
        if 'location' not in self.service_scope:
            raise ValueError('%s requires service scope to contain "location".' % title)

    # construct request fields
        url_string = '%s/user/places/daily' % self.endpoint
        parameters = self._process_dates(timezone_offset, first_date, start, end, title)

    # send request
        response_details = self._get_request(url_string, params=parameters)

        return response_details

    def get_storyline(self, timezone_offset, first_date, start=0.0, end=0.0, track_points=False):

        ''' a method to retrieve storyline details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        NOTE: if track_points=True, start and end must be no more than 6 days, 1 second apart

        :param timezone_offset: integer with timezone offset from user profile details
        :param first_date: string with ISO date from user profile details firstDate
        :param start: [optional] float with starting datetime for daily summaries
        :param end: [optional] float with ending datetime for daily summaries
        :param track_points: [optional] boolean to provide detailed tracking of user movement
        :return: dictionary of response details with storyline list inside json key

         {
            'headers': { ... },
            'code': 200,
            'error': '',
            'url': 'https://api.moves-app.com/api/1.1/user/storyline/daily'
            'json': [ SEE RESPONSE in https://dev.moves-app.com/docs/api_storyline ]
        }
        '''

        title = '%s.get_storyline' % self.__class__.__name__

    # validate scope
        if {'location', 'activity'} - set(self.service_scope):
            raise ValueError('%s requires service scope to contain "location" and "activity".' % title)

    # construct request fields
        url_string = '%s/user/storyline/daily' % self.endpoint
        parameters = self._process_dates(timezone_offset, first_date, start, end, title, track_points)
        if track_points:
            parameters['trackPoints'] = 'true'

    # send request
        storyline_details = self._get_request(url_string, params=parameters)

        return storyline_details
