__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import yaml
from gzip import compress, decompress

try:
    from labpack import labCrypt
except:
    raise ImportError('\ndrep module requires cryptography module. try: pip install cryptography')

def dump(map_input, secret_key):

# validate input and convert to yaml data
    try:
        yaml_data = yaml.dump(map_input).encode('utf-8')
    except:
        raise TypeError('Map data input is not a valid yaml data structure.')

# compress data using gzip
    compressed_data = compress(yaml_data)

# encrypt data
    encrypted_data, secret_key = labCrypt.encrypt(compressed_data, secret_key)

    return encrypted_data

def load(encrypted_data, secret_key):

# attempt to decrypt data
    try:
        byte_data = labCrypt.decrypt(encrypted_data, secret_key)
    except:
        raise ValueError('\nsecret key is not valid key for drep file.')

# decompress data using gzip
    decompressed_data = decompress(byte_data)

# load map details from yaml data
    map_output = yaml.load(decompressed_data.decode())

    return map_output

if __name__ == '__main__':
    test_map = { 'drep': 'me' }
    test_secret = 'please work'
    encrypted_data = dump(test_map, test_secret)
    map_output = load(encrypted_data, test_secret)
    print(map_output)
