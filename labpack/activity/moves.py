__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

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
            'client_id': '',
            'client_secret': '',
            'device_type': '',
            'redirect_url': '',
            'service_scope': [ 'location' ],
            'state_value': ''
        },
        'components': {
            '.device_type': {
                'discrete_values': [ 'web', 'mobile' ]
            },
            '.redirect_url': {
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

    def generate_url(self, device_type, redirect_url, service_scope, state_value=''):

        title = '%s.generate_url' % self.__class__.__name__

    # validate inputs
        input_args = {
            'device_type': device_type,
            'redirect_url': redirect_url,
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
            'redirect_url': redirect_url,
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

    def get_token(self, access_code):
        token_details = {}
        return token_details

    def renew_token(self, access_token):
        token_details = {}
        return token_details

    def check_token(self):
        token_details = {}
        return token_details

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
    redirect_url = moves_cred['oauth_redirect_url']
    moves_oauth = movesOAuth(client_id, client_secret)
    auth_url = moves_oauth.generate_url('web', redirect_url, ['location', 'activity'])
    assert auth_url.find('code') > 1

