__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import json
from gzip import compress, decompress

try:
    from labpack.encryption import cryptolab
except:
    print('\ndrep methods require the cryptography module. try: pip install cryptography')
    exit()

def dump(json_input, secret_key):

# validate input and convert to json data
    try:
        json_data = json.dumps(json_input).encode('utf-8')
    except:
        raise TypeError('Map data input is not a valid json data structure.')

# compress data using gzip
    compressed_data = compress(json_data)

# encrypt data
    encrypted_data, secret_key = cryptolab.encrypt(compressed_data, secret_key)

    return encrypted_data

def load(encrypted_data, secret_key):

# attempt to decrypt data
    try:
        byte_data = cryptolab.decrypt(encrypted_data, secret_key)
    except:
        raise ValueError('\nsecret key is not valid key for drep file.')

# decompress data using gzip
    decompressed_data = decompress(byte_data)

# load map details from json data
    map_output = json.loads(decompressed_data.decode())

    return map_output

if __name__ == '__main__':
    test_map = { 'drep': 'me' }
    test_secret = 'please work'
    encrypted_data = dump(test_map, test_secret)
    map_output = load(encrypted_data, test_secret)
    print(map_output)
