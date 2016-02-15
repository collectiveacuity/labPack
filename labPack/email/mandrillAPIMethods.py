__author__ = 'rcj1492'
__created__ = '2015'

# dependencies for mandrill requests & performance tests
# https://mandrillapp.com/api/docs/index.python.html
# pip install mandrill

from datetime import datetime
from timeit import default_timer as timer

import mandrill

from cred.credentialsDataProcessor import *


def sendEmailFromHFEMandrill(mandrill_key, userEmail, userName, emailSubject, emailText, emailTags):
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
assert sendEmailFromHFEMandrill(
    mandrillKey,
    userEmail='collectiveacuity@gmail.com',
    userName='Collective Acuity',
    emailSubject='[Activation] High Frequency Events',
    emailText='Restful python script activated for High Frequency Events at ' \
              + datetime.utcnow().isoformat() + 'Z',
    emailTags=['QA','Development','ActivationTime','HFE']
    )

