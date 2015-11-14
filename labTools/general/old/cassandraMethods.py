__author__ = 'rc1492'
__created__ = '2015'

# https://datastax.github.io/python-driver/getting_started.html
# pip install cassandra-driver

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

cassandraIP = ''
cassandraPort = ''

# instantiate a connection to cassandra node
cluster = Cluster([cassandraIP], port=cassandraPort)

# create a session with keyspace
session = cluster.connect('processorKeySpace')

