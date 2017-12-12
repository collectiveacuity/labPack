__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'


'''
PLEASE NOTE:    cassandra package requires cassandra-driver module

(install)       pip install cassandra-driver
'''

try:
    from sys import path as sys_path
    sys_path.append(sys_path.pop(0))
    from cassandra.cluster import Cluster
    sys_path.insert(0, sys_path.pop())
except:
    import sys
    print('cassandra package requires cassandra-driver module. try: pip install cassandra-driver')
    sys.exit(1)

class cassandraClient(object):

    '''
        a class of methods for interacting with a cassandra database
    
    https://datastax.github.io/python-driver/getting_started.html
    
    NOTE:   WIP
    '''
    
    _class_fields = {
        'schema': {
            'database_url': ''
        }
    }

    def __init__(self, database_url):

    # construct endpoint
        self.endpoint = database_url

    # construct cluster
        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from cassandra.cluster import Cluster
        self.cluster = Cluster([self.endpoint])
        sys_path.insert(0, sys_path.pop())

    # construct session
        self.session = self.cluster.connect()

if __name__ == '__main__':
    docker_ip = '192.168.99.100'
    cassandra_client = cassandraClient(docker_ip)
    print(cassandra_client.session)