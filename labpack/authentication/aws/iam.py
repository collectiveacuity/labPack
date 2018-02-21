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

    def __init__(self, request='', message='', errors=None, captured_error=None):

    # report request attempt
        self.errors = errors
        text = 'Failure connecting to AWS with %s request.' % request
    # test connectivity
        try:
            import requests
            requests.get('https://www.google.com')
        except:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            request_object = Request(method='GET', url='https://www.google.com')
            request_details = handle_requests(request_object)
            text += '\n%s' % request_details['error']
    # include original error message
        else:
            try:
                if captured_error:
                    raise captured_error
                else:
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
        self.verbose = verbose

    # construct iam client connection
        client_kwargs = {
            'service_name': 'iam',
            'region_name': self.region_name,
            'aws_access_key_id': self.access_id,
            'aws_secret_access_key': self.secret_key
        }
        self.connection = boto3.client(**client_kwargs)

    # construct empty lists of resources
        self.cert_list = []
        self.role_list = []
        
    # construct verbose method
        self.printer_on = True
        def _printer(msg, flush=False):
            if self.verbose and self.printer_on:
                if flush:
                    print(msg, end='', flush=True)
                else:
                    print(msg)
        self.printer = _printer
    
    # construct ingestion
        from labpack.parsing.conversion import camelcase_to_lowercase, lowercase_to_camelcase
        self.ingest = camelcase_to_lowercase
        self.prepare = lowercase_to_camelcase

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
        if 'ServerCertificateMetadataList' in response.keys():
            for certificate in response['ServerCertificateMetadataList']:
                cert_list.append(certificate['ServerCertificateName'])

    # report results and return list
        if cert_list:
            print_out = 'Found server certificate'
            if len(cert_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(cert_list)
            self.printer(print_out)
        else:
            self.printer('No server certificates found.')

        self.certificate_list = cert_list
        
        return self.certificate_list

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
        if not certificate_name in self.certificate_list:
            self.printer_on = False
            self.list_certificates()
            self.printer_on = True
            if not certificate_name in self.certificate_list:
                raise Exception('\nServer certificate %s does not exist.' % certificate_name)

    # send request for certificate details
        try:
            cert_kwargs = { 'ServerCertificateName': certificate_name }
            response = self.connection.get_server_certificate(**cert_kwargs)
        except:
            raise AWSConnectionError(title)

    # construct certificate details from response
        from labpack.records.time import labDT
        from labpack.parsing.conversion import camelcase_to_lowercase
        cert_dict = response['ServerCertificate']
        cert_details = camelcase_to_lowercase(cert_dict)
        for key, value in cert_details['server_certificate_metadata'].item():
            cert_details.update(**{key:value})
        del cert_details['server_certificate_metadata']
        date_time = cert_details['expiration']
        epoch_time = labDT(date_time).epoch()
        cert_details['expiration'] = epoch_time

        return cert_details

    def list_roles(self):
    
        '''
            a method to retrieve a list of server certificates

        :return: list with certificate name strings
        '''

        title = '%s.list_certificates' % self.__class__.__name__

    # send request for list of certificates
        self.printer('Querying AWS for iam roles.')
        try:
            response = self.connection.list_roles()
        except:
            raise AWSConnectionError(title)

    # construct certificate list from response
        role_list = []
        if 'Roles' in response.keys():
            for role in response['Roles']:
                role_list.append(role['RoleName'])

    # report results and return list
        if role_list:
            print_out = 'Found iam roles'
            if len(role_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(role_list)
            self.printer(print_out)
        else:
            self.printer('No iam roles found.')

        self.role_list = role_list
        
        return self.role_list
    
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
    iam_client.list_roles()
