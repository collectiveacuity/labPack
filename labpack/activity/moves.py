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

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct client attributes
        self.clientID = self.fields.validate(client_id, '.client_id')
        self.clientSecret = self.fields.validate(client_secret, '.client_secret')

    def generate_url(self, device_type, redirect_uri, service_scope, state_value=''):

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
            'client_id': self.clientID,
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
            'client_id': self.clientID,
            'client_secret': self.clientSecret,
            'redirect_uri': redirect_uri
        }

    # send request
        import requests
        response = requests.post(url_string, params=request_params)
        if response.status_code == 200:
            token_details = response.json()
        elif response.status_code == 400:
            raise MovesError(error_dict=response.json())
        else:
            raise Exception('%s returned status code %s' % (title, response.status_code))

        return token_details

    def renew_token(self, refresh_token, service_scope=None):

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
            'client_id': self.clientID,
            'client_secret': self.clientSecret
        }
        if service_scope:
            for item in service_scope:
                if request_params['scope']:
                    request_params['scope'] += ' '
                request_params['scope'] += item

    # send request
        import requests
        response = requests.post(url_string, params=request_params)
        if response.status_code == 200:
            token_details = response.json()
        elif response.status_code == 400:
            raise MovesError(error_dict=response.json())
        else:
            raise Exception('%s returned status code %s' % (title, response.status_code))

        return token_details

    def validate_token(self, access_token):

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
        response = requests.get(url_string, params=request_params)
        if response.status_code == 200:
            token_status = response.json()
        elif response.status_code == 404:
            raise MovesError(error_dict=response.json())
        else:
            raise Exception('%s returned status code %s' % (title, response.status_code))

        return token_status

class movesClient(object):

    _class_fields = {
        'oauth_endpoint': {
            'web': 'https://api.moves-app.com/oauth/v1',
            'mobile': 'moves://app'
        }
    }
    _method_fields = {}

    def __init__(self):
        pass

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    moves_cred = load_settings('../../../cred/moves.yaml')
    client_id = moves_cred['oauth_client_id']
    client_secret = moves_cred['oauth_client_secret']
    redirect_uri = moves_cred['oauth_redirect_url']
    moves_oauth = movesOAuth(client_id, client_secret)
    auth_url = moves_oauth.generate_url('web', redirect_uri, ['location', 'activity'])
    assert auth_url.find('code') > 0

