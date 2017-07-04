__author__ = 'rcj1492'
__created__ = '2015.08'

'''
a package of classes for managing interactions with AWS Simple Storage Service

pip install boto3
pip install python-dateutil
https://boto3.readthedocs.org/en/latest/reference/services/dynamodb.html#id1
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html
'''

from awsDB.awsValidation import s3Input, iamInput
import boto3
import os
import re
from dateutil.tz import *
import datetime
import gzip
import json
import hashlib
import base64
import time
from copy import deepcopy

class S3ConnectionError(Exception):
    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to AWS S3 with %s request.' % message
        super(S3ConnectionError, self).__init__(text)
        self.errors = errors

class awsS3(object):

    '''
        a class of methods for interacting with AWS Simple Storage Service

        dependencies:
            from awsDB.awsValidation import s3Input, iamInput
            import boto3
            import re
            import os
            import pytest
            from dateutil.tz import *
            import datetime
            import gzip
            import json
            import hashlib
            import base64
            from copy import deepcopy
    '''

    def __init__(self, aws_credentials, aws_rules, aws_region=''):

        '''
            a method for initializing the connection to S3

            checks for environmental variables:
                'OS' to determine live or localhost endpoint
                'LAB_REMOTE_DB_TESTING' to determine remote testing endpoint
        :param aws_credentials: dictionary with AWS credentials
        :param aws_rules: dictionary with AWS data rules
        :param aws_region: [optional] string with AWS region
        '''

    # validate inputs and create base methods
        self.cred = iamInput(aws_rules).credentials(aws_credentials)
        self.input = s3Input(aws_rules)
        self.rules = aws_rules

    # change region environment variable
        if aws_region:
            region = self.input.region(aws_region)
            self.cred['AWS_DEFAULT_REGION'] = aws_region

    # construct s3 client connection
        for key, value in self.cred.items():
            os.environ[key] = value
        self.connection = boto3.client('s3')

    def listBuckets(self):

        '''
            a method to retrieve a list of buckets on s3

        :return: list of buckets
        '''

        bucket_list = []

    # send request to s3
        try:
            response = self.connection.list_buckets()
        except:
            raise S3ConnectionError(self.listBuckets.__name__)

    # create list from response
        for bucket in response['Buckets']:
            bucket_list.append(bucket['Name'])

        return bucket_list

    def bucketDetails(self, bucket_name):

        '''
            a method to retrieve properties of a bucket in s3

        :param bucket_name: string with name of bucket
        :return: dictionary with details of bucket
        '''

    # validate input
        self.input.bucketName(bucket_name)

    # validate existence of bucket
        if not bucket_name in self.listBuckets():
            raise ValueError('\nS3 Bucket "%s" does not exist.' % bucket_name)

    # create details dictionary
        bucket_details = {
            'bucketName': bucket_name,
            'accessControl': 'private',
            'versionControl': False,
            'logDestination': {},
            'lifecycleRules': [],
            'bucketTags': [],
            'notificationSettings': [],
            'regionReplication': {},
            'accessPolicy': {}
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
                        bucket_details['accessControl'] = 'public-read-write'
                    else:
                        bucket_details['accessControl'] = 'public-read'
                elif log_delivery:
                    bucket_details['accessControl'] = 'log-delivery-write'
                else:
                    bucket_details['accessControl'] = 'authenticated-read'
        except:
            raise S3ConnectionError('bucketDetails access control')

    # retrieve version control details
        try:
            response = self.connection.get_bucket_versioning( Bucket=bucket_name )
            if 'Status' in response.keys():
                if response['Status'] == 'Enabled':
                    bucket_details['versionControl'] = True
        except:
            raise S3ConnectionError('bucketDetails version control')

    # retrieve log destination details
        try:
            response = self.connection.get_bucket_logging( Bucket=bucket_name )
            if 'LoggingEnabled' in response:
                res = response['LoggingEnabled']
                bucket_details['logDestination']['bucketName'] = res['TargetBucket']
                bucket_details['logDestination']['prefix'] = res['TargetPrefix']
        except:
            raise S3ConnectionError('bucketDetails logging')

    # retrieve lifecycle rules details
        try:
            response = self.connection.get_bucket_lifecycle( Bucket=bucket_name )
            for rule in response['Rules']:
                if rule['Status'] == 'Enabled':
                    details = { "prefix": rule['Prefix'] }
                    if 'Transition' in rule.keys():
                        details['longevity'] = rule['Transition']['Days']
                        details['currentVersion'] = True
                        details['action'] = 'archive'
                    elif 'Expiration' in rule.keys():
                        details['longevity'] = rule['Expiration']['Days']
                        details['currentVersion'] = True
                        details['action'] = 'delete'
                    elif 'NoncurrentVersionTransition' in rule.keys():
                        details['longevity'] = rule['NoncurrentVersionTransition']['NoncurrentDays']
                        details['currentVersion'] = False
                        details['action'] = 'archive'
                    elif 'NoncurrentVersionExpiration' in rule.keys():
                        details['longevity'] = rule['NoncurrentVersionExpiration']['NoncurrentDays']
                        details['currentVersion'] = False
                        details['action'] = 'delete'
                    bucket_details['lifecycleRules'].append(details)
        except:
            pass

    # retrieve bucket tag details
        try:
            response = self.connection.get_bucket_tagging( Bucket=bucket_name )
            for tag in response['TagSet']:
                bucket_details['bucketTags'].append(tag)
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
                    bucket_details['notificationSettings'].append(details)
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
                    bucket_details['notificationSettings'].append(details)
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
                    bucket_details['notificationSettings'].append(details)
        except:
            raise S3ConnectionError('bucketDetails notification settings')

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

        return bucket_details

    def createBucket(self, object_map):

        '''
            a method for creating a bucket in s3

            :param object_map: dictionary with bucket, metadata and object definitions
            :return: object_map
        '''

    # validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        aws_region = os.environ.get('AWS_DEFAULT_REGION')
        access_control = object_map['bucket']['accessControl']
        version_control = object_map['bucket']['versionControl']
        log_destination = object_map['bucket']['logDestination']
        lifecycle_rules = object_map['bucket']['lifecycleRules']
        bucket_tags = object_map['bucket']['bucketTags']
        notification_settings = object_map['bucket']['notificationSettings']
        region_replication = {}
        access_policy = {}

    # check to see if required buckets already exists
        response = self.listBuckets()
        max_buckets = self.rules['s3']['bucket']['maxNumberPerAccount']
        if bucket_name in response:
            raise ValueError('\nS3 Bucket "%s" already exists.' % bucket_name)
        elif len(response) >= max_buckets:
            raise Exception('\nS3 account already at maximum %s buckets.' % max_buckets)
        if log_destination:
            log_name = log_destination['bucketName']
            if not log_name in response:
                if log_name != bucket_name:
                    raise ValueError('\nS3 Bucket "%s" for logging does not exist.' % log_name)
            else:
                response = self.bucketDetails(log_name)
                if response['accessControl'] != 'log-delivery-write':
                    raise ValueError('\nS3 Bucket "%s" for logging does not have "log-delivery-write" access control.' % log_name)

    # TODO: check to see if required notification arns exist
        if notification_settings:
            for notification in notification_settings:
                arn_id = notification['arn']

    # create key word arguments dictionary
        kw_args = {
            'Bucket': bucket_name,
            'ACL': access_control
        }
        if not aws_region == 'us-east-1':
            kw_args['CreateBucketConfiguration'] = { 'LocationConstraint': aws_region }

    # send request to s3
        print('Creating bucket "%s".' % bucket_name, end='', flush=True)
        try:
            response = self.connection.create_bucket(**kw_args)
        except:
            raise S3ConnectionError('createBucket')

    # if true, activate version_control attribute
        if version_control:
            try:
                self.connection.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={ 'Status': 'Enabled' }
                )
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket versionControl')

    # if present, direct bucket logging to bucket location
        if log_destination:
            try:
                kw_args = {
                    'Bucket': bucket_name,
                    'BucketLoggingStatus': {
                        'LoggingEnabled': {
                            'TargetBucket': log_destination['bucketName']
                        }
                    }
                }
                if log_destination['prefix']:
                    kw_args['BucketLoggingStatus']['LoggingEnabled']['TargetPrefix'] = log_destination['prefix']
                self.connection.put_bucket_logging(**kw_args)
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket logDestination')

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
                    if rule['currentVersion']:
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
                    if rule['currentVersion']:
                        details['Expiration'] = { 'Days': rule['longevity'] }
                    else:
                        details['NoncurrentVersionExpiration'] = { 'NoncurrentDays': rule['longevity'] }
                kw_args['LifecycleConfiguration']['Rules'].append(details)
            try:
                response = self.connection.put_bucket_lifecycle(**kw_args)
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket lifecycle')

    # if present, assign tags to bucket
        if bucket_tags:
            try:
                self.connection.put_bucket_tagging(
                    Bucket=bucket_name,
                    Tagging={ 'TagSet': bucket_tags }
                )
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket bucketTags')

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
                # TODO: response = self.connection.put_bucket_notification_configuration(**kw_args)
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket notifications')

     # TODO: if present, assign region replication
        if region_replication:
            try:
                response = self.connection.put_bucket_replication(
                    Bucket='string',
                    ReplicationConfiguration={
                        'Role': 'string',
                        'Rules': [
                            {
                                'ID': 'string',
                                'Prefix': 'string',
                                'Status': 'Enabled',
                                'Destination': {
                                    'Bucket': 'string'
                                }
                            },
                        ]
                    }
                )
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket replication')

    # TODO: if present, assign access policy
        if access_policy:
            try:
                response = self.connection.put_bucket_policy(
                    Bucket='string',
                    Policy='string'
                )
                print('.', end='', flush=True)
            except:
                raise S3ConnectionError('createBucket access policy')

        print(' Done.')
        return object_map

    def deleteBucket(self, bucket_name):

        '''
            a method for deleting a bucket and all its files on s3

        :param bucket_name: string with name of bucket
        :return: True
        '''

    # validate inputs
        self.input.bucketName(bucket_name)

    # check for existence of bucket
        if not bucket_name in self.listBuckets():
            print('S3 bucket "%s" does not exist.' % bucket_name)
            return True

    # retrieve list of objects in bucket
        object_keys = []
        object_list, next_key = self.listVersions(bucket_name)
        for object in object_list:
            details = {
                'Key': object['objectKey'],
                'VersionId': object['versionID']
            }
            object_keys.append(details)

    # delete objects in bucket
        kw_args = {
            'Bucket': bucket_name,
            'Delete': { 'Objects': object_keys }
        }
        if object_keys:
            try:
                response = self.connection.delete_objects(**kw_args)
            except:
                raise S3ConnectionError('deleteBucket deleteObjects')

    # continue deleting objects in bucket until empty
        if next_key:
            while next_key:
                object_keys = []
                object_list, next_key = self.listVersions(bucket_name, starting_key=next_key['key'], starting_marker=next_key['marker'])
                for object in object_list:
                    details = {
                        'Key': object['objectKey'],
                        'VersionId': object['versionID']
                    }
                    object_keys.append(details)
                kw_args = {
                    'Bucket': bucket_name,
                    'Delete': { 'Objects': object_keys }
                }
                try:
                    response = self.connection.delete_objects(**kw_args)
                except:
                    raise S3ConnectionError('deleteBucket deleteObjects')

    # send delete bucket request
        try:
            self.connection.delete_bucket( Bucket=bucket_name )
        except:
            raise S3ConnectionError('deleteBucket')

    # report result and return true
        print('S3 bucket "%s" deleted.' % bucket_name)
        return True

    def updateBucket(self, object_map):

        '''
            a method for updating the properties of a bucket in S3

        :param object_map: dictionary with bucket, metadata and object definitions
        :return: True
        '''

    # validate inputs
        object_map = self.input.map(object_map)
        new_details = object_map['bucket']
        bucket_name = new_details['bucketName']

    # check for existence of bucket
        bucket_list = self.listBuckets()
        if not bucket_name in bucket_list:
            print('S3 bucket "%s" does not exist. Update not applicable.' % bucket_name)
            return True
        old_details = self.bucketDetails(bucket_name)

    # determine differences between new and old version
        change_list = deltaData(new_details, old_details).output
        if not change_list:
            print('There are no changes to make to bucket "%s".' % bucket_name)
            return True
        print('Updating bucket "%s".' % bucket_name, end='', flush=True)
        processed_list = []
        for change in change_list:

    # replace access control
            if change['path'][0] == 'accessControl' and 'accessControl' not in processed_list:
                kw_args = {
                    'Bucket': bucket_name,
                    'ACL': new_details['accessControl']
                }
                try:
                    self.connection.put_bucket_acl(**kw_args)
                    print('.', end='', flush=True)
                except:
                    raise S3ConnectionError('updateBucket accessControl')
            processed_list.append('accessControl')

    # replace version control
            if change['path'][0] == 'versionControl' and 'versionControl' not in processed_list:
                if new_details['versionControl']:
                    try:
                        self.connection.put_bucket_versioning(
                            Bucket=bucket_name,
                            VersioningConfiguration={ 'Status': 'Enabled' }
                        )
                        print('.', end='', flush=True)
                    except:
                        raise S3ConnectionError('updateBucket versionControl')
                else:
                    try:
                        self.connection.put_bucket_versioning(
                            Bucket=bucket_name,
                            VersioningConfiguration={ 'Status': 'Suspended' }
                        )
                        print('.', end='', flush=True)
                    except:
                        raise S3ConnectionError('updateBucket versionControl')
                processed_list.append('versionControl')

    # replace log destination
            if change['path'][0] == 'logDestination' and 'logDestination' not in processed_list:
                if new_details['logDestination']:
                    log_name = new_details['logDestination']['bucketName']
                    log_prefix = new_details['logDestination']['prefix']
                    if not log_name in bucket_list:
                        raise ValueError('\nS3 Bucket "%s" for logging does not exist.' % log_name)
                    else:
                        response = self.bucketDetails(log_name)
                        if response['accessControl'] != 'log-delivery-write':
                            raise ValueError('\nS3 Bucket "%s" for logging does not have "log-delivery-write" access control.' % log_name)
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
                    print('.', end='', flush=True)
                except:
                    raise S3ConnectionError('updateBucket logDestination')
                processed_list.append('logDestination')

    # replace lifecycle rules
            if change['path'][0] == 'lifecycleRules' and 'lifecycleRules' not in processed_list:
                if new_details['lifecycleRules']:
                    kw_args = {
                        'Bucket': bucket_name,
                        'LifecycleConfiguration': { 'Rules': [ ] }
                    }
                    for rule in new_details['lifecycleRules']:
                        details = {
                            'Prefix': rule['prefix'],
                            'Status': 'Enabled'
                        }
                        if rule['action'] == 'archive':
                            if rule['currentVersion']:
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
                            if rule['currentVersion']:
                                details['Expiration'] = { 'Days': rule['longevity'] }
                            else:
                                details['NoncurrentVersionExpiration'] = { 'NoncurrentDays': rule['longevity'] }
                        kw_args['LifecycleConfiguration']['Rules'].append(details)
                    try:
                        self.connection.put_bucket_lifecycle(**kw_args)
                        print('.', end='', flush=True)
                    except:
                        raise S3ConnectionError('updateBucket lifecycleRules')
                else:
                    try:
                        self.connection.delete_bucket_lifecycle( Bucket=bucket_name )
                        print('.', end='', flush=True)
                    except:
                        raise S3ConnectionError('updateBucket lifecycleRules')
                processed_list.append('lifecycleRules')

    # replace bucket tags
            if change['path'][0] == 'bucketTags' and 'bucketTags' not in processed_list:
                if new_details['bucketTags']:
                    try:
                        self.connection.put_bucket_tagging(
                            Bucket=bucket_name,
                            Tagging={ 'TagSet': new_details['bucketTags'] }
                        )
                        print('.', end='', flush=True)
                    except:
                        raise S3ConnectionError('updateBucket bucketTags')
                else:
                    try:
                        self.connection.delete_bucket_tagging( Bucket=bucket_name )
                        print('.', end='', flush=True)
                    except:
                        raise S3ConnectionError('updateBucket bucketTags')
                processed_list.append('bucketTags')

    # replace notification settings
            if change['path'][0] == 'notificationSettings' and 'notificationSettings' not in processed_list:
                kw_args = {
                    'Bucket': bucket_name,
                    'NotificationConfiguration': {}
                }
                if new_details['notificationSettings']:
                    for notification in new_details['notificationSettings']:
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
                    print('.', end='', flush=True)
                except:
                    raise S3ConnectionError('createBucket notifications')
                processed_list.append('notificationSettings')

    # TODO: replace region replication
            if change['path'][0] == 'regionReplication' and 'regionReplication' not in processed_list:
                if new_details['regionReplication']:
                    pass
                else:
                    pass
                processed_list.append('regionReplication')

    # TODO: replace access policy
            if change['path'][0] == 'accessPolicy' and 'accessPolicy' not in processed_list:
                if new_details['accessPolicy']:
                    pass
                else:
                    pass
                processed_list.append('accessPolicy')

    # report and return completion of process
        print(' Done.')
        return True

    def listObjects(self, bucket_name, prefix='', delimiter='', max_results=0, starting_key=''):

        '''
            a method for retrieving a list of the objects in a bucket

        :param bucket_name: string with name of bucket
        :param prefix: [optional] string with value limiting results to key prefix
        :param delimiter: [optional] string with value limiting results to key suffix
        :param max_results: [optional] integer with max results to return
        :param starting_key: [optional] string with key value to continue search with
        :return: list of results with key, size and date, string with ending key value
        '''

    # validate inputs
        title = 'list objects in bucket'
        self.input.bucketName(bucket_name, 'Query of ' + title)
        sub_title = '%s "%s"' % (title, bucket_name)
        if prefix:
            self.input.keyName(prefix, 'prefix for ' + sub_title)
        if delimiter:
            self.input.keyName(delimiter, 'delimiter for ' + sub_title)
        if max_results:
            req_max = self.rules['requests']['listObjects']['maxResults']
            self.input.integer(max_results, 1, req_max, 'Max results for ' + sub_title)
        if starting_key:
            self.input.keyName(starting_key, 'starting key for ' + sub_title)

    # check to see if bucket exists:
        if not bucket_name in self.listBuckets():
            raise ValueError('\nBucket "%s" for %s does not exist.' % (bucket_name, sub_title))

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
        object_list = []
        next_key = ''
        try:
            response = self.connection.list_objects(**kw_args)
        except:
            raise S3ConnectionError('listObjects')

    # add retrieved contents to object list
        if 'Contents' in response:
            for object in response['Contents']:
                details = {
                    'objectKey': object['Key'],
                    'objectSize': object['Size'],
                    'currentVersion': True,
                    'versionID': '',
                    'contentEncoding': '',
                    'contentType': '',
                    'indexMetaData': {}
                }
                date_time = object['LastModified']
                epoch_zero = datetime.datetime.fromtimestamp(0).replace(tzinfo=tzutc())
                details['lastModified'] = (date_time - epoch_zero).total_seconds()
                object_list.append(details)

    # define ending key value
        if response['IsTruncated']:
            next_key = response['NextMarker']

        return object_list, next_key

    def listVersions(self, bucket_name, prefix='', delimiter='', max_results=0, starting_key='', starting_marker=''):

        '''
            a method for retrieving a list of the versions of objects in a bucket

        :param bucket_name: string with name of bucket
        :param prefix: [optional] string with value limiting results to key prefix
        :param delimiter: [optional] string with value limiting results to key suffix
        :param max_results: [optional] integer with max results to return
        :param starting_key: [optional] string with key value to continue search with
        :param starting_marker: [optional] string with version id to continue search with
        :return: list of results with key, size and date, string with ending key value
        '''

    # validate inputs
        title = 'list objects in bucket'
        self.input.bucketName(bucket_name, 'Query of ' + title)
        sub_title = '%s "%s"' % (title, bucket_name)
        if prefix:
            self.input.keyName(prefix, 'prefix for ' + sub_title)
        if delimiter:
            self.input.keyName(delimiter, 'delimiter for ' + sub_title)
        if max_results:
            req_max = self.rules['requests']['listObjects']['maxResults']
            self.input.integer(max_results, 1, req_max, 'Max results for ' + sub_title)
        if starting_key:
            self.input.keyName(starting_key, 'starting key for ' + sub_title)
            if not starting_marker:
                raise ValueError('\nStarting marker is required for starting key for %s' % sub_title)
        if starting_marker:
            self.input.keyName(starting_marker, 'starting marker for ' + sub_title)
            if not starting_key:
                raise ValueError('\nStarting key is required for starting marker for %s' % sub_title)

    # check to see if bucket exists:
        if not bucket_name in self.listBuckets():
            raise ValueError('\nBucket "%s" for %s does not exist.' % (bucket_name, sub_title))

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name
        }
        if starting_key:
            kw_args['KeyMarker'] = starting_key
        if starting_marker:
            kw_args['VersionIdMarker'] = starting_marker
        if prefix:
            kw_args['Prefix'] = prefix
        if delimiter:
            kw_args['Delimiter'] = delimiter
        if max_results:
            kw_args['MaxKeys'] = max_results

    # send request for objects
        object_list = []
        next_key = {}
        try:
            response = self.connection.list_object_versions(**kw_args)
        except:
            raise S3ConnectionError('listVersions')

    # add version keys and ids to object list
        if 'Versions' in response:
            for object in response['Versions']:
                details = {
                    'objectKey': object['Key'],
                    'versionID': object['VersionId'],
                    'objectSize': object['Size'],
                    'currentVersion': object['IsLatest'],
                    'contentEncoding': '',
                    'contentType': '',
                    'indexMetaData': {}
                }
                date_time = object['LastModified']
                epoch_zero = datetime.datetime.fromtimestamp(0).replace(tzinfo=tzutc())
                details['lastModified'] = (date_time - epoch_zero).total_seconds()
                object_list.append(details)

    # add delete markers to object list
        if 'DeleteMarkers' in response:
            for object in response['DeleteMarkers']:
                details = {
                    'objectKey': object['Key'],
                    'versionID': object['VersionId'],
                    'objectSize': None,
                    'currentVersion': object['IsLatest'],
                    'contentEncoding': '',
                    'contentType': '',
                    'indexMetaData': {}
                }
                date_time = object['LastModified']
                epoch_zero = datetime.datetime.fromtimestamp(0).replace(tzinfo=tzutc())
                details['lastModified'] = (date_time - epoch_zero).total_seconds()
                object_list.append(details)

    # define next key value
        if response['IsTruncated']:
            next_key = {
                'key': response['NextKeyMarker'],
                'marker': response['NextVersionIdMarker']
            }

        return object_list, next_key

    def recordDetails(self, key_name, object_map, version_id='', password=''):

        '''
            a method for retrieving the attributes of a record from s3

        :param key_name: string with key value of record
        :param object_map: dictionary with object definitions
        :param version_id: [optional] string with aws id of version of record
        :param password: [optional] string to use for sha256 hash for aes256 bit key
        :return: dictionary with details of record
        '''

    #validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = ' for bucket "%s"' % bucket_name
        self.input.keyName(key_name, 'key name' + title)

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': key_name
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
            raise S3ConnectionError('retrieveRecord')

    # create record details from response data
        record_data = response['Body'].read()

    # create meta data from response
        meta_data = {
            'objectKey': key_name,
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
                raise S3ConnectionError('listVersions')

    # TODO: client-side decrypt incoming data
        if 'ContentEncryption' in meta_data['indexMetaData']:
            if not password:
                raise Exception('\nA password must be included to decrypt details%s record %s' % (title, key_name))
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

    def recordHeaders(self, key_name, object_map, version_id='', version_check=True):

        '''
            a method for retrieving the headers of a record from s3

        :param key_name: string with key value of record
        :param object_map: dictionary with object definitions
        :param version_id: [optional] string with aws id of version of record
        :param version_check: [optional] boolean to turn off currentVersion check
        :return: dictionary with headers of record
        '''

    #validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = ' for bucket "%s"' % bucket_name
        self.input.keyName(key_name, 'key name' + title)

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': key_name
        }
        if version_id:
            self.input.keyName(version_id, 'version id' + title)
            kw_args['VersionId'] = version_id

    # send request for record header
        try:
            response = self.connection.head_object(**kw_args)
        except:
            raise S3ConnectionError('retrieveRecord')

    # create meta data from response
        meta_data = {
            'objectKey': key_name,
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
                raise S3ConnectionError('listVersions')

        return meta_data

    def addRecord(self, record_details, object_map, password=''):

        '''
            a method for adding a record to s3

        :param record_details: dictionary with attributes of record
        :param object_map: dictionary with object definitions
        :param password: [optional] string to use for sha256 hash for aes256 bit key
        :return: string with key_name of record
        '''

    # validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        index = object_map['indexing']
        record_title = 'record for bucket "%s"' % bucket_name
        record_details = self.input.record(record_details, object_map, record_title)

    # construct key name for record
        key_name = ''
        for component in index['key']:
            if component == '/':
                key_name += component
            else:
                key_name += record_details[component]
        key_name = key_name + '.json.gz'

    # construct metadata for records
        meta_data = { }
        if index['metadata']:
            for key, value in index['metadata'].items():
                meta_data[key] = record_details[value]
        if password:
            meta_data['ContentEncryption'] = 'AES256'
        meta_bytes = json.dumps(meta_data).encode('utf-8')

    # serialize and compress record_details
        record_bytes = json.dumps(record_details).encode('utf-8')
        record_data = gzip.compress(record_bytes)

    # TODO: client-side encrypt data with AES 256 cipher
        if password:
            pass_title = 'password for encrypting %s' % record_title
            key_b64, digest_b64 = self.input.password(password, pass_title)
            # create aes256 cipher text from record_data and password output
            # redefine record_data and update Content Encoding

    # validate size of record
        self.input.recordSize(record_data, meta_bytes, record_title)

    # create RFC 1864 base64 encoded md5 digest of data to confirm integrity
        hash_bytes = hashlib.md5(record_data).digest()
        content_md5 = base64.b64encode(hash_bytes).decode()
        check_sum = hashlib.md5(record_data).hexdigest()

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': key_name,
            'Body': record_data,
            'ContentMD5': content_md5,
            'ContentType': 'application/json',
            'ContentEncoding': 'gzip',
            'Metadata': meta_data
        }

    # add server side encryption key to request
    #     if password:
    #         pass_title = 'password for encrypting %s' % record_title
    #         key_b64, digest_b64 = self.input.password(password, pass_title)
    #         kw_args['SSECustomerAlgorithm'] = 'AES256'
    #         kw_args['SSECustomerKey'] = key_b64
    #         kw_args['SSECustomerKeyMD5'] = digest_b64

    # send request to add object
        try:
            response = self.connection.put_object(**kw_args)
            if response['ETag'] != '"' + check_sum + '"':
                raise Exception('\nData transcription error for key "%s".' % key_name)
        except:
            raise S3ConnectionError('addRecord')

        return key_name

    def deleteRecord(self, key_name, object_map, version_id=''):

        '''
            a method for deleting an object record in s3

        :param key_name: string with key value of record
        :param object_map: dictionary with object definitions
        :param version_id: [optional] string with aws id of version of record
        :return: True
        '''

     #validate inputs
        # object_map = self.input.map(object_map)
        bucket_name = object_map['bucket']['bucketName']
        title = ' for bucket "%s"' % bucket_name
        self.input.keyName(key_name, 'key name' + title)

    # create key word argument dictionary
        kw_args = {
            'Bucket': bucket_name,
            'Key': key_name
        }
        if version_id:
            self.input.keyName(version_id, 'version id' + title)
            kw_args['VersionId'] = version_id

    # send request to delete record
        try:
            self.connection.delete_object(**kw_args)
        except:
            raise S3ConnectionError('deleteRecord')

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
            raise Exception('\n%s does not exist.' % title)

    # retrieve list of records in bucket
        record_list, next_key = self.listObjects(bucket_name)
        if next_key:
            record_number = 'first %s' % str(len(record_list))
        else:
            record_number = str(len(record_list))
        plural = ''
        if len(record_list) != 1:
            plural = 's'
        print('Exporting %s record%s from bucket "%s" to path %s.' % (record_number, plural, bucket_name, export_path), end='', flush=True)

    # retrieve data for records in bucket
        for record in record_list:
            try:
                response = self.connection.get_object(Bucket=bucket_name,Key=record['objectKey'])
            except:
                raise S3ConnectionError('retrieveRecord')
            record_data = response['Body'].read()
            file_path = export_path + record['objectKey']
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if os.path.exists(file_path) and not overwrite:
                print('\n%s already exists. File skipped.' % file_path, end='', flush=True)
            else:
                with open(file_path, 'wb') as file:
                    file.write(record_data)
                    file.close()
            print('.', end='', flush=True)

    # continue exporting records in bucket until all exported
        if next_key:
            while next_key or record_list:
                record_list, next_key = self.listObjects(bucket_name)
                if next_key:
                    record_number = 'next %s' % str(len(record_list))
                else:
                    record_number = 'last %s' % str(len(record_list))
                print('.')
                plural = ''
                if len(record_list) != 1:
                    plural = 's'
                print('Exporting %s record%s from bucket "%s" to path %s' % (record_number, plural, bucket_name, export_path), end='', flush=True)
                for record in record_list:
                    try:
                        response = self.connection.get_object(Bucket=bucket_name,Key=record['objectKey'])
                    except:
                        raise S3ConnectionError('retrieveRecord')
                    record_data = response['Body'].read()
                    file_path = export_path + record['objectKey']
                    dir_path = os.path.dirname(file_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    if os.path.exists(file_path) and not overwrite:
                        print('\n%s already exists. File skipped.' % file_path, end='', flush=True)
                    else:
                        with open(file_path, 'wb') as file:
                            file.write(record_data)
                            file.close()
                    print('.', end='', flush=True)

    # report completion and return true
        print(' Done.')
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
            raise Exception('\n%s does not exist.' % title)

    # mini-method to create a record
        def createRecord(record_details, object_map, overwrite=False):
            results = []
            index = object_map['indexing']
            key_name = ''
            for component in index['key']:
                if component == '/':
                    key_name += component
                else:
                    key_name += record_details[component]
            key_name = key_name + '.json.gz'
            bucket_name = object_map['bucket']['bucketName']
            if not overwrite:
                results, next = self.listObjects(bucket_name, key_name)
            if not overwrite and results:
                print('\n%s already exists. Record skipped.' % key_name, end='', flush=True)
            else:
                self.addRecord(record_details, object_map)
                print('.', end='', flush=True)

    # mini-method to open record from a file
        def openRecord(file_path, object_map, overwrite=False):
            try:
                record_data = open(file_path, 'rb').read()
                record_bytes = gzip.decompress(record_data)
                record_details = json.loads(record_bytes.decode())
                createRecord(record_details, object_map, overwrite)
            except:
                print('\n[WARNING]: %s does not have a compatible record format. Skipped.' % file_path, end='', flush=True)

    # mini-method to recursively find files and file path
        def findFiles(root_path, object_map, overwrite=False):
            for object in os.listdir(root_path):
                new_path = deepcopy(root_path) + object
                if os.path.isdir(new_path):
                    findFiles(new_path + '/', object_map, overwrite)
                else:
                    openRecord(new_path, object_map, overwrite)

    # run creation methods
        print('Importing records from path %s to bucket "%s".' % (import_path, bucket_name), end='', flush=True)
        findFiles(import_path, object_map, overwrite)

    # report completion and return true
        print(' Done.')
        return True

    def handler(self, function, wait=.5):

        '''
            a decorator method to deal with exception handling of requests to AWS

        :return: return of input function
        '''

        if not isinstance(wait, int) and not isinstance(wait, float):
            raise TypeError('\nawsS3.handler() wait input must be a number.')
        timeout = 0
        while timeout < 30:
            try:
                return function
            except S3ConnectionError:
                timeout += 1
                time.sleep(wait)
        raise Exception('\nConnectivity Issues with AWS.')

    def unitTests(self):
        objectMap = json.loads(open('../models/s3-obj-model.json').read())
        logMap = deepcopy(objectMap)
        logMap['bucket']['bucketName'] = 'useast1-collective-acuity-test-log'
        logMap['bucket']['accessControl'] = 'log-delivery-write'
        logMap['bucket']['versionControl'] = False
        logMap['bucket']['logDestination'] = {}
        logMap['bucket']['lifecycleRules'] = []
        logMap['bucket']['bucketTags'] = []
        logMap['bucket']['notificationSettings'] = []
        testBuckets = [ logMap['bucket']['bucketName'], objectMap['bucket']['bucketName'] ]
        for name in testBuckets:
            assert name not in self.listBuckets() # prevent deletion of live data
        for bucket in testBuckets:
            self.deleteBucket(bucket)
        self.createBucket(logMap)
        self.createBucket(objectMap)
        recordDetails = objectMap['details']
        self.addRecord(recordDetails, objectMap)
        keyName = self.addRecord(recordDetails, objectMap)
        meta_data = self.recordHeaders(keyName, objectMap)
        assert meta_data['lastModified']
        bucketList = self.listBuckets()
        for name in testBuckets:
            assert name in bucketList
        recordList, nextKey = self.listObjects(testBuckets[1])
        assert recordList[0]['objectKey'] == keyName
        data, meta_data = self.recordDetails(recordList[0]['objectKey'], objectMap)
        assert data
        assert meta_data
        newRecord = deepcopy(recordDetails)
        newRecord[objectMap['indexing']['key'][0]] = 'new'
        self.addRecord(newRecord, objectMap)
        self.exportRecords(objectMap, '../data', overwrite=True)
        self.exportRecords(objectMap, '../data')
        self.importRecords(objectMap, '../data')
        self.importRecords(objectMap, '../data', overwrite=True)
        self.deleteRecord(recordList[0]['objectKey'], objectMap)
        versionList, nextKey = self.listVersions(testBuckets[1])
        self.recordDetails(versionList[1]['objectKey'], objectMap, version_id=versionList[1]['versionID'])
        self.deleteRecord(versionList[1]['objectKey'], objectMap, versionList[1]['versionID'])
        self.deleteBucket(testBuckets[1])
        self.createBucket(objectMap)
        self.importRecords(objectMap, '../data')
        recordList, nextKey = self.handler(self.listObjects(objectMap['bucket']['bucketName']))
        assert recordList
        updateMap = {}
        updateMap['indexing'] = objectMap['indexing']
        updateMap['details'] = objectMap['details']
        updateMap['bucket'] = self.bucketDetails(testBuckets[1])
        updateMap['bucket']['accessControl'] = 'public-read'
        updateMap['bucket']['versionControl'] = False
        updateMap['bucket']['logDestination'] = {}
        updateMap['bucket']['lifecycleRules'] = []
        updateMap['bucket']['bucketTags'] = []
        self.updateBucket(updateMap)
        self.updateBucket(objectMap)
        for bucket in testBuckets:
            self.deleteBucket(bucket)
        return self

class deltaData(object):

    '''
        a class of recursive methods for identifying changes between two objects

        dependencies:
            from copy import deepcopy
    '''

    def __init__(self, new_details, old_details):

        '''
            the initialization method for the class

        :param new_details: set, list or dictionary with new details of an item
        :param old_details: set, list or dictionary with old details of an item
        :return: list with dictionary of changes
        '''

        if new_details.__class__ != old_details.__class__:
            raise TypeError('\nDatatype of new and old data must match.')
        new_map = deepcopy(new_details)
        old_map = deepcopy(old_details)
        if isinstance(new_map, dict):
            self.output = self.dict(new_map, old_map, [], [])
        elif isinstance(new_map, list):
            self.output = self.list(new_map, old_map, [], [])
        elif isinstance(new_map, set):
            self.output = self.set(new_map, old_map, [], [])
        else:
            raise TypeError('\nData inputs must be sets, lists or dictionaries.')

    def dict(self, new_dict, old_dict, change_list=None, root=None):

        '''
            a method for recursively listing changes made to a dictionary

        :param new_dict: dictionary with new key-value pairs
        :param old_dict: dictionary with old key-value pairs
        :param change_list: list of differences between old and new
        :patam root: string with record of path to the root of the main object
        :return: list of differences between old and new
        '''

        new_keys = set(new_dict.keys())
        old_keys = set(old_dict.keys())
        missing_keys = old_keys - new_keys
        extra_keys = new_keys - old_keys
        same_keys = new_keys.intersection(old_keys)
        for key in missing_keys:
            new_path = deepcopy(root)
            new_path.append(key)
            change_list.append({'action': 'DELETE', 'value': None, 'path': new_path})
        for key in extra_keys:
            for k, v in new_dict.items():
                if key == k:
                    new_path = deepcopy(root)
                    new_path.append(key)
                    change_list.append({'action': 'ADD', 'value': v, 'path': new_path})
        for key in same_keys:
            new_path = deepcopy(root)
            new_path.append(key)
            if new_dict[key].__class__ != old_dict[key].__class__:
                change_list.append({'action': 'UPDATE', 'value': new_dict[key], 'path': new_path})
            elif isinstance(new_dict[key], dict):
                self.dict(new_dict[key], old_dict[key], change_list, new_path)
            elif isinstance(new_dict[key], list):
                self.list(new_dict[key], old_dict[key], change_list, new_path)
            elif isinstance(new_dict[key], set):
                self.set(new_dict[key], old_dict[key], change_list, new_path)
            elif new_dict[key] != old_dict[key]:
                change_list.append({'action': 'UPDATE', 'value': new_dict[key], 'path': new_path})
        return change_list

    def list(self, new_list, old_list, change_list=None, root=None):

        '''
            a method for recursively listing changes made to a list

        :param new_list: list with new value
        :param old_list: list with old values
        :param change_list: list of differences between old and new
        :patam root: string with record of path to the root of the main object
        :return: list of differences between old and new
        '''

        if len(old_list) > len(new_list):
            same_len = len(new_list)
            for i in reversed(range(len(new_list), len(old_list))):
                new_path = deepcopy(root)
                new_path.append(i)
                change_list.append({'action': 'REMOVE', 'value': None, 'path': new_path})
        elif len(new_list) > len(old_list):
            same_len = len(old_list)
            append_list = []
            path = deepcopy(root)
            for i in range(len(old_list), len(new_list)):
                append_list.append(new_list[i])
            change_list.append({'action': 'APPEND', 'value': append_list, 'path': path})
        else:
            same_len = len(new_list)
        for i in range(0, same_len):
            new_path = deepcopy(root)
            new_path.append(i)
            if new_list[i].__class__ != old_list[i].__class__:
                change_list.append({'action': 'UPDATE', 'value': new_list[i], 'path': new_path})
            elif isinstance(new_list[i], dict):
                self.dict(new_list[i], old_list[i], change_list, new_path)
            elif isinstance(new_list[i], list):
                self.list(new_list[i], old_list[i], change_list, new_path)
            elif isinstance(new_list[i], set):
                self.set(new_list[i], old_list[i], change_list, new_path)
            elif new_list[i] != old_list[i]:
                change_list.append({'action': 'UPDATE', 'value': new_list[i], 'path': new_path})
        return change_list

    def set(self, new_set, old_set, change_list, root):

        '''
            a method for list changes made to a set

        :param new_set: set with new values
        :param old_set: set with old values
        :param change_list: list of differences between old and new
        :patam root: string with record of path to the root of the main object
        :return: list of differences between old and new
        '''

        path = deepcopy(root)
        missing_items = old_set - new_set
        extra_items = new_set - old_set
        for item in missing_items:
            change_list.append({'action': 'REMOVE', 'key': None, 'value': item, 'path': path})
        for item in extra_items:
            change_list.append({'action': 'ADD', 'key': None, 'value': item, 'path': path})
        return change_list

    def unitTests(self):
        newRecord = {
            'active': True,
            'id': 'd53iedBwKNcFCJXLEAWHCfCT3zGLCu93rxTG',
            'dT': 1440184621.607344,
            'score': 400,
            'dict1': { 'key': 'value' },
            'list1': [ 'item' ],
            'dict2': {
                'key1': 'string',
                'key2': 2.2,
                'key3': 2,
                'key4': True,
                'dict': {
                    'key': 'value',
                    'list1': [ 'item' ],
                    'list2': [ 'item', 2, 2.2, True, { 'key': 'newValue' } ]
                } },
            'list2': [ 'item', 2, 2.2, True, { 'key': 'value', 'list': [ 2, 2.2, True, 'item' ] } ]
        }
        oldRecord = {
            'active': True,
            'id': 'd53iedBwKNcFCJXLEAWHCfCT3zGLCu93rxTG',
            'dT': 1440184621.607344,
            'score': 400,
            'dict1': { 'key': 'value' },
            'list1': [ 'item' ],
            'dict2': {
                'key1': 'string',
                'key2': 2.2,
                'key3': 2,
                'key4': True,
                'dict': {
                    'key': 'value',
                    'list1': [ 'item' ],
                    'list2': [ 'item', 2, 2.2, True, { 'key': 'oldValue' } ]
                } },
            'list2': [ 'item', 2, 2.2, True, { 'key': 'value', 'list': [ 2, 2.2, True, 'item' ] } ]
        }
        assert self.dict(newRecord, oldRecord, [], [])[0]['path'][4] == 'key'
        return self

class awsGlacier(object):
    pass

dummy = ''
# TODO: client side encryption feature for s3 records
# TODO: bucket access policy feature for s3
# TODO: bucket region replication feature for s3
# TODO: bucket notification settings feature integration with AWS event services
# TODO: awsGlacier archive, restore and delete methods
# TODO: more variations for deltaData.unitTest()
