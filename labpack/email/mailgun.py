__author__ = 'rcj1492'
__created__ = '2017.03'
__license__ = 'MIT'

''' 
PLEASE NOTE:    mailgun requires domain verification to send messages
                api uses postmaster@sub.domain.com as sender address
                make sure to add mx record under the mailgun subdomain

SETUP:          https://documentation.mailgun.com/quickstart-sending.html#how-to-verify-your-domain    
'''

# TODO: incorporate rate limiting logic
class mailgunHandler(object):

    ''' handles responses from mailgun api and usage data '''

    _class_fields = {
        'schema': {
            'rate_limits': [
                { 'requests': 100, 'period': 3600 },
                { 'requests': 10000, 'period': 30 * 24 * 3600 }
            ]
        }
    }

    def __init__(self, usage_client=None):

        '''
            initialization method for mailgun client class
            
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

    # 200	Everything worked as expected
    # 400	Bad Request - Often missing a required parameter
    # 401	Unauthorized - No valid API key provided
    # 402	Request Failed - Parameters were valid but request failed
    # 404	Not Found - The requested item doesn’t exist
    # 500, 502, 503, 504	Server Errors - something is wrong on Mailgun’s end

        return details

# TODO: use webscraper, domain api and aws api to interact with registration
class mailgunRegister(object):

    ''' currently must be done manually '''
    ''' https://app.mailgun.com/app/account/security '''
    ''' https://documentation.mailgun.com/api-domains.html#domains '''
    ''' https://documentation.mailgun.com/quickstart-sending.html#how-to-verify-your-domain '''

    def __init__(self):
        pass

class mailgunClient(object):

    ''' a class of methods for managing email with mailgun api '''

    # https://documentation.mailgun.com/api_reference.html

    _class_fields = {
        'schema': {
            'api_endpoint': 'https://api.mailgun.net/v3',
            'account_domain': 'collectiveacuity.com',
            'api_key': 'key-e05af44440df8acc78ca21c26680fcc1',
            'email_key': 'pubkey-ed63c920744999631abf67105ace5177',
            'email_address': 'no-reply@collectiveacuity.com',
            'recipient_list': [ 'support@collectiveacuity.com' ],
            'sender_email': 'no-reply@collectiveacuity.com',
            'sender_name': 'Collective Acuity',
            'email_subject': 'Test Mailgun API',
            'content_text': 'Great to see it works!',
            'content_html': '<p>Great to see it works!</p>',
            'tracking_tags': [ 'newsletter' ],
            'cc_list': [ 'support@collectiveacuity.com' ],
            'bcc_list': [ 'support@collectiveacuity.com' ],
            'delivery_time': 1490744726.6858199
        }
    }

    def __init__(self, api_key, email_key, account_domain, usage_client=None, requests_handler=None):

        ''' 
            initialization method for mailgun client class

        :param api_key: string with api key provided by mailgun
        :param email_key: string with email validation key provide by mailgun
        :param account_domain: string with domain from which to send email
        :param usage_client: callable that records usage data
        :param requests_handler: callable that handles requests errors
        '''

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'api_key': api_key,
            'email_key': email_key,
            'account_domain': account_domain
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct client properties
        self.api_endpoint = self.fields.schema['api_endpoint']
        self.account_domain = account_domain
        self.api_key = api_key
        self.email_key = email_key

    # construct handlers
        self.service_handler = mailgunHandler(usage_client)
        self.requests_handler = requests_handler

    def _get_request(self, url, params):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'auth': ('api', self.email_key ),
            'params': params
        }

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

    def _post_request(self, url, data):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'auth': ('api', self.api_key),
            'data': data
        }

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

    def send_email(self, recipient_list, sender_email, sender_name, email_subject, content_text='', content_html='', tracking_tags=None, cc_list=None, bcc_list=None, delivery_time=0.0):

        title = '%s.send_email' % __class__.__name__

    # validate inputs
        input_fields = {
            'recipient_list': recipient_list,
            'sender_email': sender_email,
            'sender_name': sender_name,
            'email_subject': email_subject,
            'content_text': content_text,
            'content_html': content_html,
            'tracking_tags': tracking_tags,
            'cc_list': cc_list,
            'bcc_list': bcc_list,
            'delivery_time': delivery_time
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request_kwargs
        request_kwargs = {
            'url': '%s/%s/messages' % (self.api_endpoint, self.account_domain),
            'data': {
                'to': recipient_list,
                'from': '%s <%s>' % (sender_name, sender_email),
                'h:X-Mailgun-Native-Send': True,
                # 'o:require-tls': True,
                'subject': email_subject
            }
        }

    # add content
        if content_text:
            request_kwargs['data']['text'] = content_text
        elif content_html:
            request_kwargs['data']['html'] = content_html
        else:
            raise IndexError('%s() requires either a content_text or content_html arg.' % title)

    # add optional fields
        if tracking_tags:
            request_kwargs['data']['o:tag'] = tracking_tags
        if cc_list:
            request_kwargs['data']['cc'] = cc_list
        if bcc_list:
            request_kwargs['data']['bcc'] = bcc_list
        if delivery_time:
            from time import time
            current_time = time()
            if delivery_time - current_time > 3 * 24 * 60 * 60:
                raise ValueError('%s(delivery_time=%s) may not be more than 3 days from now.' % (title, delivery_time))
            elif delivery_time - current_time > 0:
                from labpack.records.time import labDT
                js_time = labDT.fromEpoch(delivery_time).rfc2822()
                request_kwargs['data']['o:deliverytime'] = js_time

    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details

    def validate_email(self, email_address):

        '''
            a method to validate an email address
            
        :param email_address: string with email address to validate
        :return: dictionary with validation fields in response_details['json']
        '''

        title = '%s.validate_email' % __class__.__name__

    # validate inputs
        object_title = '%s(email_address="")' % title
        email_address = self.fields.validate(email_address, '.email_address', object_title)

    # construct request_kwargs
        request_kwargs = {
            'url': '%s/address/validate' % self.api_endpoint,
            'params': { 'address': email_address }
        }

    # send request
        response_details = self._get_request(**request_kwargs)

        return response_details

if __name__ == '__main__':

    from labpack.records.settings import load_settings
    mailgun_cred = load_settings('../../../cred/mailgun.yaml')

# construct client
    from labpack.handlers.requests import handle_requests
    mailgun_kwargs = {
        'api_key': mailgun_cred['mailgun_api_key'],
        'email_key': mailgun_cred['mailgun_email_key'],
        'account_domain': mailgun_cred['mailgun_spf_route'],
        'requests_handler': handle_requests
    }
    mailgun_client = mailgunClient(**mailgun_kwargs)

# test validation
    email_address = 'support@collectiveacuity.com'
    response_details = mailgun_client.validate_email(email_address)
    assert response_details['json']['is_valid']

# test send email
    from time import time
    send_kwargs = {
        'recipient_list': [ email_address ],
        'sender_email': 'no-reply@collectiveacuity.com',
        'sender_name': 'Collective Acuity',
        'email_subject': 'Test Mailgun API %s' % time(),
        'content_text': 'Great to see it works!',
        'delivery_time': time() + 5
    }
    response_details = mailgun_client.send_email(**send_kwargs)
    assert response_details['code'] == 200


