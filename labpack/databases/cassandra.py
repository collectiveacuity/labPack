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

    CQL Connector
    https://datastax.github.io/python-driver/getting_started.html
    https://flask-cqlalchemy.readthedocs.io/en/latest/

    Authentication
    https://datastax.github.io/python-driver/api/cassandra/auth.html#
    https://cassandra.apache.org/doc/latest/operating/security.html#enabling-password-authentication

    NOTE:   WIP
    '''
    
    _class_fields = {
        'schema': {
            'database_url': '',
            'username': '',
            'password': ''
        }
    }

    def __init__(self, database_url, username='', password=''):

    # construct endpoint
        self.endpoint = database_url

    # construct cluster
        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from cassandra.cluster import Cluster
        from cassandra.auth import PlainTextAuthProvider
        auth_provider = None
        if username and password:
            auth_provider = PlainTextAuthProvider(
                username=username, 
                password=password
            )
        self.cluster = Cluster([self.endpoint], auth_provider=auth_provider)
        sys_path.insert(0, sys_path.pop())

    # construct session
        self.session = self.cluster.connect()

if __name__ == '__main__':
    docker_ip = '192.168.99.100'
    cassandra_client = cassandraClient(docker_ip)
    print(cassandra_client.session)