__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

from labpack.compilers.yaml import merge_yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq, Comment, Format

if __name__ == '__main__':

    target = 'test20210325c.yaml'
    sources = ['test20210325a.yaml', 'test20210325b.yaml']
    combined = merge_yaml(*sources, target=target)
    print(combined)
    # if isinstance(combined, CommentedMap):
    #     print(combined.ca.comment)
    #     for item_values in combined.ca.items.values():
    #         print(item_values)
    # for key, value in combined.items():
    #     print(value.__class__.__name__)
    #     if isinstance(value, CommentedMap):
    #         print(value.ca.comment)
    #         for item_values in value.ca.items.values():
    #             print(item_values)
    #     if isinstance(value, CommentedSeq):
    #         comment = value.ca.comment
    #         print(comment)
        
        # for method in dir(value):
        #     if method.find('comment') > -1:
        #         try:
        #             print(method, getattr(value, method))
        #         except:
        #             print(method, 'getattr failed')