__author__ = 'rcj1492'
__created__ = '2015.08'
__license__ = 'MIT'

'''
PLEASE NOTE:    ec2 package requires the boto3 module.

(all platforms) pip3 install boto3
'''

try:
    import boto3
except:
    import sys
    print('ec2 package requires the boto3 module. try: pip3 install boto3')
    sys.exit(1)

from labpack.authentication.aws.iam import AWSConnectionError

class s3Client(object):

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

    # retrieve list of objects in bucket
        record_keys = []
        record_list, next_key = self.list_versions(bucket_name)
        for record in record_list:
            details = {
                'Key': record['key'],
                'VersionId': record['version_id']
            }
            record_keys.append(details)

    # delete objects in bucket
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

    def list_records(self, bucket_name, prefix='', suffix='', max_results=1, starting_key=''):

        '''
            a method for retrieving a list of the versions of records in a bucket

        :param bucket_name: string with name of bucket
        :param prefix: [optional] string with value limiting results to key prefix
        :param suffix: [optional] string with value limiting results to key suffix
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
            'suffix': suffix,
            'max_results': max_results,
            'starting_key': starting_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # check to see if bucket exists:
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
        if suffix:
            kw_args['Delimiter'] = suffix
        if max_results:
            kw_args['MaxKeys'] = max_results

    # send request for objects
        record_list = []
        next_key = ''
        try:
            response = self.connection.list_objects(**kw_args)
        except:
            raise AWSConnectionError('listObjects')

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

    def list_versions(self, bucket_name, prefix='', suffix='', max_results=1, starting_key='', starting_version=''):

        '''
            a method for retrieving a list of the versions of records in a bucket

        :param bucket_name: string with name of bucket
        :param prefix: [optional] string with value limiting results to key prefix
        :param suffix: [optional] string with value limiting results to key suffix
        :param max_results: [optional] integer with max results to return
        :param starting_key: [optional] string with key value to continue search with
        :param starting_version: [optional] string with version id to continue search with
        :return: list of results with key, size and date, string with ending key value
        '''

        title = '%s.list_versions' % self.__class__.__name__
        
        from datetime import datetime
        from dateutil.tz import tzutc
        
        
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'prefix': prefix,
            'suffix': suffix,
            'max_results': max_results,
            'starting_key': starting_key,
            'starting_version': starting_version
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
        if starting_version or starting_key:
            if not starting_version or not starting_key:
                raise ValueError('%s inputs starting_key and starting_version each require the other.' % title)

    # check to see if bucket exists:
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
        if suffix:
            kw_args['Delimiter'] = suffix
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
                details['current_version'] = details['IsLatest']
                del details['IsLatest']
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
                details['current_version'] = details['IsLatest']
                del details['IsLatest']
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

    def create_record(self, bucket_name, record_key, record_data, record_metadata=None, overwrite=True, secret_key=''):

        '''
            a method for adding a record to an S3 bucket
            
        :param bucket_name: string with name of bucket
        :param record_key: string with name of key (path) for record
        :param record_data: byte data for record
        :param record_metadata: [optional] dictionary with metadata to attach to record
        :param overwrite: [optional] boolean to overwrite any existing record
        :param secret_key: [optional] string with key to encrypt the data
        :return: string with name of record key
        '''
        
        title = '%s.create_record' % self.__class__.__name__

        import sys
        from hashlib import md5
        from base64 import b64encode
    
    # define size limitations
        metadata_max = self.fields.metadata['limits']['metadata_max_bytes']
        record_max = self.fields.metadata['limits']['record_max_bytes']
        record_optimal = self.fields.metadata['limits']['metadata_optimal_bytes']
        
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
            import json
            metadata_size = sys.getsizeof(json.dumps(record_metadata).encode('utf-8'))
            if metadata_size > metadata_max:
                raise ValueError('%s(record_metadata={...}) cannot be greater than 2024 characters.' % title)
    
    # verify existence of bucket
        if not bucket_name in self.bucket_list:
            if not bucket_name in self.list_buckets():
                raise ValueError('S3 bucket "%s" does not exist in aws region %s.' % (bucket_name, self.iam.region_name))
    
    # verify overwrite condition
        if not overwrite:
            record_headers = self.read_headers(bucket_name, record_key)
            if record_headers:
                raise ValueError('S3 bucket "%s" already contains a record for key "%s"' % (bucket_name, record_key))
                
    # encrypt record
        if secret_key:
            from labpack.encryption import cryptolab
            record_data = cryptolab.encrypt(record_data, secret_key)
            
    # validate size of record
        record_size = sys.getsizeof(record_data)
        error_prefix = '%s(record_key="%s", record_data=...)' % (title, record_key)
        if record_size > record_max:
            raise ValueError('%s exceeds maximum record data size of %s bytes.' % (error_prefix, record_max))
        elif record_size > record_optimal:
            self.iam.printer('[WARNING] %s exceeds optimal record data size of %s bytes.' % (error_prefix, record_max))

    # determine content encoding
        content_type = ''
        content_encoding = ''
    # parse extension type
        file_extensions = {
            "json": ".+\\.json$",
            "json.gz": ".+\\.json\\.gz$",
            "yaml": ".+\\.ya?ml$",
            "yaml.gz": ".+\\.ya?ml\\.gz$",
            "drep": ".+\\.drep$"
        }
        import re
        for key, value in file_extensions.items():
            file_pattern = re.compile(value)
            if file_pattern.findall(record_key):
                if key.find('json') > -1:
                    content_type = 'application/json'
                elif key.find('yaml') > -1:
                    content_type = 'application/x-yaml'
                elif key.find('drep') > -1:
                    content_type = 'application/x-drep'
                if key.find('gz') > -1:
                    content_encoding = 'gzip'
                    
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
        if content_type:
            create_kwargs['ContentType'] = content_type
        if content_encoding:
            create_kwargs['ContentEncoding'] = content_encoding

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

    def read_headers(self, bucket_name, record_key, version_id='', version_check=True):

        '''
            a method for retrieving the headers of a record from s3

        :param record_key: string with key value of record
        :param object_map: dictionary with object definitions
        :param version_id: [optional] string with aws id of version of record
        :param version_check: [optional] boolean to turn off currentVersion check
        :return: dictionary with headers of record
        '''

    #validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = ' for bucket "%s"' % bucket_name
        self.input.keyName(record_key, 'key name' + title)

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': record_key
        }
        if version_id:
            self.input.keyName(version_id, 'version id' + title)
            kw_args['VersionId'] = version_id

    # send request for record header
        try:
            response = self.connection.head_object(**kw_args)
        except:
            raise AWSConnectionError('retrieveRecord')

    # create meta data from response
        meta_data = {
            'objectKey': record_key,
            'objectSize': response['ContentLength'],
            'indexMetaData': {},
            'versionID': version_id,
            'currentVersion': True,
            'contentEncoding': '',
            'contentType': ''
        }
        date_time = response['LastModified']
        epoch_zero = datetime.datetime.fromtimestamp(0).replace(tzinfo=tzutc())
        meta_data['lastModified'] = (date_time - epoch_zero).total_seconds()
        if 'VersionId' in response:
            meta_data['versionID'] = response['VersionId']
        if 'ContentEncoding' in response:
            meta_data['contentEncoding'] = response['ContentEncoding']
        if 'Metadata' in response:
            meta_data['indexMetaData'] = response['Metadata']
        if 'ContentType' in response:
            meta_data['contentType'] = response['ContentType']

    # determine currentVersion from version id
        if version_id and version_check:
            kw_args = {
                'Bucket': bucket_name,
                'Prefix': meta_data['objectKey']
            }
            try:
                version_check = self.connection.list_object_versions(**kw_args)
                for version in version_check['Versions']:
                    if version['VersionId'] == meta_data['versionID']:
                        meta_data['currentVersion'] = version['IsLatest']
            except:
                raise AWSConnectionError('listVersions')

        return meta_data

    def recordDetails(self, record_key, object_map, version_id='', password=''):

        '''
            a method for retrieving the attributes of a record from s3

        :param record_key: string with key value of record
        :param object_map: dictionary with object definitions
        :param version_id: [optional] string with aws id of version of record
        :param password: [optional] string to use for sha256 hash for aes256 bit key
        :return: dictionary with details of record
        '''

    #validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = ' for bucket "%s"' % bucket_name
        self.input.keyName(record_key, 'key name' + title)

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': record_key
        }
        if version_id:
            self.input.keyName(version_id, 'version id' + title)
            kw_args['VersionId'] = version_id

    # server-side decryption key with request
    #     if password:
    #         pass_title = 'decryption password' + title
    #         key_b64, digest_b64 = self.input.password(password, pass_title)
    #         kw_args['SSECustomerAlgorithm'] = 'AES256'
    #         kw_args['SSECustomerKey'] = key_b64
    #         kw_args['SSECustomerKeyMD5'] = digest_b64

    # send request for record data
        try:
            response = self.connection.get_object(**kw_args)
        except:
            raise AWSConnectionError('retrieveRecord')

    # create record details from response data
        record_data = response['Body'].read()

    # create meta data from response
        meta_data = {
            'objectKey': record_key,
            'objectSize': 0,
            'indexMetaData': {},
            'versionID': version_id,
            'currentVersion': True,
            'contentType': '',
            'contentEncoding': ''
        }
        date_time = response['LastModified']
        epoch_zero = datetime.datetime.fromtimestamp(0).replace(tzinfo=tzutc())
        meta_data['lastModified'] = (date_time - epoch_zero).total_seconds()
        if 'ContentLength' in response:
            meta_data['objectSize'] = response['ContentLength']
        if 'Metadata' in response:
            meta_data['indexMetaData'] = response['Metadata']

    # determine currentVersion from version id
        if version_id:
            kw_args = {
                'Bucket': bucket_name,
                'Prefix': meta_data['objectKey']
            }
            try:
                version_check = self.connection.list_object_versions(**kw_args)
                for version in version_check['Versions']:
                    if version['VersionId'] == meta_data['versionID']:
                        meta_data['currentVersion'] = version['IsLatest']
            except:
                raise AWSConnectionError('listVersions')

    # TODO: client-side decrypt incoming data
        if 'ContentEncryption' in meta_data['indexMetaData']:
            if not password:
                raise Exception('A password must be included to decrypt details%s record %s' % (title, record_key))
            pass_title = 'decryption password' + title
            # key_b64, digest_b64 = self.input.password(password, pass_title)
            # decipher aes256 cipher text with sha256 hash

    # decompress and deserialize the data
        record_details = {}
        if 'ContentEncoding' in response:
            meta_data['contentEncoding'] = response['ContentEncoding']
            if response['ContentEncoding'] == 'gzip':
                record_data = gzip.decompress(record_data)
        if 'ContentType' in response:
            meta_data['contentType'] = response['ContentType']
            if response['ContentType'] == 'application/json':
                record_details = json.loads(record_data.decode())

        return record_details, meta_data

    def deleteRecord(self, record_key, object_map, version_id=''):

        '''
            a method for deleting an object record in s3

        :param record_key: string with key value of record
        :param object_map: dictionary with object definitions
        :param version_id: [optional] string with aws id of version of record
        :return: True
        '''

     #validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = ' for bucket "%s"' % bucket_name
        self.input.keyName(record_key, 'key name' + title)

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': record_key
        }
        if version_id:
            self.input.keyName(version_id, 'version id' + title)
            kw_args['VersionId'] = version_id

    # send request to delete record
        try:
            self.connection.delete_object(**kw_args)
        except:
            raise AWSConnectionError('deleteRecord')

        return True

    def exportRecords(self, object_map, export_path='', overwrite=False):

        '''
            a method to export all the records from a bucket to local files

        :param object_map: dictionary with object definitions
        :param export_path: [optional] string with path to root directory for record dump
        :param overwrite: [optional] boolean to overwrite existing files matching records
        :return: True
        '''

    # validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = 'bucket "%s" in exportRecords request' % bucket_name
        if export_path:
            slash = re.compile('/$')
            if not slash.search(export_path):
                export_path = export_path + '/'
            self.input.path(export_path, 'export path for ' + title)
        else:
            export_path = './'

    # check for existence of bucket
        if not bucket_name in self.listBuckets():
            raise Exception('%s does not exist.' % title)

    # retrieve list of records in bucket
        record_list, next_key = self.listObjects(bucket_name)
        if next_key:
            record_number = 'first %s' % str(len(record_list))
        else:
            record_number = str(len(record_list))
        plural = ''
        if len(record_list) != 1:
            plural = 's'
        self.iam.printer('Exporting %s record%s from bucket "%s" to path %s.' % (record_number, plural, bucket_name, export_path), end='', flush=True)

    # retrieve data for records in bucket
        for record in record_list:
            try:
                response = self.connection.get_object(Bucket=bucket_name,Key=record['objectKey'])
            except:
                raise AWSConnectionError('retrieveRecord')
            record_data = response['Body'].read()
            file_path = export_path + record['objectKey']
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if os.path.exists(file_path) and not overwrite:
                self.iam.printer('%s already exists. File skipped.' % file_path, end='', flush=True)
            else:
                with open(file_path, 'wb') as file:
                    file.write(record_data)
                    file.close()
            self.iam.printer('.', end='', flush=True)

    # continue exporting records in bucket until all exported
        if next_key:
            while next_key or record_list:
                record_list, next_key = self.listObjects(bucket_name)
                if next_key:
                    record_number = 'next %s' % str(len(record_list))
                else:
                    record_number = 'last %s' % str(len(record_list))
                self.iam.printer('.')
                plural = ''
                if len(record_list) != 1:
                    plural = 's'
                self.iam.printer('Exporting %s record%s from bucket "%s" to path %s' % (record_number, plural, bucket_name, export_path), end='', flush=True)
                for record in record_list:
                    try:
                        response = self.connection.get_object(Bucket=bucket_name,Key=record['objectKey'])
                    except:
                        raise AWSConnectionError('retrieveRecord')
                    record_data = response['Body'].read()
                    file_path = export_path + record['objectKey']
                    dir_path = os.path.dirname(file_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    if os.path.exists(file_path) and not overwrite:
                        self.iam.printer('%s already exists. File skipped.' % file_path, end='', flush=True)
                    else:
                        with open(file_path, 'wb') as file:
                            file.write(record_data)
                            file.close()
                    self.iam.printer('.', end='', flush=True)

    # report completion and return true
        self.iam.printer(' Done.')
        return True

    def importRecords(self, object_map, import_path='', overwrite=False):

        '''
            a method to importing records from local files to a bucket

        :param object_map: dictionary with object definitions
        :param import_path: [optional] string with path to root of record file structure
        :param overwrite: [optional] boolean to overwrite records matching existing files
        :return: True
        '''

    # validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = 'bucket "%s" in importRecords request' % bucket_name
        if import_path:
            slash = re.compile('/$')
            if not slash.search(import_path):
                import_path = import_path + '/'
        else:
            import_path = './'
        self.input.path(import_path, 'import path for ' + title)

    # check for existence of bucket
        if bucket_name not in self.listBuckets():
            raise Exception('%s does not exist.' % title)

    # mini-method to create a record
        def createRecord(record_details, object_map, overwrite=False):
            results = []
            index = object_map['indexing']
            record_key = ''
            for component in index['key']:
                if component == '/':
                    record_key += component
                else:
                    record_key += record_details[component]
            record_key = record_key + '.json.gz'
            bucket_name = object_map['bucket']['bucketName']
            if not overwrite:
                results, next = self.listObjects(bucket_name, record_key)
            if not overwrite and results:
                self.iam.printer('%s already exists. Record skipped.' % record_key, end='', flush=True)
            else:
                self.addRecord(record_details, object_map)
                self.iam.printer('.', end='', flush=True)

    # mini-method to open record from a file
        def openRecord(file_path, object_map, overwrite=False):
            try:
                record_data = open(file_path, 'rb').read()
                record_bytes = gzip.decompress(record_data)
                record_details = json.loads(record_bytes.decode())
                createRecord(record_details, object_map, overwrite)
            except:
                self.iam.printer('[WARNING]: %s does not have a compatible record format. Skipped.' % file_path, end='', flush=True)

    # mini-method to recursively find files and file path
        def findFiles(root_path, object_map, overwrite=False):
            for object in os.listdir(root_path):
                new_path = deepcopy(root_path) + object
                if os.path.isdir(new_path):
                    findFiles(new_path + '/', object_map, overwrite)
                else:
                    openRecord(new_path, object_map, overwrite)

    # run creation methods
        self.iam.printer('Importing records from path %s to bucket "%s".' % (import_path, bucket_name), end='', flush=True)
        findFiles(import_path, object_map, overwrite)

    # report completion and return true
        self.iam.printer(' Done.')
        return True

if __name__ == '__main__':
    
# test instantiation
    from pprint import pprint
    from labpack.records.settings import load_settings
    aws_cred = load_settings('../../../../cred/awsLab.yaml')
    client_kwargs = {
        'access_id': aws_cred['aws_access_key_id'],
        'secret_key': aws_cred['aws_secret_access_key'],
        'region_name': aws_cred['aws_default_region'],
        'owner_id': aws_cred['aws_owner_id'],
        'user_name': aws_cred['aws_user_name']
    }
    s3_client = s3Client(**client_kwargs)

# test list bucket and verify unittesting is clean
    bucket_list = s3_client.list_buckets()
    bucket_name = 'collective-acuity-labpack-unittest-main'
    log_name = 'collective-acuity-labpack-unittest-log'
    # assert bucket_name not in bucket_list
    # assert log_name not in bucket_list
    for bucket in (bucket_name, log_name):
        s3_client.delete_bucket(bucket)

# test create buckets
    simple_kwargs = { 'bucket_name': bucket_name }
    log_kwargs = {
        'bucket_name': log_name,
        'access_control': 'log-delivery-write'
    }
    main_kwargs = {
        'bucket_name': bucket_name,
        'version_control': True,
        'tag_list': [ 
            { 'key': 'Env', 'value': 'test' }, 
            { 'key': 'BuildDate', 'value': 'now' },
            { 'key': 'Chance', 'value': 'go' },
            { 'key': 'Date', 'value': 'then' },
            { 'key': 'First', 'value': '1' },
            { 'key': 'Second', 'value': '2' }
        ],
        'lifecycle_rules': [ { 
            "action": "archive",
            "prefix": "test/",
            "longevity": 180,
            "current_version": True 
        } ],
        'log_destination': {
            'name': log_name,
            'prefix': 'test/'
        }
    }
    s3_client.create_bucket(**simple_kwargs)
    s3_client.create_bucket(**log_kwargs)

# test update bucket
    s3_client.update_bucket(**main_kwargs)
    bucket_details = s3_client.read_bucket(bucket_name)
    assert bucket_details['version_control']

# remove test buckets
    for bucket in (bucket_name, log_name):
        s3_client.delete_bucket(bucket)    


    # import json
    # from copy import deepcopy
    # objectMap = json.loads(open('../models/s3-obj-model.json').read())
    # logMap = deepcopy(objectMap)
    # logMap['bucket']['bucketName'] = 'useast1-collective-acuity-test-log'
    # logMap['bucket']['accessControl'] = 'log-delivery-write'
    # logMap['bucket']['versionControl'] = False
    # logMap['bucket']['logDestination'] = {}
    # logMap['bucket']['lifecycleRules'] = []
    # logMap['bucket']['bucketTags'] = []
    # logMap['bucket']['notificationSettings'] = []
    # testBuckets = [ logMap['bucket']['bucketName'], objectMap['bucket']['bucketName'] ]
    # for name in testBuckets:
    #     assert name not in self.listBuckets() # prevent deletion of live data
    # for bucket in testBuckets:
    #     self.deleteBucket(bucket)
    # self.createBucket(logMap)
    # self.createBucket(objectMap)
    # recordDetails = objectMap['details']
    # self.addRecord(recordDetails, objectMap)
    # keyName = self.addRecord(recordDetails, objectMap)
    # meta_data = self.recordHeaders(keyName, objectMap)
    # assert meta_data['lastModified']
    # bucketList = self.listBuckets()
    # for name in testBuckets:
    #     assert name in bucketList
    # recordList, nextKey = self.listObjects(testBuckets[1])
    # assert recordList[0]['objectKey'] == keyName
    # data, meta_data = self.recordDetails(recordList[0]['objectKey'], objectMap)
    # assert data
    # assert meta_data
    # newRecord = deepcopy(recordDetails)
    # newRecord[objectMap['indexing']['key'][0]] = 'new'
    # self.addRecord(newRecord, objectMap)
    # self.exportRecords(objectMap, '../data', overwrite=True)
    # self.exportRecords(objectMap, '../data')
    # self.importRecords(objectMap, '../data')
    # self.importRecords(objectMap, '../data', overwrite=True)
    # self.deleteRecord(recordList[0]['objectKey'], objectMap)
    # versionList, nextKey = self.listVersions(testBuckets[1])
    # self.recordDetails(versionList[1]['objectKey'], objectMap, version_id=versionList[1]['versionID'])
    # self.deleteRecord(versionList[1]['objectKey'], objectMap, versionList[1]['versionID'])
    # self.deleteBucket(testBuckets[1])
    # self.createBucket(objectMap)
    # self.importRecords(objectMap, '../data')
    # recordList, nextKey = self.handler(self.listObjects(objectMap['bucket']['bucketName']))
    # assert recordList
    # updateMap = {}
    # updateMap['indexing'] = objectMap['indexing']
    # updateMap['details'] = objectMap['details']
    # updateMap['bucket'] = self.bucketDetails(testBuckets[1])
    # updateMap['bucket']['accessControl'] = 'public-read'
    # updateMap['bucket']['versionControl'] = False
    # updateMap['bucket']['logDestination'] = {}
    # updateMap['bucket']['lifecycleRules'] = []
    # updateMap['bucket']['bucketTags'] = []
    # self.updateBucket(updateMap)
    # self.updateBucket(objectMap)
    # for bucket in testBuckets:
    #     self.deleteBucket(bucket)


dummy = ''
# TODO: client side encryption feature for s3 records
# TODO: bucket access policy feature for s3
# TODO: bucket region replication feature for s3
# TODO: bucket notification settings feature integration with AWS event services
# TODO: awsGlacier archive, restore and delete methods
# TODO: more variations for deltaData.unitTest()
