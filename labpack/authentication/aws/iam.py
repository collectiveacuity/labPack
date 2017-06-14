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

class IAMConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to AWS IAM with %s request.' % message
        super(IAMConnectionError, self).__init__(text)
        self.errors = errors

class iamClient(object):

    '''
        a class of methods for interacting with the AWS Identity & Access Management

        https://boto3.readthedocs.org/en/latest/
    '''

    def __init__(self, access_id, secret_key, default_region, owner_id, user_name):

        '''
            a method for initializing the connection to AW IAM

        :param access_id: string with access_key_id from aws IAM user setup
        :param secret_key: string with secret_access_key from aws IAM user setup
        :param default_region:
        :param owner_id:
        :param user_name:
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
            'default_region': default_region
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # validate inputs and create base methods
        self.cred = iamInput(aws_rules).credentials(aws_credentials)
        self.input = iamInput(aws_rules)
        self.rules = aws_rules

    # construct iam client connection
        import os
        for key, value in self.cred.items():
            os.environ[key] = value
        self.connection = boto3.client('iam')

    def findCertificates(self):

        '''
            a method to retrieve a list of server certificates

        :return: list with certificate name strings
        '''

        title = 'findCertificates'

    # send request for list of certificates
        print('Querying AWS for server certificates.')
        try:
            response = self.connection.list_server_certificates()
        except:
            raise IAMConnectionError(title + ' list_server_certificates()')

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
            print(print_out)
        else:
            print('No server certificates found.')

        return cert_list

    def certificateDetails(self, cert_name):

        '''
            a method to retrieve the details about a server certificate

        :param cert_name: string with name of certificate
        :return: dictionary with certificate details
        '''

        title = 'certificateDetails'

    # validate inputs
        self.input.certName('cert_name', title + ' certificate name')

    # verify existence of server certificate
        try:
            response = self.connection.list_server_certificates()
        except:
            raise IAMConnectionError(title + ' list_server_certificates()')
        cert_list = []
        if 'ServerCertificateMetadataList' in response:
            for certificate in response['ServerCertificateMetadataList']:
                cert_list.append(certificate['ServerCertificateName'])
        if not cert_name in cert_list:
            raise Exception('\nServer certificate %s does not exist.' % cert_name)

    # send requst for certificate details
        try:
            response = self.connection.get_server_certificate(
                ServerCertificateName=cert_name
            )
        except:
            raise IAMConnectionError(title + ' get_server_certificate()')

    # construct certificate details from response
        cert_dict = response['ServerCertificate']['ServerCertificateMetadata']
        date_time = cert_dict['Expiration']
        iso_datetime = date_time.isoformat().replace('+00:00', 'Z')
        cert_details = {
            'certARN': cert_dict['Arn'],
            'certName': cert_dict['ServerCertificateName'],
            'expirationDate': iso_datetime,
            'certBody': '',
            'certChain': ''
        }
        if 'CertificateBody' in response['ServerCertificate']:
            cert_details['certBody'] = response['ServerCertificate']['CertificateBody']
        if 'CertificateChain' in response['ServerCertificate']:
            cert_details['certChain'] = response['ServerCertificate']['CertificateChain']

        return cert_details

    def unitTests(self):
        certList = self.findCertificates()
        print(certList)
        if certList:
            certDetails = self.certificateDetails(certList[1])
            print(certDetails)
            assert certDetails['certARN']
        return self
