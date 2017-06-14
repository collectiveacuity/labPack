__author__ = 'rcj1492'
__created__ = '2015.07'

# pip install boto3
# https://pypi.python.org/pypi/boto3
# https://boto3.readthedocs.org/en/latest/

from awsDocker.awsValidation import ec2Input, iamInput
import boto3
import os
import json
from copy import deepcopy

class ASGConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to AWS ASG with %s request.' % message
        super(ASGConnectionError, self).__init__(text)
        self.errors = errors

class awsASG(object):
    
    '''
        a class of methods for interacting with the AWS Auto-Scaling Group
        
        dependencies:
            from labAWS.awsValidation import ec2Input, iamInput
            import boto3
            import os
    '''

    __name__ = 'awsASG'

    def __init__(self, aws_credentials, aws_rules, aws_region=''):

        '''
            a method for initializing the connection to ASG

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
        self.connection = boto3.client('autoscaling')

    def findLaunchConfigs(self):
        
        '''
            a method to discover the launch configurations on AWS EC2
        
        :return: list of launch configuration name strings
        '''

        title = 'findLaunchConfigs'

    # request list of launch configuration files
        print('Querying AWS region %s for launch configurations.' % os.environ['AWS_DEFAULT_REGION'])
        try:
            response = self.connection.describe_launch_configurations()
        except:
            raise ASGConnectionError(title + ' describe_launch_configurations')

    # create list of launch configurations from response
        lc_list = []
        if 'LaunchConfigurations' in response:
            response_list = response['LaunchConfigurations']
            for lc_dict in response_list:
                lc_list.append(lc_dict['LaunchConfigurationName'])

    # check to see if any launch configurations are found
        if lc_list:
            print_out = 'Found launch configuration'
            if len(lc_list) > 1:
                print_out += 's'
            i_counter = 0
            for config in lc_list:
                if i_counter > 0:
                    print_out += ','
                print_out += ' ' + config
                i_counter += 1
            print_out += '.'
            print(print_out)
        else:
            print('No launch configurations found.')

        return lc_list

    def launchConfigDetails(self, lc_name):

        '''
            a method to discover the details of a launch configuration on AWS EC2

        :param lc_name: string with name of launch configuration
        :return: dictionary with details of launch configuration

            launch attributes:
                ['launchConfigurationName']
                ['imageID']
                ['snapshotID']
                ['instanceType']
                ['volumeType']
                ['ebsOptimized']
                ['spotPrice']
                ['keyPair']
                ['securityGroupIDs']
                ['instanceMonitoring']
                ['iamProfileRole']
                ['region']
        '''

        title = 'launchConfigDetails'

    # validate inputs
        self.input.lcName(lc_name, title + ' launch config name')

    # check for existence of launch configuration resource
        try:
            response = self.connection.describe_launch_configurations()
        except:
            raise ASGConnectionError(title + ' describe_launch_configurations')
        lc_list = []
        if 'LaunchConfigurations' in response:
            response_list = response['LaunchConfigurations']
            for lc_dict in response_list:
                lc_list.append(lc_dict['LaunchConfigurationName'])
        if lc_name not in lc_list:
            raise Exception('\nLaunch configuration %s does not exist.' % lc_name)

    # request details about launch configuration resource
        try:
            response = self.connection.describe_launch_configurations(
                LaunchConfigurationNames=[ lc_name ]
            )
        except:
            raise ASGConnectionError(title + ' describe_launch_configurations')

    # create dictionary of launch configuration details from response
        lc_dict = response['LaunchConfigurations'][0]
        details = {}
        details['launchConfigurationName'] = lc_dict['LaunchConfigurationName']
        details['imageID'] = lc_dict['ImageId']
        details['snapshotID'] = ''
        details['instanceType'] = lc_dict['InstanceType']
        details['volumeType'] = lc_dict['BlockDeviceMappings'][0]['Ebs']['VolumeType']
        details['ebsOptimized'] = lc_dict['EbsOptimized']
        details['spotPrice'] = 0
        details['keyPair'] = lc_dict['KeyName']
        details['securityGroupIDs'] = lc_dict['SecurityGroups']
        details['instanceMonitoring'] = lc_dict['InstanceMonitoring']['Enabled']
        details['region'] = os.environ['AWS_DEFAULT_REGION']
        if 'IamInstanceProfile' in lc_dict:
            details['iamProfileRole'] = lc_dict['IamInstanceProfile']
        if 'SpotPrice' in lc_dict:
            details['spotPrice'] = lc_dict['SpotPrice']
        if 'SnapshotId' in lc_dict['BlockDeviceMappings'][0]['Ebs']:
            details['snapshotID'] = lc_dict['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
        return details

    def createLaunchConfig(self, launch_config):

        '''
            a method for creating a launch configuration file on AWS ECS

        :param launch_config: dictionary with launch configuration settings
        :return: string with launchConfigurationName
        '''

        title = 'createLaunchConfig'

    # validate inputs
        self.input.launchConfig(launch_config, title=title)

    # create block_device map
        block_device = [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeType': launch_config['volumeType']
                }
            }
        ]
        if launch_config['snapshotID']:
            block_device[0]['Ebs']['SnapshotId'] = launch_config['snapshotID']

    # create keyword argument definitions
        kw_args = {
            'LaunchConfigurationName': launch_config['launchConfigurationName'],
            'ImageId': launch_config['imageID'],
            'KeyName': launch_config['keyPair'],
            'SecurityGroups': launch_config['securityGroupIDs'],
            'InstanceType': launch_config['instanceType'],
            'BlockDeviceMappings': block_device,
            'InstanceMonitoring': { 'Enabled': launch_config['instanceMonitoring'] },
            'EbsOptimized': launch_config['ebsOptimized']
        }
        if launch_config['spotPrice']:
            kw_args['SpotPrice'] = launch_config['spotPrice']
        if launch_config['iamProfileRole']:
            kw_args['IamInstanceProfile'] = launch_config['iamProfileRole']

    # check that security groups exist

    # check that keypair exists

    # send request for launch configuration
        try:
            self.connection.create_launch_configuration(**kw_args)
        except:
            raise ASGConnectionError(title + ' create_launch_configuration()')

    # report result and return launch conifguration name
        lc_name = launch_config['launchConfigurationName']
        print('Launch Configuration %s created.' % lc_name)
        return lc_name

    def removeLaunchConfig(self, lc_name):

        '''
            a method to remove a launch configuration from AWS EC2

        :param lc_name: string with name of launch configuration
        :return: True
        '''

        title = 'removeLaunchConfig'

    # validate inputs
        self.input.lcName(lc_name, title + ' launch config name')

    # check for existence of launch configuration file
        print('Removing launch configuration %s.' % lc_name)
        try:
            response = self.connection.describe_launch_configurations(
                LaunchConfigurationNames=[ lc_name ]
            )
        except:
            raise ASGConnectionError(title + ' describe_launch_configurations()')
        if not response['LaunchConfigurations']:
            print('\nLaunch Configuration %s does not exist.' % lc_name)
            return True

    # remove launch configuration
        try:
            self.connection.delete_launch_configuration(
                LaunchConfigurationName=lc_name
            )
        except:
            raise ASGConnectionError(title + ' delete_launch_configuation()')

        print('Launch Configuration %s deleted.' % lc_name)
        return True

    def findAutoScalers(self, tag_values=None):

        '''
            a method to discover the auto-scaling groups on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of auto-scaling groups
        '''

        title = self.__name__ + '.findAutoScalers()'

    # validate inputs
        if tag_values:
            self.input.tagValues(tag_values, title + ' tag values')

    # request list of auto-scaling groups
        tag_text = ''
        if tag_values:
            tag_text = ' with tag values %s' % tag_values
        query_text = 'Querying AWS region %s for auto-scaling groups%s.' % (os.environ['AWS_DEFAULT_REGION'], tag_text)
        print(query_text)
        try:
            response = self.connection.describe_auto_scaling_groups()
        except:
            raise ASGConnectionError(title + ' describe_auto_scaling_groups()')

    # construct an index of auto-scaling groups and tags from response
        asg_index = []
        if 'AutoScalingGroups' in response.keys():
            response_list = response['AutoScalingGroups']
            for asg_dict in response_list:
                details = {
                    'autoScalingGroupName': asg_dict['AutoScalingGroupName'],
                    'tags': []
                }
                if 'Tags' in asg_dict.keys():
                    for tag in asg_dict['Tags']:
                        details['tags'].append(tag['Value'])
                asg_index.append(details)

    # construct a list of autoscaling groups from search of index
        asg_list = []
        if tag_values:
            for asg in asg_index:
                matching_set = set(tag_values) - set(asg['tags'])
                if not matching_set:
                    asg_list.append(asg['autoScalingGroupName'])
        else:
            for asg in asg_index:
                asg_list.append(asg['autoScalingGroupName'])

    # report findings and return list
        if asg_list:
            print_out = 'Found auto-scaling group'
            if len(asg_list) > 1:
                print_out += 's'
            list_counter = 0
            for name in asg_list:
                if list_counter > 0:
                    print_out += ','
                print_out += ' ' + name
                list_counter += 1
            print_out += '.'
            print(print_out)
        else:
            print('No auto-scaling groups found.')
        return asg_list

    def autoScalerDetails(self, asg_name):

        '''
            a method to discover the details of an auto-scaling group on AWS EC2

        :param asg_name: string with name of auto-scaling group
        :return: dictionary with details of auto-scaling group

            auto-scaling group attributes:
                ['autoScalingGroupName']
                ['launchConfigurationName']
                ['subnetIDs']
                ['minSize']
                ['maxSize']
                ['desiredCapacity']
                ['defaultCooldown']
                ['healthCheckType']
                ['healthCheckGracePeriod']
                ['terminationPolicies']
                ['loadBalancers']
                ['instances'][0]['instanceID']
                ['instances'][0]['healthStatus']
                ['status']
                ['tags']
                ['region']
        '''

        title = 'autoScalerDetails'

    # validate inputs
        self.input.asgName(asg_name, title + ' autoscaling group name')

    # check for existence of auto-scaler
        asg_list = []
        try:
            response = self.connection.describe_auto_scaling_groups()
        except:
            raise ASGConnectionError(title + ' describe_auto_scaling_groups()')
        if 'AutoScalingGroups' in response.keys():
            response_list = response['AutoScalingGroups']
            for group in response_list:
                asg_list.append(group['AutoScalingGroupName'])
        if not asg_name in asg_list:
            raise Exception('\nAuto-scaling group %s does not exist.' % asg_name)

    # request details about auto scaling group
        try:
            response = self.connection.describe_auto_scaling_groups(
                AutoScalingGroupNames=[ asg_name ]
            )
        except:
            raise ASGConnectionError(title + ' describe_auto_scaling_groups()')

    # construct auto scaling group details from response
        asg_dict = response['AutoScalingGroups'][0]
        details = {}
        details['launchConfigurationName'] = asg_dict['LaunchConfigurationName']
        details['autoScalingGroupName'] = asg_dict['AutoScalingGroupName']
        details['subnetIDs'] = asg_dict['VPCZoneIdentifier'].split(',')
        details['minSize'] = asg_dict['MinSize']
        details['maxSize'] = asg_dict['MaxSize']
        details['desiredCapacity'] = asg_dict['DesiredCapacity']
        details['healthCheckType'] = asg_dict['HealthCheckType']
        details['defaultCooldown'] = asg_dict['DefaultCooldown']
        details['healthCheckGracePeriod'] = asg_dict['HealthCheckGracePeriod']
        details['terminationPolicies'] = asg_dict['TerminationPolicies']
        details['region'] = os.environ['AWS_DEFAULT_REGION']

    # construct (optional) list attributes
        details['loadBalancers'] = []
        details['instances'] = []
        details['tags'] = []
        if 'LoadBalancerNames' in asg_dict.keys():
            for balancer in asg_dict['LoadBalancerNames']:
                details['loadBalancers'] = balancer
        if 'Instances' in asg_dict.keys():
            for instance in asg_dict['Instances']:
                i_details = {}
                i_details['instanceID'] = instance['InstanceId']
                i_details['healthStatus'] = instance['HealthStatus']
                details['instances'].append(i_details)
        if 'Tags' in asg_dict.keys():
            if asg_dict['Tags']:
                for tag in asg_dict['Tags']:
                    tag_details = {}
                    tag_details['Key'] = tag['Key']
                    tag_details['Value'] = tag['Value']
                    details['tags'].append(tag_details)
        return details

    def createAutoScaler(self, asg_config, tag_list=None):

        '''
            a method for creating an auto-scaling group on AWS EC2
        :param asg_config: dictionary with autoscaling group definitions
        :param tag_list: [optional] list of AWS key value tag dictionaries
        :return: string with autoScalingGroupName
        '''

        title = 'createAutoScaler'

    # validate inputs
        self.input.autoScaleConfig(asg_config, title)
        asg_name = asg_config['autoScalingGroupName']
        if tag_list:
            self.input.tags(tag_list, title)
            for tag in tag_list:
                tag['PropagateAtLaunch'] = True

    # check that auto-scaling group does not already exist
        asg_list = []
        try:
            response = self.connection.describe_auto_scaling_groups()
        except:
            raise ASGConnectionError(title + ' describe_auto_scaling_groups()')
        if 'AutoScalingGroups' in response.keys():
            response_list = response['AutoScalingGroups']
            for group in response_list:
                asg_list.append(group['AutoScalingGroupName'])
        if asg_name in asg_list:
            raise Exception('\nAuto-scaling group %s already exists.' % asg_name)

    # check that launch configuration exists
        lc_name = asg_config['launchConfigurationName']
        try:
            assert self.launchConfigDetails(lc_name)
        except:
            raise Exception('\nLaunch configuration %s for auto scaling group %s does not exist.' % (lc_name, asg_config['autoScalingGroupName']))

    # check that subnets exist

    # construct subnet string
        subnet_string = ''
        for i in range(len(asg_config['subnetIDs'])):
            if i != 0:
                subnet_string += ','
            subnet_string += asg_config['subnetIDs'][i]

    # create keyword argument definitions
        kw_args={
            'AutoScalingGroupName': asg_config['autoScalingGroupName'],
            'LaunchConfigurationName': lc_name,
            'VPCZoneIdentifier': subnet_string,
            'MinSize': asg_config['minSize'],
            'MaxSize': asg_config['maxSize'],
            'DesiredCapacity': asg_config['desiredCapacity'],
            'DefaultCooldown': asg_config['defaultCooldown'],
            'HealthCheckType': asg_config['healthCheckType'],
            'HealthCheckGracePeriod': asg_config['healthCheckGracePeriod'],
            'TerminationPolicies': asg_config['terminationPolicies']
        }
        if tag_list:
            kw_args['Tags'] = tag_list

    # send request to create aut-scaling group
        try:
            self.connection.create_auto_scaling_group(**kw_args)
        except:
            raise ASGConnectionError(title + ' create_auto_scaling_group')

        asg_name = asg_config['autoScalingGroupName']
        print('Auto-scaling group %s has been created.' % asg_name)
        return asg_name

    def updateAutoScaler(self, updated_asg_config, tag_list=None):

        '''
            a method to update the properties of an auto-scaling group on AWS EC2

        :updated_asg_config: dictionary with autoscaling group definitions
        :return: string with autoScalingGroupName
        '''

        title = ' updateAutoScaler'

    # validate inputs
        self.input.autoScaleConfig(updated_asg_config, title)
        asg_name = updated_asg_config['autoScalingGroupName']
        lc_name = updated_asg_config['launchConfigurationName']
        if tag_list:
            self.input.tags(tag_list, title)
            for tag in tag_list:
                tag['PropagateAtLaunch'] = True

    # check for existence of auto scaling group
        print('Updating auto scaling group %s.' % asg_name)
        asg_details = self.autoScalerDetails(asg_name)

    # disable metric monitoring
        lc_details = self.launchConfigDetails(lc_name)
        if lc_details['instanceMonitoring']:
            print('Instance monitoring is enabled in launch configurations.\nDisabling metric collection temporarily ...', end='', flush=True)
            try:
                self.connection.disable_metrics_collection(
                    AutoScalingGroupName=asg_name
                )
            except:
                raise ASGConnectionError(title + ' disable_metrics_collection()')
            print(' Done.')

    # construct subnet string
        subnet_string = ''
        for i in range(len(updated_asg_config['subnetIDs'])):
            if i != 0:
                subnet_string += ','
            subnet_string += updated_asg_config['subnetIDs'][i]

    # create keyword argument definitions
        kw_args={
            'AutoScalingGroupName': updated_asg_config['autoScalingGroupName'],
            'LaunchConfigurationName': lc_name,
            'VPCZoneIdentifier': subnet_string,
            'MinSize': updated_asg_config['minSize'],
            'MaxSize': updated_asg_config['maxSize'],
            'DesiredCapacity': updated_asg_config['desiredCapacity'],
            'DefaultCooldown': updated_asg_config['defaultCooldown'],
            'HealthCheckType': updated_asg_config['healthCheckType'],
            'HealthCheckGracePeriod': updated_asg_config['healthCheckGracePeriod'],
            'TerminationPolicies': updated_asg_config['terminationPolicies']
        }

    # send request to update auto-scaling group
        try:
            self.connection.update_auto_scaling_group(**kw_args)
        except:
            raise ASGConnectionError(title + ' update_auto_scaling_group()')

    # create keyword argument definitions for tag updates
        tag_create_args = {
            'Tags': []
        }
        tag_delete_args = {
            'Tags': []
        }
        if tag_list:
            for tag in tag_list:
                tag['PropagateAtLaunch'] = True
                tag['ResourceId'] = updated_asg_config['autoScalingGroupName']
                tag['ResourceType'] = 'auto-scaling-group'
                tag_create_args['Tags'].append(tag)
            if asg_details['tags']:
                for tag in asg_details['tags']:
                    tag['PropagateAtLaunch'] = True
                    tag['ResourceId'] = updated_asg_config['autoScalingGroupName']
                    tag['ResourceType'] = 'auto-scaling-group'
                    tag_delete_args['Tags'].append(tag)

    # send request to delete and update tags
        if tag_delete_args['Tags']:
            try:
                self.connection.delete_tags(**tag_delete_args)
            except:
                raise ASGConnectionError(title + ' delete_tags()')
        if tag_create_args['Tags']:
            try:
                self.connection.create_or_update_tags(**tag_create_args)
            except:
                raise ASGConnectionError(title + ' create_or_update_tags()')
        print('Auto-scaling group %s has been updated.' % asg_name)

    # re-enable metric collection on auto-scaling group
        if lc_details['instanceMonitoring']:
            print('Re-enabling metric collection ...', end='', flush=True)
            try:
                self.connection.enable_metrics_collection(
                    AutoScalingGroupName=asg_name,
                    Granularity='1Minute'
                )
            except:
                raise ASGConnectionError(title + ' enable_metrics_collection()')
            print(' Done.')

        return asg_name

    def removeAutoScaler(self, asg_name):

        '''
            a method to remove an auto-scaling group from AWS EC2

        :param asg_name: string with name of auto-scaling group
        :return: True
        '''

        title = 'removeAutoScaler'

    # validate inputs
        self.input.asgName(asg_name, title)

    # check for existence of auto-scaling group
        print('Removing auto-scaling group %s.' % asg_name)
        asg_list = []
        try:
            response = self.connection.describe_auto_scaling_groups()
        except:
            raise ASGConnectionError(title + ' describe_auto_scaling_groups()')
        if 'AutoScalingGroups' in response.keys():
            response_list = response['AutoScalingGroups']
            for group in response_list:
                asg_list.append(group['AutoScalingGroupName'])
        if not asg_name in asg_list:
            print('Auto-scaling group %s does not exist.' % asg_name)
            return True

    # remove launch configuration
        try:
            self.connection.delete_auto_scaling_group(
                AutoScalingGroupName=asg_name,
                ForceDelete=True
            )
        except:
            raise ASGConnectionError(title + ' delete_auto_scaling_group()')

    # report result and return True
        print('Auto-scaling group %s deleted.' % asg_name)
        return True

    def attachLoadBalancer(self, lb_name, asg_name):

        '''
            a method to attach a load-balancer to an auto-scaling group on AWS EC2
        :param lb_name: string with name of load-balancer
        :param asg_name: string with name of auto-scaling group
        :return: True
        '''

        title = 'attachLoadBalancer'

    # validate inputs
        self.input.lbName(lb_name, title)
        self.input.asgName(asg_name, title)

    # check for existence of auto-scaling group
        print('Attaching load-balancer %s to auto scaling group %s.' % (lb_name, asg_name))
        self.autoScalerDetails(asg_name)

    # check for existence of load balancer

    # attach load balancer to auto-scaling group
        try:
            response = self.connection.attach_load_balancers(
                AutoScalingGroupName=asg_name,
                LoadBalancerNames=[ lb_name ]
            )
        except:
            raise ASGConnectionError(title + ' attach_load_balancers()')

    # report result and return True
        print('Load balancer %s has been attached to Auto-Scaling Group %s' % (lb_name, asg_name))
        return True

    def findScalingPolicies(self, asg_name):
        response = self.connection.describe_policies(
            AutoScalingGroupName='string',
            PolicyNames=[
                'string',
            ],
            PolicyTypes=[
                'string',
            ],
            NextToken='string',
            MaxRecords=123
        )
        return True

    def createScalingPolicy(self, policy_name, asg_name):
        response = self.connection.put_scaling_policy(
            AutoScalingGroupName='string',
            PolicyName='string',
            PolicyType='string',
            AdjustmentType='string',
            MinAdjustmentStep=123,
            MinAdjustmentMagnitude=123,
            ScalingAdjustment=123,
            Cooldown=123,
            MetricAggregationType='string',
            StepAdjustments=[
                {
                    'MetricIntervalLowerBound': 123.0,
                    'MetricIntervalUpperBound': 123.0,
                    'ScalingAdjustment': 123
                },
            ],
            EstimatedInstanceWarmup=123
        )
        return True

    def updateScalingPolicy(self, policy_name, asg_name):
        response = self.connection.delete_policy(
            AutoScalingGroupName='string',
            PolicyName='string'
        )
        response = self.connection.put_scaling_policy(
            AutoScalingGroupName='string',
            PolicyName='string',
            PolicyType='string',
            AdjustmentType='string',
            MinAdjustmentStep=123,
            MinAdjustmentMagnitude=123,
            ScalingAdjustment=123,
            Cooldown=123,
            MetricAggregationType='string',
            StepAdjustments=[
                {
                    'MetricIntervalLowerBound': 123.0,
                    'MetricIntervalUpperBound': 123.0,
                    'ScalingAdjustment': 123
                },
            ],
            EstimatedInstanceWarmup=123
        )
        return True

    def unitTests(self):
        asgObj = json.loads(open('../models/asg-obj-model.json').read())
        launchConfig = deepcopy(asgObj['launchConfiguration'])
        autoScaler = deepcopy(asgObj['autoScalingConfiguration'])
        launchConfig['launchConfigurationName'] = 'test-lc-useast1-2015-10-06-21-01-34'
        launchConfig['imageID'] = 'ami-8da458e6'
        launchConfig['snapshotID'] = ''
        launchConfig['instanceMonitoring'] = True
        autoScaler['launchConfigurationName'] = 'test-lc-useast1-2015-10-06-21-01-34'
        autoScaler['autoScalingGroupName'] = 'test-asg-useast1-2015-10-15-17-51-05'
        lcList = self.findLaunchConfigs()
        assert launchConfig['launchConfigurationName'] not in lcList
        asgList = self.findAutoScalers()
        assert autoScaler['autoScalingGroupName'] not in asgList
        lcName = self.createLaunchConfig(launchConfig)
        lcDetails = self.launchConfigDetails(lcName)
        assert lcDetails['volumeType'] == 'gp2'
        asgName = self.createAutoScaler(autoScaler, [{'Key':'Stack','Value':'unitTest'}])
        asgDetails = self.autoScalerDetails(asgName)
        assert asgDetails['healthCheckType'] == 'EC2'
        autoScaler['terminationPolicies'].insert(0, 'OldestInstance')
        self.updateAutoScaler(autoScaler, [{'Key':'Stack', 'Value':'updateTest'}])
        self.removeAutoScaler(autoScaler['autoScalingGroupName'])
        self.removeLaunchConfig(launchConfig['launchConfigurationName'])
        return True

dummy = ''
# TODO: create scalingPolicy methods for awsASG class
# TODO: add CloudWatch monitoring class