__author__ = 'rcj1492'
__created__ = '2016.02'

from datetime import datetime
from cred.credentialsMandrill import mandrillCredentials
from dev.email import mandrillAPI, MandrillConnectionError

class mandrillAPITests(mandrillAPI):

    def __init__(self, mandrill_credentials):
        mandrillAPI.__init__(self, mandrill_credentials)

    def unitTests(self):
        time_stamp = datetime.utcnow().isoformat()
        test_email = {
            'user_email': 'collectiveacuity@gmail.com',
            'user_name': 'Collective Acuity',
            'email_subject': '[Activation] High Frequency Events',
            'email_text': 'Restful python script activated for High Frequency Events at %sZ' % time_stamp,
            'email_tags': ['QA','Development','ActivationTime','HFE']
        }
        self.send(**test_email)

client = mandrillAPITests(mandrillCredentials)
client.unitTests()
