__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

from labpack.platforms.aws.ssh import sshClient
from labpack.platforms.aws.ec2 import ec2Client
from labpack.records.settings import load_settings
cred_path = '../../cred/awsLab.yaml'
pem_folder = '../keys'
aws_cred = load_settings(cred_path)
client_kwargs = {
    'access_id': aws_cred['aws_access_key_id'],
    'secret_key': aws_cred['aws_secret_access_key'],
    'region_name': aws_cred['aws_default_region'],
    'owner_id': aws_cred['aws_owner_id'],
    'user_name': aws_cred['aws_user_name'],
    'verbose': False
}
ec2_client = ec2Client(**client_kwargs)
instance_list = ec2_client.list_instances(tag_values=['test'])
if not instance_list:
    raise Exception('There are no test instances running.')
instance_id = instance_list[0]
instance_details = ec2_client.read_instance(instance_id)
pem_name = instance_details['keypair']
from os import path
pem_file = path.join(pem_folder, '%s.pem' % pem_name)
if not path.exists(pem_file):
    raise Exception('Instance pem key %s.pem does not exist in keys folder.' % pem_name)
client_kwargs['instance_id'] = instance_id
client_kwargs['pem_file'] = pem_file
ssh_client = sshClient(**client_kwargs)
ssh_client.terminal()