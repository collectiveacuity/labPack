__author__ = 'rcj1492'
__created__ = '2020.06'
__license__ = '©2020 Collective Acuity'

import pytest
from copy import deepcopy
from labpack.databases.sql import SQLSession, SQLTable

if __name__ == '__main__':

    record_schema = {
        'schema': {
            'id': 0,
            'token_id': '',
            'expires_at': 0.0,
            'service_scope': [True],
            'active': False,
            'address': {
                'number': 0,
                'street': '',
                'city': '',
                'zip': ''
            },
            'document': {},
            'places': ['']
        },
        'components': {
            '.address': {
                'required_field': False
            },
            '.address.number': {
                'integer_data': True
            }
        }
    }
    details = {
        'token_id': 'unittest', 
        'places': ['here', 'there'], 
        'address': {'number': 3, 'city': 'motown'},
        'document': {'first_name': 'who', 'second_name': 'what'}
    }
    bunch = []
    cities = ['middleton', 'milton', 'madison', 'mechanicsville', 'seattle']
    places = ['nowhere', 'wherever', 'somewhere', 'nowhere,wherever', 'wherever,somewhere']
    for i in range(5):
        variant = deepcopy(details)
        variant['address']['number'] += i
        if variant['address']['number'] == 6:
            variant['address']['number'] = 7
        variant['address']['city'] = cities[i]
        variant['places'].extend(places[i].split(','))
        bunch.append(variant)

    # instantiate client
    table_name = 'Test_Records'
    database_url = 'sqlite:///../data/test_sql.db'
    session = SQLSession(database_url)

    # instantiate table and test init constructors
    table = SQLTable(session, table_name, record_schema, verbose=True)
    assert 'city' in table.default['address'].keys()
    assert '.document' in table.empty_maps
    
    # test instantiate errors
    with pytest.raises(Exception) as err:
        null_schema = deepcopy(record_schema)
        null_schema['schema']['address']['zip'] = None
        SQLTable(session, 'Not_An_Schema', null_schema)
    assert str(err).find('cannot have the null datatype') > -1

    # test helper methods
    prepped = table._prepare_record(details)
    assert 'address.city' in prepped.keys()
    assert isinstance(prepped['places'], bytes)
    statement = table.table.insert().values(**prepped)
    assert str(statement).find(':places') > -1

    # test create, read, update, delete and exists
    record_id = table.create(details)
    record = table.read(record_id)
    record['address']['city'] = 'motown'
    table.update(record)
    updated = table.read(record_id)
    assert updated['address']['city'] == 'motown'
    table.delete(record_id)
    assert not table.exists(record_id)

    # test rebuild
    record_id = table.create(details)
    str_schema = deepcopy(record_schema)
    str_schema['schema']['id'] = ''
    table = SQLTable(session, table_name, str_schema)
    record = table.read(str(record_id))
    assert isinstance(record['id'], str)
    session = SQLSession(database_url)
    table = SQLTable(session, table_name, record_schema, verbose=True)
    record = table.read(record_id)
    assert isinstance(record['id'], int)

    # test list simple filters and cursors
    for i in range(len(bunch)):
        table.create(bunch[i])
    records, cursor = table.list(filter={'address.city': 'middleton'})
    assert records[0]['address']['city'] == 'middleton'
    assert not cursor
    records, cursor = table.list(filter={'places[0]': 'nowhere'})
    assert 'nowhere' in records[0]['places']
    assert not cursor
    filter = {'address.number': {'greater_than': 3}}
    records, cursor = table.list(filter=filter, limit=2, ids_only=True)
    assert cursor
    assert isinstance(records[0], int)
    next, cursor = table.list(filter=filter, cursor=cursor, limit=2, ids_only=True)
    records.extend(next)
    assert len(set(records)) == 4

    # test multiple equality filters
    filter = {'address.city': 'seattle', 'address.number': 7, 'places[0]': 'here'}
    records, cursor = table.list(filter=filter)
    assert records

    # test filter and sort on same field
    filter = {'address.city': {'less_than': 'n'}}
    records, cursor = table.list(filter=filter, sort=[{'address.city': True}])
    assert records[0]['address']['city'] > records[-1]['address']['city']

    # test unsupported query with mix of filters
    filter = {'address.city': {'must_contain': ['n$']}, 'address.number': {'min_value': 5}}
    records, cursor = table.list(filter=filter)
    assert records[0]['address']['city'] == 'madison'
    filter = {'address.city': {'less_than': 'n', }, 'address.number': {'min_value': 6}}
    records, cursor = table.list(filter=filter)
    assert records[-1]['address']['city'] == 'mechanicsville'

    # test unsupported query with filter and sort on different fields
    filter = {'address.number': {'greater_than': 4}}
    sort = [{'address.city': True}]
    records, cursor = table.list(filter=filter, sort=sort)
    assert records[0]['address']['city'] == 'seattle'

    # test filter with = and > on separate properties
    filter = {'places[0]': 'here', 'address.number': {'min_value': 5}}
    records, cursor = table.list(filter=filter)
    assert records

    # test multiple sort properties
    sort = [{'address.city': True}, {'address.number': False}]
    records, cursor = table.list(sort=sort)
    assert records[-1]['address']['city'] == 'mechanicsville'

    # test equal filter and different first sort property
    filter = {'address.number': 5}
    sort = [{'address.city': True}]
    records, cursor = table.list(filter=filter, sort=sort)
    assert records

    # TODO test export

    # test remove
    table.remove()