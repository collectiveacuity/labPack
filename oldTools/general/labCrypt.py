__author__ = 'rcj1492'
__created__ = '2015'

# https://docs.python.org/2/library/hashlib.html
# https://docs.python.org/2/library/base64.html
# https://pypi.python.org/pypi/pysha3
# pip install pysha3
# pip install cryptography

import hashlib
import sha3
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import padding

# TODO:
# HMAC
# https://docs.python.org/3/library/hmac.html

# OAuth
# https://tools.ietf.org/html/draft-hammer-oauth-10#section-3.4.1

class labHex(object):
    def __init__(self, data):
        if isinstance(data, str):
            self.asBytes = binascii.unhexlify(data.encode())
            self.asString = data
        elif isinstance(data, labHex):
            self.asBytes = data.bytes
            self.asString = data.string
        elif isinstance(data, bytes):
            self.asString = binascii.hexlify(data).decode()
            self.asBytes = data
        else:
            raise Exception('Error, hex cannot handle ' + str(data.__class__) )
assert labHex('ab').asString == 'ab'
assert labHex(labHex('ab').asBytes).asString == 'ab'

class labHash:
    '''
        library of hashing methods
        dependencies:
        import hashlib
        import sha3 #pip install pysha3
    '''
    def MD5(string):
        '''
            get hex string from SHA3 256 hash of input
        :param string: any utf-8 string
        :return: hex string with length 64 characters
        '''
        if not isinstance(string, str):
            raise Exception('input is not a string')
        else:
            utf_bytes = string.encode('utf-8')
            hash_object = hashlib.md5(utf_bytes)
            hex_string = hash_object.hexdigest()
            return hex_string

    def SHA1(string):
        '''
            get hex string from SHA3 256 hash of input
        :param string: any utf-8 string
        :return: hex string with length 64 characters
        '''
        if not isinstance(string, str):
            raise Exception('input is not a string')
        else:
            utf_bytes = string.encode('utf-8')
            hash_object = hashlib.sha1(utf_bytes)
            hex_string = hash_object.hexdigest()
            return hex_string

    def SHA224(string):
        '''
            get hex string from SHA3 256 hash of input
        :param string: any utf-8 string
        :return: hex string with length 64 characters
        '''
        if not isinstance(string, str):
            raise Exception('input is not a string')
        else:
            utf_bytes = string.encode('utf-8')
            hash_object = hashlib.sha3_224(utf_bytes)
            hex_string = hash_object.hexdigest()
            return hex_string

    def SHA256(string):
        '''
            get hex string from SHA3 256 hash of input
        :param string: any utf-8 string
        :return: hex string with length 64 characters
        '''
        if not isinstance(string, str):
            raise Exception('input is not a string')
        else:
            utf_bytes = string.encode('utf-8')
            hash_object = hashlib.sha3_256(utf_bytes)
            hex_string = hash_object.hexdigest()
            return hex_string

    def SHA384(string):
        '''
            get hex string from SHA3 256 hash of input
        :param string: any utf-8 string
        :return: hex string with length 64 characters
        '''
        if not isinstance(string, str):
            raise Exception('input is not a string')
        else:
            utf_bytes = string.encode('utf-8')
            hash_object = hashlib.sha3_384(utf_bytes)
            hex_string = hash_object.hexdigest()
            return hex_string

    def SHA512(string):
        '''
            get hex string from SHA3 256 hash of input
        :param string: any utf-8 string
        :return: hex string with length 64 characters
        '''
        if not isinstance(string, str):
            raise Exception('input is not a string')
        else:
            utf_bytes = string.encode('utf-8')
            hash_object = hashlib.sha3_512(utf_bytes)
            hex_string = hash_object.hexdigest()
            return hex_string
assert len(labHash.MD5('hi')) == 32
assert len(labHash.SHA1('hi')) == 40
assert len(labHash.SHA224('hi')) == 56
assert len(labHash.SHA256('hi')) == 64
assert len(labHash.SHA384('hi')) == 96
assert len(labHash.SHA512('hi')) == 128
assert labHash.SHA512('hi').__class__ == str

class labCrypt:
    '''
        symmetric encryption methods from cryptography module
        https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
        dependencies
        import os
        import binascii
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        # from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.backends import openssl
        from cryptography.hazmat.primitives import padding
    '''
    def encrypt(string, password):
        '''
            uses cryptography module to encrypt utf-8 text string
            cipher: AES (128 bit block_size)
            key size: 256 bit
            padding: PKCS7
            cipher mode: CBC (16 bit random initialization vector)
            backend: openssl 1.0.2a
        :param string: utf-8 string
        :param password: utf-8 string
        :return: encrypted hexadecimal string
        '''
        if not string or not password:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str) or not isinstance(password, str):
            raise Exception('input is not the correct datatype')
        else:
            try:
                utf_bytes = string.encode('utf-8')
                pass_bytes = password.encode('utf-8')
                hash_object = hashlib.sha3_512(pass_bytes)
                hex_string = hash_object.hexdigest()
                hash_bytes = binascii.unhexlify(hex_string.encode())
                key = hash_bytes[0:32]
                iv = hash_bytes[32:48]
                # key = os.urandom(32)
                # iv = os.urandom(16)
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=openssl.backend)
                encryptor = cipher.encryptor()
                padder = padding.PKCS7(128).padder()
                padded_data = padder.update(utf_bytes)
                padded_data += padder.finalize()
                ct = encryptor.update(padded_data) + encryptor.finalize()
                hex_string = binascii.hexlify(ct).decode()
                return hex_string
            except:
                raise Exception('string is not utf-8 compatible')

    def decrypt(string, password):
        '''
            uses cryptography module to encrypt utf-8 text string
            cipher: AES (128 bit block_size)
            key size: 256 bit
            padding: PKCS7
            cipher mode: CBC (16 bit random initialization vector)
            backend: openssl (.05 sec) vs. default_backend (1.2 sec)
        :param string: encrypted hexadecimal string
        :param password: utf-8 string
        :return: decrypted utf-8 string
        '''
        if not string or not password:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str) or not isinstance(password, str):
            raise Exception('input is not the correct datatype')
        else:
            string = labHex(string).asString
            pass_bytes = password.encode('utf-8')
            hash_object = hashlib.sha3_512(pass_bytes)
            hex_string = hash_object.hexdigest()
            hash_bytes = binascii.unhexlify(hex_string.encode())
            key = hash_bytes[0:32]
            iv = hash_bytes[32:48]
            ct = binascii.unhexlify(string.encode())
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=openssl.backend)
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ct) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            utf_bytes = unpadder.update(padded_data) + unpadder.finalize()
            return utf_bytes.decode()
assert labCrypt.decrypt(labCrypt.encrypt('a secret message!', 'myPass'), 'myPass') == 'a secret message!'

print('SSL version installed is: ' + openssl.backend.openssl_version_text())





