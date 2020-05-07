__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

'''
PLEASE NOTE:   rds package requires the boto3 module.

(all platforms) pip3 install boto3
'''

try:
    import boto3
except:
    import sys

    print('rds package requires the boto3 module. try: pip3 install boto3')
    sys.exit(1)

from labpack.authentication.aws.iam import AWSConnectionError

class rdsClient(object):
    '''
        a class of methods for interacting with AWS Relational Database Store

        https://boto3.readthedocs.org/en/latest/
    '''

    def __init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True):
        '''
            a method for initializing the connection to EC2

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
        class_fields = jsonLoader(__module__, 'platforms/aws/ec2-rules.json')
        self.fields = jsonModel(class_fields)

        # construct iam connection
        from labpack.authentication.aws.iam import iamClient
        self.iam = iamClient(access_id, secret_key, region_name, owner_id, user_name, verbose)

        # construct ec2 client connection
        client_kwargs = {
            'service_name': 'rds',
            'region_name': self.iam.region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        self.connection = boto3.client(**client_kwargs)
        self.verbose = verbose

    def _validate_tags(self, tag_values, title):

        ''' a helper method to validate tag key and value pairs '''

        if tag_values:
            if len(tag_values.keys()) > 10:
                raise Exception(
                    "%s(tag_values={...}) is invalid.\n Value %s for field .tag_values failed test 'max_keys': 10" % (
                    title, len(tag_values.keys())))
            for key, value in tag_values.items():
                object_title = '%s(%s)' % (title, key)
                self.fields.validate(value, '.tag_key', object_title)
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.tag_key', object_title)

    def list_instances(self, tag_values=None):

        '''
            a method to retrieve the list of instances on AWS RDS

        :param tag_values: [optional] dictionary of tag key-values pairs
        :return: list of strings with db instance AWS ids
        '''

        title = '%s.list_instances' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'tag_values': tag_values
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        self._validate_tags(tag_values, title)

    # add tags to method arguments
        kw_args = {}
        tag_text = ''
        if tag_values:
            kw_args = {
                'Filters': []
            }
            tag_words = []
            for key, value in tag_values.items():
                kw_args['Filters'].append({ 'Name': 'tag:%s' % key, 'Values': [value] })
            from labpack.parsing.grammar import join_words
            plural_value = ''
            if len(tag_values) > 1:
                plural_value = 's'
            tag_text = ' with tag value%s %s' % (plural_value, join_words(tag_words))

    # request instance details from AWS
        self.iam.printer('Querying AWS region %s for db instances%s.' % (self.iam.region_name, tag_text))
        instance_list = []
        try:
            if tag_values:
                response = self.connection.describe_db_instances(**kw_args)
            else:
                response = self.connection.describe_db_instances()
        except:
            raise AWSConnectionError(title)

    # repeat request if any instances are currently pending
        response_list = response['DBInstances']
        # for instance in response_list:
        #     instance_info = instance['Instances'][0]
        #     if instance_info['State']['Name'] == 'pending':
        #         self.check_instance_state(instance_info['InstanceId'])
        #         try:
        #             if tag_values:
        #                 response = self.connection.describe_instances(**kw_args)
        #             else:
        #                 response = self.connection.describe_instances()
        #         except:
        #             raise AWSConnectionError(title)
        #         response_list = response['Reservations']

    # populate list of instances with instance details
        for instance in response_list:
            status_name = instance['DBInstanceStatus']
            if status_name not in ('shutting-down', 'terminated', 'deleting'):
                instance_list.append(instance['DBInstanceIdentifier'])

    # report results and return details
        if instance_list:
            print_out = 'Found db instance'
            if len(instance_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(instance_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No db instances found.')

        return instance_list

    def delete_instance(self, instance_id):

        '''
            method for removing a db instance from AWS EC2

        :param instance_id: string of instance id on AWS
        :return: string reporting state of instance
        '''

        title = '%s.delete_instance' % self.__class__.__name__

    # # validate inputs
    #     input_fields = {
    #         'instance_id': instance_id
    #     }
    #     for key, value in input_fields.items():
    #         object_title = '%s(%s=%s)' % (title, key, str(value))
    #         self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Removing db instance %s from AWS region %s.' % (instance_id, self.iam.region_name))

    # terminate instance
        try:
            response = self.connection.delete_db_instance(
                DBInstanceIdentifier=instance_id,
                SkipFinalSnapshot=True
            )
        except:
            raise AWSConnectionError(title)

    # report outcome and return true
        new_state = response['DBInstance']['DBInstanceStatus']
        self.iam.printer('Instance %s is %s.' % (instance_id, new_state))

        return response
    
if __name__ == '__main__':

# import dependencies & configs
    from pprint import pprint
    from time import time, sleep
    from labpack.records.settings import load_settings

# test rds construction
    aws_cred = load_settings('../../../../cred/aws.yaml')
    client_kwargs = {
        'access_id': aws_cred['aws_access_key_id'],
        'secret_key': aws_cred['aws_secret_access_key'],
        'region_name': aws_cred['aws_default_region'],
        'owner_id': aws_cred['aws_owner_id'],
        'user_name': aws_cred['aws_user_name']
    }
    rds_client = rdsClient(**client_kwargs)

# test rds list instances
    rds_instances = rds_client.list_instances()
    print(rds_instances)

# test rds delete instances
    for instance_id in rds_instances:
        if instance_id == 'labpostgres2019':
            rds_client.delete_instance(instance_id)
