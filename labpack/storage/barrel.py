__author__ = 'rcj1492'
__created__ = '2016.09'
__license__ = 'MIT'

import os
import sys
import pickle

def store_values(file_path, data):
    pickle_barrel = open(file_path, 'wb')
    pickle.dump(data, pickle_barrel)
    pickle_barrel.close()

def retrieve_values(file_path):
    if os.path.exists(file_path):
        pickle_barrel = open(file_path, 'rb')
        try:
            data = pickle.load(pickle_barrel)
        except:
            print('%s is not a pickle barrel.' % file_path)
            sys.exit(2)
        pickle_barrel.close()
    else:
        data = 'empty barrel'
        store_values(file_path, data)
    return data

def main(args):
    pickle_location = 'data.pkl'
    old_data = retrieve_values(pickle_location)
    if isinstance(old_data, list):
        for arg in map(print, old_data):
            assert arg == None
    else:
        print('Nothing in this barrel.')
    store_values(pickle_location, args)

if __name__ == '__main__':
    main(sys.argv[1:])