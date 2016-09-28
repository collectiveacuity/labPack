__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

try:
    import pytest
except:
    print('pytest module required to perform unittests. try: pip install pytest')
    exit()

from labpack.storage.appdata import appdataClient, appdataModel
from labpack.performance import labPerform
from jsonmodel.exceptions import InputValidationError
from copy import deepcopy

class testAppdataClient(appdataClient):

    def __init__(self):
        appdataClient.__init__(self, collection_name='Unit Tests')

    def unitTests(self):

        from time import time
        from copy import deepcopy
        testKey = 'lab/log/unittest'
        testDetails = { 'command': 'home', 'project': 'lab', 'verbose': True }
        seed_details = deepcopy(testDetails)
        seed_details['type'] = '.json'
        seed_details['time'] = time()
        seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
        self.create(key_string=seed_key, body_dict=seed_details)
        file_types = set(self.ext.__dir__()) - set(self.ext.builtins)
        for type in file_types:
            test_dt = time()
            file_type = type.replace('_','.')
            test_details = deepcopy(testDetails)
            test_details['type'] = file_type
            test_details['time'] = test_dt
            test_key = '%s/%s.%s' % (testKey, str(test_details['time']), file_type)
            secret_key = ''
            if type == 'drep':
                secret_key = 'test-key'
            self.create(key_string=test_key, body_dict=test_details, secret_key=secret_key)
            assert self.read(key_string=test_key, secret_key=secret_key)
            assert test_key in self.list(max_results=100, reverse_search=False)
            path_filters = [{0: {'must_contain': ['^lab']}, 2:{'discrete_values': ['unittest']}}]
            filter_function = self.conditionalFilter(path_filters=path_filters)
            assert test_key in self.list(filter_function=filter_function, max_results=100)
            assert self.delete(key_string=test_key)
        self.delete(key_string=seed_key)
        self.remove()

    # test filter method
        path_segments = ['lab', 'unittests', '1473719695.2165067', '.json']
        path_filters = [ { 0: { 'must_contain': [ '^lab' ] } } ]
        filter_function = self.conditionalFilter(path_filters=path_filters)
        assert filter_function(*path_segments)

    # test filter false results
        path_filters = [{0: {'must_not_contain': ['^lab']}}]
        filter_function = self.conditionalFilter(path_filters=path_filters)
        assert not filter_function(*path_segments)
        path_filters = [{0: {'must_contain': ['^lab']}, 1:{'excluded_values': ['unittests']} }]
        filter_function = self.conditionalFilter(path_filters=path_filters)
        assert not filter_function(*path_segments)
        path_filters = [{0: {'must_contain': ['^lab']}, 2: {'discrete_values': ['unittests']}}]
        filter_function = self.conditionalFilter(path_filters=path_filters)
        assert not filter_function(*path_segments)
        path_filters = [{4: {'must_contain': ['^lab']}}]
        filter_function = self.conditionalFilter(path_filters=path_filters)
        assert not filter_function(*path_segments)

    # test filter exceptions
        path_filters = [{ '0': {'must_contain': ['^lab']}}]
        with pytest.raises(TypeError):
            self.conditionalFilter(path_filters=path_filters)
        path_filters = [{ 0: 'string' }]
        with pytest.raises(TypeError):
            self.conditionalFilter(path_filters=path_filters)
        path_filters = [{ 0: {'must_contai': ['^lab']}}]
        with pytest.raises(InputValidationError):
            self.conditionalFilter(path_filters=path_filters)

        return self

    def performanceTests(self):

        from time import time, sleep
        from copy import deepcopy
        testKey = 'lab/log/performancetest'
        testDetails = {'command': 'home', 'project': 'lab', 'verbose': True}
        count = 0
        last_key = ''
        while count < 100:
            seed_details = deepcopy(testDetails)
            seed_details['type'] = '.json'
            seed_details['time'] = time()
            seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
            self.create(key_string=seed_key, body_dict=seed_details)
            count += 1
            sleep(.001)
            if count == 2:
                last_key = deepcopy(seed_key)
        path_filters = [{ 1:{'must_contain':['^log']}}]
        filter_function = self.conditionalFilter(path_filters=path_filters)
        labPerform.repeat(self.list(filter_function=filter_function, max_results=100, previous_key=last_key), 'appdataClient.list(filter_function=self.conditionalFilter(%s), max_results=100, previous_key=%s)' % (path_filters, last_key), 10000)
        self.remove()

        return self

class testAppdataModel(appdataModel):

    def __init__(self, record_schema=None, collection_settings=None, appdata_model=None):
        appdataModel.__init__(self, record_schema=record_schema, collection_settings=collection_settings, appdata_model=appdata_model)

    def unitTests(self):

    # instantiation assertions
        assert self.index
        assert isinstance(self.methods, appdataClient)
        assert not self.settings['enforce_schema']
        print(self.settings)
        print(test_record)

    # test new method
        new_record = self.new(**test_record)
        assert new_record.data
        new_record.settings['enforce_schema'] = True
        with pytest.raises(InputValidationError):
            new_record.new(**test_record)

    # test byte data in record
        new_record.settings['enforce_schema'] = False
        byte_record = deepcopy(test_record)
        import base64
        byte_data = b'\xb0mx\x0b\xec[\xc3a\xaf>Ce\x07\x08\xd1I\x8drs\x15\xedP\xc4\xef+-0^C^\x97\x17'
        byte_record['happy'] = base64.urlsafe_b64encode(byte_data).decode()
        new_record = self.new(**byte_record)
        print(new_record.data)
        import json
        t = json.dumps(new_record.data)

    # test extract value method
        new_record.settings['enforce_schema'] = False
        assert new_record._extract_value('.deviceID') == test_record['deviceID']
        assert new_record._extract_value('.metric') == 'null'

    # test extract value method with dictionary datatypes


        return self

if __name__ == '__main__':
    test_schema = { 'schema': {
        'dt': 1474505298.768161,
        'deviceID': 'ZeLPQ77bU3qnl5QI9ucwZyLK',
        'metric': 'temperature',
        'value': 34.5,
        'units': 'degrees Celsius'
    } }
    test_settings = {
        'enforce_schema': False,
        'index_fields': ['.deviceID', '.dt']
    }
    test_record = {
        'dt': 1474509314.419702,
        'deviceID': '2Pp8d9lpsappm8QPv_Ps6cL0'
    }
    testAppdataClient().unitTests()
    testAppdataClient().performanceTests()
    # test_kwargs = { 'record_schema': test_schema, 'collection_settings': test_settings }
    # test_appdata_model = testAppdataModel(**test_kwargs)
    # testAppdataModel(appdata_model=test_appdata_model).unitTests()
