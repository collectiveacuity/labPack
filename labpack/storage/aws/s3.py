__author__ = 'rcj1492'
__created__ = '2015.08'
__license__ = 'MIT'

'''
PLEASE NOTE:    s3 package requires the boto3 module.

(all platforms) pip3 install boto3
'''

try:
    import boto3
except:
    import sys
    print('s3 package requires the boto3 module. try: pip3 install boto3')
    sys.exit(1)

# TODO: bucket access policy feature for s3
# TODO: bucket region replication feature for s3
# TODO: test bucket notification settings feature integration with AWS event services
# TODO: glacierClient archive, restore and delete methods

from labpack.authentication.aws.iam import AWSConnectionError

class _s3Client(object):

    '''
        a class of methods for interacting with AWS Simple Storage Service
    '''

    def __init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True):

        '''
            a method for initializing the connection to S3
            
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
        class_fields = jsonLoader(__module__, 'storage/aws/s3-rules.json')
        self.fields = jsonModel(class_fields)

    # construct iam connection
        from labpack.authentication.aws.iam import iamClient
        self.iam = iamClient(access_id, secret_key, region_name, owner_id, user_name, verbose)

    # construct s3 client connection
        client_kwargs = {
            'service_name': 's3',
            'region_name': self.iam.region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        self.connection = boto3.client(**client_kwargs)
        self.verbose = verbose
    
    # construct object properties
        self.bucket_list = []

    def _key_digest(self, secret_key):
        
        '''
            a helper method for creating a base 64 encoded secret key and digest
        :param secret_key: string with key to encrypt/decrypt data
        :return: string with base64 key, string with base64 digest
        '''
        
        from hashlib import md5, sha256
        from base64 import b64encode
        key_bytes = sha256(secret_key.encode('utf-8')).digest()
        key_b64 = b64encode(key_bytes).decode()
        digest_bytes = md5(key_bytes).digest()
        digest_b64 = b64encode(digest_bytes).decode()
        
        return key_b64, digest_b64
    
    def list_buckets(self):

        '''
            a method to retrieve a list of buckets on s3

        :return: list of buckets
        '''

        title = '%s.list_buckets' % self.__class__.__name__
        
        bucket_list = []
        
    # send request to s3
        try:
            response = self.connection.list_buckets()
        except:
            raise AWSConnectionError(title)

    # create list from response
        for bucket in response['Buckets']:
            bucket_list.append(bucket['Name'])

        self.bucket_list = bucket_list
        
        return self.bucket_list

    def create_bucket(self, bucket_name, access_control='private', version_control=False, log_destination=None, lifecycle_rules=None, tag_list=None, notification_settings=None,  region_replication=None, access_policy=None):

        '''
            a method for creating a bucket on AWS S3
            
        :param bucket_name: string with name of bucket
        :param access_control: string with type of access control policy
        :param version_control: [optional] boolean to enable versioning of records
        :param log_destination: [optional] dictionary with bucket name and prefix of log bucket
        :param lifecycle_rules: [optional] list of dictionaries with rules for aging data
        :param tag_list: [optional] list of dictionaries with key and value for tag
        :param notification_settings: [optional] list of dictionaries with notification details
        :param region_replication: [optional] dictionary with replication settings (WIP)
        :param access_policy: [optional] dictionary with policy for user access (WIP)
        :return: string with name of bucket
        '''

        title = '%s.create_bucket' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'access_control': access_control,
            'log_destination': log_destination,
            'lifecycle_rules': lifecycle_rules,
            'tag_list': tag_list,
            'notification_settings': notification_settings,
            'region_replication': region_replication,
            'access_policy': access_policy
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify requirements and limits
        self.list_buckets()
        if bucket_name in self.bucket_list:
            raise ValueError('S3 Bucket "%s" already exists in aws region %s.' % (bucket_name, self.iam.region_name))
        max_buckets = self.fields.metadata['limits']['max_buckets_per_account']
        if len(self.bucket_list) >= max_buckets:
            raise Exception('S3 account %s already at maximum %s buckets.' % (self.iam.owner_id, max_buckets))
        if log_destination:
            log_name = log_destination['name']
            if not log_name in self.bucket_list:
                if log_name != bucket_name:
                    raise ValueError('S3 Bucket "%s" for logging does not exist in aws region %s.' % (log_name, self.iam.region_name))
            else:
                log_details = self.read_bucket(log_name)
                if log_details['access_control'] != 'log-delivery-write':
                    raise ValueError('S3 Bucket "%s" for logging does not have "log-delivery-write" access control.' % log_name)
            if not 'prefix' in log_destination.keys():
                log_destination['prefix'] = ''

    # TODO: check to see if required notification arns exist
        if notification_settings:
            for notification in notification_settings:
                arn_id = notification['arn']

    # create key word arguments dictionary
        kw_args = {
            'Bucket': bucket_name,
            'ACL': access_control
        }
        if self.iam.region_name != 'us-east-1':
            kw_args['CreateBucketConfiguration'] = { 'LocationConstraint': self.iam.region_name }

    # send request to s3
        self.iam.printer('Creating bucket "%s".' % bucket_name, flush=True)
        try:
            response = self.connection.create_bucket(**kw_args)
            self.iam.printer('.', flush=True)
        except:
            raise AWSConnectionError(title)

    # if true, activate version_control attribute
        if version_control:
            try:
                self.connection.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={ 'Status': 'Enabled' }
                )
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

    # if present, direct bucket logging to bucket location
        if log_destination:
            try:
                kw_args = {
                    'Bucket': bucket_name,
                    'BucketLoggingStatus': {
                        'LoggingEnabled': {
                            'TargetBucket': log_destination['name']
                        }
                    }
                }
                if log_destination['prefix']:
                    kw_args['BucketLoggingStatus']['LoggingEnabled']['TargetPrefix'] = log_destination['prefix']
                self.connection.put_bucket_logging(**kw_args)
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

    # if present, assign lifecycle rules
        if lifecycle_rules:
            kw_args = {
                'Bucket': bucket_name,
                'LifecycleConfiguration': { 'Rules': [ ] }
            }
            for rule in lifecycle_rules:
                details = {
                    'Prefix': rule['prefix'],
                    'Status': 'Enabled'
                }
                if rule['action'] == 'archive':
                    if rule['current_version']:
                        details['Transition'] = {
                            'Days': rule['longevity'],
                            'StorageClass': 'GLACIER'
                        }
                    else:
                        details['NoncurrentVersionTransition'] = {
                            'NoncurrentDays': rule['longevity'],
                            'StorageClass': 'GLACIER'
                        }
                else:
                    if rule['current_version']:
                        details['Expiration'] = { 'Days': rule['longevity'] }
                    else:
                        details['NoncurrentVersionExpiration'] = { 'NoncurrentDays': rule['longevity'] }
                kw_args['LifecycleConfiguration']['Rules'].append(details)
            try:
                response = self.connection.put_bucket_lifecycle(**kw_args)
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

    # if present, assign tags to bucket
        if tag_list:
            try:
                self.connection.put_bucket_tagging(
                    Bucket=bucket_name,
                    Tagging={ 'TagSet': self.iam.prepare(tag_list) }
                )
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

    # if present, assign notification rules
        if notification_settings:
            kw_args = {
                'Bucket': bucket_name,
                'NotificationConfiguration': {}
            }
            for notification in notification_settings:
                details = {
                    'Events': [],
                    'Filter': { 'Key': { 'FilterRules': [] } }
                }
                details['Events'].append(notification['event'])
                if notification['filters']:
                    for key, value in notification['filters'].items():
                        filter_details = {
                            'Name': key,
                            'Value': value
                        }
                        details['Filter']['Key']['FilterRules'].append(filter_details)
                if notification['service'] == 'sns':
                    details['TopicArn'] = notification['arn']
                    if not 'TopicConfigurations' in kw_args['NotificationConfiguration']:
                        kw_args['NotificationConfiguration']['TopicConfigurations'] = []
                    kw_args['NotificationConfiguration']['TopicConfigurations'].append(details)
                elif notification['service'] == 'sqs':
                    details['QueueArn'] = notification['arn']
                    if not 'QueueConfigurations' in kw_args['NotificationConfiguration']:
                        kw_args['NotificationConfiguration']['QueueConfigurations'] = []
                    kw_args['NotificationConfiguration']['QueueConfigurations'].append(details)
                elif notification['service'] == 'lambda':
                    if not 'LambdaFunctionConfigurations' in kw_args['NotificationConfiguration']:
                        kw_args['NotificationConfiguration']['LambdaFunctionConfigurations'] = []
                    details['LambdaFunctionArn'] = notification['arn']
                    kw_args['NotificationConfiguration']['LambdaFunctionConfigurations'].append(details)

            try:
                response = self.connection.put_bucket_notification_configuration(**kw_args)
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

     # TODO: if present, assign region replication
        if region_replication:
            try:
                # response = self.connection.put_bucket_replication(
                #     Bucket='string',
                #     ReplicationConfiguration={
                #         'Role': 'string',
                #         'Rules': [
                #             {
                #                 'ID': 'string',
                #                 'Prefix': 'string',
                #                 'Status': 'Enabled',
                #                 'Destination': {
                #                     'Bucket': 'string'
                #                 }
                #             },
                #         ]
                #     }
                # )
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

    # TODO: if present, assign access policy
        if access_policy:
            try:
                # response = self.connection.put_bucket_policy(
                #     Bucket='string',
                #     Policy='string'
                # )
                self.iam.printer('.', flush=True)
            except:
                raise AWSConnectionError(title)

        self.bucket_list.append(bucket_name)
        self.iam.printer(' done.')
        
        return bucket_name

    def read_bucket(self, bucket_name):

        '''
            a method to retrieve properties of a bucket in s3

        :param bucket_name: string with name of bucket
        :return: dictionary with details of bucket
        '''

        title = '%s.read_bucket' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # validate existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 Bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))

    # create details dictionary
        bucket_details = {
            'bucket_name': bucket_name,
            'access_control': 'private',
            'version_control': False,
            'log_destination': {},
            'lifecycle_rules': [],
            'tag_list': [],
            'notification_settings': [],
            'region_replication': {},
            'access_policy': {}
        }

    # retrieve access control details
        try:
            response = self.connection.get_bucket_acl( Bucket=bucket_name )
            if len(response['Grants']) > 1:
                log_user = 'http://acs.amazonaws.com/groups/s3/LogDelivery'
                log_delivery = False
                public_user = 'http://acs.amazonaws.com/groups/global/AllUsers'
                public_perm = []
                for grant in response['Grants']:
                    if 'URI' in grant['Grantee']:
                        if grant['Grantee']['URI'] == log_user:
                            log_delivery = True
                        if grant['Grantee']['URI'] == public_user:
                            public_perm.append(grant['Permission'])
                if public_perm:
                    if len(public_perm) > 1:
                        bucket_details['access_control'] = 'public-read-write'
                    else:
                        bucket_details['access_control'] = 'public-read'
                elif log_delivery:
                    bucket_details['access_control'] = 'log-delivery-write'
                else:
                    bucket_details['access_control'] = 'authenticated-read'
        except:
            raise AWSConnectionError(title)

    # retrieve version control details
        try:
            response = self.connection.get_bucket_versioning( Bucket=bucket_name )
            if 'Status' in response.keys():
                if response['Status'] == 'Enabled':
                    bucket_details['version_control'] = True
        except:
            raise AWSConnectionError(title)

    # retrieve log destination details
        try:
            response = self.connection.get_bucket_logging( Bucket=bucket_name )
            if 'LoggingEnabled' in response:
                res = response['LoggingEnabled']
                bucket_details['log_destination']['name'] = res['TargetBucket']
                bucket_details['log_destination']['prefix'] = ''
                if 'TargetPrefix' in res.keys():
                    bucket_details['log_destination']['prefix'] = res['TargetPrefix']
        except:
            raise AWSConnectionError(title)

    # retrieve lifecycle rules details
        try:
            response = self.connection.get_bucket_lifecycle( Bucket=bucket_name )
            for rule in response['Rules']:
                if rule['Status'] == 'Enabled':
                    details = { "prefix": rule['Prefix'] }
                    if 'Transition' in rule.keys():
                        details['longevity'] = rule['Transition']['Days']
                        details['current_version'] = True
                        details['action'] = 'archive'
                    elif 'Expiration' in rule.keys():
                        details['longevity'] = rule['Expiration']['Days']
                        details['current_version'] = True
                        details['action'] = 'delete'
                    elif 'NoncurrentVersionTransition' in rule.keys():
                        details['longevity'] = rule['NoncurrentVersionTransition']['NoncurrentDays']
                        details['current_version'] = False
                        details['action'] = 'archive'
                    elif 'NoncurrentVersionExpiration' in rule.keys():
                        details['longevity'] = rule['NoncurrentVersionExpiration']['NoncurrentDays']
                        details['current_version'] = False
                        details['action'] = 'delete'
                    bucket_details['lifecycle_rules'].append(details)
        except:
            pass

    # retrieve bucket tag details
        try:
            response = self.connection.get_bucket_tagging( Bucket=bucket_name )
            for tag in response['TagSet']:
                bucket_details['tag_list'].append(tag)
        except:
            pass

    # retrieve notification settings details
        try:
            response = self.connection.get_bucket_notification_configuration( Bucket=bucket_name)
            if 'TopicConfigurations' in response.keys():
                for notification in response['TopicConfigurations']:
                    details = {
                        'service': 'sns',
                        'arn': notification['TopicArn'],
                        'event': notification['Events'][0],
                        'filters': {}
                    }
                    if 'Filter' in notification.keys():
                        for rule in notification['Filter']['Key']['FilterRules']:
                            details['filters'][rule['Name']] = rule['Value']
                    bucket_details['notification_settings'].append(details)
            if 'QueueConfigurations' in response.keys():
                for notification in response['QueueConfigurations']:
                    details = {
                        'service': 'sqs',
                        'arn': notification['QueueArn'],
                        'event': notification['Events'][0],
                        'filters': {}
                    }
                    if 'Filter' in notification.keys():
                        for rule in notification['Filter']['Key']['FilterRules']:
                            details['filters'][rule['Name']] = rule['Value']
                    bucket_details['notification_settings'].append(details)
            if 'LambdaFunctionConfigurations' in response.keys():
                for notification in response['LambdaFunctionConfigurations']:
                    details = {
                        'service': 'lambda',
                        'arn': notification['LambdaFunctionArn'],
                        'event': notification['Events'][0],
                        'filters': {}
                    }
                    if 'Filter' in notification.keys():
                        for rule in notification['Filter']['Key']['FilterRules']:
                            details['filters'][rule['Name']] = rule['Value']
                    bucket_details['notification_settings'].append(details)
        except:
            raise AWSConnectionError(title)

    # TODO: retrieve region replication details
    #     try:
    #         response = self.connection.get_bucket_replication( Bucket=bucket_name )
    #     except:
    #         pass

    # TODO: retrieve access policy details
    #     try:
    #         response = self.connection.get_bucket_policy( Bucket=bucket_name )
    #     except:
    #         pass

        return self.iam.ingest(bucket_details)
    
    def update_bucket(self, bucket_name, access_control='private', version_control=False, log_destination=None, lifecycle_rules=None, tag_list=None, notification_settings=None, region_replication=None, access_policy=None):

        '''
            a method for updating the properties of a bucket in S3

        :param bucket_name: string with name of bucket
        :param access_control: string with type of access control policy
        :param version_control: [optional] boolean to enable versioning of records
        :param log_destination: [optional] dictionary with bucket name and prefix of log bucket
        :param lifecycle_rules: [optional] list of dictionaries with rules for aging data
        :param tag_list: [optional] list of dictionaries with key and value for tag
        :param notification_settings: [optional] list of dictionaries with notification details
        :param region_replication: [optional] dictionary with replication settings (WIP)
        :param access_policy: [optional] dictionary with policy for user access (WIP)
        :return: list of dictionaries with changes to bucket
        '''

        title = '%s.update_bucket' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'access_control': access_control,
            'version_control': version_control,
            'log_destination': log_destination,
            'lifecycle_rules': lifecycle_rules,
            'tag_list': tag_list,
            'notification_settings': notification_settings,
            'region_replication': region_replication,
            'access_policy': access_policy
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if log_destination == None:
            input_fields['log_destination'] = {}
        if lifecycle_rules == None:
            input_fields['lifecycle_rules'] = []
        if tag_list == None:
            input_fields['tag_list'] = []
        if notification_settings == None:
            input_fields['notification_settings'] = []
        if region_replication == None:
            input_fields['region_replication'] = {}
        if access_policy == None:
            input_fields['access_policy'] = {}

    # verify requirements and limits
        self.list_buckets()
        if not bucket_name in self.bucket_list:
            raise ValueError('S3 bucket "%s" does not exist in aws region %s. Update not applicable.' % (bucket_name, self.iam.region_name))
        if log_destination:
            log_name = log_destination['name']
            if not log_name in self.bucket_list:
                raise ValueError('S3 Bucket "%s" for logging does not exist in aws region %s.' % (log_name, self.iam.region_name))
            else:
                log_details = self.read_bucket(log_name)
                if log_details['access_control'] != 'log-delivery-write':
                    raise ValueError('S3 Bucket "%s" for logging does not have "log-delivery-write" access control.' % log_name)
            if not 'prefix' in log_destination.keys():
                input_fields['log_destination']['prefix'] = ''

    # TODO: check to see if required notification arns exist
        if notification_settings:
            for notification in notification_settings:
                arn_id = notification['arn']
    
    # retrieve existing bucket fields
        existing_fields = self.read_bucket(bucket_name)

    # alphabetize tag list
        if existing_fields['tag_list']:
            existing_fields['tag_list'] = sorted(existing_fields['tag_list'], key=lambda k: k['key'])
        if input_fields['tag_list']:
            input_fields['tag_list'] = sorted(input_fields['tag_list'], key=lambda k: k['key'])

    # determine difference between new and old versions
        from labpack.parsing.comparison import compare_records
        change_list = compare_records(input_fields, existing_fields)
        if not change_list:
            self.iam.printer('There are no changes to make to bucket "%s".' % bucket_name)
            return change_list
        
    # process changes
        self.iam.printer('Updating bucket "%s".' % bucket_name, flush=True)
        processed_list = []
        for change in change_list:

    # replace access control
            if change['path'][0] == 'access_control' and 'access_control' not in processed_list:
                kw_args = {
                    'Bucket': bucket_name,
                    'ACL': input_fields['access_control']
                }
                try:
                    self.connection.put_bucket_acl(**kw_args)
                    self.iam.printer('.', flush=True)
                except:
                    raise AWSConnectionError(title)
            processed_list.append('access_control')

    # replace version control
            if change['path'][0] == 'version_control' and 'version_control' not in processed_list:
                if input_fields['version_control']:
                    try:
                        self.connection.put_bucket_versioning(
                            Bucket=bucket_name,
                            VersioningConfiguration={ 'Status': 'Enabled' }
                        )
                        self.iam.printer('.', flush=True)
                    except:
                        raise AWSConnectionError(title)
                else:
                    try:
                        self.connection.put_bucket_versioning(
                            Bucket=bucket_name,
                            VersioningConfiguration={ 'Status': 'Suspended' }
                        )
                        self.iam.printer('.', flush=True)
                    except:
                        raise AWSConnectionError(title)
                processed_list.append('version_control')

    # replace log destination
            if change['path'][0] == 'log_destination' and 'log_destination' not in processed_list:
                if input_fields['log_destination']:
                    log_name = input_fields['log_destination']['name']
                    log_prefix = input_fields['log_destination']['prefix']
                    kw_args = {
                        'Bucket': bucket_name,
                        'BucketLoggingStatus': {
                            'LoggingEnabled': {
                                'TargetBucket': log_name
                            }
                        }
                    }
                    if log_prefix:
                        kw_args['BucketLoggingStatus']['LoggingEnabled']['TargetPrefix'] = log_prefix
                else:
                    kw_args = {
                        'Bucket': bucket_name,
                        'BucketLoggingStatus': {}
                    }
                try:
                    self.connection.put_bucket_logging(**kw_args)
                    self.iam.printer('.', flush=True)
                except:
                    raise AWSConnectionError(title)
                processed_list.append('log_destination')

    # replace lifecycle rules
            if change['path'][0] == 'lifecycle_rules' and 'lifecycle_rules' not in processed_list:
                if input_fields['lifecycle_rules']:
                    kw_args = {
                        'Bucket': bucket_name,
                        'LifecycleConfiguration': { 'Rules': [ ] }
                    }
                    for rule in input_fields['lifecycle_rules']:
                        details = {
                            'Prefix': rule['prefix'],
                            'Status': 'Enabled'
                        }
                        if rule['action'] == 'archive':
                            if rule['current_version']:
                                details['Transition'] = {
                                    'Days': rule['longevity'],
                                    'StorageClass': 'GLACIER'
                                }
                            else:
                                details['NoncurrentVersionTransition'] = {
                                    'NoncurrentDays': rule['longevity'],
                                    'StorageClass': 'GLACIER'
                                }
                        else:
                            if rule['current_version']:
                                details['Expiration'] = { 'Days': rule['longevity'] }
                            else:
                                details['NoncurrentVersionExpiration'] = { 'NoncurrentDays': rule['longevity'] }
                        kw_args['LifecycleConfiguration']['Rules'].append(details)
                    try:
                        self.connection.put_bucket_lifecycle(**kw_args)
                        self.iam.printer('.', flush=True)
                    except:
                        raise AWSConnectionError(title)
                else:
                    try:
                        self.connection.delete_bucket_lifecycle( Bucket=bucket_name )
                        self.iam.printer('.', flush=True)
                    except:
                        raise AWSConnectionError(title)
                processed_list.append('lifecycle_rules')

    # replace bucket tags
            if change['path'][0] == 'tag_list' and 'tag_list' not in processed_list:
                if input_fields['tag_list']:
                    try:
                        self.connection.put_bucket_tagging(
                            Bucket=bucket_name,
                            Tagging={ 'TagSet': self.iam.prepare(input_fields['tag_list']) }
                        )
                        self.iam.printer('.', flush=True)
                    except:
                        raise AWSConnectionError(title)
                else:
                    try:
                        self.connection.delete_bucket_tagging( Bucket=bucket_name )
                        self.iam.printer('.', flush=True)
                    except:
                        raise AWSConnectionError(title)
                processed_list.append('tag_list')

    # replace notification settings
            if change['path'][0] == 'notification_settings' and 'notification_settings' not in processed_list:
                kw_args = {
                    'Bucket': bucket_name,
                    'NotificationConfiguration': {}
                }
                if input_fields['notification_settings']:
                    for notification in input_fields['notification_settings']:
                        details = {
                            'Events': [],
                            'Filter': { 'Key': { 'FilterRules': [] } }
                        }
                        details['Events'].append(notification['event'])
                        if notification['filters']:
                            for key, value in notification['filters'].items():
                                filter_details = {
                                    'Name': key,
                                    'Value': value
                                }
                                details['Filter']['Key']['FilterRules'].append(filter_details)
                        if notification['service'] == 'sns':
                            details['TopicArn'] = notification['arn']
                            if not 'TopicConfigurations' in kw_args['NotificationConfiguration']:
                                kw_args['NotificationConfiguration']['TopicConfigurations'] = []
                            kw_args['NotificationConfiguration']['TopicConfigurations'].append(details)
                        elif notification['service'] == 'sqs':
                            details['QueueArn'] = notification['arn']
                            if not 'QueueConfigurations' in kw_args['NotificationConfiguration']:
                                kw_args['NotificationConfiguration']['QueueConfigurations'] = []
                            kw_args['NotificationConfiguration']['QueueConfigurations'].append(details)
                        elif notification['service'] == 'lambda':
                            if not 'LambdaFunctionConfigurations' in kw_args['NotificationConfiguration']:
                                kw_args['NotificationConfiguration']['LambdaFunctionConfigurations'] = []
                            details['LambdaFunctionArn'] = notification['arn']
                            kw_args['NotificationConfiguration']['LambdaFunctionConfigurations'].append(details)
                try:
                    # TODO: response = self.connection.put_bucket_notification_configuration(**kw_args)
                    self.iam.printer('.', flush=True)
                except:
                    raise AWSConnectionError(title)
                processed_list.append('notification_settings')

    # TODO: replace region replication
            if change['path'][0] == 'region_replication' and 'region_replication' not in processed_list:
                if input_fields['region_replication']:
                    pass
                else:
                    pass
                processed_list.append('region_replication')

    # TODO: replace access policy
            if change['path'][0] == 'access_policy' and 'access_policy' not in processed_list:
                if input_fields['access_policy']:
                    pass
                else:
                    pass
                processed_list.append('access_policy')

    # report and return change list
        self.iam.printer(' done.')
        return change_list
    
    def delete_bucket(self, bucket_name):

        '''
            a method to delete a bucket in s3 and all its contents

        :param bucket_name: string with name of bucket
        :return: string with status of method
        '''

        title = '%s.delete_bucket' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # check for existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                status_msg = 'S3 bucket "%s" does not exist.' % bucket_name
                self.iam.printer(status_msg)
                return status_msg

    # retrieve list of records in bucket
        record_keys = []
        record_list, next_key = self.list_versions(bucket_name)
        for record in record_list:
            details = {
                'Key': record['key'],
                'VersionId': record['version_id']
            }
            record_keys.append(details)

    # delete records in bucket
        kw_args = {
            'Bucket': bucket_name,
            'Delete': { 'Objects': record_keys }
        }
        if record_keys:
            try:
                response = self.connection.delete_objects(**kw_args)
            except:
                raise AWSConnectionError(title)

    # continue deleting objects in bucket until empty
        if next_key:
            while next_key:
                record_keys = []
                record_list, next_key = self.list_versions(bucket_name, starting_key=next_key['key'], starting_version=next_key['version_id'])
                for record in record_list:
                    details = {
                        'Key': record['key'],
                        'VersionId': record['version_id']
                    }
                    record_keys.append(details)
                kw_args = {
                    'Bucket': bucket_name,
                    'Delete': { 'Objects': record_keys }
                }
                try:
                    response = self.connection.delete_objects(**kw_args)
                except:
                    raise AWSConnectionError(title)

    # send delete bucket request
        try:
            self.connection.delete_bucket( Bucket=bucket_name )
        except:
            raise AWSConnectionError(title)

    # report result and return true
        status_msg = 'S3 bucket "%s" deleted.' % bucket_name
        self.iam.printer(status_msg)
        
        return status_msg

    def list_records(self, bucket_name, prefix='', delimiter='', max_results=1000, starting_key=''):

        '''
            a method for retrieving a list of the versions of records in a bucket

        :param bucket_name: string with name of bucket
        :param prefix: [optional] string with value limiting results to key prefix
        :param delimiter: string with value which results must not contain (after prefix)
        :param max_results: [optional] integer with max results to return
        :param starting_key: [optional] string with key value to continue search with
        :return: list of results with key, size and date, string with ending key value
        '''
        
        title = '%s.list_records' % self.__class__.__name__
        
        from datetime import datetime
        from dateutil.tz import tzutc
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'prefix': prefix,
            'delimiter': delimiter,
            'max_results': max_results,
            'starting_key': starting_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 Bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name
        }
        if starting_key:
            kw_args['Marker'] = starting_key
        if prefix:
            kw_args['Prefix'] = prefix
        if delimiter:
            kw_args['Delimiter'] = delimiter
        if max_results:
            kw_args['MaxKeys'] = max_results

    # send request for objects
        record_list = []
        next_key = ''
        try:
            response = self.connection.list_objects(**kw_args)
        except:
            raise AWSConnectionError(title)

    # add retrieved contents to object list
        if 'Contents' in response:
            for record in response['Contents']:
                details = {
                    'key': ''
                }
                details = self.iam.ingest(record, details)
                epoch_zero = datetime.fromtimestamp(0).replace(tzinfo=tzutc())
                details['last_modified'] = (details['last_modified'] - epoch_zero).total_seconds()
                record_list.append(details)

    # define ending key value
        if response['IsTruncated']:
            next_key = response['NextMarker']

        return record_list, next_key

    def list_versions(self, bucket_name, prefix='', delimiter='', max_results=1000, starting_key='', starting_version=''):

        '''
            a method for retrieving a list of the versions of records in a bucket

        :param bucket_name: string with name of bucket
        :param prefix: [optional] string with value limiting results to key prefix
        :param delimiter: [optional] string with value limiting results to key delimiter
        :param max_results: [optional] integer with max results to return
        :param starting_key: [optional] string with key value to continue search with
        :param starting_version: [optional] string with version id to continue search with
        :return: list of results with key, size and date, dictionary with key and version id
        '''

        title = '%s.list_versions' % self.__class__.__name__
        
        from datetime import datetime
        from dateutil.tz import tzutc
         
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'prefix': prefix,
            'delimiter': delimiter,
            'max_results': max_results,
            'starting_key': starting_key,
            'starting_version': starting_version
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # validate mutual requirements
        if starting_version or starting_key:
            if not starting_version or not starting_key:
                raise ValueError('%s inputs starting_key and starting_version each require the other.' % title)

    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 Bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name
        }
        if starting_key:
            kw_args['KeyMarker'] = starting_key
        if starting_version:
            kw_args['VersionIdMarker'] = starting_version
        if prefix:
            kw_args['Prefix'] = prefix
        if delimiter:
            kw_args['Delimiter'] = delimiter
        if max_results:
            kw_args['MaxKeys'] = max_results

    # send request for objects
        record_list = []
        next_key = {}
        try:
            response = self.connection.list_object_versions(**kw_args)
        except:
            raise AWSConnectionError(title)

    # add version keys and ids to object list
        if 'Versions' in response:
            for record in response['Versions']:
                details = {
                    'key': '',
                    'version_id': ''
                }
                details = self.iam.ingest(record, details)
                epoch_zero = datetime.fromtimestamp(0).replace(tzinfo=tzutc())
                details['last_modified'] = (details['last_modified'] - epoch_zero).total_seconds()
                details['current_version'] = details['is_latest']
                del details['is_latest']
                record_list.append(details)

    # add delete markers to object list
        if 'DeleteMarkers' in response:
            for record in response['DeleteMarkers']:
                details = {
                    'key': '',
                    'version_id': ''
                }
                details = self.iam.ingest(record, details)
                epoch_zero = datetime.fromtimestamp(0).replace(tzinfo=tzutc())
                details['last_modified'] = (details['last_modified'] - epoch_zero).total_seconds()
                details['current_version'] = details['is_latest']
                del details['is_latest']
                if not 'size' in details.keys():
                    details['size'] = 0
                record_list.append(details)

    # define next key value
        if response['IsTruncated']:
            next_key = {
                'key': response['NextKeyMarker'],
                'version_id': response['NextVersionIdMarker']
            }

        return record_list, next_key

    def create_record(self, bucket_name, record_key, record_data, record_metadata=None, record_mimetype='', record_encoding='', overwrite=True):

        '''
            a method for adding a record to an S3 bucket
            
        :param bucket_name: string with name of bucket
        :param record_key: string with name of key (path) for record
        :param record_data: byte data for record
        :param record_metadata: [optional] dictionary with metadata to attach to record
        :param record_mimetype: [optional] string with content mimetype of record data
        :param record_encoding: [optional] string with content encoding of record data
        :param overwrite: [optional] boolean to overwrite any existing record
        :return: string with name of record key
        '''
        
        title = '%s.create_record' % self.__class__.__name__

        import sys
        from hashlib import md5
        from base64 import b64encode
    
    # define size limitations
        metadata_max = self.fields.metadata['limits']['metadata_max_bytes']
        record_max = self.fields.metadata['limits']['record_max_bytes']
        record_optimal = self.fields.metadata['limits']['record_optimal_bytes']
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'record_key': record_key,
            'record_metadata': record_metadata,
            'secret_key': secret_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # validate metadata fields
        if record_metadata:
            for key, value in record_metadata.items():
                object_title = '%s(record_metadata={%s:...})' % (title, key)
                self.fields.validate(key, '.metadata_keys', object_title)
                object_title = '%s(record_metadata={%s:%s})' % (title, key, value)
                self.fields.validate(value, '.metadata_values', object_title)
        else:
            record_metadata = {}
    
    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))
    
    # verify overwrite condition
        if not overwrite:
            record_status = self.read_headers(bucket_name, record_key)
            if record_status:
                error_msg = 'S3 bucket "%s" already contains a record for key "%s"' % (bucket_name, record_key)
                raise ValueError(error_msg)
        
    # validate size of metadata
        import json
        metadata_size = sys.getsizeof(json.dumps(record_metadata).encode('utf-8'))
        if metadata_size > metadata_max:
            raise ValueError('%s(record_metadata={...}) cannot be greater than %s bytes.' % (title, metadata_max))
                
    # validate size of record
        record_size = sys.getsizeof(record_data)
        error_prefix = '%s(record_key="%s", record_data=...)' % (title, record_key)
        if record_size > record_max:
            raise ValueError('%s exceeds maximum record data size of %s bytes.' % (error_prefix, record_max))
        elif record_size > record_optimal:
            self.iam.printer('[WARNING] %s exceeds optimal record data size of %s bytes.' % (error_prefix, record_optimal))

    # determine content encoding
        if not record_encoding or not record_mimetype:
            import mimetypes
            guess_mimetype, guess_encoding = mimetypes.guess_type(record_key)
            if not record_mimetype:
                record_mimetype = guess_mimetype
            if not record_encoding:
                record_encoding = guess_encoding
                    
    # create RFC 1864 base64 encoded md5 digest of data to confirm integrity
        hash_bytes = md5(record_data).digest()
        content_md5 = b64encode(hash_bytes).decode()
        check_sum = md5(record_data).hexdigest()

    # create key word argument dictionary
        create_kwargs = {
            'Bucket': bucket_name,
            'Key': record_key,
            'Body': record_data,
            'ContentMD5': content_md5
        }
        if record_metadata:
            create_kwargs['Metadata'] = record_metadata
        if record_mimetype:
            create_kwargs['ContentType'] = record_mimetype
        if record_encoding:
            create_kwargs['ContentEncoding'] = record_encoding

    # add server side encryption key to request
    #     if server_encryption:
    #         key_b64, digest_b64 = self._key_digest(secret_key)
    #         kw_args['SSECustomerAlgorithm'] = 'AES256'
    #         kw_args['SSECustomerKey'] = key_b64
    #         kw_args['SSECustomerKeyMD5'] = digest_b64

    # send request to add object
        try:
            response = self.connection.put_object(**create_kwargs)
            if response['ETag'] != '"%s"' % check_sum:
                raise Exception('%s experienced a data transcription error for record "%s".' % record_key)
        except:
            raise AWSConnectionError(title)

        return record_key

    def read_headers(self, bucket_name, record_key, record_version='', version_check=False):

        '''
            a method for retrieving the headers of a record from s3

        :param bucket_name: string with name of bucket
        :param record_key: string with key value of record
        :param record_version: [optional] string with aws id of version of record
        :param version_check: [optional] boolean to enable current version check
        :return: dictionary with headers of record
        '''
        
        title = '%s.read_headers' % self.__class__.__name__
        
        from datetime import datetime
        from dateutil.tz import tzutc
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'record_key': record_key,
            'record_version': record_version
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))
                
    # create key word argument dictionary
        headers_kwargs = {
            'Bucket': bucket_name,
            'Key': record_key
        }
        if record_version:
            headers_kwargs['VersionId'] = record_version

    # create metadata default
        metadata_details = {}
        
    # send request for record header
        try:
            record = self.connection.head_object(**headers_kwargs)
        except Exception as err:
            try:
                import requests
                requests.get('https://www.google.com')
                return metadata_details
            except:
                raise AWSConnectionError(title, captured_error=err)

    # create metadata from response
        metadata_details = {
            'key': record_key,
            'version_id': '',
            'current_version': True,
            'content_type': '',
            'content_encoding': '',
            'metadata': {}
        }
        metadata_details = self.iam.ingest(record, metadata_details)
        epoch_zero = datetime.fromtimestamp(0).replace(tzinfo=tzutc())
        metadata_details['last_modified'] = (metadata_details['last_modified'] - epoch_zero).total_seconds()
        if 'response_metadata' in metadata_details.keys():
            del metadata_details['response_metadata']

    # determine current version from version id
        if record_version and version_check:
            version_kwargs = {
                'Bucket': bucket_name,
                'Prefix': record_key
            }
            try:
                version_check = self.connection.list_object_versions(**version_kwargs)
                for version in version_check['Versions']:
                    if version['VersionId'] == metadata_details['version_id']:
                        metadata_details['current_version'] = version['IsLatest']
                        break
            except:
                raise AWSConnectionError(title)

        return metadata_details

    def read_record(self, bucket_name, record_key, record_version='', version_check=False):

        '''
            a method for retrieving data of record from AWS S3
            
        :param bucket_name: string with name of bucket
        :param record_key: string with name of key (path) for record
        :param record_version: [optional] string with aws id of version of record
        :param version_check: [optional] boolean to enable current version check
        :return: byte data for record, dictionary with metadata details
        '''

        title = '%s.read_record' % self.__class__.__name__
        
        from datetime import datetime
        from dateutil.tz import tzutc
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'record_key': record_key,
            'record_version': record_version
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))
                
    # create key word argument dictionary
        record_kwargs = {
            'Bucket': bucket_name,
            'Key': record_key
        }
        if record_version:
            record_kwargs['VersionId'] = record_version

    # server-side decryption key with request
    #     if password:
    #         pass_title = 'decryption password' + title
    #         key_b64, digest_b64 = self.input.password(password, pass_title)
    #         kw_args['SSECustomerAlgorithm'] = 'AES256'
    #         kw_args['SSECustomerKey'] = key_b64
    #         kw_args['SSECustomerKeyMD5'] = digest_b64

    # send request for record data
        try:
            response = self.connection.get_object(**record_kwargs)
        except:
            raise AWSConnectionError(title)

    # parse record data from response data
        record_data = response['Body'].read()
        del response['Body']

    # create metadata from response
        metadata_details = {
            'key': record_key,
            'version_id': '',
            'current_version': True,
            'content_type': '',
            'content_encoding': '',
            'metadata': {}
        }
        metadata_details = self.iam.ingest(response, metadata_details)
        epoch_zero = datetime.fromtimestamp(0).replace(tzinfo=tzutc())
        metadata_details['last_modified'] = (metadata_details['last_modified'] - epoch_zero).total_seconds()
        if 'response_metadata' in metadata_details.keys():
            del metadata_details['response_metadata']

    # determine current version from version id
        if record_version and version_check:
            version_kwargs = {
                'Bucket': bucket_name,
                'Prefix': record_key
            }
            try:
                version_check = self.connection.list_object_versions(**version_kwargs)
                for version in version_check['Versions']:
                    if version['VersionId'] == metadata_details['version_id']:
                        metadata_details['current_version'] = version['IsLatest']
                        break
            except:
                raise AWSConnectionError(title)

        return record_data, metadata_details

    def delete_record(self, bucket_name, record_key, record_version=''):

        '''
            a method for deleting an object record in s3

        :param bucket_name: string with name of bucket
        :param record_key: string with key value of record
        :param record_version: [optional] string with aws id of version of record
        :return: dictionary with status of delete request
        '''

        title = '%s.delete_record' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'record_key': record_key,
            'record_version': record_version
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))
                
    # create key word argument dictionary
        delete_kwargs = {
            'Bucket': bucket_name,
            'Key': record_key
        }
        if record_version:
            delete_kwargs['VersionId'] = record_version

    # send request to delete record
        try:
            response = self.connection.delete_object(**delete_kwargs)
        except:
            raise AWSConnectionError(title)

    # report status
        response_details = {
            'version_id': ''
        }
        response_details = self.iam.ingest(response, response_details)
        if 'response_metadata' in response_details.keys():
            del response_details['response_metadata']
        
        return response_details

    def export_records(self, bucket_name, export_path='', overwrite=True):

        '''
            a method to export all the records from a bucket to local files

        :param bucket_name: string with name of bucket
        :param export_path: [optional] string with path to root directory for record dump
        :param overwrite: [optional] boolean to overwrite existing files matching records
        :return: True
        '''

        title = '%s.export_records' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'export_path': export_path
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
    # validate path
        from os import path, makedirs
        if not export_path:
            export_path = './'
        if not path.exists(export_path):
            raise ValueError('%s(export_path="%s") is not a valid path.' % (title, export_path))
        elif not path.isdir(export_path):
            raise ValueError('%s(export_path="%s") must be a directory.' % (title, export_path))
    
    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))

    # retrieve list of records in bucket
        record_list, next_key = self.list_records(bucket_name)
        if next_key:
            record_number = 'first %s' % str(len(record_list))
        else:
            record_number = str(len(record_list))
        plural = ''
        if len(record_list) != 1:
            plural = 's'
        self.iam.printer('Exporting %s record%s from bucket "%s" to path "%s"' % (record_number, plural, bucket_name, export_path), flush=True)

    # define local save function
        def save_to_file(_export_path, _bucket_name, _record_key, _overwrite):
            
            try:
                response = self.connection.get_object(Bucket=_bucket_name,Key=_record_key)
            except:
                raise AWSConnectionError(title)
            record_data = response['Body'].read()
            file_path = path.join(_export_path, _record_key)
            dir_path = path.dirname(file_path)
            if not path.exists(dir_path):
                makedirs(dir_path)
            if path.exists(file_path) and not _overwrite:
                self.iam.printer('.\n%s already exists. File skipped. Continuing.' % file_path, flush=True)
            else:
                with open(file_path, 'wb') as file:
                    file.write(record_data)
                    file.close()
                self.iam.printer('.', flush=True)
            
    # retrieve data for records in bucket
        for record in record_list:
            save_to_file(export_path, bucket_name, record['key'], overwrite)

    # continue exporting records in bucket until all exported
        if next_key:
            while next_key or record_list:
                record_list, next_key = self.list_records(bucket_name)
                if next_key:
                    record_number = 'next %s' % str(len(record_list))
                else:
                    record_number = 'last %s' % str(len(record_list))
                self.iam.printer('.')
                plural = ''
                if len(record_list) != 1:
                    plural = 's'
                self.iam.printer('Exporting %s record%s from bucket "%s" to path "%s"' % (record_number, plural, bucket_name, export_path), flush=True)
                for record in record_list:
                    save_to_file(export_path, bucket_name, record['key'], overwrite)

    # report completion and return true
        self.iam.printer(' done.')
        return True

    def import_records(self, bucket_name, import_path='', overwrite=True):

        '''
            a method to importing records from local files to a bucket

        :param bucket_name: string with name of bucket
        :param export_path: [optional] string with path to root directory of files
        :param overwrite: [optional] boolean to overwrite existing files matching records
        :return: True
        '''

        title = '%s.import_records' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'import_path': import_path
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate path
        from os import path
        if not import_path:
            import_path = './'
        if not path.exists(import_path):
            raise ValueError('%s(import_path="%s") is not a valid path.' % (title, import_path))
        elif not path.isdir(import_path):
            raise ValueError('%s(import_path="%s") must be a directory.' % (title, import_path))
    
    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))

    # create records from walk of local path
        self.iam.printer('Importing records from path "%s" to bucket "%s".' % (import_path, bucket_name), flush=True)
        from labpack.platforms.localhost import localhostClient
        localhost_client = localhostClient()
        import_path = path.abspath(import_path)
        for file_path in localhost_client.walk(import_path):
            relative_path = path.relpath(file_path, import_path)
            try:
                byte_data = open(file_path, 'rb').read()
                self.create_record(bucket_name, relative_path, byte_data, overwrite=overwrite)
                self.iam.printer('.', flush=True)
            except ValueError as err:
                if str(err).find('already contains') > -1:
                    self.iam.printer('.\n%s already exists. Record skipped. Continuing.' % relative_path, flush=True)
                else:
                    raise
            except:
                raise AWSConnectionError(title)

    # report completion and return true
        self.iam.printer(' done.')
        return True

class s3Client(object):
    
    ''' a class of methods to manage file storage on AWS S3 '''
    
    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'collection_name': 'User Data',
            'record_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.ogg',
            'secret_key': '6tZ0rUexOiBcOse2-dgDkbeY',
            'prefix': 'obs/terminal',
            'delimiter': '2016-03-17T17-24-51-687845Z.yaml',
            'encryption': 'lab512',
            'max_results': 1
        },
        'components': {
            '.org_name': {
                'max_length': 58,
                'must_not_contain': ['/', '^\\.']
            },
            '.prod_name': {
                'max_length': 58,
                'must_not_contain': ['/', '^\\.']
            },
            '.collection_name': {
                'max_length': 58,
                'must_not_contain': ['/', '^\\.']
            },
            '.record_key': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            },
            '.secret_key': {
                'must_not_contain': [ '[\\t\\n\\r]' ]
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            }
        }
    }
    
    def __init__(self, access_id, secret_key, region_name, owner_id, user_name, collection_name='', prod_name='', org_name='', access_control='private', version_control=False, log_destination=None, lifecycle_rules=None, tag_list=None, notification_settings=None, region_replication=None, access_policy=None, verbose=True):
    
        title = '%s.__init__' % self.__class__.__name__
        
    # construct boto3 client method
        self.s3 = _s3Client(access_id, secret_key, region_name, owner_id, user_name, verbose)
    
    # construct s3Client fields
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'collection_name': collection_name,
            'prod_name': prod_name,
            'org_name': org_name
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
    # determine defaults
        if not collection_name:
            collection_name = 'User Data'
        if not prod_name:
            prod_name = user_name
        if not org_name:
            org_name = owner_id
    
    # create collection name property
        from copy import deepcopy
        self.collection_name = deepcopy(collection_name)
    
    # construct bucket name
        collection_name = collection_name.replace(' ', '-').lower()
        prod_name = prod_name.replace(' ', '-').lower()
        org_name = org_name.replace(' ', '-').lower()
        self.bucket_name = '%s-%s-%s' % (org_name, prod_name, collection_name)
    
    # create (or update) bucket
        self.s3.list_buckets()
        if self.bucket_name in self.s3.bucket_list:
            self.s3.update_bucket(self.bucket_name, access_control, version_control, log_destination, lifecycle_rules, tag_list, notification_settings, region_replication, access_policy)
        else:
            self.s3.create_bucket(self.bucket_name, access_control, version_control, log_destination, lifecycle_rules, tag_list, notification_settings, region_replication, access_policy)
    
    def _import(self, record_key, record_data, overwrite=True, encryption='', last_modified=0.0, **kwargs):
        
        '''
            a helper method for other storage clients to import into s3
            
        :param record_key: string with key for record
        :param record_data: byte data for body of record
        :param overwrite: [optional] boolean to overwrite existing records
        :param encryption: [optional] string with encryption type add to metadata
        :param kwargs: [optional] keyword arguments from other import methods 
        :return: boolean indicating whether record was imported
        '''

    # define keyword arguments
        from time import time
        create_kwargs = {
            'bucket_name': self.bucket_name,
            'record_key': record_key,
            'record_data': record_data,
            'overwrite': overwrite,
            'record_metadata': { 'last_modified': str(time()) }
        }
    
    # add encryption and last_modified
        if encryption:
            create_kwargs['record_metadata']['encryption'] = encryption
        if last_modified:
            create_kwargs['record_metadata']['last_modified'] = str(last_modified)
            
    # add record mimetype and encoding
        import mimetypes
        guess_mimetype, guess_encoding = mimetypes.guess_type(record_key)
        if not guess_mimetype:
            if record_key.find('.yaml') or record_key.find('.yml'):
                guess_mimetype = 'application/x-yaml'
            if record_key.find('.drep'):
                guess_mimetype = 'application/x-drep'
        if guess_mimetype:
            create_kwargs['record_mimetype'] = guess_mimetype
        if guess_encoding:
            create_kwargs['record_encoding'] = guess_encoding
            
    # create record
        try:
            self.s3.create_record(**create_kwargs)
        except ValueError as err:
            if str(err).find('already contains') > -1:
                self.s3.iam.printer('%s already exists in %s collection. Skipping.' % (record_key, self.bucket_name))
                return False
            # elif str(err).find('exceeds maximum record') > -1:
            #     self.s3.iam.printer('%s exceeds the maximum size for files on S3. Skipping.' % record_key)
            else:
                raise
        except:
            raise

        return True
    
    def exists(self, record_key):
        
        ''' 
            a method to determine if a record exists in collection

        :param record_key: string with key of record
        :return: boolean reporting status
        '''
        
        title = '%s.exists' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # read record headers
        record_status = self.s3.read_headers(self.bucket_name, record_key)
        if record_status:
            return True
        return False
    
    def save(self, record_key, record_data, overwrite=True, secret_key=''):
        
        ''' 
            a method to create a file in the collection folder on S3

        :param record_key: string with name to assign to record (see NOTES below)
        :param record_data: byte data for record body
        :param overwrite: [optional] boolean to overwrite records with same name
        :param secret_key: [optional] string with key to encrypt data
        :return: string with name of record

        NOTE:   record_key may only contain alphanumeric, /, _, . or -
                characters and may not begin with the . or / character.

        NOTE:   using one or more / characters splits the key into
                separate segments. these segments will appear as a
                sub directories inside the record collection and each
                segment is used as a separate index for that record
                when using the list method
                eg. lab/unittests/1473719695.2165067.json is indexed:
                [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
        '''

        title = '%s.save' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key,
            'secret_key': secret_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # validate byte data
        if not isinstance(record_data, bytes):
            raise ValueError('%s(record_data=b"...") must be byte data.' % title)
    
    # encrypt data
        if secret_key:
            from labpack.encryption import cryptolab
            record_data, secret_key = cryptolab.encrypt(record_data, secret_key)
            
    # define keyword arguments
        from time import time
        create_kwargs = {
            'bucket_name': self.bucket_name,
            'record_key': record_key,
            'record_data': record_data,
            'overwrite': overwrite,
            'record_metadata': { 'last_modified': str(time()) }
        }
    
    # add encryption metadata
        if secret_key:
            create_kwargs['record_metadata']['encryption'] = 'lab512'
    
    # add record mimetype and encoding
        import mimetypes
        guess_mimetype, guess_encoding = mimetypes.guess_type(record_key)
        if not guess_mimetype:
            if record_key.find('.yaml') or record_key.find('.yml'):
                guess_mimetype = 'application/x-yaml'
            if record_key.find('.drep'):
                guess_mimetype = 'application/x-drep'
        if guess_mimetype:
            create_kwargs['record_mimetype'] = guess_mimetype
        if guess_encoding:
            create_kwargs['record_encoding'] = guess_encoding
            
    # create record
        self.s3.create_record(**create_kwargs)

        return record_key
    
    def load(self, record_key, secret_key=''):
        
        '''
            a method to retrieve byte data of an S3 record

        :param record_key: string with name of record
        :param secret_key: [optional] string used to decrypt data
        :return: byte data for record body
        '''
        
        title = '%s.load' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key,
            'secret_key': secret_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # retrieve record data from s3
        record_data, record_metadata = self.s3.read_record(self.bucket_name, record_key)
    
    # validate secret key
        error_msg = '%s(secret_key="...") required to decrypt record "%s"' % (title, record_key)
        if 'encryption' in record_metadata['metadata'].keys():
            if record_metadata['metadata']['encryption'] == 'lab512':
                if not secret_key:
                    raise Exception(error_msg)
            else:
                self.s3.iam.printer('[WARNING]: %s uses unrecognized encryption method. Decryption skipped.' % record_key)
                secret_key = ''
                
    # decrypt (if necessary)
        if secret_key:
            from labpack.encryption import cryptolab
            record_data = cryptolab.decrypt(record_data, secret_key)
    
        return record_data
    
    def conditional_filter(self, path_filters):

        ''' a method to construct a conditional filter function for class list method

        :param path_filters: dictionary or list of dictionaries with query criteria
        :return: filter_function object

        path_filters:
        [ { 0: { conditional operators }, 1: { conditional_operators }, ... } ]

        conditional operators:
            "byte_data": false,
            "discrete_values": [ "" ],
            "excluded_values": [ "" ],
            "equal_to": "",
            "greater_than": "",
            "less_than": "",
            "max_length": 0,
            "max_value": "",
            "min_length": 0,
            "min_value": "",
            "must_contain": [ "" ],
            "must_not_contain": [ "" ],
            "contains_either": [ "" ]
        '''

        title = '%s.conditional_filter' % self.__class__.__name__
        
        from labpack.compilers.filters import positional_filter
        filter_function = positional_filter(path_filters, title)
        
        return filter_function
    
    def list(self, prefix='', delimiter='', filter_function=None, max_results=1, previous_key=''):
    
        ''' 
            a method to list keys in the collection

        :param prefix: string with prefix value to filter results
        :param delimiter: string with value results must not contain (after prefix)
        :param filter_function: (positional arguments) function used to filter results
        :param max_results: integer with maximum number of results to return
        :param previous_key: string with key in collection to begin search after
        :return: list of key strings
        
        NOTE:   each key string can be divided into one or more segments
                based upon the / characters which occur in the key string as
                well as its file extension type. if the key string represents
                a file path, then each directory in the path, the file name
                and the file extension are all separate indexed values.

                eg. lab/unittests/1473719695.2165067.json is indexed:
                [ 'lab', 'unittests', '1473719695.2165067', '.json' ]

                it is possible to filter the records in the collection according
                to one or more of these path segments using a filter_function.

        NOTE:   the filter_function must be able to accept an array of positional
                arguments and return a value that can evaluate to true or false.
                while searching the records, list produces an array of strings
                which represent the directory structure in relative path of each
                key string. if a filter_function is provided, this list of strings
                is fed to the filter function. if the function evaluates this input
                and returns a true value the file will be included in the list
                results.
        '''
        
        title = '%s.list' % self.__class__.__name__

    # validate input
        input_fields = {
            'prefix': prefix,
            'delimiter': delimiter,
            'max_results': max_results,
            'record_key': previous_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # construct default response
        results_list = []
        
    # handle filter function filter
        if filter_function:
        
        # validate filter function
            try:
                path_segments = [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
                filter_function(*path_segments)
            except:
                err_msg = '%s(filter_function=%s)' % (title, filter_function.__class__.__name__)
                raise TypeError('%s must accept positional arguments.' % err_msg)
            
        # construct keyword arguments
            list_kwargs = {
                'bucket_name': self.bucket_name,
                'prefix': prefix,
                'delimiter': delimiter
            }
            
        # determine starting key
            starting_key = '1'
            if previous_key:
                previous_kwargs = {}
                previous_kwargs.update(**list_kwargs)
                previous_kwargs['max_results'] = 1
                previous_kwargs['starting_key'] = previous_key
                search_list, next_key = self.s3.list_records(**list_kwargs)
                list_kwargs['starting_key'] = next_key
        
        # iterate filter over collection
            import os
            while starting_key:
                search_list, starting_key = self.s3.list_records(**list_kwargs)
                for record in search_list:
                    record_key = record['key']
                    path_segments = record_key.split(os.sep)
                    if filter_function(*path_segments):
                        results_list.append(record_key)
                    if len(results_list) == max_results:
                        return results_list
        
    # handle other filters
        else:
            
        # construct keyword arguments
            list_kwargs = {
                'bucket_name': self.bucket_name,
                'prefix': prefix,
                'delimiter': delimiter,
                'max_results': max_results
            }
        
        # determine starting key
            if previous_key:
                previous_kwargs = {}
                previous_kwargs.update(**list_kwargs)
                previous_kwargs['max_results'] = 1
                previous_kwargs['starting_key'] = previous_key
                search_list, starting_key = self.s3.list_records(**list_kwargs)
                list_kwargs['starting_key'] = starting_key
    
        # retrieve results 
            search_list, starting_key = self.s3.list_records(**list_kwargs)
    
        # construct result list
            for record in search_list:
                results_list.append(record['key'])
        
        return results_list
    
    def delete(self, record_key):
        
        ''' a method to delete a record from S3

        :param record_key: string with key of record
        :return: string reporting outcome
        '''
    
        title = '%s.delete' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # delete record
        try:
            self.s3.delete_record(self.bucket_name, record_key)
        except:
            if not self.exists(record_key):
                exit_msg = '%s does not exist.' % record_key
                return exit_msg
            raise
        
        exit_msg = '%s has been deleted.' % record_key
        return exit_msg
    
    def remove(self):
        
        ''' 
            a method to remove collection and all records in the collection

        :return: string with confirmation of deletion
        '''
    
        title = '%s.remove' % self.__class__.__name__
    
    # request bucket delete 
        self.s3.delete_bucket(self.bucket_name)

    # return confirmation
        exit_msg = '%s collection has been removed from S3.' % self.bucket_name
        return exit_msg
    
    def export(self, storage_client, overwrite=True):
    
        '''
            a method to export all the records in collection to another platform
            
        :param storage_client: class object with storage client methods
        :return: string with exit message
        '''
        
        title = '%s.export' % self.__class__.__name__
        
    # validate storage client
        method_list = [ 'save', 'load', 'list', 'export', 'delete', 'remove', '_import', 'collection_name' ]
        for method in method_list:
            if not getattr(storage_client, method, None):
                from labpack.parsing.grammar import join_words
                raise ValueError('%s(storage_client=...) must be a client object with %s methods.' % (title, join_words(method_list)))
    
    # define copy record function
        def _copy_record(_record, _storage_client):
            record_key = _record['key']
            record_data, record_metadata = self.s3.read_record(self.bucket_name, record_key)
            encryption = ''
            if 'encryption' in record_metadata['metadata'].keys():
                encryption = record_metadata['metadata']['encryption']
            last_modified = 0.0
            if 'last_modified' in record_metadata['metadata'].keys():
                try:
                    last_modified = float(record_metadata['metadata']['last_modified'])
                except:
                    pass
            outcome = _storage_client._import(record_key, record_data, overwrite=overwrite, encryption=encryption, last_modified=last_modified)
            return outcome
            
    # retrieve list of records in bucket
        count = 0
        skipped = 0
        record_list, next_key = self.s3.list_records(self.bucket_name)
        for record in record_list:
            outcome = _copy_record(record, storage_client)
            if outcome:
                count += 1
            else:
                skipped += 1
        
    # continue through bucket
        if next_key:
            while next_key:
                record_list, next_key = self.s3.list_records(self.bucket_name, starting_key=next_key)
                for record in record_list:
                    outcome = _copy_record(record, storage_client)
                    if outcome:
                        count += 1
                    else:
                        skipped += 1
    
    # report outcome
        from os import path
        plural = ''
        skip_insert = ''
        new_root, new_folder = path.split(storage_client.collection_folder)
        if count != 1:
            plural = 's'
        if skipped > 0:
            skip_plural = ''
            if skipped > 1:
                skip_plural = 's'
            skip_insert = ' %s record%s skipped to avoid overwrite.' % (str(skipped), skip_plural)
        exit_msg = '%s record%s exported to %s.%s' % (str(count), plural, new_folder, skip_insert)
        return exit_msg
