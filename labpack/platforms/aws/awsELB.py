__author__ = 'rcj1492'
__created__ = '2015.10'

# pip install boto3
# https://pypi.python.org/pypi/boto3
# https://boto3.readthedocs.org/en/latest/

from awsDocker.awsValidation import ec2Input, iamInput
import boto3
import os
import json

class ELBConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to AWS ELB with %s request.' % message
        super(ELBConnectionError, self).__init__(text)
        self.errors = errors

class awsELB(object):

    '''
        a class of methods for interacting with the AWS Elastic Load Balancer

        dependencies:
            from labAWS.awsValidation import ec2Input, iamInput
            import boto3
            import os
            import json
    '''

    __name__ = 'awsELB'

    def __init__(self, aws_credentials, aws_rules, aws_region=''):

        '''
            a method for initializing the connection to ELB

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

    # construct elb client connection
        for key, value in self.cred.items():
            os.environ[key] = value
        self.connection = boto3.client('elb')

    def findLoadBalancers(self, tag_values=None):
        
        '''
            a method to discover load-balancers on AWS ELB

        :param tag_values: [optional] list of tag values
        :return: list of load balancer name strings
        '''

        title = self.__name__ + '.findLoadBalancers()'

    # validate inputs
        if tag_values:
            self.input.tagValues(tag_values, title + ' tag values')

    # request list of load balancers
        tag_text = ''
        if tag_values:
            tag_text = ' with tag values %s' % tag_values
        query_text = 'Querying AWS region %s for load balancers%s.' % (os.environ['AWS_DEFAULT_REGION'], tag_text)
        print(query_text)
        try:
            response = self.connection.describe_load_balancers()
        except:
            raise ELBConnectionError(title + ' describe_load_balancers()')

    # construct an index of load balancers and tags from response
        lb_index = []
        if 'LoadBalancerDescriptions' in response.keys():
            for lb_dict in response['LoadBalancerDescriptions']:
                details = {
                    'loadBalancerName': lb_dict['LoadBalancerName'],
                    'tags': []
                }
                lb_index.append(details)

    # retrieve tags associated with load-balancers
        for balancer in lb_index:
            try:
                response = self.connection.describe_tags(
                    LoadBalancerNames=[balancer['loadBalancerName']]
                )
            except:
                raise ELBConnectionError(title + ' describe_tags()')
            if 'TagDescriptions' in response.keys():
                for lb_dict in response['TagDescriptions']:
                    if 'Tags' in lb_dict.keys():
                        for tag in lb_dict['Tags']:
                            balancer['tags'].append(tag['Value'])

    # construct a list of autoscaling groups from search of index
        lb_list = []
        if tag_values:
            for balancer in lb_index:
                matching_set = set(tag_values) - set(balancer['tags'])
                if not matching_set:
                    lb_list.append(balancer['loadBalancerName'])
        else:
            for balancer in lb_index:
                lb_list.append(balancer['loadBalancerName'])

    # report results and return list
        if lb_list:
            print_out = 'Found load balancer'
            if len(lb_list) > 1:
                print_out += 's'
            i_counter = 0
            for balancer in lb_list:
                if i_counter > 0:
                    print_out += ','
                print_out += ' ' + balancer
                i_counter += 1
            print_out += '.'
            print(print_out)
        else:
            print('No load balancers found.')

        return lb_list

    def loadBalancerDetails(self, lb_name):

        '''
            a method to discover the details of a load balancer on AWS ELB

        :param lb_name: string with name of load balancer
        :return: dictionary with details of load balancer

            load balancer attributes:
                ['loadBalancerName']
                ['dnsName']
                ['securityGroupIDs']
                ['vpcID']
                ['subnetIDs']
                ['healthCheckTarget']
                ['healthCheckTimeout']
                ['healthCheckInterval']
                ['healthyThreshold']
                ['unhealthyThreshold']
                ['region']
                ['sslCertARN']
                ['instanceIDs']
                ['policies']
                ['listeners']
                ['tags']
        '''

        title = self.__name__ + '.loadBalancerDetails()'

    # validate inputs
        self.input.lbName(lb_name, title + ' load balancer name')

    # check for existence of load-balancer
        try:
            response = self.connection.describe_load_balancers()
        except:
            raise ELBConnectionError(title + ' describe_load_balancers()')
        lb_list = []
        for lb_dict in response['LoadBalancerDescriptions']:
            lb_list.append(lb_dict['LoadBalancerName'])
        if lb_name not in lb_list:
            raise Exception('\nLoad balancer %s does not exist.' % lb_name)

    # request load balancer description from AWS
        try:
            response = self.connection.describe_load_balancers(
                LoadBalancerNames=[ lb_name ]
            )
        except:
            raise ELBConnectionError(title + ' describe_load_balancers()')
        lb_dict = response['LoadBalancerDescriptions'][0]
        print(lb_dict)
    # construct launch configuration details from response
        details = {}
        details['loadBalancerName'] = lb_dict['LoadBalancerName']
        details['dnsName'] = lb_dict['DNSName']
        details['securityGroupIDs'] = lb_dict['SecurityGroups']
        details['vpcID'] = lb_dict['VPCId']
        details['subnetIDs'] = lb_dict['Subnets']
        details['healthCheckTarget'] = lb_dict['HealthCheck']['Target']
        details['healthCheckTimeout'] = lb_dict['HealthCheck']['Timeout']
        details['healthCheckInterval'] = lb_dict['HealthCheck']['Interval']
        details['healthyThreshold'] = lb_dict['HealthCheck']['HealthyThreshold']
        details['unhealthyThreshold'] = lb_dict['HealthCheck']['UnhealthyThreshold']
        details['region'] = os.environ['AWS_DEFAULT_REGION']
        details['sslCertARN'] = '',
        details['listeners'] = []
        details['instanceIDs'] = []
        details['policies'] = []
        details['tags'] = []
        for listener in lb_dict['ListenerDescriptions']:
            listener_details = {
                'protocol': listener['Listener']['Protocol'],
                'publicPort': listener['Listener']['LoadBalancerPort'],
                'instancePort': listener['Listener']['InstancePort']
            }
            if 'SSLCertificateId' in listener['Listener']:
                details['sslCertARN'] = listener['Listener']['SSLCertificateId']
            details['listeners'].append(listener_details)
        if 'Instances' in lb_dict.keys():
            for instance in lb_dict['Instances']:
                details['instanceIDs'].append(instance['InstanceId'])
        if 'Policies' in lb_dict.keys():
            details['policies'] = lb_dict['Policies']

    # retrieve tags associated with load-balancer
        try:
            response = self.connection.describe_tags(
                LoadBalancerNames=[details['loadBalancerName']]
            )
        except:
            raise ELBConnectionError(title + ' describe_tags()')
        if 'TagDescriptions' in response.keys():
            for lb_dict in response['TagDescriptions']:
                if 'Tags' in lb_dict.keys():
                    details['tags'] = lb_dict['Tags']

        return details

    def createLoadBalancer(self, load_balancer_config, tag_list=None):

        '''
            a method to create a load-balancer on AWS EC2

        :param load_balancer_config: dictionary with load-balancer definitions
        :param tag_list: [optional] list of AWS key value tag dictionaries
        :return: string with DNS address of load balancer
        '''

        title = 'createLoadBalancer'

    # validate input
        self.input.loadBalancerConfig(load_balancer_config, title + ' load balancer configuration')

    # create listener list
        add_ssl_policy = False
        listener_list = []
        for listener in load_balancer_config['listeners']:
            details = {
                'Protocol': listener['publicProtocol'],
                'LoadBalancerPort': listener['publicPort'],
                'InstanceProtocol': listener['instanceProtocol'],
                'InstancePort': listener['instancePort']
            }
            if listener['publicProtocol'] == 'HTTPS':
                add_ssl_policy = True
                details['SSLCertificateId'] = load_balancer_config['sslCertARN']
            listener_list.append(details)

    # create keyword argument definitions
        kw_args = {
            'LoadBalancerName': load_balancer_config['loadBalancerName'],
            'Listeners': listener_list,
            'Subnets': load_balancer_config['subnetIDs'],
            'SecurityGroups': load_balancer_config['securityGroupIDs'],
        }
        if tag_list:
            self.input.tags(tag_list, title + ' tag list')
            kw_args['Tags'] = tag_list

    # send request to create load-balancer
        try:
            response = self.connection.create_load_balancer(**kw_args)
        except:
            raise ELBConnectionError(title + ' create_load_balancer()')

    # send request to attach health check
        health_args = {
            'LoadBalancerName': load_balancer_config['loadBalancerName'],
            'HealthCheck': {
                'Target': load_balancer_config['healthCheckTarget'],
                'Interval': load_balancer_config['healthCheckInterval'],
                'Timeout': load_balancer_config['healthCheckTimeout'],
                'UnhealthyThreshold': load_balancer_config['unhealthyThreshold'],
                'HealthyThreshold': load_balancer_config['healthyThreshold']
            }
        }
        try:
            self.connection.configure_health_check(**health_args)
        except:
            raise ELBConnectionError(title + ' configure_health_check()')

    # send request to attach ssl policy
        if add_ssl_policy:
            ssl_attr_list = self.rules['ec2']['loadBalancers']['policyAttributeDescriptions']['sslNegotiation']
            ssl_args = {
                'LoadBalancerName': load_balancer_config['loadBalancerName'],
                'PolicyTypeName': 'SSLNegotiationPolicyType',
                'PolicyAttributes': ssl_attr_list
            }
            ssl_args['PolicyName'] = ssl_args['PolicyTypeName'] + '-' + ssl_args['LoadBalancerName']
            try:
                self.connection.create_load_balancer_policy(**ssl_args)
            except:
                raise ELBConnectionError(title + ' create_load_balancer_policy()')

    # report result and return DNS name
        print('Load-balancer %s created.' % load_balancer_config['loadBalancerName'])
        dns_name = response['DNSName']
        return dns_name

    def removeLoadBalancer(self, lb_name):

        '''
            a method to remove a load balancer from AWS EC2

        :param lc_name: string with name of load balancer
        :return: True
        '''

        title = 'removeLoadBalancer'

    # validate inputs
        self.input.lbName(lb_name, title + ' launch config name')

    # validate list of launch configuration files
        try:
            response = self.connection.describe_load_balancers()
        except:
            raise ELBConnectionError(title + ' describe_load_balancers()')
        lb_list = []
        for lb_dict in response['LoadBalancerDescriptions']:
            lb_list.append(lb_dict['LoadBalancerName'])
        if not lb_name in lb_list:
            print('Load-balancer %s does not exist.' % lb_name)
            return True

    # remove launch configuration
        try:
            self.connection.delete_load_balancer(
                LoadBalancerName=lb_name
            )
        except:
            raise ELBConnectionError(title + ' delete_load_balancer()')

        print('Load-balancer %s deleted.' % lb_name)
        return True

    def checkInstanceHealth(self, lb_name, instance_id):

        '''
            a method to determine whether instance is InService on AWS ELB

        :param lb_name: string with name of load balancer
        :param instance_id: string with AWS id of instance
        :return: string with ELB health status
        '''

        title = 'checkInstanceHealth'

    # validate inputs
        self.input.instanceID(instance_id, title + ' instanceID')
        self.input.lbName(lb_name, title + ' load balancer name')

    # check for existence of resources
        lb_details = self.loadBalancerDetails(lb_name)
        if not lb_details['instanceIDs']:
            raise Exception('\nLoad-balancer %s currently has no instances registered to it.' % lb_name)
        elif not instance_id in lb_details['instanceIDs']:
            raise Exception('\nInstance %s is not part of load-balancer %s.' % (instance_id, lb_name))

    # send request for instance health report
        try:
            response = self.connection.describe_instance_health(
                LoadBalancerName=lb_name,
                Instances=[ { 'InstanceId': instance_id } ]
            )
        except:
            raise ELBConnectionError(title + ' describe_instance_health()')
        instance_state = response['InstanceStates'][0]['State']

        return instance_state

    def unitTests(self, elb_obj):
        elbObj = self.input.elbSettings(elb_obj, self.__name__ + '.unitTests()')
        lbConfig = elbObj['loadBalancerConfiguration']
        lbList = self.findLoadBalancers()
        assert lbConfig['loadBalancerName'] not in lbList # prevent deletion of live assets
        if lbList:
            lbName = lbList[0]
            lbDetails = self.loadBalancerDetails(lbName)
            text = 'Load-balancer %s currently has no instances registered to it.' % lbName
            if lbDetails['instanceIDs']:
                instanceID = lbDetails['instanceIDs'][0]
                instanceState = self.checkInstanceHealth(lbName, instanceID)
                text = 'Instance %s registered to load-balancer "%s" is %s' % (instanceID, lbName, instanceState)
            print(text)
        self.createLoadBalancer(lbConfig)
        newDetails = self.loadBalancerDetails(lbConfig['loadBalancerName'])
        assert newDetails['sslCertARN']
        self.removeLoadBalancer(newDetails['loadBalancerName'])
        return self

dummy = ''