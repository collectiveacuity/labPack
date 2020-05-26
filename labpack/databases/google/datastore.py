__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

'''
PLEASE NOTE:    datastore package requires the google cloud datastore module.

(all platforms) pip3 install google-cloud-datastore
'''

try:
    from google.cloud import datastore
except:
    import sys

    print('datastore package requires the google cloud datastore module. try: pip3 install google-cloud-datastore')
    sys.exit(1)

import re
import json
from labpack.records.id import labID
from jsonmodel.validators import jsonModel


class DatastoreTable(object):

    def __init__(self):
        pass
        
