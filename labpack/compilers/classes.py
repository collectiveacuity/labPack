__author__ = 'rcj1492'
__created__ = '2016.09'
__license__ = 'MIT'

class _method_constructor(object):
    ''' a class constructor for sub-method attributes '''
    def __init__(self, method_dict):
        for k, v in method_dict.items():
            setattr(self, k, v)

class _walk_constructor(object):
    ''' a walking class constructor for sub-method attributes '''
    def __init__(self, input_dict):
        for key, value in input_dict.items():
            if isinstance(value, dict):
                setattr(self, key, _walk_constructor(value))
            else:
                setattr(self, key, value)

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