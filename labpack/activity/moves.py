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

    def __init__(self, client_id, client_secret):

        '''
            initialization method for moves oauth class

        :param client_id: string with client id registered for app with moves api
        :param client_secret: string with client secret registered for app with moves api
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct client attributes
        self.client_id = self.fields.validate(client_id, '.client_id')
        self.client_secret = self.fields.validate(client_secret, '.client_secret')

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
        "access_token": "1j0v33o6c5b34cVPqIiB_M2LYb_iM5S9Vcy7Rx7jA2630pK7HIjEXvJoiE8V5rRF",
        "token_type": "bearer",
        "expires_at": 1478559072,
        "refresh_token": "A27CSzZXKf2EPB45lvLQyT56sZ80dXNtp_lA7lvZ6UIKAy94GNvW9g9aGmJtbl28",
        "user_id": 23138311640030064
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
        import requests
        from time import time
        from copy import deepcopy
        current_time = time()
        response = requests.post(url_string, params=request_params)
        if response.status_code == 200:
            token_details = response.json()
        elif response.status_code == 400:
            raise MovesError(error_dict=response.json())
        else:
            raise Exception('%s returned status code %s' % (title, response.status_code))

    # convert expiration info to epoch time
        token_details['expires_at'] = int(current_time) + deepcopy(token_details['expires_in'])
        del token_details['expires_in']

        return token_details

    def renew_token(self, refresh_token, service_scope=None):

        '''
            a method to renew an access token with moves api

        :param refresh_token: string with refresh token value received with prior token
        :param service_scope: dictionary with service type permissions
        :return: dictionary with token details

        {
        "access_token": "1j0v33o6c5b34cVPqIiB_M2LYb_iM5S9Vcy7Rx7jA2630pK7HIjEXvJoiE8V5rRF",
        "token_type": "bearer",
        "expires_at": 1478559072,
        "refresh_token": "A27CSzZXKf2EPB45lvLQyT56sZ80dXNtp_lA7lvZ6UIKAy94GNvW9g9aGmJtbl28",
        "user_id": 23138311640030064
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
        import requests
        from time import time
        current_time = time()
        response = requests.post(url_string, params=request_params)
        if response.status_code == 200:
            token_details = response.json()
        elif response.status_code == 400:
            raise MovesError(error_dict=response.json())
        else:
            raise Exception('%s returned status code %s' % (title, response.status_code))

    # convert expiration info to epoch time
        token_details['expires_at'] = int(current_time) + token_details['expires_in']
        del token_details['expires_in']

        return token_details

    def validate_token(self, access_token):

        '''
            a method to retrieve status of an access token with moves api

        :param access_token: string with access token value received from prior request
        :return: dictionary with status details

        {
        "client_id": "4j_HGYX1K166lC7Q83m5w0MYXYl45Aj6",
        "scope": "activity",
        "expires_in": 4468335,
        "user_id": 23138311640030064
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
        import requests
        from time import time
        current_time = time()
        response = requests.get(url_string, params=request_params)
        if response.status_code == 200:
            status_details = response.json()
        elif response.status_code == 404:
            raise MovesError(error_dict=response.json())
        else:
            raise Exception('%s returned status code %s' % (title, response.status_code))

    # convert expiration info to epoch time
        status_details['expires_at'] = int(current_time) + status_details['expires_in']
        del status_details['expires_in']

    # convert service scope info to class format
        status_details['service_scope'] = status_details['scope'].split()
        del status_details['scope']

        return status_details

class movesClient(object):

    _class_fields = {
        'schema': {
            'api_endpoint': 'https://api.moves-app.com/api/1.1',
            'access_token': 'I6oW3Jd53enK2bQhlQ36o92rgb_tUZtZsClFggwqsrejLyCIB4ihj6A7ewz_m0r0'
        }
    }

    def __init__(self, access_token):

        '''
            initialization method for moves client class

        :param access_token: string with access token for user provided by moves oauth
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct client attributes
        self.access_token = self.fields.validate(access_token, '.access_token')
        self.base_url = self.fields.schema['api_endpoint']

if __name__ == '__main__':
    config_path = '../../../cred/moves.yaml'
    token_path = '../../keys/moves-token.yaml'
    from labpack.records.settings import load_settings, save_settings
    moves_cred = load_settings(config_path)
    moves_token = load_settings(token_path)
    client_id = moves_cred['oauth_client_id']
    client_secret = moves_cred['oauth_client_secret']
    redirect_uri = moves_cred['oauth_redirect_url']
    moves_oauth = movesOAuth(client_id, client_secret)
    auth_url = moves_oauth.generate_url('web', redirect_uri, ['location', 'activity'])
    assert auth_url.find('code') > 0
    status_details = moves_oauth.validate_token(moves_token['access_token'])
    old_expiration = status_details['expires_at']
    token_details = moves_oauth.renew_token(moves_token['refresh_token'])
    new_token = { 'contact_id': moves_token['contact_id'] }
    new_token.update(token_details)
    print(new_token)
    save_settings(new_token, token_path, overwrite=True)
    status_details = moves_oauth.validate_token(new_token['access_token'])
    assert status_details['expires_at'] > old_expiration
    moves_client = movesClient(new_token['access_token'])


