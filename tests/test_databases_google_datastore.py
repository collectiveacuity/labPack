__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

import pytest
from copy import deepcopy
from labpack.databases.google.datastore import DatastoreTable
from labpack.records.id import labID

if __name__ == '__main__':

    lab = labID()
    record_schema = {
        'schema': {
            'id': 0.0,
            'token_id': '',
            'expires_at': 0.0,
            'service_scope': [ {} ],
            'active': False,
            'address': {
                'number': 0,
                'street': '',
                'city': '',
                'zip': ''
            },
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
    indices = ['address.city', 'address.number', 'places']
    details = {'token_id': 'unittest', 'places': ['here', 'there'], 'address': {'number': 3, 'city': 'motown'}}
    query_criteria = {
        'id': 'zZyl9ipT25Id0SfMyvcUUbQts9Br8ONlSjjw',
        '.places': {'value_exists': True},
        '.address.city': {'greater_than': 'mot'},
        'address.number': {'value_exists': False},
        '.address.street': {'less_than': 'cont'},
        '.token_id': {'discrete_values': ['unittest', 'lab', 'unittests']},
        '.places[0]': {'contains_either': ['there']}
    }

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
    with pytest.raises(Exception):
        error_indices = ['service_scope[0]']
        DatastoreTable(client, 'Not A Table', record_schema, indices=error_indices)

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
    
    # test create, read, update, delete and exists
    record_id = table.create(details)
    record = table.read(record_id)
    record['address']['city'] = 'middletown'
    table.update(record)
    updated = table.read(record_id)
    assert updated['address']['city'] == 'middletown'
    table.delete(record_id)
    assert not table.exists(record_id)

    # test list

    # TODO test export

    # # test remove
    # table.remove()