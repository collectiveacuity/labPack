__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

class twilioClient(object):

    def __init__(self, account_sid, auth_token, twilio_phone):

        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_phone = twilio_phone

        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from twilio.rest import TwilioRestClient
        sys_path.insert(0, sys_path.pop())

        self.client = TwilioRestClient(self.account_sid, self.auth_token)

    def send_message(self, phone_number, message_text):

        ''' send an SMS from the Twilio account to phone number

        :param phone_number: string with phone number with country and area code
        :param message_text: string with message text
        :return: dictionary with details of response

        {
            'direction': 'outbound-api',
            'to': '+18001234567',
            'status': 'queued',
            'dt': 1479603651.0,
            'body': 'good times',
            'error_code': None,
            'from': '+19001234567'
        }

        '''

        response = self.client.messages.save(
            to=phone_number,
            from_=self.twilio_phone,
            body=message_text
        )

        keys = ['body', 'status', 'error_code', 'direction', 'date_updated', 'to', 'from_']
        response_details = {}
        import re
        builtin_pattern = re.compile('^_')
        for method in dir(response):
            if not builtin_pattern.findall(method):
                if method == 'date_updated':
                    from labpack.records.time import labDT
                    python_dt = getattr(response, method)
                    from tzlocal import get_localzone
                    python_dt = python_dt.replace(tzinfo=get_localzone())
                    response_details[method] = labDT.fromPython(python_dt).epoch()
                elif method in keys:
                    response_details[method] = getattr(response, method)

        return response_details

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    twilio_config = load_settings('../../../cred/twilio.yaml')
    account_sid = twilio_config['twilio_account_sid']
    auth_token = twilio_config['twilio_auth_token']
    twilio_phone = twilio_config['twilio_phone_number']
    twilio_client = twilioClient(account_sid, auth_token, twilio_phone)
    response_details = twilio_client.send_message('+13109361571', 'good times')
    print(response_details)