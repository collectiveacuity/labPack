__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

from labpack.compilers.git import merge_diff

if __name__ == '__main__':

    f1 = 'test20210330a.scss'
    f2 = 'test20210330b.scss'
    f3 = 'test20210330c.scss'
    merged = merge_diff(f1, f2, f3)
    
    assert merged.find('// A new header') == 0
    assert merged.find('$index-content') < merged.find('$index-header')
    assert merged.find('// a new sections') < merged.find('// determine line heights')
    assert merged.find('// a new section at end') > merged.find('$height-title')
    assert merged.find('$width-desktop: 1750') == -1
    assert merged.find('a new comment') == -1
    assert merged.find('// change near end') == -1
    assert merged.find('$height-title: 10028;') == -1
    assert merged.find('$height-portrait-ratio: 1;') + len('$height-portrait-ratio: 1;') == len(merged)