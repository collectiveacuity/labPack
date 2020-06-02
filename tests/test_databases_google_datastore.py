__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

import pytest
from copy import deepcopy
from labpack.databases.google.datastore import DatastoreTable

if __name__ == '__main__':

    record_schema = {
        'schema': {
            'id': 0.0,
            'token_id': '',
            'expires_at': 0.0,
            'service_scope': [ True ],
            'active': False,
            'address': {
                'number': 0,
                'street': '',
                'city': '',
                'zip': ''
            },
            'document': {},
            'places': [ '' ]
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
    indices = ['address.city']
    # indices = ['address.city', 'address.number', 'places[0]']
    details = {'token_id': 'unittest', 'places': ['here', 'there'], 'address': {'number': 3, 'city': 'motown'}, 'document': { 'first_name': 'who', 'second_name': 'what' } }
    bunch = []
    cities = ['middleton','milton','madison','mechanicsville','seattle']
    places = ['nowhere','wherever','somewhere','nowhere,wherever','wherever,somewhere']
    for i in range(5):
        variant = deepcopy(details)
        variant['address']['number'] += i
        variant['address']['city'] = cities[i]
        variant['places'].extend(places[i].split(','))
        bunch.append(variant)

    # instantiate client
    google_cred = '../keys/google-service-account.json'
    from google.cloud.datastore import Client as DatastoreClient
    from google.cloud.datastore import Entity
    client = DatastoreClient.from_service_account_json(google_cred)

    # instantiate table and test init constructors
    table = DatastoreTable(client, 'Test Records', record_schema, indices=indices, verbose=True)
    assert 'address.city' in table.indices
    assert 'city' in table.default['address'].keys()
    assert '.service_scope' in table.json_lists

    # test instantiate errors
    with pytest.raises(Exception) as err:
        error_indices = ['service_scope[0]']
        DatastoreTable(client, 'Not An Index', record_schema, indices=error_indices)
    assert str(err).find('for lists of strings or numbers') > -1
    with pytest.raises(Exception) as err:
        error_indices = ['document']
        DatastoreTable(client, 'Not An Index', record_schema, indices=error_indices)
    assert str(err).find('cannot be a map datatype') > -1
    
    # test helper methods
    prepped = table._prepare_record(details)
    assert 'address.city' in prepped.keys()
    assert 'here' in prepped['places']
    gen_key = table.client.key(table.kind)
    entity = Entity(**{'key': gen_key})
    del prepped['id']
    entity.update(prepped)
    reconstructed = table._reconstruct_record(entity)
    assert reconstructed['id']
    assert 'city' in reconstructed['address'].keys()
    assert 'here' in reconstructed['places']
    assert details['document'] == reconstructed['document']

    # test create, read, update, delete and exists
    record_id = table.create(details)
    record = table.read(record_id)
    record['address']['city'] = 'middletown'
    table.update(record)
    updated = table.read(record_id)
    assert updated['address']['city'] == 'middletown'
    table.delete(record_id)
    assert not table.exists(record_id)

    # test update index
    new_indices = ['address.city', 'address.number', 'places[0]']
    for i in range(len(bunch)):
        if i == 2:
            table = DatastoreTable(client, 'Test Records', record_schema, indices=new_indices, verbose=True)
        table.create(bunch[i])
    count = table._update_indices(2)
    assert count

    # test list simple filters and cursors
    records, cursor = table.list(filter={'address.city':'middleton'})
    assert records[0]['address']['city'] == 'middleton'
    assert not cursor
    records, cursor = table.list(filter={'places[0]': 'nowhere'})
    assert 'nowhere' in records[0]['places']
    assert not cursor
    filter = {'address.number': { 'greater_than': 3 } }
    records, cursor = table.list(filter=filter, limit=2, ids_only=True)
    assert cursor
    next, cursor = table.list(filter=filter, cursor=cursor, limit=2, ids_only=True)
    records.extend(next)
    assert len(set(records)) == 4

    # test multiple equality filters
    filter = { 'address.city': 'seattle', 'address.number': 7, 'places[0]': 'here' }
    records, cursor = table.list(filter=filter)
    assert records

    # test filter and sort on same field
    filter = {'address.city': { 'less_than': 'n' } }
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
    filter = { 'address.number': { 'greater_than': 4 } }
    sort = [{'address.city': True }]
    records, cursor = table.list(filter=filter, sort=sort)
    assert records[0]['address']['city'] == 'seattle'

    # test errors which require composite indexing
    # test error for = and > on separate properties
    with pytest.raises(Exception) as err:
        filter = { 'places[0]': 'here', 'address.number': {'min_value': 5} }
        records, cursor = table.list(filter=filter)
    assert str(err).find('no matching index found') > -1

    # test error for multiple sort properties
    with pytest.raises(Exception) as err:
        sort = [ { 'address.city': True }, { 'address.number': False } ]
        records, cursor = table.list(sort=sort)
    assert str(err).find('no matching index found') > -1

    # test error for equal filter and different first sort property
    with pytest.raises(Exception) as err:
        filter = { 'address.number': 5 }
        sort = [ { 'address.city': True } ]
        records, cursor = table.list(filter=filter, sort=sort)
    assert str(err).find('no matching index found') > -1

    # TODO test export

    # test remove
    table.remove()