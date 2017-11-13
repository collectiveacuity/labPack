__author__ = 'rcj1492'
__created__ = '2017.11'
__license__ = '©2017 Collective Acuity'

# http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Polly.html#constructor-property
# http://boto3.readthedocs.io/en/latest/reference/services/polly.html

'''
PLEASE NOTE:    polly package requires the boto3 module.

(all platforms) pip3 install boto3
'''

try:
    import boto3
except:
    import sys
    print('polly package requires the boto3 module. try: pip3 install boto3')
    sys.exit(1)

from labpack.authentication.aws.iam import AWSConnectionError

class pollyClient(object):
    
    ''' a class of methods for interacting with AWS Polly API '''
    
    def __init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True, usage_client=None):

        '''
            a method for initializing the connection to AWS Polly
            
        :param access_id: string with access_key_id from aws IAM user setup
        :param secret_key: string with secret_access_key from aws IAM user setup
        :param region_name: string with name of aws region
        :param owner_id: string with aws account id
        :param user_name: string with name of user access keys are assigned to
        :param verbose: boolean to enable process messages
        :param usage_client: callable object to track resource usage
        '''
        
        title = '%s.__init__' % self.__class__.__name__

    # initialize model
        from labpack import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        class_fields = jsonLoader(__module__, 'speech/aws/polly-rules.json')
        self.fields = jsonModel(class_fields)

    # construct iam connection
        from labpack.authentication.aws.iam import iamClient
        self.iam = iamClient(access_id, secret_key, region_name, owner_id, user_name, verbose)

    # construct polly client connection
        client_kwargs = {
            'service_name': 'polly',
            'region_name': self.iam.region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        self.connection = boto3.client(**client_kwargs)
        self.verbose = verbose
        self.usage_client = usage_client
    
    # construct range of polly options
        self.voice_ids = self.fields.components['.voice_id']['discrete_values']
        self.output_formats = self.fields.components['.output_format']['discrete_values']
        
    # construct pythonic conversion method
        from labpack.parsing.conversion import camelcase_to_lowercase
        self.ingest = camelcase_to_lowercase

    def synthesize(self, message_text, voice_id='Nicole', output_format='mp3', sample_rate='22050', stream_response=False):
    
        '''
            a method to synthesize speech from text
            
        :param message_text: string with text to synthesize
        :param voice_id: string with name of voice id in AWS polly to use
        :param output_format: string with file type of audio output
        :param sample_rate: string with the audio frequency specified in Hz
        :param stream_response: boolean to return a StreamingBody object 
        :return: dictionary with synthesized speech fields
        
        output:
        {
            'audio_stream': b'', # or StreamingBody
            'content_type': 'string',
            'request_characters': 123
        }
        
        from botocore.response import StreamingBody
        StreamingBody.read
        StreamingBody.close
        StreamingBody.set_socket_timeout
        
        Nicole: aussie female
        Russell: aussie male
        Gwyneth: irish female
        Geraint: welsh male
        Emma: english female
        Brian: english male
        Joey: american male (east coast)
        Matthew: american male (west coast)
        Karl: scandinavian male (heavy accent)
        Marlene: dutch female
        Ruben: dutch male
        Justin: male child
        Astrid: german female (heavy accent)
        Maxim: russian male (in Russian)
        '''
        
        title = '%s.synthesize' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'message_text': message_text,
            'voice_id': voice_id,
            'output_format': output_format,
            'sample_rate': sample_rate
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # construct speech params
        speech_params = {
            'OutputFormat': output_format,
            'Text': message_text,
            'TextType': 'text',
            'VoiceId': voice_id,
            'SampleRate': sample_rate
        }
    
    # send request for synthesis
        try:
            response = self.connection.synthesize_speech(**speech_params)
        except:
            raise AWSConnectionError(title)

    # convert output to pythonic
        response_details = self.ingest(response)
    
    # read audio stream
        if not stream_response:
            response_details['audio_stream'] = response_details['audio_stream'].read()
        
    # TODO usage client methods / format
        if self.usage_client:
            self.usage_client.update('polly', 'synthesis', response_details)

        return response_details
    
if __name__ == '__main__':

# test client initialization
    from labpack.records.settings import load_settings
    aws_cred = load_settings('../../../../cred/aws-polly.yaml')
    client_kwargs = {
        'access_id': aws_cred['aws_polly_access_key_id'],
        'secret_key': aws_cred['aws_polly_secret_access_key'],
        'region_name': aws_cred['aws_polly_default_region'],
        'owner_id': aws_cred['aws_polly_owner_id'],
        'user_name': aws_cred['aws_polly_user_name']
    }
    polly_client = pollyClient(**client_kwargs)

# test speech synthesis
    test_text = 'Hopefully this works well enough to discern the accent.'
    test_speech = '../../../data/test_speech.mp3'
    with open(test_speech, 'wb') as f:
        response = polly_client.synthesize(test_text, voice_id='Emma')
        f.write(response['audio_stream'])
        f.close()