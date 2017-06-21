__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'

class dropboxHandler(object):

    ''' handles responses from dropbox api and usage data'''

    _class_fields = {
        'schema': {
            'rate_limits': []
        }
    }

    def __init__(self, usage_client=None):

        ''' initialization method for dropbox handler class

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
        if details['code'] in (200, 201, 202):
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()

        return details

class dropboxRegister(object):
    ''' currently must be done manually '''
    # https://www.dropbox.com/developers/apps
    def __init__(self, app_settings):
        pass

    def setup(self):
        return self

    def update(self):
        return self

class dropboxClient(object):

    ''' a class of methods to manage file storage on Dropbox API '''

    # https://www.dropbox.com/developers/documentation/http/documentation

    def __init__(self, access_token):
        pass

if __name__ == '__main__':
    pass

