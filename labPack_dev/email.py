__author__ = 'rcj1492'
__created__ = '2015'

'''
Mandrill
https://mandrillapp.com/api/docs/index.python.html
pip install mandrill

Kickbox
http://docs.kickbox.io/
email verification

'''

from timeit import default_timer as timer
from jsonmodel.validators import jsonModel

import mandrill

class MandrillConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to Mandrill API with %s request.' % message
        super(MandrillConnectionError, self).__init__(text)
        self.errors = errors

class mandrillAPI(object):

    __name__ = 'Mandrill API'

    def __init__(self, mandrill_credentials):

        '''
            a method to initialize mandrill API class

        :param mandrill_credentials: dictionary with appKey
        :return: mandrillAPI
        '''

        sample_cred = {
            'schema': {
                'appKey': 'abcdef1456790xyz',
                'fromEmail': 'no-reply@collectiveacuity.com',
                'fromName': 'Collective Acuity',
                'bccEmail': '',
                'throttle': {}
            }
        }
        jsonModel(sample_cred).validate(mandrill_credentials)
        self.key = mandrill_credentials['appKey']
        self.client = mandrill.Mandrill(self.key)
        self.accountName = mandrill_credentials['fromName']
        self.replyTo = mandrill_credentials['fromEmail']
        self.bcc = ''
        if 'bccEmail' in mandrill_credentials.keys():
            self.bcc = mandrill_credentials['bccEmail']

    def send(self, user_email, user_name, email_subject, email_text, email_tags):

        '''
            sends an email Mandrill account to user
            returns the response from Mandrill API to email send request
            includes a performance test of API response time
        '''

    # construct message from inputs
        message = {
            'from_email': self.replyTo,
            'from_name': self.accountName,
            'headers': {
                'Reply-To': self.replyTo
            },
            'subject': email_subject,
            'text': email_text,
            'tags': email_tags, # emailTags must be an array
            'to': [{
                'email': user_email,
                'name': user_name,
                'type': 'to'
            }],
            'track_opens': True,
            # 'track_clicks': True # creates really weird looking links
        }
        if self.bcc:
            message['bcc_address'] = self.bcc

    # construct keyword arguments in request
        kw_args = {
            'message': message,
            'async': False,
            'ip_pool': 'Main Pool',
        }
        # send_time = (t1 - timedelta(days=1)).isoformat() + 'Z'
        # kw_args['send_at'] = send_time # requires a balance to schedule future emails

    # send email request to API
        try:
            t1 = timer()
            response = self.client.messages.send(**kw_args)
            print('Email Sent')
            t2 = timer()
            print(self.__name__ + ': ' + format((t2 - t1), '.5f') + ' seconds')
        except:
            raise MandrillConnectionError('%s.send(%s)' % (self.__name__, message))

        return response

