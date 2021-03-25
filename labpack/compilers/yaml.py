''' a package of methods to merge two or more yaml files preserving order & comments '''
__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

'''
PLEASE NOTE:    yaml package requires the ruamel.yaml module.

(all platforms) pip3 install ruamel.yaml
'''

try:
    from ruamel.yaml import YAML
except:
    import sys
    print('yaml package requires the ruamel.yaml module. try: pip3 install ruamel.yaml')
    sys.exit(1)

def merge_maps(target, source, overwrite, prune):
    return target

def merge_seqs(target, source, overwrite, prune):
    return target

def merge_yaml(*sources, target='', overwrite=False, prune=False):

    # import libraries
    from copy import deepcopy
    from ruamel.yaml.util import load_yaml_guess_indent
    from ruamel.yaml.comments import CommentedMap, CommentedSeq
    yml = YAML(typ='rt')
    # yaml.default_flow_style = False

    # define variables
    combined = None
    indent = 2
    seq_indent = 0

    # open and combine sources
    for yaml_path in sources:
        text = open(yaml_path).read()
        result, indent, seq_indent = load_yaml_guess_indent(text)
        code = yml.load(text)
        if not isinstance(code, CommentedMap) and not isinstance(code, CommentedSeq):
            raise ValueError('Source files must be either lists or dictionaries.')
        if not combined:
            combined = deepcopy(code)
        elif combined.__class__.__name__ != code.__class__.__name__:
            raise ValueError('Source files must be the same top-level datatype: either lists or dictionaries.')
        elif isinstance(code, CommentedMap):
            combined = merge_maps(combined, code, overwrite, prune)
        elif isinstance(code, CommentedSeq):
            combined = merge_seqs(combined, code, overwrite, prune)

    # save to target path
    if target:
        yml.indent(sequence=indent, offset=seq_indent)
        with open(target, 'w') as f:
            yml.dump(combined, f)

    return combined
