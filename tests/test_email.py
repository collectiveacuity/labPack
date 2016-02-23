__author__ = 'rcj1492'
__created__ = '2016.02'

from cred.credentialsMandrill import mandrillKey
from labPack.email import sendEmailFromHFEMandrill
from datetime import datetime

assert sendEmailFromHFEMandrill(
    mandrillKey,
    userEmail='collectiveacuity@gmail.com',
    userName='Collective Acuity',
    emailSubject='[Activation] High Frequency Events',
    emailText='Restful python script activated for High Frequency Events at ' \
              + datetime.utcnow().isoformat() + 'Z',
    emailTags=['QA','Development','ActivationTime','HFE']
    )