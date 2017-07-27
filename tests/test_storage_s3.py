__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

from labpack.storage.aws.s3 import _s3Client, s3Client

if __name__ == '__main__':
    
# test instantiation
    from pprint import pprint
    from labpack.records.settings import load_settings
    aws_cred = load_settings('../../cred/awsLab.yaml')
    _client_kwargs = {
        'access_id': aws_cred['aws_access_key_id'],
        'secret_key': aws_cred['aws_secret_access_key'],
        'region_name': aws_cred['aws_default_region'],
        'owner_id': aws_cred['aws_owner_id'],
        'user_name': aws_cred['aws_user_name']
    }
    _s3_client = _s3Client(**_client_kwargs)

# test list bucket and verify unittesting is clean
    bucket_list = _s3_client.list_buckets()
    bucket_name = 'collective-acuity-labpack-unittest-main'
    log_name = 'collective-acuity-labpack-unittest-log'
    assert bucket_name not in bucket_list
    assert log_name not in bucket_list
    for bucket in (bucket_name, log_name):
        _s3_client.delete_bucket(bucket)

# test create buckets
    simple_kwargs = { 'bucket_name': bucket_name }
    log_kwargs = {
        'bucket_name': log_name,
        'access_control': 'log-delivery-write'
    }
    main_kwargs = {
        'bucket_name': bucket_name,
        'version_control': True,
        'tag_list': [ 
            { 'key': 'Env', 'value': 'test' }, 
            { 'key': 'BuildDate', 'value': 'now' },
            { 'key': 'Chance', 'value': 'go' },
            { 'key': 'Date', 'value': 'then' },
            { 'key': 'First', 'value': '1' },
            { 'key': 'Second', 'value': '2' }
        ],
        'lifecycle_rules': [ { 
            "action": "archive",
            "prefix": "test/",
            "longevity": 180,
            "current_version": True 
        } ],
        'log_destination': {
            'name': log_name,
            'prefix': 'test/'
        }
    }
    _s3_client.create_bucket(**simple_kwargs)
    _s3_client.create_bucket(**log_kwargs)

# test update bucket
    _s3_client.update_bucket(**main_kwargs)
    bucket_details = _s3_client.read_bucket(bucket_name)
    assert bucket_details['version_control']

# test create record
    import json
    from time import time
    secret_key = 'testpassword'
    record_key = 'unittest/%s.json' % str(time())
    record_data = json.dumps(main_kwargs).encode('utf-8')
    record_mimetype = 'application/json'
    _s3_client.create_record(bucket_name, record_key, record_data, record_mimetype=record_mimetype)

# test update record
    main_kwargs['additional_key'] = True
    record_data = json.dumps(main_kwargs).encode('utf-8')
    _s3_client.create_record(bucket_name, record_key, record_data, record_mimetype=record_mimetype)

# test list records and versions
    log_list, log_key = _s3_client.list_records(log_name)
    record_list, next_key = _s3_client.list_versions(bucket_name)
    record_version = record_list[1]['version_id']

# test read headers and read record
    header_details = _s3_client.read_headers(bucket_name, record_key)
    assert not _s3_client.read_headers(bucket_name, 'notakey')
    data, headers = _s3_client.read_record(bucket_name, record_key, record_version)
    assert header_details['content_type'] == headers['content_type']
    assert header_details['current_version']
    record_details = json.loads(data.decode())
    assert record_details['bucket_name'] == bucket_name

# test delete record
    for record in record_list:
        delete_output = _s3_client.delete_record(bucket_name, record['key'])
        print('record version %s deleted.' % delete_output['version_id'])

# test import and export
    from os import listdir
    test_dir = './tests/testing'
    dir_size = len(listdir(test_dir))
    _s3_client.import_records(bucket_name, test_dir)
    _s3_client.import_records(bucket_name, test_dir, overwrite=False)
    _s3_client.export_records(bucket_name, test_dir, overwrite=False)
    _s3_client.export_records(bucket_name, test_dir)
    assert len(listdir(test_dir)) == dir_size

# remove test buckets
    for bucket in (bucket_name, log_name):
        _s3_client.delete_bucket(bucket)    

# create collection
    client_kwargs = {
        'collection_name': 'Unittest Main'
    }
    client_kwargs.update(**_client_kwargs)
    s3_client = s3Client(**client_kwargs)

# test save record
    import json
    secret_key = 'password'
    record_key = 'testing/lab/test.json'
    record_data = json.dumps(main_kwargs).encode('utf-8')
    s3_client.save(record_key, record_data, secret_key=secret_key)
    assert s3_client.exists(record_key)

# test list record
    record_list = s3_client.list(prefix='testing/', delimiter='.yaml')
    record_filter = { 2: {'must_contain': ['json$']}}
    filter_function = s3_client.conditional_filter(record_filter)
    filter_list = s3_client.list(prefix='testing/', filter_function=filter_function)
    assert record_list[0] == filter_list[0]

# test load record
    record_load = s3_client.load(record_key, secret_key=secret_key)
    record_details = json.loads(record_load.decode())
    assert record_details == main_kwargs

# test export collection
    from labpack.storage.appdata import appdataClient
    appdata_client = appdataClient(collection_name='Unittest Local')
    print(s3_client.export(appdata_client))
    export_data = appdata_client.load(record_key, secret_key)
    assert json.loads(export_data.decode()) == main_kwargs
    print(appdata_client.export(s3_client, overwrite=False))
    export_list = appdata_client.list()
    print(export_list)
    appdata_client.remove()

# test delete record
    print(s3_client.delete(record_key))

# remove collection
    s3_client.remove()

