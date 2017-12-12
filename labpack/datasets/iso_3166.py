''' a package of methods for compiling information about ISO 3166 country codes '''
__author__ = 'rcj1492'
__created__ = '2017.10'
__license__ = 'MIT'

# TODO scrape an online table to get latest csv values
def update_csv(csv_url=''):
    
    pass

def compile_list(csv_file='datasets/iso_3166.csv'):
    
    from os import path
    import csv
    from labpack import __module__
    from importlib.util import find_spec
    
# construct file path
    module_path = find_spec(__module__).submodule_search_locations[0]
    csv_path = path.join(module_path, csv_file)

# construct placeholder list
    rows = []
    
# retrieve model from file
    if not path.isfile(csv_path):
        raise Exception('%s is not a valid file path.' % csv_path)
    with open(csv_path, 'rt', errors='ignore') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            item = []
            for column in row:
                item.append(column)
            rows.append(item)
    
    return rows

def compile_map(key_column='Alpha-3 code', csv_list=None):

# determine csv list
    if not csv_list:
        csv_list = compile_list()

# validate inputs
    if not csv_list or not isinstance(csv_list, list):
        raise ValueError('csv_list argument must be a list generated from a csv table.')
    elif not isinstance(csv_list[0], list):
        raise ValueError('csv_list argument must be a list generated from a csv table.')
    elif not key_column in csv_list[0]:
        raise ValueError('key_column value "%s" is not a key in the csv table headers.' % key_column)
    
# determine index of key value
    key_index = csv_list[0].index(key_column)

# construct default map
    table_map = {}

# iterate over items in csv list
    for i in range(len(csv_list)):
        if i:
            row = csv_list[i]
            if row[key_index]:
                if not isinstance(row, list):
                    raise ValueError('csv_list argument must be a list generated from a csv table.')
                table_map[row[key_index]] = row
    
    return table_map

if __name__ == '__main__':
    
    code_map = compile_map()
    print(code_map.keys())