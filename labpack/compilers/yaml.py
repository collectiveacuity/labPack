''' a package of methods to merge two or more yaml documents preserving order & comments '''
__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

'''
PLEASE NOTE:    yaml package requires the ruamel.yaml module.

(all platforms) pip3 install ruamel.yaml
'''

try:
    from ruamel.yaml import YAML, version_info as ruamel_yaml_version
    from ruamel.yaml.comments import CommentedMap, CommentedSeq, Comment
    from ruamel.yaml.tokens import CommentToken
except:
    import sys
    print('yaml package requires the ruamel.yaml module. try: pip3 install ruamel.yaml')
    sys.exit(1)

# add get comments attribute to Commented Objects
def get_comments_map(self, key, default=None):
    coms = []
    comments = self.ca.items.get(key)
    if comments is None:
        return default
    for token in comments:
        if token is None:
            continue
        elif isinstance(token, list):
            coms.extend(token)
        else:
            coms.append(token)
    return coms

def get_comments_seq(self, idx, default=None):
    coms = []
    comments = self.ca.items.get(idx)
    if comments is None:
        return default
    for token in comments:
        if token is None:
            continue
        elif isinstance(token, list):
            coms.extend(token)
        else:
            coms.append(token)
    return coms

setattr(CommentedMap, 'get_comments', get_comments_map)
setattr(CommentedSeq, 'get_comments', get_comments_seq)

def walk_data(target, source):
    
    ''' method to recursively walk parse tree and merge source into target '''

    from copy import deepcopy

    # skip if target and source are different datatypes
    if target.__class__.__name__ != source.__class__.__name__:
        pass
    # handle maps
    elif isinstance(target, CommentedMap):
        count = 0
        for k, v in source.items():
            # retrieve comments of field in source
            comments = source.get_comments(k)
            if comments:
                comments = '\n'.join([ comment.value for comment in comments ])
            # insert fields not found in target
            if k not in target.keys():
                target.insert(count, k, v, comments)
            else:
                # add comments from source when missing from target
                if comments:
                    if not target.get_comments(k):
                        target.ca.items[k] = source.ca.items.get(k)
                # walk down maps and sequences
                if isinstance(v, CommentedMap) or isinstance(v, CommentedSeq):
                    walk_data(target[k], v)
            count += 1
    # handle sequences
    elif isinstance(target, CommentedSeq):
        for idx, item in enumerate(target):
            # walk down maps and sequences
            source_copy = deepcopy(source[0])
            if isinstance(item, CommentedMap) or isinstance(item, CommentedSeq):
                if source:
                    walk_data(item, source_copy)
            # add comments to items found in both target and source
            elif source:
                if item in source:
                    comments = source.ca.items.get(source.index(item))
                    if comments:
                        if not target.get_comments(idx):
                            target.ca.items[idx] = comments

def merge_yaml_strings(*sources, output=''):

    '''
        method for merging two or more yaml strings

    this method walks the parse tree of yaml data to merge the fields
    (and comments) found in subsequent sources into the data structure of the
    initial sources. any number of sources can be added to the source args, but
    only new fields and new comments from subsequent sources will be added. to
    overwrite the values in the initial source, it suffices to simply reverse 
    the order of the sources

    PLEASE NOTE:    since there is no way to uniquely identify list items between
                    two yaml documents, items are not added to existing lists.

    PLEASE NOTE:    however, lists are transversed in order to evaluate comments
                    and keys of nested dictionaries using the first item of any
                    subsequent list as a model for the scope

    PLEASE NOTE:    the way that ruamel.yaml keeps track of multi-line comments
                    can create odd results for comments which appear at the start
                    or the end of lists and dictionaries when new fields and comments 
                    are added. it is best to restrict comments to the start of lists
                    and dictionaries.

    :param sources: variable-length argument list of strings with yaml text
    :param output: [optional] string with type of output: '' [default], io
    :return: string with merged data [or StringIO object]
    '''

    # import libraries
    import re
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
        result, indent, seq_indent = load_yaml_guess_indent(text)
        data = yml.load(text)
        try:
            head = [comment.value for comment in data.ca.comment[1]]
        except:
            if ruamel_yaml_version <= (0, 17, 0):
                raise
            else:
                raise NotImplementedError
        if not isinstance(data, CommentedMap) and not isinstance(data, CommentedSeq):
            raise ValueError('Source documents must be either lists or dictionaries.')
        if not combined:
            combined = deepcopy(data)
            combined_head = head
        elif combined.__class__.__name__ != data.__class__.__name__:
            pass
            # raise ValueError('Source documents must be the same top-level datatype or use rule="overwrite"')
        else:
            walk_data(combined, data)

        # add comments to head of document
        if head:
            for comment in head:
                if comment not in combined_head:
                    combined_head.append(comment)
            head_comments = []
            for comment in combined_head:
                comment = re.sub('^# ?','',comment)
                comment = re.sub('\n$','',comment)
                head_comments.append(comment)
            lines = '\n'.join(head_comments)
            combined.yaml_set_start_comment(lines, indent=0)

    # apply indentation and return string
    stream = StringIO()
    yml.indent(sequence=indent, offset=seq_indent)
    yml.dump(combined, stream)
    if output == 'io':
        return stream
    return stream.getvalue()

def merge_yaml(*sources, output=''):
    
    '''
        method for merging two or more yaml strings

    this method walks the parse tree of yaml data to merge the fields
    (and comments) found in subsequent sources into the data structure of the
    initial sources. any number of sources can be added to the source args, but
    only new fields and new comments from subsequent sources will be added. to
    overwrite the values in the initial source, it suffices to simply reverse 
    the order of the sources

    PLEASE NOTE:    since there is no way to uniquely identify list items between
                    two yaml documents, items are not added to existing lists.
                    the overwrite rule also has no effect on items in lists

    PLEASE NOTE:    however, lists are transversed in order to evaluate comments
                    and keys of nested dictionaries using the first item of any
                    subsequent list as a model for the scope

    PLEASE NOTE:    the way that ruamel.yaml keeps track of multi-line comments
                    can create odd results for comments which appear at the start
                    or the end of lists and dictionaries when new fields and comments 
                    are added. it is best to restrict comments to the start of lists
                    and dictionaries.

    PLEASE NOTE:    this method makes no checks to ensure the file path of the 
                    sources exist nor the folder path to any output

    :param sources: variable-length argument list of strings with path to yaml files
    :param output: [optional] string with path to save the combined yaml data to file
    :return: string with merged data
    '''

    # open and combine sources
    src = [ open(yaml_path).read() for yaml_path in sources ]
    stream = merge_yaml_strings(*src, output='io')

    # save to file and return combined string
    if output:
        from shutil import copyfileobj
        with open(output, 'w') as f:
            stream.seek(0)
            copyfileobj(stream, f)
            f.close()
    return stream.getvalue()
