__author__ = 'rcj1492'
__created__ = '2017.08'
__license__ = 'MIT'

import pytest
from labpack.databases.sql import sqlClient

if __name__ == '__main__':

# construct client
    from copy import deepcopy
    record_schema = {
      'schema': {
        'token_id': '',
        'expires_at': 0.0,
        'service_scope': [''],
        'active': False,
        'address': {
          'number': 0,
          'street': '',
          'city': '',
          'zip': ''
        },
        'places': ['']
      },
      'components': {
        '.address': {
          'required_field': False
        },
        '.address.number': {
          'integer_data': True
        },
        '.places': {
          'required_field': False
        },
        '.service_scope': {
          'required_field': False
        }
      }
    }
    sql_kwargs = {
        'table_name': 'tokens',
        'database_url': 'sqlite:///../data/records.db',
        'record_schema': record_schema
    }
    sql_client = sqlClient(**sql_kwargs)

# test create
    record_details = { 'token_id': 'unittest', 'places': ['here', 'there'], 'address': {'number': 3, 'city': 'motown' } }
    record_id = sql_client.create(record_details)

# test read
    generated_details = sql_client.read(record_id)
    anonymous_details = deepcopy(generated_details)
    del anonymous_details['id']
    assert anonymous_details == record_details

# test update
    new_details = deepcopy(generated_details)
    new_details['address']['street'] = 'construction road'
    new_details['places'].append('everywhere')
    del new_details['address']['number']
    update_list = sql_client.update(new_details, generated_details)
    updated_details = sql_client.read(record_id)
    assert len(updated_details['places']) == 3
    assert updated_details['address']['street']

# test list
    query_criteria = {
        '.id':{ 'equal_to': 'zZyl9ipT25Id0SfMyvcUUbQts9Br8ONlSjjw' }, 
        '.places': { 'value_exists': True }, 
        '.address.city': { 'greater_than': 'mot' },
        '.address.number': { 'value_exists': False },
        '.address.street': { 'less_than': 'cont' },
        '.token_id': { 'discrete_values': [ 'unittest', 'lab', 'unittests']},
        '.places[0]': { 'contains_either': [ 'there'] }
    }
    for record in sql_client.list(query_criteria):
        print(record)

# test descending order by
    order_criteria = [
        { '.id': 'descend' }
    ]
    for record in sql_client.list(order_criteria=order_criteria):
        print(record)
        break

# test migration of database
    migration_kwargs = {
        'table_name': 'migrated_tokens',
        'database_url': 'sqlite:///../data/migrated-records.db',
        'record_schema': record_schema
    }
    migration_client = sqlClient(**migration_kwargs)
    sql_client.export(migration_client)
    for record in migration_client.list(order_criteria=order_criteria):
        print(record)
        break

# remove migration database
    exit_msg = migration_client.remove()
    print(exit_msg)

# test delete and exists
    exit_msg = sql_client.delete(record_id)
    print(exit_msg)
    assert not sql_client.exists(record_id)

# remove table from database
    # exit_msg = sql_client.remove()
    # print(exit_msg)