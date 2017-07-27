__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

from labpack.storage.google.drive import driveClient

if __name__ == '__main__':
    
# initialize client
    import pytest
    from pprint import pprint
    from labpack.records.settings import load_settings
    google_tokens = load_settings('../../cred/tokens/google-drive.yaml')
    access_token = google_tokens['google_drive_access_token']
    drive_client = driveClient(access_token, 'Unit Test')

# prevent accidental use
    assert drive_client.drive_space == 'appDataFolder'
    count = 0
    for id, name, mimetype in drive_client._list_directory():
        count += 1
        break
    assert not count

# construct test records
    import json
    from hashlib import md5
    from labpack.compilers import drep
    secret_key = 'upside'
    test_record = {
        'dt': 1474509314.419702,
        'deviceID': '2Pp8d9lpsappm8QPv_Ps6cL0'
    }
    test_data = open('../data/test_voice.ogg', 'rb').read()
    data_key = 'lab/voice/unittest.ogg'
    record_data = json.dumps(test_record).encode('utf-8')
    record_key = 'lab/device/unittest.json'
    drep_data = drep.dump(test_record, secret_key)
    drep_key = 'lab/device/unittest.drep'

# test save method
    old_hash = md5(test_data).digest()
    drive_client.save(data_key, test_data, secret_key=secret_key)
    drive_client.save(record_key, record_data)
    drive_client.save(drep_key, drep_data)
    assert drive_client.exists(drep_key)
    assert not drive_client.exists('notakey')

# test list with different filters
    data_filter = { 2:{'must_contain': ['ogg$']}}
    filter_function = drive_client.conditional_filter(data_filter)
    data_search = drive_client.list(filter_function=filter_function, max_results=3)
    prefix_search = drive_client.list(prefix='lab/dev', delimiter='drep', max_results=3)
    print(prefix_search)

# test import and export method
    try:
        from labpack.storage.appdata import appdataClient
        export_client = appdataClient(collection_name='Test Export')
        drive_client.export(export_client)
        export_status = drive_client.export(export_client, overwrite=False)
        print(export_status)
        export_list = export_client.list(filter_function=filter_function, max_results=3)
        print(export_list)
        import_status = export_client.export(drive_client)
        print(import_status)
        export_client.remove()
    except Exception as err:
        print(err)

# test load method
    new_data = drive_client.load(data_search[0], secret_key=secret_key)
    new_hash = md5(new_data).digest()
    assert old_hash == new_hash
    load_data = drive_client.load(prefix_search[0])
    record_details = json.loads(load_data.decode())
    assert record_details == test_record
    with pytest.raises(Exception):
        drive_client.load('notakey')

# test delete
    delete_status = drive_client.delete(data_key)

# test removal
    remove_status = drive_client.remove()
    print(remove_status)