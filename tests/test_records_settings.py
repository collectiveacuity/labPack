__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

from labpack.records.settings import *

if __name__ == '__main__':

# define arguments
    import os
    os.environ['labpack_records_settings'] = '2'
    model_path = 'test-model.json'
    file_path = 'test-settings.yaml'

# test ingest environ
    assert ingest_environ()['LABPACK_RECORDS_SETTINGS'] == 2
    model_env = ingest_environ(model_path)
    assert model_env['labpack_records_settings'] == 2

# test load settings from module path
    assert load_settings(file_path='model-rules.json', module_name='jsonmodel')

# test save settings
    test_details = load_settings(model_path)
    try:
        import pytest
    except:
        print('pytest module required to perform unittests. try: pip install pytest')
        exit()
    with pytest.raises(Exception):
        save_settings(test_details, model_path)
    assert save_settings(test_details, model_path, overwrite=True)

# test compile settings
    from jsonmodel.exceptions import InputValidationError
    with pytest.raises(InputValidationError): # exception for not a string
        test_details = compile_settings(model_path, file_path)
    test_details = compile_settings(model_path, file_path, ignore_errors=True)
    assert not test_details['labpack_records_details'] # empty value
    assert test_details['labpack_records_settings'] == 2 # environment variable
    assert test_details['labpack_records_creds'] == 'sunlight' # default value
    assert test_details['labpack_records_configs'] == 'days' # cred file