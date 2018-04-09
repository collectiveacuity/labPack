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

class cassandraSession(object):

    '''
        a class of methods for creating a session to a cassandra database

    CQL Connector
    https://datastax.github.io/python-driver/getting_started.html
    https://flask-cqlalchemy.readthedocs.io/en/latest/
    https://datastax.github.io/python-driver/cqlengine/third_party.html

    Authentication
    https://datastax.github.io/python-driver/api/cassandra/auth.html#
    https://cassandra.apache.org/doc/latest/operating/security.html#enabling-password-authentication
    '''
    
    _class_fields = {
        'schema': {
            'hostname': [ '127.0.0.1' ],
            'port': 0,
            'username': '',
            'password': '',
            'cert_path': ''
        },
        'components': {
            'hostname[0]': {
                "contains_either": [ 
                    "\\d+\\.\\d+\\.\\d+\\.\\d+", 
                    "[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$" 
                ]
            }
        }
    }

    def __init__(self, hostname, port=9042, username='', password='', cert_path=''):

        title = '%s.__init__' % self.__class__.__name__

    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # ingest hostname
        self_hostname = hostname
        if isinstance(hostname, str):
            if hostname:
                self_hostname = [ hostname ]

    # validate inputs
        input_fields = {
            'hostname': self_hostname,
            'port': port,
            'username': username,
            'password': password,
            'cert_path': cert_path
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct endpoint
        self.hostname = self_hostname
        self.port = port
        self.username = username
        self.password = password
        self.cert_path = cert_path

    # construct cluster
        cluster_kwargs = {
            'contact_points': self.hostname,
            'port': self.port
        }
        if self.username and self.password:
            from sys import path as sys_path
            sys_path.append(sys_path.pop(0))
            from cassandra.auth import PlainTextAuthProvider
            sys_path.insert(0, sys_path.pop())
            cluster_kwargs['auth_provider'] = PlainTextAuthProvider(
                username=username, 
                password=password
            )
        if cert_path:
            from os import path
            import ssl
            if not path.exists(cert_path):
                raise ValueError('%s(cert_path="%s") is not a valid file path.' % (title, cert_path))
            cluster_kwargs['ssl_options'] = {
                'ca_certs': cert_path,
                'cert_reqs': ssl.CERT_REQUIRED,
                'ssl_version': ssl.PROTOCOL_TLSv1
            }
        self.cluster = Cluster(**cluster_kwargs)

    # construct session
        self.session = self.cluster.connect()

class cassandraTable(object):
    
    '''
        a class of methods for interacting with a table on cassandra

    CQL Connector
    https://datastax.github.io/python-driver/getting_started.html
    https://cassandra.apache.org/doc/latest/cql/dml.html

    NOTE:   WIP
    '''
    
    _class_fields = {
        'schema': {
            'keyspace_name': '',
            'table_name': '',
            'record_schema': {},
            'replication_strategy': {
                'class': 'SimpleStrategy'
            }
        },
        'components': {
            'keyspace_name': {
                'max_length': 48
            },
            'table_name': {
                'max_length': 48
            },
            'replication_strategy': {
                'extra_fields': True
            },
            'replication_strategy.class': {
                'discrete_values': [ 'SimpleStrategy', 'NetworkTopologyStrategy' ]
            }
        }
    }

    def __init__(self, keyspace_name, table_name, record_schema, cassandra_session, replication_strategy=None):

        title = '%s.__init__' % self.__class__.__name__
    
    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'keyspace_name': keyspace_name,
            'table_name': table_name,
            'record_schema': record_schema,
            'replication_strategy': replication_strategy
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate cassandra session
        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from cassandra.cluster import Session
        sys_path.insert(0, sys_path.pop())
        if not isinstance(cassandra_session, Session):
            raise ValueError('%s(cassandra_session) must be a cassandra.cluster.Session datatype.' % title)
        self.session = cassandra_session

    # test, create or update keyspace
    
    # test, create or update table
    
    
    
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
    cassandra_session = cassandraSession(
        hostname=cass_hostname,
        port=cass_port,
        username=cass_cred['cassandra_account_username'],
        password=cass_cred['cassandra_account_password'],
        cert_path=cert_path
    )
    print(cassandra_session.session)
    print(cassandra_session.session.__class__)

# test failure of ssl error
    import pytest

# test failure of authentication error

# test cassandra user login disabled error
