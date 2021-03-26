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

import re

def _parse_top(text):
    comments = []
    for line in text.split('\n'):
        comment = re.match('^# ?(.*?)$', line)
        if not comment:
            break
        comments.append(comment[1])
    return comments

def _parse_comments(text):
    ''' a method to parse lines with comments using regex'''
    comments = {}
    count = 0
    for line in text.split('\n'):
        comment = re.match('^(.*?) (#.*?)$', line)
        if comment:
            comments[count] = {
                'comment': comment[2] + '\n'
            }
            parts = comment[1].strip().split(':')
            if len(parts) == 1:
                comments[count]['item'] = re.sub('^(- )','',parts[0])
            else:
                comments[count]['key'] = re.sub('^(- )','',parts[0])
                comments[count]['value'] = ':'.join(parts[1:]).strip()
        count += 1
    return comments

def _get_comments(obj):
    ''' a method to retrieve comments from CommentMap data '''
    # https://sourceforge.net/p/ruamel-yaml/tickets/293/
    comments = {}
    if isinstance(obj, CommentedMap):
        comment = obj.ca.comment
        if comment:
            for sub in comment:
                if sub is None:
                    continue
                if isinstance(sub, list):
                    for com in sub:
                        comments[com.start_mark.line] = com.value
                else:
                    comments[sub.start_mark.line] = sub.value
        for v in obj.ca.items.values():
            if v:
                for comment in v:
                    if comment is None:
                        continue
                    if isinstance(comment, list):
                        for com in comment:
                            comments[com.start_mark.line] = com.value
                    elif comment.value and comment.value.strip():
                        comments[comment.start_mark.line] = comment.value
    if isinstance(obj, CommentedSeq):
        comment = obj.ca.comment
        if comment:
            for sub in comment:
                if sub is None:
                    continue
                if isinstance(sub, list):
                    for com in sub:
                        comments[com.start_mark.line] = com.value
                else:
                    comments[sub.start_mark.line] = sub.value
    return comments

def merge_maps(target, source, rule, prune, comments):

    if isinstance(target, CommentedMap):
        if prune:
            p = set(target.keys()) - set(source.keys())
            for k in p:
                del target[k]
        map_comments = _get_comments(source)
        shared_comments = set(map_comments.keys()).intersection(set(comments.keys()))
        shared = {}
        if shared_comments:
            for k in shared_comments:
                if map_comments[k] == comments[k]['comment']:
                    shared[map_comments[k]] = comments[k]
        count = 0
        for key, value in source.items():
            if key in target.keys():
                # TODO insert key at start of map https://stackoverflow.com/a/40705671/4941585
                merge_maps(target[key], value, rule, prune, comments)
            else:
                comment = None
                for k, v in shared.items():
                    if v['key'] == key and v['value'] == value:
                        comment = k
                target.insert(count, key, value, comment=comment)
            count += 1
    elif isinstance(target, CommentedSeq):
        merge_seqs(target, source, rule, prune, comments)
    elif rule == 'overwrite':
        target = source

def merge_seqs(target, source, rule, prune, comments):

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
                merge_maps(item, source[0], rule, prune, comments)
        if rule == 'extend':
            target.extend(source)
    else:
        for item in target:
            if isinstance(item, CommentedSeq):
                merge_seqs(item, source[0], rule, prune, comments)
        if rule == 'extend':
            target.extend(source)

def merge_yaml(*sources, target='', rule='update', prune=False):

    '''
        core method for merging two or more yaml files

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

    # import libraries
    from copy import deepcopy
    from ruamel.yaml.util import load_yaml_guess_indent
    yml = YAML(typ='rt')
    yml.default_flow_style = False

    # define variables
    combined = None
    indent = 2
    seq_indent = 0
    combined_top = None

    # open and combine sources
    for yaml_path in sources:
        text = open(yaml_path).read()
        comments = _parse_comments(text)
        top = _parse_top(text)
        result, indent, seq_indent = load_yaml_guess_indent(text)
        code = yml.load(text)
        if not isinstance(code, CommentedMap) and not isinstance(code, CommentedSeq):
            raise ValueError('Source files must be either lists or dictionaries.')
        if not combined:
            combined = deepcopy(code)
            combined_top = top
        elif combined.__class__.__name__ != code.__class__.__name__:
            raise ValueError('Source files must be the same top-level datatype: either lists or dictionaries.')
        elif isinstance(code, CommentedMap):
            merge_maps(combined, deepcopy(code), rule, prune, comments)
        elif isinstance(code, CommentedSeq):
            merge_seqs(combined, deepcopy(code), rule, prune, comments)

        # add top comments if more comments
        if len(combined_top) < len(top):
            lines = '\n'.join(top)
            if combined_top:
                combined_top.extend(top[len(combined_top):])
                lines = '\n'.join(combined_top)
            else:
                combined_top = top
            combined.yaml_set_start_comment(lines, indent=0)

    # save to target path
    if target:
        yml.indent(sequence=indent, offset=seq_indent)
        with open(target, 'w') as f:
            yml.dump(combined, f)

    return combined
