__author__ = 'rcj1492'
__created__ = '2016.06'
__license__ = 'MIT'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json
from cred.credentialsAWSLab import awsCredentials
aws_rules = json.loads(open('aws-rules.json').read())

from awsDocker.awsELB import awsELB

client = awsELB(awsCredentials, aws_rules)
lb_list = client.findLoadBalancers()
lb_details = client.loadBalancerDetails('lab-lb-useast1-prod-574f16b4')
