__author__ = 'rcj1492'
__created__ = '2016.02'

from urllib.request import urlopen
from os import path, makedirs
import json
from copy import deepcopy
from awsDocker.exceptions import AWSConnectionError

class awsPrices(object):

    '''
        a class of methods for retrieving pricing information from AWS
    '''

    __name__ = 'awsPrices'

    def __init__(self):

        '''
            method for initializing the awsPrices class & retrieving pricing tables index
        '''

    # construct downloads folder
        from os import path
        from labpack import __module__
        from labpack.storage.appdata import appdataClient
        client_kwargs = {
            'collection_name': 'Downloads',
            'prod_name': __module__
        }
        appdata_client = appdataClient(**client_kwargs)

    # define class parameters
        self.freshInstall = False
        self.baseURL = 'https://pricing.us-east-1.amazonaws.com'
        self.indexURL = '%s/offers/v1.0/aws/index.json' % self.baseURL
        self.fileFolder = path.join(appdata_client.collection_folder, 'tables')
        self.indexFile = 'aws-table-index.json'
        self.indexPath = '%s/%s' % (self.fileFolder, self.indexFile)
        self.regions = {
            'us-gov-west-1': "AWS GovCloud (US)",
            'ap-northeast-1': "Asia Pacific (Tokyo)",
            'ap-northeast-2': "Asia Pacific (Seoul)",
            'ap-southeast-1': "Asia Pacific (Singapore)",
            'ap-southeast-2': "Asia Pacific (Sydney)",
            'eu-central-1': "EU (Frankfurt)",
            'eu-west-1': "EU (Ireland)",
            'sa-east-1': "South America (Sao Paulo)",
            'us-east-1': "US East (N. Virginia)",
            'us-west-1': "US West (N. California)",
            'us-west-2': "US West (Oregon)"
        }
        self.tables = {
            'AmazonS3': 'aws-s3-prices.json',
            'AmazonGlacier': 'aws-glacier-prices.json',
            'AmazonEC2': 'aws-ec2-prices.json',
            'AmazonSES': 'aws-ses-prices.json',
            'AmazonRDS': 'aws-rds-prices.json',
            'AmazonSimpleDB': 'aws-sdb-json',
            'AmazonDynamoDB': 'aws-ddb-prices.json',
            'AmazonRoute53': 'aws-r53-prices.json',
            'AmazonRedshift': 'aws-redshift-prices.json',
            'AmazonElastiCache': 'aws-ec-prices.json',
            'AmazonCloudFront': 'aws-cf-prices.json',
            'awskms': 'aws-kms-prices.json',
            'AmazonVPC': 'aws-vpc-prices.json'
        }

    # create folder for pricing files
        if not path.isdir(self.fileFolder):
            print('Creating tables sub-folder... ', end='', flush=True)
            makedirs(self.fileFolder)
            print('done.')

    # download pricing tables index if not present
        if not path.exists(self.indexPath):
            print('Downloading AWS Price Tables Index... ', end='', flush=True)
            try:
                response = urlopen(self.indexURL)
            except:
                raise AWSConnectionError('urlopen(%s)' % self.indexURL)
            with open(self.indexPath, 'wb') as f:
                f.write(response.read())
                f.close()
            print('done.')
            self.freshInstall = True

    # load index as dictionary
        self.tableIndex = json.loads(open(self.indexPath).read())
        self.newPrices = False

    def updateIndex(self):

        '''
            a method to download the latest pricing table index from AWS

        :return: dictionary with new index or empty
        '''

        title = '%s.updateIndex' % self.__name__

    # retrieve latest pricing tables index file
        try:
            print('Checking AWS website for pricing table updates... ', end='', flush=True)
            response = urlopen(self.indexURL)
            print('done.')
        except:
            raise AWSConnectionError('urlopen(%s)' % self.indexURL)
        download_data = json.loads(response.read().decode())
        download_date = download_data['publicationDate']

    # update local file if publication date is different and return status
        try:
            index_data = json.loads(open(self.indexPath).read())
        except:
            raise TypeError('File at %s is not a valid json file.' % self.indexPath)
        index_date = index_data['publicationDate']
        if download_date > index_date:
            with open(self.indexPath, 'wb') as f:
                f.write(response.read())
                f.close()
            print('New pricing tables available.')
            return download_data
        else:
            print('Existing pricing tables are up-to-date.')
            return {}

    def downloadData(self, aws_service, table_url, save_file=False):

        '''
            a method to download price table data from AWS

        :param aws_service: string with name of AWS service
        :param table_url: string with url to AWS service
        :param save_file: boolean to retain a copy of the file
        :return: boolean
        '''

        title = '%s.downloadData' % self.__name__

    # validate inputs
        service_list = self.tableIndex['offers'].keys()
        if not isinstance(aws_service, str):
            raise TypeError('%s aws_service input must be a string.' % title)
        elif aws_service not in service_list:
            raise ValueError('%s aws_service input must be one of %s values.' % (title,service_list))
        elif not isinstance(table_url, str):
            raise TypeError('%s table_url input must be a string.' % title)

    # download local copy of file if not present
        try:
            print('Retrieving AWS price table data for %s... ' % aws_service, end='', flush=True)
            response = urlopen(table_url)
            data_bytes = response.read()
        except:
            raise AWSConnectionError('urlopen(%s)' % table_url)
        price_table = json.loads(data_bytes.decode())
        print('done.')

    # save a local copy of data
        if save_file:
            full_file = deepcopy(self.tables[aws_service])
            full_file = full_file.replace('.json','-full.json')
            file_path = '%s/%s' % (self.fileFolder, full_file)
            print('Saving AWS price table data for %s as %s... ' % (aws_service, full_file), end='', flush=True)
            with open(file_path, 'wb') as f:
                f.write(data_bytes)
                f.close()
            print('done.')

        return price_table

    def summarizeEC2(self, price_table):

        title = '%s.summarizeData' % self.__name__

    # validate input
        if not isinstance(price_table, dict):
            raise TypeError('%s aws_service input must be a string.' % title)

    # construct the empty dictionaries
        price_summary = {}
        region_index = {}
        region_map = deepcopy(self.regions)
        for key, value in region_map.items():
            price_summary[key] = {}
            region_index[value] = key

    # populate price summary by iterating over price table
        for key, value in price_table['products'].items():
            if 'operatingSystem' in value['attributes'].keys():
                if value['attributes']['operatingSystem'] == 'Linux':
                    region_name = value['attributes']['location']
                    instance_id = value['attributes']['instanceType']
                    sku_value = value['sku']
                    instance_price = ''
                    demand_price = price_table['terms']['OnDemand'][sku_value]
                    for k1, v1 in demand_price.items():
                        if isinstance(v1, dict):
                            if 'priceDimensions' in v1.keys():
                                price_dim = demand_price[k1]['priceDimensions']
                                for k2, v2 in price_dim.items():
                                    if isinstance(v2, dict):
                                        if 'pricePerUnit' in v2.keys():
                                            unit_price = price_dim[k2]['pricePerUnit']
                                            if 'USD' in unit_price.keys():
                                                instance_price = unit_price['USD']
                    price_summary[region_index[region_name]][instance_id] = {
                        'sku': sku_value,
                        'price': instance_price,
                        'terms': 'OnDemand'
                    }

        return price_summary

    def updateTable(self, aws_service, save_full=False):

        title = '%s.updateTable' % self.__name__

    # validate inputs
        service_list = self.tableIndex['offers'].keys()
        if not isinstance(aws_service, str):
            raise TypeError('%s aws_service input must be a string.' % title)
        elif aws_service not in service_list:
            raise ValueError('%s aws_service input must be one of %s values.' % (title,service_list))

    # retrieve latest data from AWS
        table_url = '%s%s' % (self.baseURL, self.tableIndex['offers'][aws_service]['currentVersionUrl'])
        file_name = deepcopy(self.tables[aws_service])
        file_path = '%s/%s' % (self.fileFolder, file_name)
        if not path.exists(file_path) or self.newPrices or self.freshInstall:
            if not path.exists(file_path):
                print('Local AWS price table for %s does not exist.' % aws_service)
            else:
                print('Local AWS price table for %s is out of date.' % aws_service)
            price_table = self.downloadData(aws_service, table_url, save_file=save_full)

    # calculate summary price table from retrieved data
            if aws_service == 'AmazonEC2':
                print('Saving AWS price table for %s as %s... ' % (aws_service, file_name), end='', flush=True)
                new_table = self.summarizeEC2(price_table)
    # save summary price table as local json file
                with open(file_path, 'wb') as f:
                    f.write(json.dumps(new_table).encode('utf-8'))
                    f.close()
                print('done.')
            else:
                print('Summary price table not available for %s.' % aws_service)

        return True

    def update(self, aws_service, save_full=False):

        title = '%s.update' % self.__name__

    # validate inputs
        service_list = self.tableIndex['offers'].keys()
        if not isinstance(aws_service, str):
            raise TypeError('%s aws_service input must be a string.' % title)
        elif aws_service not in service_list:
            raise ValueError('%s aws_service input must be one of %s values.' % (title,service_list))

    # check for updates to table index on aws web page
        if not self.freshInstall:
            updated_index = self.updateIndex()
            if updated_index:
                self.newPrices = True
                self.tableIndex = updated_index

    # pass through any updated info to the summary pricing table
        self.updateTable(aws_service, save_full=save_full)

        return self

# TODO: Create pricing summaries for non-EC2 services
# TODO: Dynamically retrieve region endpoint information
