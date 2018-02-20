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
            'hostname': [ '127.0.0.1' ],
            'port': 0,
            'username': '',
            'password': '',
            'cert_path': ''
        }
    }

    def __init__(self, hostname, port=9042, username='', password='', cert_path=''):

    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        self_hostname = hostname
        if isinstance(hostname, str):
            if hostname:
                self_hostname = [ hostname ]

    # construct endpoint
        self.hostname = self_hostname
        self.port = port
        self.username = username
        self.password = password
        self.cert_path = cert_path

    # import cassandra-driver methods
        import ssl
        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from cassandra.cluster import Cluster
        from cassandra.auth import PlainTextAuthProvider
        sys_path.insert(0, sys_path.pop())
    
    # construct cluster
        cluster_kwargs = {
            'contact_points': self.hostname,
            'port': self.port
        }
        if self.username and self.password:
            cluster_kwargs['auth_provider'] = PlainTextAuthProvider(
                username=username, 
                password=password
            )
        if cert_path:
            cluster_kwargs['ssl_options'] = {
                'ca_certs': cert_path,
                'cert_reqs': ssl.CERT_REQUIRED,
                'ssl_version': ssl.PROTOCOL_TLSv1
            }
        self.cluster = Cluster(**cluster_kwargs)

    # construct session
        self.session = self.cluster.connect()

if __name__ == '__main__':

# test client init (with auth and ssl)
    test_public = False
    from labpack.records.settings import load_settings
    cass_cred = load_settings('../../../cred/cassandra-account.yaml')
    cert_path = '../../keys/root.cass.20180220.crt'
    cass_hostname = '127.0.0.1'
    cass_port = 9042
    if test_public:
        cass_hostname = cass_cred['cassandra_database_hostname']
        cass_port = cass_cred['cassandra_database_port']
    cassandra_client = cassandraClient(
        hostname=cass_hostname,
        port=cass_port,
        username=cass_cred['cassandra_account_username'],
        password=cass_cred['cassandra_account_password'],
        cert_path=cert_path
    )
    print(cassandra_client.session)

# test failure of ssl error
    import pytest

# test failure of authentication error

# test cassandra user login disabled error
