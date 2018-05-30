__author__ = 'rcj1492'
__created__ = '2015.07'
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

class ec2Client(object):

    '''
        a class of methods for interacting with AWS Elastic Computing Cloud

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
            'service_name': 'ec2',
            'region_name': self.iam.region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        self.connection = boto3.client(**client_kwargs)
        self.verbose = verbose

    def check_instance_state(self, instance_id, wait=True):
        
        '''
            method for checking the state of an instance on AWS EC2
            
        :param instance_id: string with AWS id of instance
        :param wait: [optional] boolean to wait for instance while pending
        :return: string reporting state of instance
        '''

        title = '%s.check_instance_state' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'instance_id': instance_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # notify state check
        self.iam.printer('Querying AWS region %s for state of instance %s.' % (self.iam.region_name, instance_id))

    # check connection to API
        try:
            self.connection.describe_instances()
        except:
            raise AWSConnectionError(title)
                
    # check existence of instance
        try:
            response = self.connection.describe_instances(
                InstanceIds=[ instance_id ]
            )
        except:
            raise ValueError('\nInstance %s does not exist.' % instance_id)
        if not 'Reservations' in response.keys():
            raise ValueError('\nInstance %s does not exist.' % instance_id)
        elif not response['Reservations']:
            raise ValueError('\nInstance %s does not exist.' % instance_id)
        elif not 'Instances' in response['Reservations'][0].keys():
            raise ValueError('\nInstance %s does not exist.' % instance_id)
        elif not response['Reservations'][0]['Instances'][0]:
            raise ValueError('\nInstance %s does not exist.' % instance_id)
                
    # check into state of instance
        elif not 'State' in response['Reservations'][0]['Instances'][0].keys():
            from time import sleep
            from timeit import timeit as timer
            self.iam.printer('Checking into the status of instance %s ... ' % instance_id, flush=True)
            state_timeout = 0
            while not 'State' in response['Reservations'][0]['Instances'][0].keys():
                self.iam.printer('.', flush=True)
                sleep(3)
                state_timeout += 1
                response = self.connection.describe_instances(
                    InstanceIds=[ instance_id ]
                )
                if state_timeout > 3:
                    raise Exception('\nFailure to determine status of instance %s.' % instance_id)
            self.iam.printer('done.')
            
    # return None if instance has already been terminated
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if instance_state == 'shutting-down' or instance_state == 'terminated':
            self.iam.printer('Instance %s has already been terminated.' % instance_id)
            return None
            
    # wait while instance is pending
        elif instance_state == 'pending':
            self.iam.printer('Instance %s is %s.' % (instance_id, instance_state), flush=True)
            if not wait:
                return instance_state
            else:
                from time import sleep
                from timeit import timeit as timer
                delay = 3
                while instance_state == 'pending':
                    self.iam.printer('.', flush=True)
                    sleep(delay)
                    t3 = timer()
                    response = self.connection.describe_instances(
                        InstanceIds=[ instance_id ]
                    )
                    t4 = timer()
                    response_time = t4 - t3
                    if 3 - response_time > 0:
                        delay = 3 - response_time
                    else:
                        delay = 0
                    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
                self.iam.printer(' done.')

    # report outcome
        self.iam.printer('Instance %s is %s.' % (instance_id, instance_state))

        return instance_state

    def check_instance_status(self, instance_id, wait=True):

        '''
            a method to wait until AWS instance reports an OK status

        :param instance_id: string of instance id on AWS
        :param wait: [optional] boolean to wait for instance while initializing
        :return: True
        '''

        title = '%s.check_instance_status' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'instance_id': instance_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # notify status check
        self.iam.printer('Querying AWS region %s for status of instance %s.' % (self.iam.region_name, instance_id))
        
    # check state of instance
        self.iam.printer_on = False
        self.check_instance_state(instance_id)
        self.iam.printer_on = True

    # check instance status
        response = self.connection.describe_instance_status(
            InstanceIds=[ instance_id ]
        )
        if not response['InstanceStatuses']:
            from time import sleep
            from timeit import timeit as timer
            sleep(1)
            response = self.connection.describe_instance_status(
                InstanceIds=[ instance_id ]
            )
            self.iam.printer(response)
        instance_status = response['InstanceStatuses'][0]['InstanceStatus']['Status']

    # wait for instance status to be ok
        if instance_status != 'ok' and wait:
            from time import sleep
            from timeit import timeit as timer
            self.iam.printer('Waiting for initialization of instance %s to stop' % instance_id, flush=True)
            delay = 3
            status_timeout = 0
            while instance_status != 'ok':
                self.iam.printer('.', flush=True)
                sleep(delay)
                t3 = timer()
                response = self.connection.describe_instance_status(
                    InstanceIds=[ instance_id ]
                )
                t4 = timer()
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
                status_timeout += 1
                if status_timeout > 300:
                    raise Exception('\nTimeout. Failure initializing instance %s on AWS in less than 15min' % instance_id)
                instance_status = response['InstanceStatuses'][0]['InstanceStatus']['Status']
            print(' done.')
        
    # report outcome
        self.iam.printer('Instance %s is %s.' % (instance_id, instance_status))
        
        return instance_status

    def list_instances(self, tag_values=None):

        '''
            a method to retrieve the list of instances on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of strings with instance AWS ids
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
            
    # add tags to method arguments
        kw_args = {}
        tag_text = ''
        if tag_values:
            kw_args = {
                'Filters': [ { 'Name': 'tag-value', 'Values': tag_values } ]
            }
            from labpack.parsing.grammar import join_words
            plural_value = ''
            if len(tag_values) > 1:
                plural_value = 's'
            tag_text = ' with tag value%s %s' % (plural_value, join_words(tag_values))
            
    # request instance details from AWS
        self.iam.printer('Querying AWS region %s for instances%s.' % (self.iam.region_name, tag_text))
        instance_list = []
        try:
            if tag_values:
                response = self.connection.describe_instances(**kw_args)
            else:
                response = self.connection.describe_instances()
        except:
            raise AWSConnectionError(title)

    # repeat request if any instances are currently pending
        response_list = response['Reservations']
        for instance in response_list:
            instance_info = instance['Instances'][0]
            if instance_info['State']['Name'] == 'pending':
                self.check_instance_state(instance_info['InstanceId'])
                try:
                    if tag_values:
                        response = self.connection.describe_instances(**kw_args)
                    else:
                        response = self.connection.describe_instances()
                except:
                    raise AWSConnectionError(title)
                response_list = response['Reservations']

    # populate list of instances with instance details
        for instance in response_list:
            instance_info = instance['Instances'][0]
            state_name = instance_info['State']['Name']
            if state_name not in ('shutting-down', 'terminated'):
                instance_list.append(instance_info['InstanceId'])

    # report results and return details
        if instance_list:
            print_out = 'Found instance'
            if len(instance_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(instance_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No instances found.')

        return instance_list

    def read_instance(self, instance_id):

        '''
            a method to retrieving the details of a single instances on AWS EC2

        :param instance_id: string of instance id on AWS
        :return: dictionary with instance attributes

        relevant fields:
        
        'instance_id': '',
        'image_id': '',
        'instance_type': '',
        'region': '',
        'state': { 'name': '' },
        'key_name': '',
        'public_dns_name': '',
        'public_ip_address': '',
        'tags': [{'key': '', 'value': ''}]
        '''

        title = '%s.read_instance' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'instance_id': instance_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Querying AWS region %s for properties of instance %s.' % (self.iam.region_name, instance_id))

    # check instance state
        self.iam.printer_on = False
        self.check_instance_state(instance_id)
        self.iam.printer_on = True

    # discover details associated with instance id
        try:
            response = self.connection.describe_instances(InstanceIds=[ instance_id ])
        except:
            raise AWSConnectionError(title)
        instance_info = response['Reservations'][0]['Instances'][0]

    # repeat request if any instances are currently pending
        if instance_info['State']['Name'] == 'pending':
            self.check_instance_state(instance_info['InstanceId'])
            try:
                response = self.connection.describe_instances(
                    InstanceIds=[ instance_id ]
                )
            except:
                raise AWSConnectionError(title)
            instance_info = response['Reservations'][0]['Instances'][0]

    # create dictionary of instance details
        instance_details = {
            'instance_id': '',
            'image_id': '',
            'key_name': '',
            'instance_type': '',
            'region': self.iam.region_name,
            'tags': [],
            'public_ip_address': '',
            'public_dns_name': '',
            'security_groups': [],
            'subnet_id': '',
            'vpc_id': ''
        }
        instance_details = self.iam.ingest(instance_info, instance_details)

        return instance_details

    def tag_instance(self, instance_id, tag_list):

        '''
            a method for adding or updating tags on an AWS instance

        :param instance_id: string of instance id on AWS
        :param tag_list: list of single key-value pairs
        :return: dictionary with aws response info
        '''

        title = '%s.tag_instance' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'instance_id': instance_id,
            'tag_list': tag_list
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # retrieve tag list of instance
        self.iam.printer_on = False
        instance_details = self.read_instance(instance_id)
        self.iam.printer_on = True
        old_tags = instance_details['tags']
    
    # determine tags to remove
        delete_list = []
        tag_map = {}
        for tag in tag_list:
            tag_map[tag['key']] = tag['value']
        for tag in old_tags:
            if tag['key'] not in tag_map.keys():
                delete_list.append(tag)
            elif tag['value'] != tag_map[tag['key']]:
                delete_list.append(tag)

    # convert tag list to camelcase
        delete_list = self.iam.prepare(delete_list)
        tag_list = self.iam.prepare(tag_list)
    
    # remove tags from instance
        if delete_list:
            try:
                delete_kwargs = {
                    'Resources': [ instance_id ],
                    'Tags': delete_list
                }
                self.connection.delete_tags(**delete_kwargs)
            except:
                AWSConnectionError(title)
            
    # tag instance with updated tags
        try:
            create_kwargs = {
                'Resources': [ instance_id ],
                'Tags': tag_list
            }
            response = self.connection.create_tags(**create_kwargs)
        except:
            raise AWSConnectionError(title)
        
        return response

    def create_instance(self, image_id, pem_file, group_ids, instance_type, volume_type='gp2', ebs_optimized=False, instance_monitoring=False, iam_profile='', tag_list=None, auction_bid=0.0):

        '''
            a method for starting an instance on AWS EC2
            
        :param image_id: string with aws id of image for instance 
        :param pem_file: string with path to pem file to access image
        :param group_ids: list with aws id of security group(s) to attach to instance
        :param instance_type: string with type of instance resource to use
        :param volume_type: string with type of on-disk storage
        :param ebs_optimized: [optional] boolean to activate ebs optimization 
        :param instance_monitoring: [optional] boolean to active instance monitoring
        :param iam_profile: [optional] string with name of iam instance profile role
        :param tag_list: [optional] list of single key-pair tags for instance
        :param auction_bid: [optional] float with dollar amount to bid for instance hour
        :return: string with id of instance
        '''

        title = '%s.create_instance' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id,
            'pem_file': pem_file,
            'group_ids': group_ids,
            'instance_type': instance_type,
            'volume_type': volume_type,
            'iam_profile': iam_profile,
            'tag_list': tag_list,
            'auction_bid': auction_bid
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # print warning about auction
        if auction_bid:
            self.iam.printer('[WARNING]: auction bidding is not yet available.')

    # turn off verbosity
        self.iam.printer_on = False
        
    # verify existence of image
        try:
            self.read_image(image_id)
        except:
            raise ValueError('Image %s does not exist in EC2 account or permission scope.')
        
    # verify existence of security group
        group_list = self.list_security_groups()
        for id in group_ids:
            if id not in group_list:
                raise ValueError('Security group %s does not exist in EC2 account.' % id)
        
    # verify existence of iam profile
        if iam_profile:    
            if not iam_profile in self.iam.list_roles():
                raise ValueError('Iam instance profile %s does not exist in IAM account.' % iam_profile)

    # validate path to pem file
        from os import path
        if not path.exists(pem_file):
            raise ValueError('%s is not a valid path on localhost.' % pem_file)
    
    # verify existence of pem name
        pem_absolute = path.abspath(pem_file)
        pem_root, pem_ext = path.splitext(pem_absolute)
        pem_path, pem_name = path.split(pem_root)
        if not pem_name in self.list_keypairs():
            raise ValueError('Pem file name %s does not exist in EC2 account.' % pem_name)
    
    # turn on verbosity
        self.iam.printer_on = True
    
    # create client token and timestamp for instance
        from labpack.records.id import labID
        record_id = labID()
        client_token = 'CT-%s' % record_id.id36
        from labpack.records.time import labDT
        timestamp = labDT.new().zulu()
    
    # construct tag list
        if not tag_list:
            tag_list = []
        for tag in tag_list:
            if tag['key'] == 'BuildDate':
                tag['value'] = timestamp

    # create keyword argument definitions
        kw_args = {
            'DryRun': False,
            'ImageId': image_id,
            'MinCount': 1,
            'MaxCount': 1,
            'KeyName': pem_name,
            'SecurityGroupIds': group_ids,
            'InstanceType': instance_type,
            'ClientToken': client_token,
            'Monitoring': { 'Enabled': instance_monitoring },
            'EbsOptimized': ebs_optimized,
            'BlockDeviceMappings': []
        }
        kw_args['BlockDeviceMappings'].append(
            { "DeviceName": "/dev/xvda", "Ebs": { "VolumeType": volume_type } }
        )
        if iam_profile:
            kw_args['IamInstanceProfile'] = { 'Name': iam_profile }

    # start instance on aws
        self.iam.printer('Initiating instance of image %s.' % image_id)
        try:
            response = self.connection.run_instances(**kw_args)
        except Exception as err:
            if str(err).find('non-VPC'):
                self.iam.printer('Default VPC Error Detected!\nAttempting to add Subnet declaration.')
                group_details = self.read_security_group(group_ids[0])
                env_type = ''
                for tag in group_details['tags']:
                    if tag['Key'] == 'Env':
                        env_type = tag['Value']
                if env_type:
                    subnet_list = self.list_subnets(tag_values=[env_type])
                else:
                    subnet_list = self.list_subnets()
                error_msg = '%s requires a Subnet match the Security Group %s' % (title, group_ids[0])
                if not subnet_list:
                    raise AWSConnectionError(error_msg)
                subnet_id = ''
                for subnet in subnet_list:
                    subnet_details = self.read_subnet(subnet)
                    if subnet_details['vpc_id'] == group_details['vpc_id']:
                        subnet_id = subnet
                if not subnet_id:
                    raise AWSConnectionError(error_msg)
                kw_args['SubnetId'] = subnet_id
                try:
                    response = self.connection.run_instances(**kw_args)
                except:
                    raise AWSConnectionError('%s(%s)' % (title, kw_args))
            else:
                raise AWSConnectionError('%s(%s)' % (title, kw_args))

    # parse instance id from response
        instance_id = ''
        instance_list = response['Instances']
        for i in range(0, len(instance_list)):
            if instance_list[i]['ClientToken'] == client_token:
                instance_id = instance_list[i]['InstanceId']
        if instance_id:
            self.iam.printer('Instance %s has been initiated.' % instance_id)
        else:
            raise Exception('Failure creating instance from image %s.' % image_id)

    # tag instance with instance tags
        self.tag_instance(instance_id, tag_list)

        return instance_id

    def delete_instance(self, instance_id):

        '''
            method for removing an instance from AWS EC2

        :param instance_id: string of instance id on AWS
        :return: string reporting state of instance
        '''

        title = '%s.delete_instance' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'instance_id': instance_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Removing instance %s from AWS region %s.' % (instance_id, self.iam.region_name))

    # retrieve state
        old_state = self.check_instance_state(instance_id)

    # discover tags associated with instance id
        tag_list = []
        try:
            response = self.connection.describe_tags(
                Filters=[ { 'Name': 'resource-id', 'Values': [ instance_id ] } ]
            )
            import re
            aws_tag_pattern = re.compile('aws:')
            for i in range(0, len(response['Tags'])):
                if not aws_tag_pattern.findall(response['Tags'][i]['Key']):
                    tag = {}
                    tag['Key'] = response['Tags'][i]['Key']
                    tag['Value'] = response['Tags'][i]['Value']
                    tag_list.append(tag)
        except:
            raise AWSConnectionError(title)

    # remove tags from instance
        try:
            self.connection.delete_tags(
                Resources=[ instance_id ],
                Tags=tag_list
            )
            self.iam.printer('Tags have been deleted from %s.' % instance_id)
        except:
            raise AWSConnectionError(title)

    # stop instance
        try:
            self.connection.stop_instances(
                InstanceIds=[ instance_id ]
            )
        except:
            raise AWSConnectionError(title)

    # terminate instance
        try:
            response = self.connection.terminate_instances(
                InstanceIds=[ instance_id ]
            )
            new_state = response['TerminatingInstances'][0]['CurrentState']['Name']
        except:
            raise AWSConnectionError(title)

    # report outcome and return true
        self.iam.printer('Instance %s was %s.' % (instance_id, old_state))
        self.iam.printer('Instance %s is %s.' % (instance_id, new_state))
        return new_state

    def list_addresses(self, tag_values=None):
        
        '''
            a method to list elastic ip addresses associated with account on AWS
            
        :param tag_values: [optional] list of tag values
        :return: list of strings with ip addresses
        '''
        
        title = '%s.list_addresses' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'tag_values': tag_values
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
            
    # add tags to method arguments
        kw_args = {}
        tag_text = ''
        if tag_values:
            kw_args = {
                'Filters': [ { 'Name': 'tag-value', 'Values': tag_values } ]
            }
            from labpack.parsing.grammar import join_words
            plural_value = ''
            if len(tag_values) > 1:
                plural_value = 's'
            tag_text = ' with tag value%s %s' % (plural_value, join_words(tag_values))
    
    # report query
        self.iam.printer('Querying AWS region %s for elastic ip addresses%s.' % (self.iam.region_name, tag_text))
        address_list = []
        
    # discover details associated with instance id
        try:
            response = self.connection.describe_addresses(**kw_args)
        except:
            raise AWSConnectionError(title)

    # populate address list with response
        response_list = response['Addresses']
        for address in response_list:
            address_list.append(address['PublicIp'])

        return address_list
    
    def read_address(self, ip_address):
        
        '''
            a method to retrieve details about an elastic ip address associated with account on AWS
            
        :param ip_address: string with elastic ipv4 address on ec2 
        :return: dictionary with ip address details
        '''
        
        title = '%s.read_address' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'ip_address': ip_address
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # report query
        self.iam.printer('Querying AWS region %s for properties of elastic ip %s.' % (self.iam.region_name, ip_address))
        
    # discover details associated with instance id
        try:
            response = self.connection.describe_addresses(PublicIps=[ ip_address ])
            address_info = response['Addresses'][0]
        except:
            raise AWSConnectionError(title)

    # create dictionary of instance details
        address_details = {
            'instance_id': '',
            'public_ip': '',
            'allocation_id': '',
            'association_id': '',
            'domain': '',
            'network_interface_id': '',
            'network_interface_owner_id': '',
            'private_ip_address': '',
            'tags': [],
            'region': self.iam.region_name
        }
        address_details = self.iam.ingest(address_info, address_details)

        return address_details

    def assign_address(self, ip_address, instance_id):
        
        '''
            a method to assign (or reassign) an elastic ip to an instance on AWS
            
        :param ip_address: string with elastic ipv4 address on ec2  
        :param instance_id: string with aws id for running instance
        :return: dictioanry with response metadata fields
        '''
        
        title = '%s.assign_address' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'ip_address': ip_address,
            'instance_id': instance_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Assigning elastic ip address %s to instance %s.' % (ip_address, instance_id))

    # discover details associated with instance id
        try:
            response = self.connection.associate_address(
                InstanceId=instance_id,
                PublicIp=ip_address
            )
        except:
            raise AWSConnectionError(title)

        return response

    def check_image_state(self, image_id, wait=True):

        '''
            method for checking the state of an image on AWS EC2

        :param image_id: string with AWS id of image
        :param wait: [optional] boolean to wait for image while pending
        :return: string reporting state of image
        '''

        title = '%s.check_image_state' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # notify state check
        self.iam.printer('Querying AWS region %s for state of image %s.' % (self.iam.region_name, image_id))
        
    # check connection to API
        try:
            self.connection.describe_instances()
        except:
            raise AWSConnectionError(title)

    # check existence of image
        try:
            response = self.connection.describe_images(ImageIds=[ image_id ])
        except:
            raise ValueError('\nImage %s does not exist in your permission scope.' % image_id)
        if not 'Images' in response.keys():
            raise ValueError('\nImage %s does not exist in your permission scope.' % image_id)
        elif not response['Images'][0]:
            raise ValueError('\nImage %s does not exist in your permission scope.' % image_id)

    # check into state of image
        elif not 'State' in response['Images'][0].keys():
            from time import sleep
            from timeit import timeit as timer
            self.iam.printer('Checking into the status of image %s' % image_id, flush=True)
            state_timeout = 0
            while not 'State' in response['Images'][0].keys():
                self.iam.printer('.', flush=True)
                sleep(3)
                state_timeout += 1
                response = self.connection.describe_images(
                    ImageIds=[ image_id ]
                )
                if state_timeout > 3:
                    raise Exception('\nFailure to determine status of image %s.' % image_id)
            self.iam.printer(' done.')
        image_state = response['Images'][0]['State']

    # return None if image has already been deregistered or is invalid
        if image_state == 'deregistered':
            self.iam.printer('Image %s has already been deregistered.' % image_id)
            return None
        elif image_state == 'invalid' or image_state == 'transient' or image_state == 'failed':
            self.iam.printer('Image %s is %s.' % (image_id, image_state))
            return None

    # wait while image is pending
        elif image_state == 'pending':
            self.iam.printer('Image %s is %s.' % (image_id, image_state), flush=True)
            if not wait:
                return image_state
            else:
                from time import sleep
                from timeit import timeit as timer
                delay = 3
                state_timeout = 0
                while image_state != 'available':
                    self.iam.printer('.', flush=True)
                    sleep(delay)
                    t3 = timer()
                    response = self.connection.describe_images(
                        ImageIds=[ image_id ]
                    )
                    t4 = timer()
                    state_timeout += 1
                    response_time = t4 - t3
                    if 3 - response_time > 0:
                        delay = 3 - response_time
                    else:
                        delay = 0
                    if state_timeout > 300:
                        raise Exception('\nTimeout. Failure initializing image %s on AWS in less than 15min' % image_id)
                    image_state = response['Images'][0]['State']
                self.iam.printer(' done.')

    # report outcome
        self.iam.printer('Image %s is %s.' % (image_id, image_state))
        
        return image_state

    def list_images(self, tag_values=None):

        '''
            a method to retrieve the list of images of account on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of image AWS ids
        '''

        title = '%s.list_images' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'tag_values': tag_values
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
            
    # add tags to method arguments
        kw_args = { 'Owners': [ self.iam.owner_id ] }
        tag_text = ''
        if tag_values:
            kw_args = {
                'Filters': [ { 'Name': 'tag-value', 'Values': tag_values } ]
            }
            from labpack.parsing.grammar import join_words
            plural_value = ''
            if len(tag_values) > 1:
                plural_value = 's'
            tag_text = ' with tag value%s %s' % (plural_value, join_words(tag_values))
            
    # request image details from AWS
        self.iam.printer('Querying AWS region %s for images%s.' % (self.iam.region_name, tag_text))
        image_list = []
        try:
            response = self.connection.describe_images(**kw_args)
        except:
            raise AWSConnectionError(title)
        response_list = response['Images']

    # repeat request
        if not response_list:
            from time import sleep
            from timeit import default_timer as timer
            self.iam.printer('No images found initially. Checking again', flush=True)
            state_timeout = 0
            delay = 3
            while not response_list and state_timeout < 12:
                self.iam.printer('.', flush=True)
                sleep(delay)
                t3 = timer()
                try:
                    response = self.connection.describe_images(**kw_args)
                except:
                    raise AWSConnectionError(title)
                response_list = response['Images']
                t4 = timer()
                state_timeout += 1
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
            self.iam.printer(' done.')

    # wait until all images are no longer pending
        for image in response_list:
            image_list.append(image['ImageId'])

    # report outcome and return results
        if image_list:
            print_out = 'Found image'
            if len(image_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(image_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No images found.')

        return image_list

    def read_image(self, image_id):

        '''
            a method to retrieve the details of a single image on AWS EC2

        :param image_id: string with AWS id of image
        :return: dictionary of image attributes

        relevant fields:
        
        'image_id': '',
        'snapshot_id': '',
        'region': '',
        'state': '',
        'tags': []
        '''

        title = '%s.read_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Querying AWS region %s for properties of image %s.' % (self.iam.region_name, image_id))

    # check image state
        self.iam.printer_on = False
        self.check_image_state(image_id)
        self.iam.printer_on = True

    # discover tags and snapshot id associated with image id
        try:
            response = self.connection.describe_images(ImageIds=[ image_id ])
        except:
            raise AWSConnectionError(title)
        image_info = response['Images'][0]

    # construct image details from response
        image_details = {
            'image_id': '',
            'state': '',
            'name': '',
            'region': self.iam.region_name,
            'tags': []
        }
        image_details = self.iam.ingest(image_info, image_details)
        image_details['snapshot_id'] = image_details['block_device_mappings'][0]['ebs']['snapshot_id']
        
        return image_details

    def tag_image(self, image_id, tag_list):

        '''
            a method for adding or updating tags on an AWS instance

        :param image_id: string with AWS id of instance
        :param tag_list: list of tags to add to instance
        :return: dictionary with response data
        '''

        title = '%s.tag_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id,
            'tag_list': tag_list
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # retrieve tag list of image
        self.iam.printer_on = False
        image_details = self.read_image(image_id)
        self.iam.printer_on = True
        old_tags = image_details['tags']
    
    # determine tags to remove
        delete_list = []
        tag_map = {}
        for tag in tag_list:
            tag_map[tag['key']] = tag['value']
        for tag in old_tags:
            if tag['key'] not in tag_map.keys():
                delete_list.append(tag)
            elif tag['value'] != tag_map[tag['key']]:
                delete_list.append(tag)

    # convert tag list to camelcase
        delete_list = self.iam.prepare(delete_list)
        tag_list = self.iam.prepare(tag_list)
    
    # remove tags from instance
        if delete_list:
            try:
                delete_kwargs = {
                    'Resources': [ image_id ],
                    'Tags': delete_list
                }
                self.connection.delete_tags(**delete_kwargs)
            except:
                AWSConnectionError(title)
            
    # tag instance with updated tags
        try:
            create_kwargs = {
                'Resources': [ image_id ],
                'Tags': tag_list
            }
            response = self.connection.create_tags(**create_kwargs)
        except:
            raise AWSConnectionError(title)

        return response

    def create_image(self, instance_id, image_name, tag_list=None):

        '''
            method for imaging an instance on AWS EC2

        :param instance_id: string with AWS id of running instance
        :param image_name: string with name to give new image
        :param tag_list: [optional] list of resources tags to add to image
        :return: string with AWS id of image
        '''

        title = '%s.create_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'instance_id': instance_id,
            'image_name': image_name,
            'tag_list': tag_list
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # check instance state
        self.iam.printer('Initiating image of instance %s.' % instance_id)
        instance_state = self.check_instance_state(instance_id)

    # stop instance
        if instance_state == 'running':
            self.iam.printer('Instance %s is %s.\nStopping instance %s to image it.' % (instance_id, instance_state, instance_id))
            try:
                response = self.connection.stop_instances(
                    InstanceIds=[ instance_id ]
                )
                instance_state = response['StoppingInstances'][0]['CurrentState']['Name']
            except:
                raise AWSConnectionError(title)
        if instance_state == 'stopping':
            from time import sleep
            from timeit import timeit as timer
            self.iam.printer('Instance %s is %s' % (instance_id, instance_state), flush=True)
            delay = 3
            while instance_state == 'stopping':
                self.iam.printer('.', flush=True)
                sleep(delay)
                t3 = timer()
                try:
                    response = self.connection.describe_instances(
                        InstanceIds=[ instance_id ]
                    )
                except:
                    raise AWSConnectionError(title)
                t4 = timer()
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
                instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
            self.iam.printer(' done.')
        if instance_state != 'stopped':
            raise Exception('Instance %s is currently in a state that cannot be imaged.' % instance_id)

    # discover tags associated with instance
        old_tags = []
        try:
            response = self.connection.describe_instances(
                    InstanceIds=[ instance_id ]
                )
            instance_tags = response['Reservations'][0]['Instances'][0]['Tags']
            import re
            aws_tag_pattern = re.compile('aws:')
            for i in range(0, len(instance_tags)):
                if not aws_tag_pattern.findall(instance_tags[i]['Key']):
                    tag = {}
                    tag['Key'] = instance_tags[i]['Key']
                    tag['Value'] = instance_tags[i]['Value']
                    old_tags.append(tag)
        except:
            raise AWSConnectionError(title)

    # replace tag list if new tag input
        new_tags = True
        if not tag_list:
            tag_list = self.iam.ingest(old_tags)
            new_tags = False

    # create image of the instance
        try:
            response = self.connection.create_image(
                InstanceId=instance_id,
                Name=image_name
            )
            image_id = response['ImageId']
            self.iam.printer('Image %s is being created.' % image_name)
        except:
            raise AWSConnectionError(title)

    # add tags to image
        self.tag_image(image_id, tag_list)
        if new_tags:
            self.iam.printer('Tags from input have been added to image %s.' % image_id)
        else:
            self.iam.printer('Instance %s tags have been added to image %s.' % (instance_id, image_id))

    # restart instance
        try:
            self.connection.start_instances(
                    InstanceIds=[ instance_id ]
            )
            self.iam.printer('Restarting instance %s now.' % instance_id)
        except:
            raise AWSConnectionError

        return image_id

    def delete_image(self, image_id):

        '''
            method for removing an image from AWS EC2

        :param image_id: string with AWS id of instance
        :return: string with AWS response from snapshot delete
        '''

        title = '%s.delete_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Removing image %s from AWS region %s.' % (image_id, self.iam.region_name))

    # retrieve state
        old_state = self.check_image_state(image_id)

    # discover snapshot id and tags associated with instance id
        image_details = self.read_image(image_id)
        tag_list = image_details['tags']
        snapshot_id = image_details['snapshot_id']

    # remove tags from instance
        try:
            delete_kwargs = {
                'Resources': [ image_id ],
                'Tags': self.iam.prepare(tag_list)
            }
            self.connection.delete_tags(**delete_kwargs)
            self.iam.printer('Tags have been deleted from %s.' % image_id)
        except:
            raise AWSConnectionError(title)

    # deregister image
        try:
            self.connection.deregister_image(
                ImageId=image_id
            )
        except:
            raise AWSConnectionError(title)
        self.iam.printer('Image %s has been deregistered.' % image_id)

    # delete snapshot
        try:
            response = self.connection.delete_snapshot(
                SnapshotId=snapshot_id
            )
        except:
            raise AWSConnectionError(title)
        self.iam.printer('Snapshot %s associated with image %s has been deleted.' % (snapshot_id, image_id))

        return response

    def import_image(self, image_id, region_name):

        '''
            a method to import an image from another AWS region

            https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html

            REQUIRED: aws credentials must have valid access to both regions

        :param image_id: string with AWS id of source image
        :param region_name: string with AWS region of source image
        :return: string with AWS id of new image
        '''

        title = '%s.import_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        input_fields = {
            'region_name': region_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.iam.fields.validate(value, '.%s' % key, object_title)
        if region_name == self.iam.region_name:
            raise ValueError('%s cannot import an image from the same region.' % title)
    
    # construct ec2 client connection for source region
        client_kwargs = {
            'service_name': 'ec2',
            'region_name': region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        source_connection = boto3.client(**client_kwargs)

    # check existence of image
        try:
            response = source_connection.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise ValueError('Image %s does not exist in AWS region %s.' % (image_id, region_name))
        if not 'Images' in response.keys():
            raise ValueError('Image %s does not exist in AWS region %s.' % (image_id, region_name))
        elif not response['Images'][0]:
            raise ValueError('Image %s does not exist in AWS region %s.' % (image_id, region_name))

    # check into state of image
        elif not 'State' in response['Images'][0].keys():
            from time import sleep
            from timeit import default_timer as timer
            self.iam.printer('Checking into the status of image %s in AWS region %s' % (image_id, region_name), flush=True)
            state_timeout = 0
            while not 'State' in response['Images'][0].keys():
                self.iam.printer('.', flush=True)
                sleep(3)
                state_timeout += 1
                response = source_connection.describe_images(
                    ImageIds=[ image_id ]
                )
                if state_timeout > 3:
                    raise Exception('Failure to determine status of image %s.' % image_id)
            self.iam.printer(' done.')
        image_state = response['Images'][0]['State']

    # raise error if image is deregistered or otherwise invalid
        if image_state == 'deregistered' or image_state == 'invalid' or image_state == 'transient' or image_state == 'failed':
            raise Exception('Image %s in AWS region %s is %s.' % (image_id, region_name, image_state))

    # wait while image is pending
        elif image_state == 'pending':
            from time import sleep
            from timeit import default_timer as timer
            self.iam.printer('Image %s is %s' % (image_id, image_state), flush=True)
            delay = 3
            state_timeout = 0
            while image_state != 'available':
                self.iam.printer('.', flush=True)
                sleep(delay)
                t3 = timer()
                response = source_connection.describe_images(
                    ImageIds=[ image_id ]
                )
                t4 = timer()
                state_timeout += 1
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
                if state_timeout > 300:
                    raise Exception('Timeout. Failure initializing image %s in region %s in less than 15min' % (image_id, region_name))
                image_state = response['Images'][0]['State']
            self.iam.printer(' done.')

    # discover tags and name associated with source image
        try:
            response = source_connection.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise AWSConnectionError(title)
        image_info = response['Images'][0]

    # construct image details from response
        image_name = image_info['Name']
        tag_list = self.iam.ingest(image_info['Tags'])

    # copy image over to current region
        self.iam.printer('Copying image %s from region %s.' % (image_id, region_name))
        try:
            response = self.connection.copy_image(
                SourceRegion=region_name,
                SourceImageId=image_id,
                Name=image_name
            )
        except:
            raise AWSConnectionError
        new_id = response['ImageId']

    # check into state of new image
        self.check_image_state(new_id, wait=False)

    # add tags from source image to new image
        self.tag_image(new_id, tag_list)
        self.iam.printer('Tags from image %s have been added to image %s.' % (image_id, new_id))

        return new_id

    def export_image(self, image_id, region_name):

        '''
            a method to add a copy of an image to another AWS region

            https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html

            REQUIRED: iam credentials must have valid access to both regions

        :param image_id: string of AWS id of image to be copied
        :param region_name: string of AWS region to copy image to
        :return: string with AWS id of new image
        '''

        title = '%s.export_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        input_fields = {
            'region_name': region_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.iam.fields.validate(value, '.%s' % key, object_title)
        if region_name == self.iam.region_name:
            raise ValueError('%s cannot export an image to the same region.' % title)
        
    # construct ec2 client connection for source region
        client_kwargs = {
            'service_name': 'ec2',
            'region_name': region_name,
            'aws_access_key_id': self.iam.access_id,
            'aws_secret_access_key': self.iam.secret_key
        }
        destination_connection = boto3.client(**client_kwargs)

    # check state of image to be copied
        self.check_image_state(image_id)

    # discover tags and name associated with image to be copied
        image_details = self.read_image(image_id)
        tag_list = image_details['tags']
        image_name = image_details['name']

    # copy image over to current region
        self.iam.printer('Copying image %s to region %s.' % (image_id, region_name))
        try:
            response = destination_connection.copy_image(
                SourceRegion=self.iam.region_name,
                SourceImageId=image_id,
                Name=image_name
            )
        except:
            raise AWSConnectionError(title)
        new_id = response['ImageId']

    # check into state of new image
        try:
            response = destination_connection.describe_images(
                ImageIds=[ new_id ]
            )
        except:
            raise AWSConnectionError(title)
        if not 'State' in response['Images'][0].keys():
            from time import sleep
            from timeit import default_timer as timer
            self.iam.printer('Checking into the status of image %s in AWS region %s' % (new_id, region_name), flush=True)
            state_timeout = 0
            while not 'State' in response['Images'][0].keys():
                self.iam.printer('.', flush=True)
                sleep(3)
                state_timeout += 1
                try:
                    response = destination_connection.describe_images(
                        ImageIds=[ new_id ]
                    )
                except:
                    raise AWSConnectionError(title)
                if state_timeout > 3:
                    raise Exception('Failure to determine status of image %s in AWS region %s.' % (new_id, region_name))
            self.iam.printer(' done.')
        image_state = response['Images'][0]['State']

    # wait while image is pending
        if image_state == 'pending':
            from time import sleep
            from timeit import default_timer as timer
            self.iam.printer('Image %s in AWS region %s is %s' % (new_id, region_name, image_state), flush=True)
            delay = 3
            state_timeout = 0
            while image_state != 'available':
                self.iam.printer('.', flush=True)
                sleep(delay)
                t3 = timer()
                try:
                    response = destination_connection.describe_images(
                        ImageIds=[ new_id ]
                    )
                except:
                    raise AWSConnectionError(title)
                t4 = timer()
                state_timeout += 1
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
                if state_timeout > 300:
                    raise Exception('Timeout. Failure initializing image %s in region %s in less than 15min' % (new_id, region_name))
                image_state = response['Images'][0]['State']
            self.iam.printer(' done.')

    # add tags from image to image copy
        try:
            destination_connection.create_tags(
                Resources=[ new_id ],
                Tags=tag_list
            )
        except:
            raise AWSConnectionError(title)
        self.iam.printer('Tags from image %s have been added to image %s.' % (image_id, new_id))

        return new_id

    def list_keypairs(self):

        '''
            a method to discover the list of key pairs on AWS

        :return: list of key pairs
        '''

        title = '%s.list_keypairs' % self.__class__.__name__

    # request subnet list from AWS
        self.iam.printer('Querying AWS region %s for key pairs.' % self.iam.region_name)
        keypair_list = []
        try:
            response = self.connection.describe_key_pairs()
        except:
            raise AWSConnectionError(title)
        response_list = []
        if 'KeyPairs' in response:
            response_list = response['KeyPairs']

    # construct list of keypairs from response
        for sub_dict in response_list:
            keypair_list.append(sub_dict['KeyName'])

    # report results and return list
        if keypair_list:
            print_out = 'Found key pair'
            if len(keypair_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(keypair_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No key pairs found.')

        return keypair_list

    def list_subnets(self, tag_values=None):

        '''
            a method to discover the list of subnets on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of strings with subnet ids
        '''

        title = '%s.list_subnets' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'tag_values': tag_values
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
            
    # add tags to method arguments
        kw_args = {}
        tag_text = ''
        if tag_values:
            kw_args = {
                'Filters': [ { 'Name': 'tag-value', 'Values': tag_values } ]
            }
            from labpack.parsing.grammar import join_words
            plural_value = ''
            if len(tag_values) > 1:
                plural_value = 's'
            tag_text = ' with tag value%s %s' % (plural_value, join_words(tag_values))
            
    # request instance details from AWS
        self.iam.printer('Querying AWS region %s for subnets%s.' % (self.iam.region_name, tag_text))
        subnet_list = []
        try:
            if kw_args:
                response = self.connection.describe_subnets(**kw_args)
            else:
                response = self.connection.describe_subnets()
        except:
            raise AWSConnectionError(title)
        response_list = []
        if 'Subnets' in response:
            response_list = response['Subnets']

    # construct list of subnets from response
        for sub_dict in response_list:
            subnet_list.append(sub_dict['SubnetId'])

    # report results and return list
        if subnet_list:
            print_out = 'Found subnet'
            if len(subnet_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(subnet_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No subnets found.')

        return subnet_list

    def read_subnet(self, subnet_id):

        '''
            a method to retrieve the details about a subnet

        :param subnet_id: string with AWS id of subnet
        :return: dictionary with subnet details

        relevant fields:
        
        'subnet_id': '',
        'vpc_id': '',
        'availability_zone': '',
        'state': '',
        'tags': [{'key': '', 'value': ''}]
        '''

        title = '%s.read_subnet' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'subnet_id': subnet_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Querying AWS region %s for properties of subnet %s.' % (self.iam.region_name, subnet_id))
        
    # construct keyword definitions
        kw_args = { 'SubnetIds': [ subnet_id ] }

    # send request for details about subnet
        try:
            response = self.connection.describe_subnets(**kw_args)
        except:
            raise AWSConnectionError(title)

    # construct subnet details from response
        subnet_dict = response['Subnets'][0]
        subnet_details = {
            'subnet_id': '',
            'vpc_id': '',
            'availability_zone': '',
            'state': '',
            'tags': []
        }
        subnet_details = self.iam.ingest(subnet_dict, subnet_details)

        return subnet_details

    def list_security_groups(self, tag_values=None):

        '''
            a method to discover the list of security groups on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of strings with security group ids
        '''

        title = '%s.list_security_groups' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'tag_values': tag_values
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
            
    # add tags to method arguments
        kw_args = {}
        tag_text = ''
        if tag_values:
            kw_args = {
                'Filters': [ { 'Name': 'tag-value', 'Values': tag_values } ]
            }
            from labpack.parsing.grammar import join_words
            plural_value = ''
            if len(tag_values) > 1:
                plural_value = 's'
            tag_text = ' with tag value%s %s' % (plural_value, join_words(tag_values))
            
    # request instance details from AWS
        self.iam.printer('Querying AWS region %s for security groups%s.' % (self.iam.region_name, tag_text))
        group_list = []
        try:
            if kw_args:
                response = self.connection.describe_security_groups(**kw_args)
            else:
                response = self.connection.describe_security_groups()
        except:
            raise AWSConnectionError(title)
        response_list = []
        if 'SecurityGroups' in response:
            response_list = response['SecurityGroups']

    # construct list of subnets from response
        for sub_dict in response_list:
            group_list.append(sub_dict['GroupId'])

    # report results and return list
        if group_list:
            print_out = 'Found security group'
            if len(group_list) > 1:
                print_out += 's'
            from labpack.parsing.grammar import join_words
            print_out += ' %s.' % join_words(group_list)
            self.iam.printer(print_out)
        else:
            self.iam.printer('No security groups found.')

        return group_list
    
    def read_security_group(self, group_id):

        '''
            a method to retrieve the details about a security group

        :param group_id: string with AWS id of security group
        :return: dictionary with security group details

        relevant fields:
        
        'group_id: '',
        'vpc_id': '',
        'group_name': '',
        'tags': [{'key': '', 'value': ''}]
        'ip_permissions': [{
            'from_port': 0, 
            'ip_ranges':[{'cidr_ip':'0.0.0.0/0'}]
        }]
        '''

        title = '%s.read_security_group' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_id': group_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # report query
        self.iam.printer('Querying AWS region %s for properties of security group %s.' % (self.iam.region_name, group_id))

    # construct keyword definitions
        kw_args = { 'GroupIds': [ group_id ] }

    # send request for details about security group
        try:
            response = self.connection.describe_security_groups(**kw_args)
        except:
            raise AWSConnectionError(title)

    # construct security group details from response
        group_info = response['SecurityGroups'][0]
        group_details = {
            'group_id': '',
            'vpc_id': '',
            'group_name': '',
            'tags': [],
            'ip_permissions': []
        }
        group_details = self.iam.ingest(group_info, group_details)
        
        return group_details

    def cleanup(self):

        '''
            a method for removing instances and images in unusual states

        :return: True
        '''

    # find non-running instances
        self.iam.printer('Cleaning up AWS region %s.' % self.iam.region_name)
        response = self.connection.describe_instances()
        instance_list = response['Reservations']
        for instance in instance_list:
            instance_info = instance['Instances'][0]
            if instance_info['State']['Name'] == 'pending':
                self.check_instance_state(instance_info['InstanceId'])
                response = self.connection.describe_instances(
                    InstanceIds=[ instance_info['InstanceId'] ]
                )
                instance_info = response['Reservations'][0]['Instances'][0]
            if instance_info['State']['Name'] != 'running':

    # try to remove tags associated with non-running instance
                try:
                    response = self.connection.describe_tags(
                        Filters=[ { 'Name': 'resource-id', 'Values': [ instance_info['InstanceId'] ] } ]
                    )
                    tag_list = []
                    import re
                    aws_tag_pattern = re.compile('aws:')
                    for i in range(0, len(response['Tags'])):
                        if not aws_tag_pattern.findall(response['Tags'][i]['Key']):
                            tag = {}
                            tag['Key'] = response['Tags'][i]['Key']
                            tag['Value'] = response['Tags'][i]['Value']
                            tag_list.append(tag)
                    self.connection.delete_tags(
                        Resources=[ instance_info['InstanceId'] ],
                        Tags=tag_list
                    )
                    self.iam.printer('Tags have been deleted from instance %s.' % instance_info['InstanceId'])
                except:
                    pass

    # try stopping non-running instance
                try:
                    self.connection.stop_instances(
                        InstanceIds=[ instance_info['InstanceId'] ]
                    )
                    self.iam.printer('Instance %s is stopping.' % instance_info['InstanceId'])
                except:
                    pass

    # try terminating non-running instance
                try:
                    self.connection.terminate_instances(
                        InstanceIds=[ instance_info['InstanceId'] ]
                    )
                    self.iam.printer('Instance %s is terminating.' % instance_info['InstanceId'])
                except:
                    pass

    # find non-available images
        response = self.connection.describe_images(
            Owners=[ self.iam.owner_id ]
        )
        image_list = response['Images']
        for image in image_list:
            image_info = image.copy()
            if image_info['State'] == 'pending':
                self.check_image_state(image_info['ImageId'])
                response = self.connection.describe_images(
                    ImageIds=[ image_info['ImageId'] ]
                )
                image_info = response['Images'][0]
            if image_info['State'] != 'available':

    # try removing tags from non-available images
                try:
                    response = self.connection.describe_images(
                        ImageIds=[ image_info['ImageId'] ]
                    )
                    image_tags = response['Images'][0]['Tags']
                    tag_list = []
                    for i in range(0, len(image_tags)):
                        tag = {}
                        tag['Key'] = image_tags[i]['Key']
                        tag['Value'] = image_tags[i]['Value']
                        tag_list.append(tag)
                    self.connection.delete_tags(
                        Resources=[ image_info['ImageId'] ],
                        Tags=tag_list
                    )
                    self.iam.printer('Tags have been deleted from image %s.' % image_info['ImageId'])
                except:
                    pass

    # try deregistering non-available image
                try:
                    self.connection.deregister_image(
                        ImageId=image_info['ImageId']
                    )
                    self.iam.printer('Image %s has been deregistered.' % image_info['ImageId'])
                except:
                    pass

    # try deleting snapshot associated with non-available image
                try:
                    self.connection.delete_snapshot(
                        SnapshotId=image_info['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
                    )
                    snap_id = image_info['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
                    image_id = image_info['ImageId']
                    self.iam.printer('Snapshot %s associated with image %s has been deleted.' % (snap_id, image_id))
                except:
                    pass

    # find snapshots with errors
        response = self.connection.describe_snapshots(
            OwnerIds=[ self.iam.owner_id ]
        )
        snapshot_list = response['Snapshots']
        for snapshot in snapshot_list:
            snapshot_info = snapshot.copy()
            if snapshot_info['State'] == 'error':

    # try deleting snapshot with errors
                try:
                    self.connection.delete_snapshot(
                        SnapshotId=snapshot_info['SnapshotId']
                    )
                    self.iam.printer('Snapshot %s has been deleted.' % snapshot_info['SnapshotId'])
                except:
                    pass

        return True

if __name__ == '__main__':

# test instantiation
    from labpack.records.settings import load_settings
    aws_cred = load_settings('../../../../cred/awsLab.yaml')
    client_kwargs = {
        'access_id': aws_cred['aws_access_key_id'],
        'secret_key': aws_cred['aws_secret_access_key'],
        'region_name': aws_cred['aws_default_region'],
        'owner_id': aws_cred['aws_owner_id'],
        'user_name': aws_cred['aws_user_name']
    }
    ec2_client = ec2Client(**client_kwargs)

# test list keypairs
    keypair_list = ec2_client.list_keypairs()

# test list instances
    ec2_client.list_instances()
    instance_list = ec2_client.list_instances(tag_values=['test'])

# determine instance id
    if not instance_list:
        print('There are no test instances running for unittesting.')
        import sys
        sys.exit()
    instance_id = instance_list[0]

# test instance state and status
    instance_state = ec2_client.check_instance_state(instance_id)
    instance_status = ec2_client.check_instance_status(instance_id)

# test read instance
    instance_details = ec2_client.read_instance(instance_id)
    assert instance_details['instance_id'] == instance_id
    group_id = instance_details['security_groups'][0]['group_id']
    subnet_id = instance_details['subnet_id']

# test security group
    group_list = ec2_client.list_security_groups()
    assert group_id in group_list
    group_details = ec2_client.read_security_group(group_id)
    assert group_details['group_id'] == group_id
    
# test subnet
    subnet_list = ec2_client.list_subnets(tag_values=['test'])
    assert subnet_id in subnet_list
    subnet_details = ec2_client.read_subnet(subnet_id)
    assert subnet_details['subnet_id'] == subnet_id

# test tag instances
    tag_list = instance_details['tags']
    tag_found = False
    for tag in tag_list:
        if tag['key'] == 'TestTag':
            if tag['value'] == 'testing-%s' % instance_id:
                tag_found = True
                break
    assert not tag_found
    new_tags = []
    new_tags.extend(tag_list)
    new_tags.append({ 'key':'TestTag', 'value':'testing-%s' % instance_id })
    ec2_client.tag_instance(instance_id, new_tags)
    new_details = ec2_client.read_instance(instance_id)
    tag_found = False
    for tag in new_details['tags']:
        if tag['key'] == 'TestTag':
            if tag['value'] == 'testing-%s' % instance_id:
                tag_found = True
                break
    assert tag_found
    ec2_client.tag_instance(instance_id, tag_list)
    instance_details = ec2_client.read_instance(instance_id)
    assert len(tag_list) == len(instance_details['tags'])

# test list images
    # image_list = ec2_client.list_images()

# test check image & read image
    image_id = instance_details['image_id']
    image_state = ec2_client.check_image_state(image_id)
    image_details = ec2_client.read_image(image_id)
    assert image_details['image_id'] == image_id
    
# construct instance kwargs
    from os import listdir, path
    pem_file = ''
    key_path = '../../../keys'
    key_folder = listdir(key_path)
    for key_name in keypair_list:
        if key_name.find('test') > 1:
            pem_name = '%s.pem' % key_name
            if pem_name in key_folder:
                pem_file = path.join(key_path, pem_name)
                break        
    from time import time
    instance_kwargs = {
        'image_id': 'ami-62745007',
        'pem_file': pem_file,
        'group_ids': [group_id],
        'instance_type': 't2.micro',
        'tag_list': [
            { 'key': 'Name', 'value': 'lab-unittest-%s' % str(time()) },
            { 'key': 'Env', 'value': 'dev' },
            { 'key': 'BuildDate', 'value': 'to-be-generated' },
            { 'key': 'UserName', 'value': 'ec2-user'}
        ]
    }

# test create instance and remove instance
    instance_id = ec2_client.create_instance(**instance_kwargs)
    ec2_client.check_instance_status(instance_id)
    instance_state = ec2_client.delete_instance(instance_id)

    from pprint import pprint
    # pprint(image_details)
    # pprint(instance_details['tags'])
    

