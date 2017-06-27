__author__ = 'rcj1492'
__created__ = '2015'

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
import time
import re
from copy import deepcopy
from timeit import default_timer as timer

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
    
    # construct ingestion
        from labpack.parsing.conversion import camelcase_to_lowercase, lowercase_to_camelcase
        self.ingest = camelcase_to_lowercase
        self.prepare = lowercase_to_camelcase

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
            self.iam.printer('Checking into the status of instance %s ... ' % instance_id, flush=True)
            state_timeout = 0
            while not 'State' in response['Reservations'][0]['Instances'][0].keys():
                self.iam.printer('.', flush=True)
                time.sleep(3)
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
                delay = 3
                while instance_state == 'pending':
                    self.iam.printer('.', flush=True)
                    time.sleep(delay)
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
            time.sleep(1)
            response = self.connection.describe_instance_status(
                InstanceIds=[ instance_id ]
            )
            self.iam.printer(response)
        instance_status = response['InstanceStatuses'][0]['InstanceStatus']['Status']

    # wait for instance status to be ok
        if instance_status != 'ok' and wait:
            self.iam.printer('Waiting for initialization of instance %s to stop' % instance_id, flush=True)
            delay = 3
            status_timeout = 0
            while instance_status != 'ok':
                self.iam.printer('.', flush=True)
                time.sleep(delay)
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

    def checkImageState(self, image_id):

        '''
            method for checking the state of an image on AWS EC2

        :param image_id: string with AWS id of image
        :return: string reporting state of image
        '''

        title = 'checkImageState'

    # validate input
        self.input.imageID(image_id)

    # check connection to API
        try:
            response = self.connection.describe_instances()
        except:
            raise EC2ConnectionError('checkImageState describe_instances()')

    # check existence of image
        try:
            response = self.connection.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise ValueError('\nImage %s does not exist.' % image_id)
        if not 'Images' in response.keys():
            raise ValueError('\nImage %s does not exist.' % image_id)
        elif not response['Images'][0]:
            raise ValueError('\nImage %s does not exist.' % image_id)

    # check into state of image
        elif not 'State' in response['Images'][0].keys():
            print('Checking into the status of image %s' % image_id, end='', flush=True)
            state_timeout = 0
            while not 'State' in response['Images'][0].keys():
                print('.', end='', flush=True)
                time.sleep(3)
                state_timeout += 1
                response = self.connection.describe_images(
                    ImageIds=[ image_id ]
                )
                if state_timeout > 3:
                    raise Exception('\nFailure to determine status of image %s.' % image_id)
            print(' Done.')
        image_state = response['Images'][0]['State']

    # return None if image has already been deregistered or is invalid
        if image_state == 'deregistered':
            print('Image %s has already been deregistered.' % image_id)
            return None
        elif image_state == 'invalid' or image_state == 'transient' or image_state == 'failed':
            print('Image %s is %s.' % (image_id, image_state))
            return None

    # wait while image is pending
        elif image_state == 'pending':
            print('Image %s is %s' % (image_id, image_state), end='', flush=True)
            delay = 3
            state_timeout = 0
            while image_state != 'available':
                print('.', end='', flush=True)
                time.sleep(delay)
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
            print(' Done.')

        return image_state

    def tag_instance(self, instance_id, tag_list):

        '''
            a method for adding or updating tags on an AWS instance

        :param instance_id: string of instance id on AWS
        :param tag_list: list of single key-value pairs
        :return: True
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
        delete_list = self.prepare(delete_list)
        tag_list = self.prepare(tag_list)
    
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

    def tagImage(self, image_id, image_tags):

        '''
            a method for adding or updating tags on an AWS instance

        :param instance_id: string with AWS id of instance
        :param instance_tags: list of tags to add to instance
        :return: True
        '''

        title = 'tagImage'

    # validate input
        self.input.imageID(image_id)
        self.input.tags(image_tags, title + ' tag list')

    # check image state
        self.checkImageState(image_id)

    # tag instance with instance tags
        try:
            self.connection.create_tags(
                Resources=[ image_id ],
                Tags=image_tags
            )
        except:
            raise EC2ConnectionError(title + ' create_tags()')

        return True

    def startInstance(self, init_params):

        '''
            method for starting an instance on AWS EC2

        :param init_params: dictionary with initialization parameters
        :return: string with instance id
        '''

        title = 'startInstance'

    # validate input
        init_params = deepcopy(self.input.initParams(init_params, title))

    # create client token for instance
        time_stamp = self.input.timeStamp()
        client_token = 'CT-' + time_stamp

    # add current datetime to image name
        for tag in init_params['tags']:
            if tag['Key'] == 'BuildDate':
                tag['Value'] = self.input.timeStampISO()

    # create keyword argument definitions
        kw_args = {
            'DryRun': False,
            'ImageId': init_params['imageID'],
            'MinCount': 1,
            'MaxCount': 1,
            'KeyName': init_params['keyPair'],
            'SecurityGroupIds': init_params['securityGroupIDs'],
            'InstanceType': init_params['instanceType'],
            'ClientToken': client_token,
            'Monitoring': { 'Enabled': init_params['instanceMonitoring'] },
            'EbsOptimized': init_params['ebsOptimized'],
            'BlockDeviceMappings': []
        }
        kw_args['BlockDeviceMappings'].append(
            { "DeviceName": "/dev/xvda", "Ebs": { "VolumeType": init_params['volumeType'] } }
        )
        if init_params['iamProfileRole']:
            kw_args['IamInstanceProfile'] = { 'Name': init_params['iamProfileRole'] }

    # start instance on aws
        print('Initiating instance of image %s.' % init_params['imageID'])
        try:
            response = self.connection.run_instances(**kw_args)
        except Exception as err:
            if str(err).find('non-VPC'):
                print('Default VPC Error Detected!\nAttempting to add Subnet declaration.')
                sg_details = self.securityGroupDetails(init_params['securityGroupIDs'][0])
                stack_type = ''
                for tag in sg_details['tags']:
                    if tag['Key'] == 'Stack':
                        stack_type = tag['Value']
                if stack_type:
                    subnet_list = self.findSubnets(tag_values=[stack_type])
                else:
                    subnet_list = self.findSubnets()
                if not subnet_list:
                    raise EC2ConnectionError('%s run_instances() requires a Subnet match the Security Group %s' % (title, init_params['securityGroupIDs'][0]))
                subnet_id = ''
                for subnet in subnet_list:
                    subnet_details = self.subnetDetails(subnet)
                    if subnet_details['vpcID'] == sg_details['vpcID']:
                        subnet_id = subnet
                if not subnet_id:
                    raise EC2ConnectionError('%s run_instances() requires a Subnet match the Security Group %s' % (title, init_params['securityGroupIDs'][0]))
                kw_args['SubnetId'] = subnet_id
                try:
                    response = self.connection.run_instances(**kw_args)
                except:
                    raise EC2ConnectionError('%s run_instances(%s)' % (title, kw_args))
            else:
                raise EC2ConnectionError('%s run_instances(%s)' % (title, kw_args))

    # parse instance id from response
        instance_id = ''
        instance_list = response['Instances']
        for i in range(0, len(instance_list)):
            if instance_list[i]['ClientToken'] == client_token:
                instance_id = instance_list[i]['InstanceId']
        if instance_id:
            print('Instance %s has been initiated.' % instance_id)
        else:
            raise Exception('\nFailure creating instance from image %s.' % init_params['ImageId'])

# tag instance with instance tags
        self.tagInstance(instance_id, init_params['tags'])

        return instance_id

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
            response = self.connection.describe_instances(
                InstanceIds=[ instance_id ]
            )
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
        instance_details = self.ingest(instance_info, instance_details)

        return instance_details

    def list_instances(self, tag_values=None):

        '''
            a method to retrieve the list of instances on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of instance AWS ids
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

    def removeInstance(self, instance_id):

        '''
            method for removing an instance from AWS EC2

        :param instance_id: string of instance id on AWS
        :return: string reporting state of instance
        '''

        title = 'removeInstance'

    # validate input
        self.input.instanceID(instance_id, title + ' instance id')

    # check instance state
        print('Removing instance %s.' % instance_id)
        old_state = self.check_instance_state(instance_id)
        new_state = deepcopy(old_state)

    # discover tags associated with instance id
        tag_list = []
        try:
            response = self.connection.describe_tags(
                Filters=[ { 'Name': 'resource-id', 'Values': [ instance_id ] } ]
            )
            aws_tag_pattern = re.compile('aws:')
            for i in range(0, len(response['Tags'])):
                if not aws_tag_pattern.findall(response['Tags'][i]['Key']):
                    tag = {}
                    tag['Key'] = response['Tags'][i]['Key']
                    tag['Value'] = response['Tags'][i]['Value']
                    tag_list.append(tag)
        except:
            raise EC2ConnectionError(title + ' describe_tags')

    # remove tags from instance
        try:
            self.connection.delete_tags(
                Resources=[ instance_id ],
                Tags=tag_list
            )
            print('Tags have been deleted from %s.' % instance_id)
        except:
            raise EC2ConnectionError(title + ' delete_tags')

    # stop instance
        try:
            self.connection.stop_instances(
                InstanceIds=[ instance_id ]
            )
        except:
            raise EC2ConnectionError(title + ' stop_instances')

    # terminate instance
        try:
            response = self.connection.terminate_instances(
                InstanceIds=[ instance_id ]
            )
            new_state = response['TerminatingInstances'][0]['CurrentState']['Name']
        except:
            raise EC2ConnectionError(title + ' terminate_instances')

    # report outcome and return true
        print('Instance %s was %s.' % (instance_id, old_state))
        print('Instance %s is %s.' % (instance_id, new_state))
        return True

    def imageInstance(self, instance_id, image_name, image_tags=None):

        '''
            method for imaging an instance on AWS EC2

        :param instance_id: string with AWS id of running instance
        :param image_name: string with name to give new image
        :param image_tags: [optional] list of image_tags to add to image
        :return: string with AWS id of image
        '''

        title = 'imageInstance'

    # validate input
        self.input.instanceID(instance_id, title + ' instance id')
        sub_title = '%s instance id %s' % (title, instance_id)
        self.input.imageName(image_name, sub_title + ' image name')
        if image_tags:
            self.input.tags(image_tags, sub_title + ' image tags')

    # check instance state
        print('Initiating image of instance %s.' % instance_id)
        instance_state = self.check_instance_state(instance_id)

    # stop instance
        if instance_state == 'running':
            print('Instance %s is %s.\nStopping instance %s to image it.' % (instance_id, instance_state, instance_id))
            try:
                response = self.connection.stop_instances(
                    InstanceIds=[ instance_id ]
                )
                instance_state = response['StoppingInstances'][0]['CurrentState']['Name']
            except:
                raise EC2ConnectionError(title + ' stop_instances()')
        if instance_state == 'stopping':
            print('Instance %s is %s' % (instance_id, instance_state), end='', flush=True)
            delay = 3
            while instance_state == 'stopping':
                print('.', end='', flush=True)
                time.sleep(delay)
                t3 = timer()
                try:
                    response = self.connection.describe_instances(
                        InstanceIds=[ instance_id ]
                    )
                except:
                    raise EC2ConnectionError(title + ' describe_instances()')
                t4 = timer()
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
                instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
            print(' Done.')
        if instance_state != 'stopped':
            raise Exception('\nInstance %s is currently in a state that cannot be imaged.' % instance_id)

    # discover tags associated with instance
        tag_list = []
        try:
            response = self.connection.describe_instances(
                    InstanceIds=[ instance_id ]
                )
            instance_tags = response['Reservations'][0]['Instances'][0]['Tags']
            aws_tag_pattern = re.compile('aws:')
            for i in range(0, len(instance_tags)):
                if not aws_tag_pattern.findall(instance_tags[i]['Key']):
                    tag = {}
                    tag['Key'] = instance_tags[i]['Key']
                    tag['Value'] = instance_tags[i]['Value']
                    tag_list.append(tag)
        except:
            raise EC2ConnectionError(title + ' describe_instances()')

    # replace tag list if new tag input
        new_tags = False
        if image_tags:
            tag_list = deepcopy(image_tags)
            new_tags = True

    # create image of the instance
        try:
            response = self.connection.create_image(
                InstanceId=instance_id,
                Name=image_name
            )
            image_id = response['ImageId']
            print('Image %s is being created.' % image_name)
        except:
            raise EC2ConnectionError(title + ' create_image()')

    # add tags to image
        self.tagImage(image_id, tag_list)
        if new_tags:
            print('Tags from input have been added to image %s.' % image_id)
        else:
            print('Instance %s tags have been added to image %s.' % (instance_id, image_id))

    # restart instance
        try:
            self.connection.start_instances(
                    InstanceIds=[ instance_id ]
            )
            print('Restarting instance %s now.' % instance_id)
        except:
            raise EC2ConnectionError(title + ' start_instances()')

        return image_id

    def imageDetails(self, image_id):

        '''
            a method to retrieve the details of a single image on AWS EC2

        :param image_id: string with AWS id of image
        :return: dictionary of image attributes

            image attributes:
                ['imageID']
                ['snapshotID']
                ['name']
                ['state']
                ['region']
                ['tags']
        '''

        title = 'imageDetails'

    # validate input
        self.input.imageID(image_id, title + ' image id')

    # check image state
        self.checkImageState(image_id)

    # discover tags and snapshot id associated with image id
        try:
            response = self.connection.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise EC2ConnectionError(title + ' describe_images()')
        image_info = response['Images'][0]

    # wait for image state to stabilize
        if image_info['State'] == 'pending':
            self.checkImageState(image_info['ImageId'])
            try:
                response = self.connection.describe_images(
                    ImageIds=[ image_info['ImageId'] ]
                )
            except:
                raise EC2ConnectionError(title + ' describe_images()')
            image_info = response['Images'][0]

    # construct image details from response
        image = {}
        image['imageID'] = image_info['ImageId']
        image['snapshotID'] = image_info['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
        image['state'] = image_info['State']
        image['name'] = image_info['Name']
        image['region'] = os.environ['AWS_DEFAULT_REGION']
        try:
            image['tags'] = image_info['Tags']
        except:
            image['tags'] = []

        return image

    def findImages(self, tag_values=None):

        '''
            a method to retrieve the list of images on AWS EC2

        :param tag_values: [optional] list of tag values
        :return: list of image AWS ids
        '''

        title = 'findImages'

    # validate input
        kw_args = { 'Owners' : [ os.environ['AWS_OWNER_ID'] ] }
        if tag_values:
            self.input.tagValues(tag_values, title + ' tag values')
            kw_args['Filters'] = [ { 'Name': 'tag-value', 'Values': tag_values } ]

    # request image details from AWS
        tag_text = ''
        if tag_values:
            tag_text = ' with tag values %s' % tag_values
        query_text = 'Querying AWS region %s for images%s.' % (os.environ['AWS_DEFAULT_REGION'], tag_text)
        print(query_text)
        image_list = []
        try:
            response = self.connection.describe_images(**kw_args)
        except:
            raise EC2ConnectionError(title + ' describe_images()')
        response_list = response['Images']

        if not response_list:
            print('No images found initially. Checking again', end='', flush=True)
            state_timeout = 0
            delay = 3
            while not response_list and state_timeout < 12:
                print('.', end='', flush=True)
                time.sleep(delay)
                t3 = timer()
                try:
                    response = self.connection.describe_images(**kw_args)
                except:
                    raise EC2ConnectionError(title + ' describe_images()')
                response_list = response['Images']
                t4 = timer()
                state_timeout += 1
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
            print(' Done.')

    # wait until all images are no longer pending
        for image in response_list:
            if image['State'] == 'pending':
                self.checkImageState(image['ImageId'])
            try:
                response = self.connection.describe_images(
                    ImageIds=[ image['ImageId'] ]
                )
            except:
                raise EC2ConnectionError(title + ' describe_images()')
            image_info = response['Images'][0]

    # construct image details from response list
            if image_info['State'] == 'available':
                image_list.append(image_info['ImageId'])

    # report outcome and return results
        if image_list:
            print_out = 'Found image'
            if len(image_list) > 1:
                print_out += 's'
            i_counter = 0
            for id in image_list:
                if i_counter > 0:
                    print_out += ','
                print_out += ' ' + str(id)
                i_counter += 1
            print_out += '.'
            print(print_out)
        else:
            print('No images found.')

        return image_list

    def removeImage(self, image_id):

        '''
            method for removing an image from AWS EC2

        :param image_id: string with AWS id of instance
        :return: True
        '''

        title = 'removeImage'

    # validate input
        self.input.imageID(image_id, title + ' image_id')

    # check image state
        print('Removing image %s.' % image_id)
        self.checkImageState(image_id)

    # discover tags and snapshot id associated with image id
        tag_list = []
        try:
            response = self.connection.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise EC2ConnectionError(title + ' describe_images()')
        image_tags = response['Images'][0]['Tags']
        snapshot_id = response['Images'][0]['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
        for i in range(0, len(image_tags)):
            tag = {}
            tag['Key'] = image_tags[i]['Key']
            tag['Value'] = image_tags[i]['Value']
            tag_list.append(tag)

    # remove tags from image
        try:
            self.connection.delete_tags(
                Resources=[ image_id ],
                Tags=tag_list
            )
        except:
            raise EC2ConnectionError(title + ' delete_tags()')
        print('Tags have been deleted from %s.' % image_id)

    # deregister image
        try:
            self.connection.deregister_image(
                ImageId=image_id
            )
        except:
            raise EC2ConnectionError(title + ' deregister_image()')
        print('Image %s has been deregistered.' % image_id)

    # delete snapshot
        try:
            self.connection.delete_snapshot(
                SnapshotId=snapshot_id
            )
        except:
            raise EC2ConnectionError(title + ' delete_snapshot()')
        print('Snapshot %s associated with image %s has been deleted.' % (snapshot_id, image_id))

        return True

    def importImage(self, image_id, aws_region):

        '''
            a method to import an image from another AWS region

            https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html

            REQUIRED: awsCredentials must have valid access to import region

        :param image_id: string with AWS id of source image
        :param aws_region: string with AWS region of source image
        :return: string with AWS id of new image
        '''

        title = 'importImage'

    # validate input
        self.input.imageID(image_id, title + ' image id')
        self.input.region(aws_region)
        region_cred = deepcopy(self.cred)
        region_cred['AWS_DEFAULT_REGION'] = aws_region
        if region_cred['AWS_DEFAULT_REGION'] == self.cred['AWS_DEFAULT_REGION']:
            raise IndexError('\n%s cannot import an image from the same region.' % title)

    # set environmental variables of region of source image
        for key, value in region_cred.items():
            os.environ[key] = value
        client = boto3.client('ec2')

    # check existence of image
        try:
            response = client.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise ValueError('\nImage %s in region %s does not exist.' % (image_id, aws_region))
        if not 'Images' in response.keys():
            raise ValueError('\nImage %s in region %s does not exist.' % (image_id, aws_region))
        elif not response['Images'][0]:
            raise ValueError('\nImage %s in region %s does not exist.' % (image_id, aws_region))

    # check into state of image
        elif not 'State' in response['Images'][0].keys():
            print('Checking into the status of image %s in region %s' % (image_id, aws_region), end='', flush=True)
            state_timeout = 0
            while not 'State' in response['Images'][0].keys():
                print('.', end='', flush=True)
                time.sleep(3)
                state_timeout += 1
                response = client.describe_images(
                    ImageIds=[ image_id ]
                )
                if state_timeout > 3:
                    raise Exception('\nFailure to determine status of image %s.' % image_id)
            print(' Done.')
        image_state = response['Images'][0]['State']

    # raise error if image is deregistered or otherwise invalid
        if image_state == 'deregistered' or image_state == 'invalid' or image_state == 'transient' or image_state == 'failed':
            raise Exception('\nImage %s in region %s is %s.' % (image_id, aws_region, image_state))

    # wait while image is pending
        elif image_state == 'pending':
            print('Image %s is %s' % (image_id, image_state), end='', flush=True)
            delay = 3
            state_timeout = 0
            while image_state != 'available':
                print('.', end='', flush=True)
                time.sleep(delay)
                t3 = timer()
                response = client.describe_images(
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
                    raise Exception('\nTimeout. Failure initializing image %s in region %s in less than 15min' % (image_id, aws_region))
                image_state = response['Images'][0]['State']
            print(' Done.')

    # discover tags and name associated with source image
        try:
            response = client.describe_images(
                ImageIds=[ image_id ]
            )
        except:
            raise EC2ConnectionError(title + ' describe_images()')
        image_info = response['Images'][0]

    # construct image details from response
        image_name = image_info['Name']
        image_region = region_cred['AWS_DEFAULT_REGION']
        tag_list = image_info['Tags']

    # reset environmental variables and connection method
        for key, value in self.cred.items():
            os.environ[key] = value
        self.connection = boto3.client('ec2')

    # copy image over to current region
        try:
            response = self.connection.copy_image(
                SourceRegion=image_region,
                SourceImageId=image_id,
                Name=image_name
            )
        except:
            raise EC2ConnectionError(title + ' copy_image()')
        new_id = response['ImageId']

    # check into state of new image
        self.checkImageState(new_id)

    # add tags from source image to new image
        try:
            self.connection.create_tags(
                Resources=[ new_id ],
                Tags=tag_list
            )
        except:
            raise EC2ConnectionError(title + ' create_tags()')
        print('Tags from image %s have been added to image %s.' % (image_id, new_id))

        return new_id

    def exportImage(self, image_id, aws_region):

        '''
            a method to add a copy of an image to another AWS region

            https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html

            REQUIRED: awsCredentials must have valid access to export region

        :param image_id: string of AWS id of image to be copied
        :param aws_region: string of AWS region to copy image to
        :return: string with AWS id of new image
        '''

        title = 'exportImage'

    # validate input
        self.input.imageID(image_id, title + ' image id')
        self.input.region(aws_region)
        region_cred = deepcopy(self.cred)
        region_cred['AWS_DEFAULT_REGION'] = aws_region
        if region_cred['AWS_DEFAULT_REGION'] == self.cred['AWS_DEFAULT_REGION']:
            raise IndexError('\n%s cannot export an image to the same region.' % title)

    # check state of image to be copied
        self.checkImageState(image_id)

    # discover tags and name associated with image to be copied
        image_details = self.imageDetails(image_id)
        tag_list = image_details['tags']
        image_name = image_details['name']

    # set environmental variables of region to export image to
        print('Copying image %s to region %s.' % (image_id, aws_region))
        for key, value in region_cred.items():
            os.environ[key] = value
        client = boto3.client('ec2')

    # copy image over to current region
        try:
            response = client.copy_image(
                SourceRegion=self.cred['AWS_DEFAULT_REGION'],
                SourceImageId=image_id,
                Name=image_name
            )
        except:
            raise EC2ConnectionError(title + ' copy_image()')
        new_id = response['ImageId']

    # check into state of new image
        try:
            response = client.describe_images(
                ImageIds=[ new_id ]
            )
        except:
            raise EC2ConnectionError(title + ' describe_images()')
        if not 'State' in response['Images'][0].keys():
            print('Checking into the status of image %s in region %s' % (new_id, aws_region), end='', flush=True)
            state_timeout = 0
            while not 'State' in response['Images'][0].keys():
                print('.', end='', flush=True)
                time.sleep(3)
                state_timeout += 1
                try:
                    response = client.describe_images(
                        ImageIds=[ new_id ]
                    )
                except:
                    raise EC2ConnectionError(title + ' describe_images()')
                if state_timeout > 3:
                    raise Exception('\nFailure to determine status of image %s in region %s.' % (new_id, aws_region))
            print(' Done.')
        image_state = response['Images'][0]['State']

    # wait while image is pending
        if image_state == 'pending':
            print('Image %s in region %s is %s' % (new_id, aws_region, image_state), end='', flush=True)
            delay = 3
            state_timeout = 0
            while image_state != 'available':
                print('.', end='', flush=True)
                time.sleep(delay)
                t3 = timer()
                try:
                    response = client.describe_images(
                        ImageIds=[ new_id ]
                    )
                except:
                    raise EC2ConnectionError(title + ' describe_images()')
                t4 = timer()
                state_timeout += 1
                response_time = t4 - t3
                if 3 - response_time > 0:
                    delay = 3 - response_time
                else:
                    delay = 0
                if state_timeout > 300:
                    raise Exception('\nTimeout. Failure initializing image %s in region %s in less than 15min' % (new_id, aws_region))
                image_state = response['Images'][0]['State']
            print(' Done.')

    # add tags from image to image copy
        try:
            client.create_tags(
                Resources=[ new_id ],
                Tags=tag_list
            )
        except:
            raise EC2ConnectionError(title + ' create_tags()')
        print('Tags from image %s have been added to image %s.' % (image_id, new_id))

    # reset environmental variables and connection method
        for key, value in self.cred.items():
            os.environ[key] = value
        self.connection = boto3.client('ec2')

        return new_id

    def cleanupEC2(self):

        '''
            a method for removing instances and images in unusual states

        :return: True
        '''

    # find non-running instances
        print('Cleaning up region %s.' % str(os.environ['AWS_DEFAULT_REGION']))
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
                    print('Tags have been deleted from instance %s.' % instance_info['InstanceId'])
                except:
                    pass

    # try stopping non-running instance
                try:
                    self.connection.stop_instances(
                        InstanceIds=[ instance_info['InstanceId'] ]
                    )
                    print('Instance %s is stopping.' % instance_info['InstanceId'])
                except:
                    pass

    # try terminating non-running instance
                try:
                    self.connection.terminate_instances(
                        InstanceIds=[ instance_info['InstanceId'] ]
                    )
                    print('Instance %s is terminating.' % instance_info['InstanceId'])
                except:
                    pass

    # find non-available images
        response = self.connection.describe_images(
            Owners=[ os.environ['AWS_OWNER_ID'] ]
        )
        image_list = response['Images']
        for image in image_list:
            image_info = image.copy()
            if image_info['State'] == 'pending':
                self.checkImageState(image_info['ImageId'])
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
                    print('Tags have been deleted from image %s.' % image_info['ImageId'])
                except:
                    pass

    # try deregistering non-available image
                try:
                    self.connection.deregister_image(
                        ImageId=image_info['ImageId']
                    )
                    print('Image %s has been deregistered.' % image_info['ImageId'])
                except:
                    pass

    # try deleting snapshot associated with non-available image
                try:
                    self.connection.delete_snapshot(
                        SnapshotId=image_info['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
                    )
                    snap_id = image_info['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
                    image_id = image_info['ImageId']
                    print('Snapshot %s associated with image %s has been deleted.' % (snap_id, image_id))
                except:
                    pass

    # find snapshots with errors
        response = self.connection.describe_snapshots(
            OwnerIds=[ os.environ['AWS_OWNER_ID'] ]
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
                    print('Snapshot %s has been deleted.' % snapshot_info['SnapshotId'])
                except:
                    pass

        return True

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
            if len(instance_list) > 1:
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
        subnet_details = self.ingest(subnet_dict, subnet_details)

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
            if len(instance_list) > 1:
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
        group_details = self.ingest(group_info, group_details)
        
        return group_details

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


    # from pprint import pprint
    # pprint(tag_list)
    # pprint(instance_details['tags'])
    

