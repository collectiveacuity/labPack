__author__ = 'rcj1492'
__created__ = '2016.01'

'''
a set of methods for interacting with the local environment
'''

from re import compile
from os import path

def save(self, file_name=''):
    yaml_file = self.file
    file_type = compile('\.yaml$')
    if file_name:
        if not file_type.findall(file_name):
            raise Exception('%s must have a .yaml file type' % file_name)
    # check to see that directory exists
        elif not path.isdir(path.dirname(file_name)):
            raise Exception('%s must be a valid file path.' % file_name)
        yaml_file = file_name
    with open(yaml_file, 'wb') as f:
        f.write(self.yaml.encode('utf-8'))
        f.close()