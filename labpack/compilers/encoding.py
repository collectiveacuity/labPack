''' a package for encoding/decoding record data from ext type '''
__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

def encode_data(file_name, python_object, mimetype='', secret_key=''):

# parse extension type
    file_type = ''
    extension_map = {
        '.+\\.json$': 'json',
        '.+\\.json\\.gz$': 'json.gz',
        '.+\\.ya?ml$': 'yaml',
        '.+\\.ya?ml\\.gz$': 'yaml.gz',
        '.+\\.drep$': 'drep',
        '.+\\.md$': 'txt',
        '.+\\.txt$': 'txt'
    }
    import re
    for key, value in extension_map.items():
        file_pattern = re.compile(key)
        if file_pattern.findall(file_name):
            file_type = value
            break

# construct file data
    if file_type == 'json':
        import json
        byte_data = json.dumps(python_object, indent=2).encode('utf-8')
    elif file_type == 'yaml':
        import yaml
        byte_data = yaml.dump(python_object).encode('utf-8')
    elif file_type == 'json.gz':
        import json
        import gzip
        file_bytes = json.dumps(python_object).encode('utf-8')
        byte_data = gzip.compress(file_bytes)
    elif file_type == 'yaml.gz':
        import yaml
        import gzip
        file_bytes = yaml.dump(python_object).encode('utf-8')
        byte_data = gzip.compress(file_bytes)
    elif file_type == 'drep':
        from labpack.compilers import drep
        byte_data = drep.dump(python_object, secret_key)
    elif file_type == 'txt':
        byte_data = python_object.encode('utf-8')
    elif secret_key:
        from labpack.encryption import cryptolab
        byte_data, secret_key = cryptolab.encrypt(python_object, secret_key)
    else:
        if not isinstance(python_object, bytes):
            raise ValueError('%s file data must be byte data.' % file_name)
        byte_data = python_object
    
    return byte_data

def decode_data(file_name, byte_data, mimetype='', secret_key=''):
    
# parse extension type
    file_type = ''
    extension_map = {
        '.+\\.json$': 'json',
        '.+\\.json\\.gz$': 'json.gz',
        '.+\\.ya?ml$': 'yaml',
        '.+\\.ya?ml\\.gz$': 'yaml.gz',
        '.+\\.drep$': 'drep',
        '.+\\.md$': 'txt',
        '.+\\.txt$': 'txt'
    }
    import re
    for key, value in extension_map.items():
        file_pattern = re.compile(key)
        if file_pattern.findall(file_name):
            file_type = value
            break

# read byte data
    if not isinstance(byte_data, bytes):
        try:
            byte_data = byte_data.read()
        except:
            raise ValueError('%s must be byte data.' % file_name)
        
# decode based upon file type
    if file_type == 'json':
        import json
        try:
            python_object = json.loads(byte_data.decode())
        except:
            raise ValueError('%s is not valid json data.' % file_name)
    elif file_type == 'yaml':
        import yaml
        try:
            python_object = yaml.load(byte_data)
        except:
            raise ValueError('%s is not valid yaml data.' % file_name)
    elif file_type == 'json.gz':
        import gzip
        import json
        try:
            byte_data = gzip.decompress(byte_data)
        except:
            raise ValueError('%s is not valid gzip compressed data.' % file_name)
        try:
            python_object = json.loads(byte_data.decode())
        except:
            raise ValueError('%s is not valid json data.' % file_name)
    elif file_type == 'yaml.gz':
        import gzip
        import yaml
        try:
            byte_data = gzip.decompress(byte_data)
        except:
            raise ValueError('%s is not valid gzip compressed data.' % file_name)
        try:
            python_object = yaml.load(byte_data.decode())
        except:
            raise ValueError('%s is not valid yaml data.' % file_name)
    elif file_type == 'drep':
        from labpack.compilers import drep
        try:
            python_object = drep.load(encrypted_data=byte_data, secret_key=secret_key)
        except:
            raise ValueError('%s is not valid drep data.' % file_name)
    elif file_type == 'txt':
        try:
            python_object = byte_data.decode('utf-8')
        except:
            raise ValueError('%s is not valid text data.' % file_name)
    elif secret_key:
        from labpack.encryption import cryptolab
        python_object = cryptolab.decrypt(byte_data, secret_key)
    else:
        python_object = byte_data
        
    return python_object

if __name__ == '__main__':
    
    test_json = { 'key': [ 'item1', 'item2' ] }
    test_md = '#Markdown\n##Test\nDescription'
    secret_key = 'password'
    
    for name in ( 'test.json.gz', 'test.yaml.gz', 'test.yaml', 'test.json' ):
        print(name)
        test_data = encode_data(name, test_json)
        assert decode_data(name, test_data) == test_json
        
    for name in ('test.md', 'test.txt'):
        print(name)
        test_data = encode_data(name, test_md)
        assert decode_data(name, test_data) == test_md
    
    print('test.drep')
    test_data = encode_data('test.drep', test_json, secret_key=secret_key)
    assert decode_data('test.drep', test_data, secret_key=secret_key) == test_json
    
    print('encrypteddata')
    test_data = encode_data('encrypteddata', test_md.encode('utf-8'), secret_key=secret_key)
    assert decode_data('encrypteddata', test_data, secret_key=secret_key) == test_md.encode('utf-8')