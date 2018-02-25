__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'

class oauth2Client(object):

    _class_fields = {
        'schema': {
            'client_id': 'kvdjmcsiarzqndpqouejzvgqakizlyqy',
            'client_secret': 'p-EWtuOG3kdMXzwv0HR94pyZEIvYBVS1frm8h29f3U83fuwM',
            'auth_endpoint': 'https://secure.meetup.com/oauth2/authorize',
            'token_endpoint': 'https://secure.meetup.com/oauth2/access',
            'status_endpoint': 'https://api.moves-app.com/oauth/v1/tokeninfo',
            'redirect_uri': 'https://myoauth2endpoint.mydomain.com/authorize/servicename',
            'request_mimetype': '',
            'error_map': {},
            'requests_handler': 'labpack.handlers.requests.handle_requests',
            'device_type': 'web',
            'service_scope': ['ageless'],
            'additional_fields': {},
            'state_value': 'xCOZIVMyAPdXblu_b-Bb99QYAoeumIyULAci',
            'auth_code': 'HF8AeprpNlByLiya9QgzcHsmkyMf1TvuNrMD0p6fxeIlOCWq',
            'refresh_token': 'BPb0b0zTEG0TU8YE5_xDGICUpaaa8RKy3HPVBMSEZQpoMkch',
            'access_token': ''
        },
        'components': {
            '.device_type': {
                'discrete_values': ['web', 'mobile']
            },
            '.redirect_uri': {
                'must_contain': ['^https?://']
            },
            '.auth_endpoint': {
                'must_contain': ['^https://']
            },
            '.token_endpoint': {
                'must_contain': ['^https://']
            },
            '.service_scope': {
                'unique_values': True
            },
            '.request_mimetype': {
                'discrete_values': [ 'application/json', 'application/x-www-form-urlencoded' ]
            },
            '.state_value': {
                'max_length': 63
            }
        }
    }

    _class_objects = {
        'token': {
            'schema': {
                'access_token': '',
                'token_type': '',
                'expires_at': 0,
                'refresh_token': ''
            }
        },
        'auth_errors': {
            'schema': {
                'invalid_request': 'The request is missing a required parameter, includes an invalid parameter value, includes a parameter more than once, or is otherwise malformed.',
                'unauthorized_client': 'The client is not authorized to request an authorization code using this method.',
                'access_denied': 'The resource owner or authorization server denied the request.',
                'unsupported_response_type': 'The authorization server does not support obtaining an authorization code using this method.',
                'invalid_scope': 'The requested scope is invalid, unknown, or malformed.',
                'server_error': 'The authorization server encountered an unexpected condition that prevented it from fulfilling the request.',
                'temporarily_unavailable': 'The authorization server is currently unable to handle the request due to a temporary overloading or maintenance of the server.'
            }
        },
        'token_errors': {
            'schema': {
                '400': 'Bad input parameter. The response body is a plaintext message with more information.',
                '401': 'Bad or expired token. This can happen if the access token is expired or if the access token has been revoked. To fix this, you should re-authenticate the user.',
                '429': 'Your app is making too many requests for the given user or team and is being rate limited. Your app should wait for the number of seconds specified in the "Retry-After" response header before trying again. The Content-Type of the response can be JSON or plaintext.'
            }
        }
    }

    def __init__(self, client_id, client_secret, auth_endpoint, token_endpoint, redirect_uri, request_mimetype='', status_endpoint='', requests_handler=None, error_map=None):

        ''' the initialization method for oauth2 client class

        :param client_id: string with client id registered for app with service
        :param client_secret: string with client secret registered for app with service
        :param auth_endpoint: string with service endpoint for authorization code requests
        :param token_endpoint: string with service endpoint for token post requests
        :param redirect_uri: string with url for redirect callback registered with service
        :param request_mimetype: [optional] string with mimetype for token post requests
        :param status_endpoint: [optional] string with service endpoint to retrieve status of token
        :param requests_handler: [optional] callable that handles requests errors
        :param error_map: [optional] dictionary with key value strings for service error msgs
        '''

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct class object models
        object_models = {}
        for key, value in self._class_objects.items():
            object_models[key] = jsonModel(value)
        from labpack.compilers.objects import _method_constructor
        self.objects = _method_constructor(object_models)

    # validate inputs
        input_fields = {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_endpoint': auth_endpoint,
            'token_endpoint': token_endpoint,
            'redirect_uri': redirect_uri,
            'request_mimetype': request_mimetype,
            'status_endpoint': status_endpoint,
            'error_map': error_map
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct class properties
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.redirect_uri = redirect_uri
        self.request_mimetype = request_mimetype
        self.status_endpoint = status_endpoint

    # construct handlers
        self.requests_handler = requests_handler
        self.error_map = error_map

    def _ingest_response(self, response):

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
        if details['code'] in (200, 201, 202):
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()
            if self.error_map:
                import re
                for key, value in self.error_map.items():
                    error_pat = re.compile(key)
                    if error_pat.findall(details['error']):
                        details['error'] = value
                        break
            else:
                for key, value in self.objects.token_errors.schema.items():
                    if int(key) == details['code']:
                        details['error'] = value
                        break

        return details

    def _post_request(self, url, headers=None, params=None, data=None, json=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url
        }
        if headers:
            request_kwargs['headers'] = headers
        if params:
            request_kwargs['params'] = params
        if data:
            request_kwargs['data'] = data
        if json:
            request_kwargs['json'] = json

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
        response_details = self._ingest_response(response)

        return response_details

    def generate_url(self, service_scope=None, state_value='', additional_fields=None):

        ''' a method to generate an authorization url to oauth2 service for client

        :param service_scope: [optional] list with scope of permissions for agent
        :param state_value: [optional] string with unique identifier for callback
        :param additional_fields: [optional] dictionary with key value strings for service
        :return: string with authorization url
        '''

        title = '%s.generate_url' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'state_value': state_value,
            'service_scope': service_scope,
            'additional_fields': additional_fields
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate additional fields
        if additional_fields:
            for key, value in additional_fields.items():
                if not isinstance(value, str):
                    raise TypeError("%s(additional_fields={'%s':'...'}) must be a string datatype." % (title, key))

    # construct query parameters
        query_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        if state_value:
            query_params['state'] = state_value
        if service_scope:
            for item in service_scope:
                if 'scope' not in query_params.keys():
                    query_params['scope'] = ''
                if query_params['scope']:
                    query_params['scope'] += ' '
                query_params['scope'] += item
        if additional_fields:
            query_params.update(**additional_fields)

    # encode query parameters
        from urllib.parse import urlencode
        url_string = '%s?%s' % (self.auth_endpoint, urlencode(query_params))

        return url_string

    def get_token(self, auth_code):

        ''' a method to retrieve an access token from an oauth2 authorizing party

        :param auth_code: string with code provided by client redirect
        :return: dictionary with access token details inside [json] key

        token_details = self.objects.token.schema
        '''

        title = '%s.get_token' % self.__class__.__name__

    # validate inputs
        input_args = {
            'auth_code': auth_code
        }

        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, value)
                self.fields.validate(value, '.%s' % key, object_title)

    # construct base url
        request_kwargs = {
            'url': self.token_endpoint
        }

    # construct token fields
        token_fields = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
        }

    # construct request params
        if self.request_mimetype == 'application/x-www-form-urlencoded':
            request_kwargs['data'] = token_fields
        elif self.request_mimetype == 'application/json':
            request_kwargs['json'] = token_fields
        else:
            request_kwargs['params'] = token_fields

    # send request
        from time import time
        current_time = time()
        token_details = self._post_request(**request_kwargs)

    # convert expiration info to epoch timestamp
        details = token_details['json']
        if details:
            details['expires_at'] = 0
            if 'expires_in' in details.keys():
                details['expires_at'] = int(current_time) + int(details['expires_in'])
                del details['expires_in']

        return token_details

    def renew_token(self, refresh_token):

        ''' a method to renew an access token from an oauth2 authorizing party

        :param auth_code: string with refresh token provided by service with access token
        :return: dictionary with access token details inside [json] key

        token_details = self.objects.token.schema
        '''

        title = '%s.renew_token' % self.__class__.__name__

    # validate inputs
        input_args = {
            'refresh_token': refresh_token
        }

        for key, value in input_args.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, value)
                self.fields.validate(value, '.%s' % key, object_title)

    # construct base url
        request_kwargs = {
            'url': self.token_endpoint
        }

    # construct token fields
        token_fields = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

    # construct request params
        if self.request_mimetype == 'application/x-www-form-urlencoded':
            request_kwargs['data'] = token_fields
        elif self.request_mimetype == 'application/json':
            request_kwargs['json'] = token_fields
        else:
            request_kwargs['params'] = token_fields

    # send request
        from time import time
        current_time = time()
        token_details = self._post_request(**request_kwargs)

    # convert expiration info to epoch timestamp
        details = token_details['json']
        details['expires_at'] = 0
        if details:
            if 'expires_in' in details.keys():
                details['expires_at'] = int(current_time) + int(details['expires_in'])
                del details['expires_in']

        return token_details

if __name__ == '__main__':
    from labpack.storage.appdata import appdataClient
    from labpack.records.settings import load_settings
    from labpack.randomization.randomlab import random_characters
    from string import ascii_lowercase
    config_paths = [
        '../../../cred/dropbox.yaml',
        '../../../cred/moves.yaml',
        '../../../cred/meetup.yaml'
    ]
    for path in config_paths:
        oauth2_config = load_settings(path)
        oauth2_kwargs = {
            'client_id': oauth2_config['oauth_client_id'],
            'client_secret': oauth2_config['oauth_client_secret'],
            'auth_endpoint': oauth2_config['oauth_auth_endpoint'],
            'token_endpoint': oauth2_config['oauth_token_endpoint'],
            'redirect_uri': oauth2_config['oauth_redirect_uri'],
            'request_mimetype': oauth2_config['oauth_request_mimetype']
        }
        oauth2_client = oauth2Client(**oauth2_kwargs)
        url_kwargs = {
            'state_value': random_characters(ascii_lowercase, 48)
        }
        if oauth2_config['oauth_service_scope']:
            url_kwargs['service_scope'] = oauth2_config['oauth_service_scope'].split()
        auth_url = oauth2_client.generate_url(**url_kwargs)
    # retrieve access token
        service_name = oauth2_config['oauth_service_name']
        log_client = appdataClient(collection_name='Logs', prod_name='Fitzroy')
        path_filters = [{
            0: {'discrete_values': ['knowledge']},
            1: {'discrete_values': ['tokens']},
            2: {'discrete_values': [service_name]}}
        ]
        import yaml
        token_list = log_client.list(log_client.conditional_filter(path_filters), reverse_search=True)
        token_data = log_client.load(token_list[0])
        token_details = yaml.load(token_data.decode())
    # # test access token renewal
    #     new_details = oauth2_client.renew_token(token_details['refresh_token'])
    #     print(new_details['json'])
    #     token_details.update(**new_details['json'])
    #     new_key = 'knowledge/tokens/%s/%s/%s.yaml' % (service_name, token_details['user_id'], token_details['expires_at'])
    #     log_client.create(new_key, token_details)
        