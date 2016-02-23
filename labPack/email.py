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

class mandrillAPI(object):

    def __init__(self, mandrill_credentials):

        '''
            a method to initialize mandrill API class

        :param mandrill_credentials: dictionary with appKey
        :return: mandrillAPI
        '''

        sample_cred = {
            'schema': {
                'appKey': 'abcdef1456790xyz',
                'throttle': {}
            }
        }
        jsonModel(sample_cred).validate(mandrill_credentials)
        self.appKey = mandrill_credentials['appKey']

    def send(self, user_email, user_name, email_subject, email_text, email_tags):

        '''
            sends an email through Collective Acuity Mandrill account to user
            returns the response from Mandrill API to email send request
            includes a performance test of API response time
            dependencies:
            import mandrill
            from datetime import datetime
        '''
        urlTitle = 'Mandrill API'
        mandrill_client = mandrill.Mandrill(mandrill_key)
        message = {
            'from_email': 'no-reply@collectiveacuity.com',
            'from_name': 'High Frequency Events',
            'bcc_address': 'collectiveacuity@gmail.com',
            'headers': {
                'Reply-To': 'no-reply@collectiveacuity.com'
            },
            'subject': emailSubject,
            'text': emailText,
            'tags': emailTags, # emailTags must be an array
            'to': [{
                'email': userEmail,
                'name': userName,
                'type': 'to'
            }],
            'track_opens': True,
            # 'track_clicks': True # creates really weird looking links
        }
        # sendTime = (t1 - timedelta(days=1)).isoformat() + 'Z'
        t1 = timer()
        response = mandrill_client.messages.send(
            message=message,
            async=False,
            ip_pool='Main Pool',
            # send_at=sendTime # requires a balance to schedule future emails
        )
        print('Email Sent')
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return response


