__author__ = 'rcj1492'
__created__ = '2015.10'

'''
PLEASE NOTE:    iam package requires the boto3 module.

(all platforms) pip3 install boto3
'''

try:
    import boto3
except:
    import sys
    print('iam package requires the boto3 module. try: pip3 install boto3')
    sys.exit(1)

class AWSConnectionError(Exception):

    def __init__(self, request='', message='', errors=None):

        self.errors = errors
        text = '\nFailure connecting to AWS with %s request.' % request
        try:
            raise
        except Exception as err:
            text += '\n%s' % err
        if message:
            text += '\n%s' % message

        super(AWSConnectionError, self).__init__(text)

class iamClient(object):

    '''
        a class of methods for interacting with the AWS Identity & Access Management

        https://boto3.readthedocs.org/en/latest/
    '''

    def __init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True):

        '''
            a method for initializing the connection to AW IAM

        :param access_id: string with access_key_id from aws IAM user setup
        :param secret_key: string with secret_access_key from aws IAM user setup
        :param region_name: string with name of aws region
        :param owner_id: string with aws account id
        :param user_name: string with name of user access keys are assigned to
        :param verbose: boolean to enable process messages
        '''

        title = '%s.__init__' % self.__class__.__name__

    # initialize model
        from labpack import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        class_fields = jsonLoader(__module__, 'authentication/aws/iam-rules.json')
        self.fields = jsonModel(class_fields)

    # validate inputs
        input_fields = {
            'access_id': access_id,
            'secret_key': secret_key,
            'region_name': region_name,
            'owner_id': owner_id,
            'user_name': user_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # construct credential methods
        self.access_id = access_id
        self.secret_key = secret_key
        self.region_name = region_name
        self.owner_id = owner_id
        self.user_name = user_name

    # construct iam client connection
        client_kwargs = {
            'service_name': 'iam',
            'region_name': self.region_name,
            'aws_access_key_id': self.access_id,
            'aws_secret_access_key': self.secret_key
        }
        self.connection = boto3.client(**client_kwargs)

    # construct verbose method
        def _null_printer(msg):
            pass
        def _printer(msg):
            if verbose:
                print(msg)
        self.printer_on = _printer
        self.printer_off = _null_printer
        self.printer = self.printer_on

    def list_certificates(self):

        '''
            a method to retrieve a list of server certificates

        :return: list with certificate name strings
        '''

        title = '%s.list_certificates' % self.__class__.__name__

    # send request for list of certificates
        self.printer('Querying AWS for server certificates.')
        try:
            response = self.connection.list_server_certificates()
        except:
            raise AWSConnectionError(title)

    # construct certificate list from response
        cert_list = []
        if 'ServerCertificateMetadataList' in response:
            for certificate in response['ServerCertificateMetadataList']:
                cert_list.append(certificate['ServerCertificateName'])

    # report results and return list
        if cert_list:
            print_out = 'Found server certificate'
            if len(cert_list) > 1:
                print_out += 's'
            i_counter = 0
            for certificate in cert_list:
                if i_counter > 0:
                    print_out += ','
                print_out += ' ' + certificate
                i_counter += 1
            print_out += '.'
            self.printer(print_out)
        else:
            self.printer('No server certificates found.')

        return cert_list

    def read_certificate(self, certificate_name):

        '''
            a method to retrieve the details about a server certificate

        :param certificate_name: string with name of server certificate
        :return: dictionary with certificate details
        '''

        title = '%s.read_certificate' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'certificate_name': certificate_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # verify existence of server certificate
        self.printer = self.printer_off
        cert_list = self.list_certificates()
        self.printer = self.printer_on
        if not certificate_name in cert_list:
            raise Exception('\nServer certificate %s does not exist.' % certificate_name)

    # send request for certificate details
        try:
            cert_kwargs = { 'ServerCertificateName': certificate_name }
            response = self.connection.get_server_certificate(**cert_kwargs)
        except:
            raise AWSConnectionError(title)

    # construct certificate details from response
        from labpack.records.time import labDT
        cert_dict = response['ServerCertificate']['ServerCertificateMetadata']
        date_time = cert_dict['Expiration']
        epoch_time = labDT(date_time).epoch()
        cert_details = {
            'cert_arn': cert_dict['Arn'],
            'cert_name': cert_dict['ServerCertificateName'],
            'expiration_date': epoch_time,
            'cert_body': '',
            'cert_chain': ''
        }
        if 'CertificateBody' in response['ServerCertificate']:
            cert_details['cert_body'] = response['ServerCertificate']['CertificateBody']
        if 'CertificateChain' in response['ServerCertificate']:
            cert_details['cert_body'] = response['ServerCertificate']['CertificateChain']

        return cert_details

if __name__ == '__main__':

    from labpack.records.settings import load_settings
    test_cred = load_settings('../../../../cred/awsLab.yaml')
    client_kwargs = {
        'access_id': test_cred['aws_access_key_id'],
        'secret_key': test_cred['aws_secret_access_key'],
        'region_name': test_cred['aws_default_region'],
        'owner_id': test_cred['aws_owner_id'],
        'user_name': test_cred['aws_user_name']
    }
    iam_client = iamClient(**client_kwargs)
    iam_client.list_certificates()
