__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

'''
PLEASE NOTE:   r53 package requires the boto3 module.

(all platforms) pip3 install boto3
'''

try:
    import boto3
except:
    import sys

    print('r53 package requires the boto3 module. try: pip3 install boto3')
    sys.exit(1)

from labpack.authentication.aws.iam import AWSConnectionError

class r53Client(object):
    '''
        a class of methods for interacting with AWS Route 53

        https://boto3.readthedocs.org/en/latest/
    '''

    def __init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True):
        '''
            a method for initializing the connection to Route 53

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
            'service_name': 'route53',
            'region_name': self.iam.region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        self.connection = boto3.client(**client_kwargs)
        self.verbose = verbose

    def list_zones(self):

        '''
            a method to retrieve the list of hosted zones on AWS Route 53

        :return: list of strings with hosted zone ids
        '''

        title = '%s.list_zones' % self.__class__.__name__

        # request list of hosted zones
        self.iam.printer('Querying AWS region %s for hosted zones.' % self.iam.region_name)
        zone_list = []
        try:
            response = self.connection.list_hosted_zones()
        except:
            raise AWSConnectionError(title)

        # populate list from response
        if 'HostedZones' in response:
            response_list = response['HostedZones']
            for zone in response_list:
                zone_id = zone['Id'].replace('/hostedzone/', '')
                zone_list.append(zone_id)

        # report results and return details
        if zone_list:
            print_out = 'Found zone'
            if len(zone_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(zone_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No zones found.')

        return zone_list

    def list_records(self, zone_id):
        
        '''
            method for listing records associated with a hosted zone
            
        :param zone_id: string of hosted zone id on AWS
        :return: list of dictionaries with record fields
        
        'name': 'string',
        'dnsName': 'string',
        'evaluateTargetHealth': false,
        'hostedZoneID': 'string'
        
        '''

        title = '%s.list_zones' % self.__class__.__name__

        # request list of records for zone
        self.iam.printer('Querying AWS region %s for records of hosted zone %s.' % (self.iam.region_name, zone_id))
        record_list = []
        try:
            response = self.connection.list_resource_record_sets(
                HostedZoneId=zone_id
            )
        except:
            raise AWSConnectionError(title)
    
        # populate a list of records from response
        if 'ResourceRecordSets' in response.keys():
            for record in response['ResourceRecordSets']:
                record_list.append(record)

        return record_list

    def create_record(self, zone_id, record_fields):

        '''
            method to create a record on a hosted zone on AWS Route 53
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets

        :param zone_id: string of hosted zone id on AWS
        :param record_fields: dictionary with fields associated with record
        :return: dictionary with aws response

        record_fields: {
            'Name': 'collectiveacuity.com.',
            'ResourceRecords': [{'Value': '54.166.58.146'}],
            'TTL': 300,
            'Type': 'A'
        }
        '''

        title = '%s.create_record' % self.__class__.__name__

        # report query
        self.iam.printer('Creating record %s on %s.' % (record_fields['Name'], zone_id))

        # send request to add record
        kwargs = {
            'HostedZoneId': zone_id,
            'ChangeBatch': {'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': record_fields
                }
            ]}
        }
        try:
            response = self.connection.change_resource_record_sets(**kwargs)
        except:
            raise AWSConnectionError(title)

        # report outcome and return true
        new_state = response['ChangeInfo']['Status']
        self.iam.printer('Creation of record %s for zone %s is %s.' % (record_fields['Name'], zone_id, new_state))

        return response

    def update_record(self, zone_id, record_fields):

        ''' 
            method to update a hosted zone record on AWS Route 53
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets
            
        :param zone_id: string of hosted zone id on AWS
        :param record_fields: dictionary with fields associated with record
        :return: dictionary with aws response

        record_fields: {
            'Name': 'collectiveacuity.com.',
            'ResourceRecords': [{'Value': '54.166.58.146'}],
            'TTL': 300,
            'Type': 'A'
        }
        '''

        title = '%s.update_record' % self.__class__.__name__

        # report query
        self.iam.printer('Updating record %s on %s.' % (record_fields['Name'], zone_id))

        # send request to upsert record
        kwargs = {
            'HostedZoneId': zone_id,
            'ChangeBatch': {'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': record_fields
                }
            ]}
        }
        try:
            response = self.connection.change_resource_record_sets(**kwargs)
        except:
            raise AWSConnectionError(title)

        # report outcome and return true
        new_state = response['ChangeInfo']['Status']
        self.iam.printer('Update of record %s for zone %s is %s.' % (record_fields['Name'], zone_id, new_state))

        return response

    def delete_record(self, zone_id, record_fields):
        
        ''' 
            method to delete a hosted zone record on AWS Route 53
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets
            
        :param zone_id: string of hosted zone id on AWS
        :param record_fields: dictionary with fields associated with record
        :return: dictionary with aws response

        record_fields: {
            'Name': 'collectiveacuity.com.',
            'ResourceRecords': [{'Value': '54.166.58.146'}],
            'TTL': 300,
            'Type': 'A'
        }
        '''

        title = '%s.delete_record' % self.__class__.__name__

        # report query
        self.iam.printer('Deleting record %s from %s.' % (record_fields['Name'], zone_id))

        # send request to delete record
        kwargs = {
            'HostedZoneId': zone_id,
            'ChangeBatch': {'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': record_fields
                }
            ]}
        }
        try:
            response = self.connection.change_resource_record_sets(**kwargs)
        except:
            raise AWSConnectionError(title)

        # report outcome and return true
        new_state = response['ChangeInfo']['Status']
        self.iam.printer('Deletion of record %s from zone %s is %s.' % (record_fields['Name'], zone_id, new_state))

        return response

    def delete_zone(self, zone_id):

        '''
            method to delete zone from AWS Route 53
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_hosted_zone
            PLEASE NOTE: method will first remove all record types besides SOA and NS
            
        :param zone_id: string of hosted zone id on AWS
        :return: dictionary with response info
        '''

        title = '%s.delete_zone' % self.__class__.__name__

        # request list of records
        record_list = self.list_records(zone_id)

        # report query
        self.iam.printer('Removing all records from zone %s.' % zone_id)

        # compile list of all but SOA and NS records
        change_list = []
        for record in record_list:
            if record['Type'] not in ('SOA','NS'):
                details = {
                    'Action': 'DELETE',
                    'ResourceRecordSet': record
                }
                change_list.append(details)

        # send request to update alias targets
        if change_list:
            try:
                self.connection.change_resource_record_sets(
                    HostedZoneId=zone_id,
                    ChangeBatch={ 'Changes': change_list }
                )
            except:
                raise AWSConnectionError(title)

        # report query
        self.iam.printer('Deleting zone %s from AWS region %s.' % (zone_id, self.iam.region_name))

        # terminate zone
        try:
            response = self.connection.delete_hosted_zone(
                Id=zone_id
            )
        except:
            raise AWSConnectionError(title)

        # report outcome and return true
        new_state = response['ChangeInfo']['Status']
        self.iam.printer('Deletion of zone %s is %s.' % (zone_id, new_state))

        return response

if __name__ == '__main__':
    
    # import dependencies & configs
    from labpack.records.settings import load_settings

    # test r53 construction
    aws_cred = load_settings('../../../../cred/aws.yaml')
    client_kwargs = {
        'access_id': aws_cred['aws_access_key_id'],
        'secret_key': aws_cred['aws_secret_access_key'],
        'region_name': aws_cred['aws_default_region'],
        'owner_id': aws_cred['aws_owner_id'],
        'user_name': aws_cred['aws_user_name']
    }
    r53_client = r53Client(**client_kwargs)

    # test r53 list zones
    zone_list = r53_client.list_zones()
    print(zone_list)

    # test listing of zones
    for zone_id in zone_list:
        record_list = r53_client.list_records(zone_id)

        # test deleting os zones
        if zone_id == 'Z28LK2G8P1JIHK':
            r53_client.delete_zone(zone_id)