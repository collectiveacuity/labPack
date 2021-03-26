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
    from ruamel.yaml.comments import CommentedMap, CommentedSeq, Comment
except:
    import sys
    print('yaml package requires the ruamel.yaml module. try: pip3 install ruamel.yaml')
    sys.exit(1)

# add get comments attribute to Commented Objects
def _get_comments_map(self, key):
    coms = []
    comments = self.ca.items.get(key)
    if comments is None:
        return coms
    for token in comments:
        if token is None:
            continue
        elif isinstance(token, list):
            coms.extend(token)
        else:
            coms.append(token)
    return coms

def _get_comments_seq(self, idx):
    coms = []
    comments = self.ca.items.get(idx)
    if comments is None:
        return coms
    for token in comments:
        if token is None:
            continue
        elif isinstance(token, list):
            coms.extend(token)
        else:
            coms.append(token)
    return coms

setattr(CommentedMap, 'get_comments', _get_comments_map)
setattr(CommentedSeq, 'get_comments', _get_comments_seq)

def _parse_head(text):
    ''' a method to parse initial comments at head of file using regex '''
    import re
    comments = []
    for line in text.split('\n'):
        comment = re.match('^# ?(.*?)$', line)
        if not comment:
            break
        comments.append(comment[1])
    return comments

def _merge_maps(target, source, rule, prune):

    if isinstance(target, CommentedMap):
        if prune:
            p = set(target.keys()) - set(source.keys())
            for k in p:
                del target[k]
        # map_comments = _get_comments(source)
        # shared_comments = set(map_comments.keys()).intersection(set(comments.keys()))
        # shared = {}
        # if shared_comments:
        #     for k in shared_comments:
        #         if map_comments[k] == comments[k]['comment']:
        #             shared[map_comments[k]] = comments[k]
        count = 0
        for key, value in source.items():
            if key in target.keys():
                # TODO insert key at start of map https://stackoverflow.com/a/40705671/4941585
                _merge_maps(target[key], value, rule, prune)
            else:
                target[key] = value
                # comment = None
                # for k, v in shared.items():
                #     if v['key'] == key and v['value'] == value:
                #         comment = k
                # target.insert(count, key, value, comment=comment)
            count += 1
    elif isinstance(target, CommentedSeq):
        _merge_seqs(target, source, rule, prune)
    elif rule == 'overwrite':
        target = source

def _merge_seqs(target, source, rule, prune):

    if rule == 'overwrite' and (not target or not source):
        target = source
    elif rule == 'overwrite' and target[0].__class__.__name__ != source[0].__class__.__name__:
        target = source
    elif not target or not source:
        pass
    elif target[0].__class__.__name__ != source[0].__class__.__name__:
        pass
    elif not isinstance(target[0], CommentedMap) and not isinstance(target[0], CommentedSeq):
        if rule == 'overwrite':
            target = source
        elif rule == 'extend':
            target.extend(source)
    elif isinstance(target[0], CommentedMap):
        for item in target:
            if isinstance(item, CommentedMap):
                _merge_maps(item, source[0], rule, prune)
        if rule == 'extend':
            target.extend(source)
    else:
        for item in target:
            if isinstance(item, CommentedSeq):
                _merge_seqs(item, source[0], rule, prune)
        if rule == 'extend':
            target.extend(source)

def merge_yaml_strings(*sources, rule='update', prune=False, output=''):

    '''
        core method for merging two or more yaml strings

        this method runs recursively down the nested trees of yaml datatypes
        to merge values between two or more yaml files while maximally preserving
        order and comments from the original files

        there are three different rules:
        update - [default] adds only new fields to earlier sources
        extend - adds new fields to earlier sources and appends items
        overwrite - adds new fields and items and overwrites any earlier values 

        when merging more than two files, the order of the input files matters
        as each subsequent input will treat the previous merger as its earlier input

        PLEASE NOTE:    update only adds new fields to dictionaries, existing list
                        length is preserved, but dictionaries within a list are
                        updated with any new fields which occur in the first item of
                        a subsequent file

        PLEASE NOTE:    this method makes no checks to ensure the file path of the 
                        sources exist nor the folder path to any target output
    
    :param sources: variable-length argument list of strings with yaml text
    :param rule: [optional] string to determine rule for merging: update, extend, overwrite
    :param prune: boolean to remove fields in earlier files not found in subsequent files
    :param output: [optional] string with type of output: default = string, io = StringIO
    :return: CommentedMap or CommentedSeq with combined values
    '''

    # import libraries
    from copy import deepcopy
    from ruamel.yaml.compat import StringIO
    from ruamel.yaml.util import load_yaml_guess_indent
    yml = YAML(typ='rt')
    yml.default_flow_style = False

    # define variables
    combined = None
    indent = 2
    seq_indent = 0
    combined_head = None

    # open and combine sources
    for text in sources:
        head = _parse_head(text)
        result, indent, seq_indent = load_yaml_guess_indent(text)
        code = yml.load(text)
        if not isinstance(code, CommentedMap) and not isinstance(code, CommentedSeq):
            raise ValueError('Source documents must be either lists or dictionaries.')
        if not combined:
            combined = deepcopy(code)
            combined_head = head
        elif combined.__class__.__name__ != code.__class__.__name__:
            if rule == 'overwrite':
                combined = deepcopy(code)
                combined_head = head
            else:
                raise ValueError('Source documents must be the same top-level datatype or use rule="overwrite"')
        elif isinstance(code, CommentedMap):
            _merge_maps(combined, deepcopy(code), rule, prune)
        elif isinstance(code, CommentedSeq):
            _merge_seqs(combined, deepcopy(code), rule, prune)

        # add to header comments if there are more comments to add
        if rule == 'overwrite':
            if head:
                combined.yaml_set_start_comment('\n'.join(head))
        elif len(combined_head) < len(head):
            lines = '\n'.join(head)
            if combined_head:
                combined_head.extend(head[len(combined_head):])
                lines = '\n'.join(combined_head)
            else:
                combined_head = head
            combined.yaml_set_start_comment(lines, indent=0)

    # apply indentation and return string
    stream = StringIO()
    yml.indent(sequence=indent, offset=seq_indent)
    yml.dump(combined, stream)
    if output == 'io':
        return stream
    return stream.getvalue()

def merge_yaml_files(*sources, target='', rule='update', prune=False):
    
    '''
        method for merging two or more yaml files

        this method runs recursively down the nested trees of yaml datatypes
        to merge values between two or more yaml files while maximally preserving
        order and comments from the original files

        there are three different rules:
        update - [default] adds only new fields to earlier sources
        extend - adds new fields to earlier sources and appends items
        overwrite - adds new fields and items and overwrites any earlier values 

        when merging more than two files, the order of the input files matters
        as each subsequent input will treat the previous merger as its earlier input

        PLEASE NOTE:    update only adds new fields to dictionaries, existing list
                        length is preserved, but dictionaries within a list are
                        updated with any new fields which occur in the first item of
                        a subsequent file

        PLEASE NOTE:    this method makes no checks to ensure the file path of the 
                        sources exist nor the folder path to any target output

    :param sources: variable-length argument list of strings with path to yaml files
    :param target: [optional] string with path to save the combined yaml data to file
    :param rule: [optional] string to determine rule for merging: update, overwrite
    :param prune: boolean to remove fields in earlier files not found in subsequent files
    :return: CommentedMap or CommentedSeq with combined values
    '''

    # open and combine sources
    src = [ open(yaml_path).read() for yaml_path in sources ]
    stream = merge_yaml_strings(*src, rule=rule, prune=prune, output='io')

    # save to file and return combined string
    if target:
        from shutil import copyfileobj
        with open(target, 'w') as f:
            stream.seek(0)
            copyfileobj(stream, f)
            f.close()
    return stream.getvalue()
