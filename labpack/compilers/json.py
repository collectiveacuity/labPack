''' a package of methods to merge two or more json documents preserving order & comments '''
__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

import json as json_lib

from collections import OrderedDict

def walk_data(target, source):

    ''' method to recursively walk parse tree and extend target '''

    from copy import deepcopy

    # skip if target and source are different datatypes
    if target.__class__.__name__ != source.__class__.__name__:
        pass
    # handle maps
    elif isinstance(target, dict):
        count = 0
        target = OrderedDict(target)
        for k, v in source.items():
            # insert fields not found in target
            if k not in target.keys():
                target[k] = v
                for ii, key in enumerate(list(target.keys())):
                    if ii >= count and key != k:
                        target.move_to_end(key)
            # else walk down maps and sequences
            elif isinstance(v, list) or isinstance(v, dict):
                target[k] = walk_data(target[k], v)
            count += 1
    # handle sequences
    elif isinstance(target, list):
        # walk down maps and sequences
        for i in range(len(target)):
            item = target[i]
            source_copy = deepcopy(source[0])
            if isinstance(item, dict) or isinstance(item, list):
                if source:
                    target[i] = walk_data(item, source_copy)

    return target
    
def extend_json(*sources, output=''):

    '''
        method for merging two or more json files

    this method walks the parse tree of json data to extend the fields
    found in subsequent sources into the data structure of the initial source. 
    any number of sources can be added to the source args, but only new fields
    from subsequent sources will be added. to overwrite values instead, it 
    suffices to simply reverse the order of the sources

    PLEASE NOTE:    since there is no way to uniquely identify list items between
                    two json documents, items are not added to existing lists.

    PLEASE NOTE:    however, lists are transversed in order to evaluate keys of 
                    nested dictionaries using the first item of any subsequent list
                    as a model for the scope

    :param sources: variable-length argument list of strings with json text
    :param output: [optional] string with path to save the combined json data to file
    :return: OrderedDict or list with merged data
    '''

    # import libraries
    from copy import deepcopy

    # define variables
    combined = None

    # open and combine sources
    src = [open(json_path).read() for json_path in sources]
    for text in src:
        data = json_lib.loads(text)
        if not isinstance(data, list) and not isinstance(data, dict):
            raise ValueError('Source documents must be either lists or dictionaries.')
        if not combined:
            combined = deepcopy(data)
        elif combined.__class__.__name__ != data.__class__.__name__:
            pass
            # raise ValueError('Source documents must be the same top-level datatype or use rule="overwrite"')
        else:
            combined = walk_data(combined, data)

    # save file and return combined data
    if output:
        with open(output, 'w') as f:
            f.write(json_lib.dumps(combined, indent=2))

    return combined
