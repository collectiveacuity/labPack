__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

import pytest
from labpack.databases.google.datastore import DatastoreTable
from labpack.records.id import labID

if __name__ == '__main__':

    lab = labID()
    record_schema = {
        'schema': {
            'id': 0.0,
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
    indices = ['address.city']
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
    client = DatastoreClient.from_service_account_json(google_cred)

    # instantiate table
    accounts = DatastoreTable(client, 'test_record', record_schema, page_size=2, verbose=True)
    assert 'places' in accounts.excluded_indices
    print(accounts._prepare_record(details))
    # record_id = accounts.create(details)
    record_id = 5632499082330112
    record = accounts.read(record_id)
    print(record)
    # accounts.model.validate(record)