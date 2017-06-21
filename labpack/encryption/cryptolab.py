__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

'''
PLEASE NOTE:    cryptolab package requires both the cryptography and pycrypto modules.
                pycrypto requires a number of C libraries to install.

(alpine)        apk add gcc
                apk add g++
                apk add make
                apk add libffi-dev
                apk add openssl-dev
                apk add python3-dev build-base --update-cache
                pip3 install pycrypto

(debian)        apt-get --fix-missing install -y python
                apt-get install -y build-essential
                apt-get install -y libssl-dev
                apt-get install -y libffi-dev
                apt-get install -y python-dev
                apt-get install -y python3-pip
                pip3 install cryptography
'''

import hashlib
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import openssl
    from cryptography.hazmat.primitives import padding
except:
    print('\ncryptolab requires the cryptography module. try: pip install cryptography')
    exit()

def encrypt(byte_data, secret_key=''):

    '''
        uses cryptography module to encrypt byte data
        cipher: AES (128 bit block_size)
        hash: sha512
        key size: 256 bit (first 32 bytes of secret key hash)
        vector size: 128 bit (next 16 bytes of secret key hash)
        padding: PKCS7
        cipher mode: CBC
        backend: openssl 1.0.2a

        NOTE:   if secret_key is left blank,
                method generates a 32 byte hexadecimal string

    :param byte_data: bytes with data to encrypt
    :param secret_key: [optional] string used to encrypt data
    :return: encrypted byte data, secret key hex string
    '''

# validate input
    if not isinstance(byte_data, bytes):
        raise TypeError('\nbyte data input must be a byte datatype.')

# validate secret key or create secret key
    if secret_key:
        if not isinstance(secret_key, str):
            raise TypeError('\nsecret key input must be a utf-8 encoded string.')
    else:
        from os import urandom
        from binascii import hexlify
        secret_key = hexlify(urandom(32)).decode()

# retrieve cipher key and initialization vector from sha256 hash of secret key
    key_bytes = hashlib.sha512(secret_key.encode('utf-8')).digest()
    cipher_key = key_bytes[0:32]
    cipher_vector = key_bytes[32:48]

# construct encryptor
    cipher_kwargs = {
        'algorithm': algorithms.AES(cipher_key),
        'mode': modes.CBC(cipher_vector),
        'backend': openssl.backend
    }
    cipher = Cipher(**cipher_kwargs)
    encryptor = cipher.encryptor()

# encrypt and add padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(byte_data)
    padded_data += padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_data, secret_key

def decrypt(encrypted_data, secret_key):

    '''
        uses cryptography module to decrypt byte data
        cipher: AES (128 bit block_size)
        hash: sha512
        key size: 256 bit (first 32 bytes of secret key hash)
        vector size: 128 bit (next 16 bytes of secret key hash)
        padding: PKCS7
        cipher mode: CBC
        backend: openssl 1.0.2a
    :param encrypted_data: bytes with data to decrypt
    :param secret_key: [optional] string used to decrypt data
    :return: encrypted byte data, secret key hex string
    '''

# validate input
    if not isinstance(encrypted_data, bytes):
        raise TypeError('\nbyte data input must be byte datatype.')
    elif not isinstance(secret_key, str):
        raise TypeError('\nsecret key input must be a utf-8 encoded string.')

# retrieve cipher key and initialization vector from sha256 hash of secret key
    key_bytes = hashlib.sha512(secret_key.encode('utf-8')).digest()
    cipher_key = key_bytes[0:32]
    cipher_vector = key_bytes[32:48]

# construct decryptor
    cipher_kwargs = {
        'algorithm': algorithms.AES(cipher_key),
        'mode': modes.CBC(cipher_vector),
        'backend': openssl.backend
    }
    cipher = Cipher(**cipher_kwargs)
    decryptor = cipher.decryptor()

# decrypt and remove padding
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    byte_data = unpadder.update(padded_data) + unpadder.finalize()

    return byte_data

if __name__ == '__main__':
    import json
    test_details = { 'cryptolab': 'me' }
    test_data = json.dumps(test_details).encode('utf-8')
    encrypted_data, secret_key = encrypt(test_data)
    decrypted_data = decrypt(encrypted_data, secret_key)
    decrypted_details = json.loads(decrypted_data.decode())
    assert decrypted_details['cryptolab'] == test_details['cryptolab']
    print(decrypted_details)
