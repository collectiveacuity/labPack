__author__ = 'rcj1492'
__created__ = '2021.03'
__license__ = '©2021 Collective Acuity'

from labpack.compilers.yaml import merge_yaml

if __name__ == '__main__':

    target = 'test20210325c.yaml'
    sources = ['test20210325a.yaml', 'test20210325b.yaml']
    combined = merge_yaml(*sources, target=target)
    print(combined)
    for key, value in combined.items():
        print(value.__class__.__name__)
