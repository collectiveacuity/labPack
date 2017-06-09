__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'

# https://datastax.github.io/python-driver/getting_started.html
# pip install cassandra-driver

class cassandraClient(object):

    _class_fields = {
        'schema': {
            'cassandra_ip': ''
        }
    }

    def __init__(self, cassandra_ip):

        self.endpoint = cassandra_ip

        try:
            from sys import path as sys_path
            sys_path.append(sys_path.pop(0))
            from cassandra.cluster import Cluster
            self.cluster = Cluster([self.endpoint])
            sys_path.insert(0, sys_path.pop())
        except:
            print('cassandra-driver module required to use cassandraClient. try: pip install cassandra-driver')
            exit()

        self.session = self.cluster.connect()

if __name__ == '__main__':
    docker_ip = '192.168.99.100'
    cassandra_client = cassandraClient(docker_ip)
    print(cassandra_client.session)