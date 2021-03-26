__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

from labpack.compilers.yaml import merge_yaml_files, merge_yaml_strings
from ruamel.yaml.comments import CommentedMap, CommentedSeq, Comment, Format

if __name__ == '__main__':

    str_a = """\
        # comments at head of file
        date: 20210101 # comment on key-value pair
        brands:        # comment on key to map
          new:
            - toothpaste
            - floss
          old: 
            # comment before list items
            - face cream # comment on item
            - skin cream
        campaigns:
          - name: west coast
            places:             # comment on key to list
              - city: Seattle   
                state: WA
              # comment after map
              - city: Portland
                state: OR
            # comment after list
          - name: midwest
            places:
              - city: Chicago
                state: IL
              - city: Cincinnati
                state: OH
        """
    str_b = """\
        # different comment at head of file
        # additional comment at head
        date: 20210102 # different comment on key-value pair
        topic: branding # comment on key-value pair
        # comment before key
        brands:
          # comment at beginning of map
          protential:
            - vitamins # comment on item
          new:
            - floss # new comment on item
            - toothbrushes # comment on item
          old:
            - face cream # different comment on item
          # comment at end of map
        campaigns:  # comment on key for list
          - name: midwest # new comment on item
            season: winter # comment on key-value pair
            places:
              # comment before list items
              - city: Cincinnati 
                state: OH
                neighborhood: suburbs # comment on key-value pair
              # comment after list items
          - name: east coast
            places:
              - city: Charleston 
                state: SC
              - city: Philadelphia 
                state: PA  
        """
    merged = merge_yaml_strings(str_a, str_b)
    print(merged)

    target = 'test20210325c.yaml'
    sources = ['test20210325a.yaml', 'test20210325b.yaml']
    combined = merge_yaml_files(*sources, target=target)
    print(combined)
