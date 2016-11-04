__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

from labpack.compilers.objects import _method_constructor, _walk_constructor, retrieve_function

if __name__ == '__main__':
    method_name = 'ext'
    sub_methods = { 'foo': 'bar' }
    class _file_types(object):
        def __init__(self, method_name, sub_methods):
            method_object = _method_constructor(sub_methods)
            setattr(self, method_name, method_object)
    f = _file_types(method_name, sub_methods)
    assert f.ext.foo == 'bar'
    method_dict = {
        'ext': { 'foo': 'bar', 'fooz': { 'me': 'you' } },
        'txt': { 'sunny': 'day'}
    }
    g = _walk_constructor(method_dict)
    assert g.ext.fooz.me == 'you'
    assert g.txt.sunny == 'day'
    library_func = retrieve_function('yaml.dump')
    global_func = retrieve_function('_walk_constructor', globals())
    file_func = retrieve_function('../labpack/records/settings:load_settings')
    file_func = retrieve_function('../labpack/storage/appdata.py:appdataClient')
    assert 'create' in dir(file_func)