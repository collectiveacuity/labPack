__author__ = 'rcj1492'
__created__ = '2015.10'

# pip install boto3
# https://pypi.python.org/pypi/boto3
# https://boto3.readthedocs.org/en/latest/

from awsDocker.awsValidation import ec2Input, iamInput
import boto3
import os
from copy import deepcopy

class R53ConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to AWS Route 53 with %s request.' % message
        super(R53ConnectionError, self).__init__(text)
        self.errors = errors

class awsR53(object):

    '''
        a class of methods for interacting with the AWS Route 53

        dependencies:
            from labAWS.awsValidation import ec2Input, iamInput
            import boto3
            import os
    '''

    __name__ = 'awsR53'

    def __init__(self, aws_credentials, aws_rules, aws_region=''):

        '''
            a method for initializing the connection to Route 53

        :param aws_credentials: dictionary with AWS credentials
        :param aws_rules: dictionary with AWS data rules
        :param aws_region: [optional] string with AWS region
        '''

    # validate inputs and create base methods
        self.cred = iamInput(aws_rules).credentials(aws_credentials)
        self.input = ec2Input(aws_rules)
        self.rules = aws_rules

    # change region environment variable
        if aws_region:
            self.input.region(aws_region)
            self.cred['AWS_DEFAULT_REGION'] = aws_region

    # construct route 53 client connection
        for key, value in self.cred.items():
            os.environ[key] = value
        self.connection = boto3.client('route53')

    def findHostedZones(self):

        '''
            a method to discover the hosted zones on AWS EC2

        :return: list of AWS hosted zone ids
        '''

        title = self.__name__ + '.findHostedZones()'

    # request list of hosted zones
        print('Querying AWS region %s for hosted zones.' % os.environ['AWS_DEFAULT_REGION'])
        try:
            response = self.connection.list_hosted_zones()
        except:
            raise R53ConnectionError(title + ' list_hosted_zones()')

    # create list of launch configurations from response
        hz_list = []
        if 'HostedZones' in response:
            response_list = response['HostedZones']
            for hz_dict in response_list:
                hz_id = hz_dict['Id'].replace('/hostedzone/', '')
                hz_list.append(hz_id)

    # check to see if any launch configurations are found
        if hz_list:
            print_out = 'Found hosted zone'
            if len(hz_list) > 1:
                print_out += 's'
            i_counter = 0
            for zone in hz_list:
                if i_counter > 0:
                    print_out += ','
                print_out += ' ' + zone
                i_counter += 1
            print_out += '.'
            print(print_out)
        else:
            print('No hosted zones found.')

        return hz_list

    def aliasTargetList(self, hosted_zone_id):

        '''
            a method to retrieve the list of alias targets of a hosted zone

        :param hosted_zone_id: string with AWS hosted zone id
        :return: list of alias target dictionaries

            'name': 'string',
            'dnsName': 'string',
            'evaluateTargetHealth': false,
            'hostedZoneID': 'string'
        '''

        title = self.__name__ + '.aliasTargetList()'

    # validate inputs
        self.input.hostedZoneID(hosted_zone_id, title)

    # check for existence of hosted zone
        try:
            response = self.connection.list_hosted_zones()
        except:
            raise R53ConnectionError(title + ' list_hosted_zones()')
        hz_list = []
        if 'HostedZones' in response:
            response_list = response['HostedZones']
            for hz_dict in response_list:
                hz_id = hz_dict['Id'].replace('/hostedzone/', '')
                hz_list.append(hz_id)
        if hosted_zone_id not in hz_list:
            raise Exception('\nHosted Zone %s does not exist.' % hosted_zone_id)

    # retrieve list of record sets associated with hosted zone
        try:
            response = self.connection.list_resource_record_sets(
                HostedZoneId=hosted_zone_id
            )
        except:
            raise R53ConnectionError(title + ' list_resource_record_sets()')

    # construct alias list from response
        alias_list = []
        if 'ResourceRecordSets' in response.keys():
            for rs_dict in response['ResourceRecordSets']:
                if rs_dict['Type'] == 'A':
                    details = {
                        'name': rs_dict['Name']
                    }
                    if 'AliasTarget' in rs_dict.keys():
                        details['dnsName'] = rs_dict['AliasTarget']['DNSName']
                        details['evaluateTargetHealth'] = rs_dict['AliasTarget']['EvaluateTargetHealth']
                        details['hostedZoneID'] = rs_dict['AliasTarget']['HostedZoneId']
                    else:
                        details['dnsName'] = rs_dict['ResourceRecords'][0]['Value']
                        details['evaluateTargetHealth'] = ''
                        details['hostedZoneID'] = hosted_zone_id
                    alias_list.append(details)

        return alias_list

    def updateAliasTargets(self, hosted_zone_id, alias_list):

        '''
            a method to update the list of alias targets of a hosted zone

        :param hosted_zone_id: string with AWS id of hosted zone
        :param alias_list: list of alias target dictionaries
        :return: True
        '''

        title = self.__name__ + '.updateAliasTargets()'

    # validate inputs
        self.input.hostedZoneID(hosted_zone_id, title)
        self.input.aliasList(alias_list, title + ' alias_list')

    # check for existence of hosted zone
        try:
            response = self.connection.list_hosted_zones()
        except:
            raise R53ConnectionError(title + ' list_hosted_zones()')
        hz_list = []
        if 'HostedZones' in response:
            response_list = response['HostedZones']
            for hz_dict in response_list:
                hz_id = hz_dict['Id'].replace('/hostedzone/', '')
                hz_list.append(hz_id)
        if hosted_zone_id not in hz_list:
            raise Exception('\nHosted Zone %s does not exist.' % hosted_zone_id)

    # retrieve current alias target names from hosted zone records
        current_name_list = []
        current_alias_list = self.aliasTargetList(hosted_zone_id)
        for alias in current_alias_list:
            current_name_list.append(alias['name'])

    # construct new name list from input
        new_name_list = []
        for alias in alias_list:
            new_name_list.append(alias['name'])

    # create list of actions
        create_list = list(set(new_name_list) - set(current_name_list))
        delete_list = list(set(current_name_list) - set(new_name_list))
        upsert_list = list(set(new_name_list).intersection(set(current_name_list)))

    # create keyword argument definitions
        kw_args = {
            'HostedZoneId': hosted_zone_id,
            'ChangeBatch': { 'Changes': [] }
        }
        for alias in alias_list:
            change_details = {
                'ResourceRecordSet': {
                    'Name': alias['name'],
                    'Type': 'A',
                    'AliasTarget': {
                        'HostedZoneId': alias['hostedZoneID'],
                        'DNSName': alias['dnsName'],
                        'EvaluateTargetHealth': alias['evaluateTargetHealth']
                    }
                }
            }
            if alias['name'] in upsert_list:
                change_details['Action'] = 'UPSERT'
            elif alias['name'] in create_list:
                change_details['Action'] = 'CREATE'
            kw_args['ChangeBatch']['Changes'].append(change_details)
        for alias in current_alias_list:
            if alias['name'] in delete_list:
                change_details = {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': alias['name'],
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': alias['hostedZoneID'],
                            'DNSName': alias['dnsName'],
                            'EvaluateTargetHealth': alias['evaluateTargetHealth']
                        }
                    }
                }
                kw_args['ChangeBatch']['Changes'].append(change_details)

    # send request to update alias targets
        try:
            self.connection.change_resource_record_sets(**kw_args)
        except:
            raise R53ConnectionError(title + ' change_resource_record_sets()')

    # report result and return True
        print('Hosted zone %s alias target records updated.' % hosted_zone_id)
        return True

    def unitTests(self):
        hzList = self.findHostedZones()
        aliasList = self.aliasTargetList(hzList[0])
        newList = deepcopy(aliasList)
        new_target = deepcopy(newList[0])
        new_target['name'] = 'api.collectiveacuity.com.'
        newList.append(new_target)
        self.updateAliasTargets(hzList[0], newList)
        self.updateAliasTargets(hzList[0], aliasList)
        return self

dummy = ''
# TODO: add ipv6 dns to awsR53.aliasTargetList() validation
