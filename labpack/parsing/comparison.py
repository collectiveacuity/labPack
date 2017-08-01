''' a package of methods to generate the differences between two data architectures '''
__author__ = 'rcj1492'
__created__ = '2015.08'
__license__ = 'MIT'

def compare_records(new_record, old_record):

    '''
        a method to generate the differences between two data architectures
        
    :param new_record: set, list or dictionary with new details of an item
    :param old_record: set, list or dictionary with old details of an item
    :return: list with dictionary of changes between old and new records
    
    [ { 
        'path': [ 'dict2', 'dict', 'list2', 4, 'key' ],
        'action': 'UPDATE',
        'value': 'newValue'
    } ]
    '''

    if new_record.__class__ != old_record.__class__:
        raise TypeError('Datatype of new and old data must match.')
    from copy import deepcopy
    new_map = deepcopy(new_record)
    old_map = deepcopy(old_record)
    if isinstance(new_map, dict):
        return _compare_dict(new_map, old_map, [], [])
    elif isinstance(new_map, list):
        return _compare_list(new_map, old_map, [], [])
    elif isinstance(new_map, set):
        return _compare_set(new_map, old_map, [], [])
    else:
        raise TypeError('Records must be either sets, lists or dictionaries.')

def _compare_dict(new_dict, old_dict, change_list=None, root=None):

    '''
        a method for recursively listing changes made to a dictionary

    :param new_dict: dictionary with new key-value pairs
    :param old_dict: dictionary with old key-value pairs
    :param change_list: list of differences between old and new
    :patam root: string with record of path to the root of the main object
    :return: list of differences between old and new
    '''

    from copy import deepcopy
    
    new_keys = set(new_dict.keys())
    old_keys = set(old_dict.keys())
    missing_keys = old_keys - new_keys
    extra_keys = new_keys - old_keys
    same_keys = new_keys.intersection(old_keys)
    for key in missing_keys:
        new_path = deepcopy(root)
        new_path.append(key)
        change_list.append({'action': 'DELETE', 'value': None, 'path': new_path})
    for key in extra_keys:
        for k, v in new_dict.items():
            if key == k:
                new_path = deepcopy(root)
                new_path.append(key)
                change_list.append({'action': 'ADD', 'value': v, 'path': new_path})
    for key in same_keys:
        new_path = deepcopy(root)
        new_path.append(key)
        if new_dict[key].__class__ != old_dict[key].__class__:
            change_list.append({'action': 'UPDATE', 'value': new_dict[key], 'path': new_path})
        elif isinstance(new_dict[key], dict):
            _compare_dict(new_dict[key], old_dict[key], change_list, new_path)
        elif isinstance(new_dict[key], list):
            _compare_list(new_dict[key], old_dict[key], change_list, new_path)
        elif isinstance(new_dict[key], set):
            _compare_set(new_dict[key], old_dict[key], change_list, new_path)
        elif new_dict[key] != old_dict[key]:
            change_list.append({'action': 'UPDATE', 'value': new_dict[key], 'path': new_path})
    return change_list

def _compare_list(new_list, old_list, change_list=None, root=None):

    '''
        a method for recursively listing changes made to a list

    :param new_list: list with new value
    :param old_list: list with old values
    :param change_list: list of differences between old and new
    :param root: string with record of path to the root of the main object
    :return: list of differences between old and new
    '''

    from copy import deepcopy
    if len(old_list) > len(new_list):
        same_len = len(new_list)
        for i in reversed(range(len(new_list), len(old_list))):
            new_path = deepcopy(root)
            new_path.append(i)
            change_list.append({'action': 'REMOVE', 'value': None, 'path': new_path})
    elif len(new_list) > len(old_list):
        same_len = len(old_list)
        append_list = []
        path = deepcopy(root)
        for i in range(len(old_list), len(new_list)):
            append_list.append(new_list[i])
        change_list.append({'action': 'APPEND', 'value': append_list, 'path': path})
    else:
        same_len = len(new_list)
    for i in range(0, same_len):
        new_path = deepcopy(root)
        new_path.append(i)
        if new_list[i].__class__ != old_list[i].__class__:
            change_list.append({'action': 'UPDATE', 'value': new_list[i], 'path': new_path})
        elif isinstance(new_list[i], dict):
            _compare_dict(new_list[i], old_list[i], change_list, new_path)
        elif isinstance(new_list[i], list):
            _compare_list(new_list[i], old_list[i], change_list, new_path)
        elif isinstance(new_list[i], set):
            _compare_set(new_list[i], old_list[i], change_list, new_path)
        elif new_list[i] != old_list[i]:
            change_list.append({'action': 'UPDATE', 'value': new_list[i], 'path': new_path})
    return change_list

def _compare_set(new_set, old_set, change_list, root):

    '''
        a method for list changes made to a set

    :param new_set: set with new values
    :param old_set: set with old values
    :param change_list: list of differences between old and new
    :patam root: string with record of path to the root of the main object
    :return: list of differences between old and new
    '''

    from copy import deepcopy
    path = deepcopy(root)
    missing_items = old_set - new_set
    extra_items = new_set - old_set
    for item in missing_items:
        change_list.append({'action': 'REMOVE', 'key': None, 'value': item, 'path': path})
    for item in extra_items:
        change_list.append({'action': 'ADD', 'key': None, 'value': item, 'path': path})
    return change_list

if __name__ == '__main__':
    newRecord = {
        'active': True,
        'id': 'd53iedBwKNcFCJXLEAWHCfCT3zGLCu93rxTG',
        'dT': 1440184621.607344,
        'score': 400,
        'dict1': { 'key': 'value' },
        'list1': [ 'item' ],
        'dict2': {
            'key1': 'string',
            'key2': 2.2,
            'key3': 2,
            'key4': True,
            'dict': {
                'key': 'value',
                'list1': [ 'item' ],
                'list2': [ 'item', 2, 2.2, True, { 'key': 'newValue' } ]
            } },
        'list2': [ 'item', 2, 2.2, True, { 'key': 'value', 'list': [ 2, 2.2, True, 'item' ] } ]
    }
    oldRecord = {
        'active': True,
        'id': 'd53iedBwKNcFCJXLEAWHCfCT3zGLCu93rxTG',
        'dT': 1440184621.607344,
        'score': 400,
        'dict1': { 'key': 'value' },
        'list1': [ 'item' ],
        'dict2': {
            'key1': 'string',
            'key2': 2.2,
            'key3': 2,
            'key4': True,
            'dict': {
                'key': 'value',
                'list1': [ 'item' ],
                'list2': [ 'item', 2, 2.2, True, { 'key': 'oldValue' } ]
            } },
        'list2': [ 'item', 2, 2.2, True, { 'key': 'value', 'list': [ 2, 2.2, True, 'item' ] } ]
    }
    test_comparison = _compare_dict(newRecord, oldRecord, [], [])
    assert test_comparison[0]['path'][4] == 'key'
    print(test_comparison)
    test_comparison = compare_records(newRecord, oldRecord)
    print(test_comparison)