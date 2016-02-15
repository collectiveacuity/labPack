__author__ = 'rcj1492'
__created__ = '2015'

# pip install twilio
# https://www.twilio.com/user/account/developer-tools/api-explorer/message-create

from timeit import default_timer as timer
import re

from twilio.rest import TwilioRestClient

from cred.credentialsDataProcessor import *


def sendSMSfromTrialTwilio(twilio_id, twilio_token, twilio_phone, phone, msg):
    '''
        send an SMS from the trial Twilio account to registered number
        recipient number must be registered and verified through Twilio
        max msg character length is 122 (160 - 38 length of trial text)
        includes a performance test of API response time
        dependencies:
        from twilio.rest import TwilioRestClient
        from timeit import default_timer as timer
        import re
    :param phone: string
    :param msg: string
    :return: none
    '''
    urlTitle = 'Twilio SMS API'
    Twilio_ACCOUNT_SID = twilio_id
    Twilio_AUTH_TOKEN = twilio_token
    Twilio_PHONE_NUMBER = twilio_phone
    t1 = timer()
    client = TwilioRestClient(Twilio_ACCOUNT_SID, Twilio_AUTH_TOKEN)
    client.messages.create(
	    to=phone,
	    from_=Twilio_PHONE_NUMBER,
	    body=msg
    )
    pattern = re.compile('(\+\d+)(\d{3})(\d{3})(\d{4})')
    segments = pattern.findall(phone)
    phoneText = segments[0][1] + '.' + segments[0][2] + '.' + segments[0][3]
    print('SMS Sent to ' + phoneText)
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    return True
assert sendSMSfromTrialTwilio(
    twilioID,
    twilioToken,
    twilioPhone,
    '+12037019145',
    'Twilio SMS has been activated'
)

