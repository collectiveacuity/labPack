__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

try:
    import pytest
except:
    print('pytest module required to perform unittests. try: pip install pytest')
    exit()

from labpack.storage.appdata import appdataClient
from labpack.performance import performlab
from jsonmodel.exceptions import InputValidationError

if __name__ == '__main__':
    
    from time import time, sleep
    from copy import deepcopy
    
# initialize client
    appdata_client = appdataClient(collection_name='Unit Tests')
    export_client = appdataClient(collection_name='Test Export')

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
    appdata_client.save(data_key, test_data, secret_key=secret_key)
    appdata_client.save(record_key, record_data)
    appdata_client.save(drep_key, drep_data)
    assert appdata_client.exists(drep_key)
    assert not appdata_client.exists('notakey')

# test export method
    exit_msg = appdata_client.export(export_client)
    exit_msg = appdata_client.export(export_client, overwrite=False)
    assert exit_msg.find('3')
    
# test list arguments
    path_segments = ['lab', 'unittests', '1473719695.2165067', '.json']
    path_filters = [ { 0: { 'must_contain': [ '^lab' ] } } ]
    filter_function = export_client.conditional_filter(path_filters=path_filters)
    assert filter_function(*path_segments)
    test_filter = appdata_client.conditional_filter([{2:{'must_contain':['unittest\.ogg$']}}])
    filter_search = appdata_client.list(filter_function=test_filter)
    prefix_search = export_client.list(prefix=record_key)
    assert prefix_search[0] == record_key
    delimiter_search = export_client.list(prefix='lab/device/', delimiter='.json')
    assert delimiter_search[0] == drep_key
    multi_filter = { 2: { 'must_contain': [ '.json$' ] } }
    multi_function = appdata_client.conditional_filter(multi_filter)
    multi_search = appdata_client.list(prefix='lab/device/', filter_function=multi_function)
    assert multi_search[0] == prefix_search[0]

# test load argument
    new_data = appdata_client.load(filter_search[0], secret_key=secret_key)
    new_hash = md5(new_data).digest()
    assert old_hash == new_hash
    load_data = export_client.load(prefix_search[0])
    record_details = json.loads(load_data.decode())
    assert record_details == test_record

# test filter false results
    path_filters = [{0: {'must_not_contain': ['^lab']}}]
    filter_function = export_client.conditional_filter(path_filters=path_filters)
    assert not filter_function(*path_segments)
    path_filters = [{0: {'must_contain': ['^lab']}, 1:{'excluded_values': ['unittests']} }]
    filter_function = export_client.conditional_filter(path_filters=path_filters)
    assert not filter_function(*path_segments)
    path_filters = [{0: {'must_contain': ['^lab']}, 2: {'discrete_values': ['unittests']}}]
    filter_function = export_client.conditional_filter(path_filters=path_filters)
    assert not filter_function(*path_segments)
    path_filters = [{4: {'must_contain': ['^lab']}}]
    filter_function = export_client.conditional_filter(path_filters=path_filters)
    assert not filter_function(*path_segments)

# test filter exceptions
    path_filters = [{ '0': {'must_contain': ['^lab']}}]
    with pytest.raises(TypeError):
        export_client.conditional_filter(path_filters=path_filters)
    path_filters = [{ 0: 'string' }]
    with pytest.raises(TypeError):
        export_client.conditional_filter(path_filters=path_filters)
    path_filters = [{ 0: {'must_contai': ['^lab']}}]
    with pytest.raises(InputValidationError):
        export_client.conditional_filter(path_filters=path_filters)
    
# test delete method
    assert appdata_client.delete(filter_search[0])

# test list performance
    testKey = 'lab/log/performancetest'
    testDetails = {'command': 'home', 'project': 'lab', 'verbose': True}
    count = 0
    last_key = ''
    while count < 100:
        seed_details = deepcopy(testDetails)
        seed_data = json.dumps(seed_details).encode('utf-8')
        seed_details['type'] = '.json'
        seed_details['time'] = time()
        seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
        appdata_client.save(record_key=seed_key, record_data=seed_data)
        count += 1
        sleep(.001)
        if count == 2:
            last_key = deepcopy(seed_key)
    path_filters = [{ 1:{'must_contain':['^log']}}]
    filter_function = appdata_client.conditional_filter(path_filters=path_filters)
    filter_kwargs = {
        'filter_function': filter_function, 
        'max_results': 100, 
        'previous_key': last_key
    }
    prefix_kwargs = {
        'prefix': 'lab/log/performancetest',
        'max_results': 100,
        'previous_key': last_key
    }
    performlab.repeat(appdata_client.list, filter_kwargs, 'appdataClient.list(filter_function=self.conditional_filter(%s), max_results=100, previous_key=%s)' % (path_filters, last_key), 1000)
    performlab.repeat(appdata_client.list, prefix_kwargs, 'appdataClient.list(prefix="%s", max_results=100, previous_key=%s' % (prefix_kwargs['prefix'], last_key), 1000)
        
# remove client
    appdata_client.remove()
    export_client.remove()
