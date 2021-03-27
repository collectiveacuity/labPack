__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

from labpack.compilers.yaml import merge_yaml_files, merge_yaml_strings

str_a = """\
# comments at head of file
date: 20210101 # comment on key-value pair
division: marketing # missing from prune
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
# new comment before key
brands:
  # new comment at beginning of map
  protential:
    - vitamins # comment on new item
  new:
    - floss # new comment on item
    - toothbrushes # comment on new item
  old:
    - face cream # different comment on item
  # new comment at end of map
campaigns:  # new comment on key for list
  - name: midwest # new comment on item
    season: winter # comment on new key-value pair
    places:
      # different comment before list items
      - city: Cincinnati 
        neighborhood: suburbs # comment on new key-value pair
      # different comment after list items
  - name: east coast
    places:
      - city: Charleston 
      - city: Philadelphia
"""
        
if __name__ == '__main__':

    # test default merge
    merged = merge_yaml_strings(str_a, str_b)
    assert merged.find('# different comment at head of file') > -1
    assert merged.find('date: 20210101') > -1
    assert merged.find('# new comment on item') > -1
    assert merged.find('# new comment on key for list') > -1
    assert merged.find('# comment on new key-value pair') > -1
    assert merged.find('# different comment on key-value pair') == -1
    assert merged.find('# new comment at beginning of map') == -1
    assert merged.find('# new comment at end of map') == -1

    # test overwrite and prune
    merged = merge_yaml_strings(str_a, str_b, rule='overwrite', prune=True)
    assert merged.find('# comments at head of file') == -1
    assert merged.find('date: 20210102') > -1
    assert merged.find('# different comment on item') > -1
    assert merged.find('# different comment after list items') > -1
    assert merged.find('# different comment on key-value pair') > -1
    assert merged.find('state: ') == -1
    assert merged.find('# missing from prune') == -1

    target = 'test20210325c.yaml'
    sources = ['test20210325a.yaml', 'test20210325b.yaml']
    merged = merge_yaml_files(*sources, target=target)
    assert merged.find('# different comment at head of file') > -1
    assert merged.find('date: 20210101') > -1
    assert merged.find('# new comment on item') > -1
    assert merged.find('# new comment on key for list') > -1
    assert merged.find('# comment on new key-value pair') > -1
    assert merged.find('# different comment on key-value pair') == -1
    assert merged.find('# new comment at beginning of map') == -1
    assert merged.find('# new comment at end of map') == -1
