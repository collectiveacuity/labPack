__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

import re
from jsonmodel.validators import jsonModel
from labpack.compilers.classes import _method_constructor

class labRegex(object):

    _class_methods = {
        'schema': {
            '__init__': {
                'regex_schema': { 'json.gz': '\\.json\\.gz?' },
                'override': False
            },
            'map': {
                'string_input': 'the website for the lab is collectiveacuity.com',
                'n_grams': 0
            }
        },
        'components': {
            '.__init__.regex_schema': {
                'extra_fields': True
            },
            '.__init__.regex_schema.json.gz': {
                'required_field': False
            },
            '.map.n_grams': {
                'integer_data': True,
                'min_value': 1
            }
        }
    }

    def __init__(self, regex_schema, override=False):

        '''
            instantiates class with a regular expression dictionary

        :param regex_schema: dictionary with regular expression name, pattern key-pairs
        :param override: boolean to ignore value errors raised from regex name conflicts
        '''

        class_name = self.__class__.__name__

    # construct class method validator
        self.fields = jsonModel(self._class_methods)

    # validate inputs
        object_title = '%s.__init__(regex_schema={...})' % class_name
        regex_schema = self.fields.validate(regex_schema, '.__init__.regex_schema', object_title)

    # construct builtin list to differentiate custom methods
        self.builtins = []
        for item in self.__dir__():
            self.builtins.append(item)

    # construct a method for each regex pattern in input
        for key, value in regex_schema.items():
            if key in self.builtins:
                if not override:
                    raise ValueError('\nRegex key %s is the name of a %s builtin method.' % (key, class_name))
            else:
                pro_char = re.compile('[^\w]')
                first_char = re.compile('[a-zA-Z]')
                method_name = pro_char.sub('_', key)
                if first_char.match(method_name):
                    try:
                        getattr(self, method_name)
                        if not override:
                            raise ValueError('\nThe method for regex key %s will conflict with another key.' % key)
                    except:
                        pass
                    sub_methods = {
                        'pattern': re.compile(value),
                        'name': key
                    }
                    method_object = _method_constructor(sub_methods)
                    setattr(self, method_name, method_object)
                elif not override:
                    raise ValueError('\Regex key %s must begin with a letter.' % key)

    def map(self, string_input, n_grams=1):

        title = '%s.map' % self.__class__.__name__

    # validate inputs
        input_dict = { '.map.string_input': string_input, '.map.n_grams': n_grams }
        for key, value in input_dict.items():
            object_title = '%s(%s)' % (title, key.replace('.map.', ''))
            value = self.fields.validate(value, key, object_title)

    # construct empty method fields
        word_list = []

    # construct set of regex methods
        custom_methods = set(self.__dir__()) - set(self.builtins)

    # construct n gram list
        gram_list = string_input.split()
        if n_grams > 1:
            token_list = string_input.split()
            if n_grams <= len(token_list):
                gram_list = []
                stop_point = len(token_list) - n_grams + 1
                for i in range(stop_point):
                    n_token = ''
                    for j in range(i, i + n_grams):
                        if n_token:
                            n_token += ' '
                        n_token += token_list[j]
                    gram_list.append(n_token)

    # analyze each item in n gram list for regex match
        for i in range(0, len(gram_list)):
            token_map = {
                'word': gram_list[i],
            }
            for method in custom_methods:
                regex_method = getattr(self, method)
                regex_pattern = getattr(regex_method, 'pattern')
                regex_name = getattr(regex_method, 'name')
                token_map[regex_name] = False
                if regex_pattern.findall(gram_list[i]):
                    token_map[regex_name] = True
            word_list.append(token_map)

        return word_list

if __name__ == '__main__':
    test_schema = {
        "valid email": "^[\\w\\-_\\.\\+]{1,36}?@[\\w\\-\\.]{1,36}?\\.[a-z]{2,10}$",
        "valid url": "[\\w\\-\\.]+\\.[a-z]{2,10}$",
        "json extension": ".+\\.json$",
        "non-ascii characters": "[^\x00-\x7F]+",
        "invalid filename": '[/<>!`:\\\"\\*\\?\\n\\t\\r\\|]+|^\\.|[\\.\\s]$'
    }
    regex = labRegex(test_schema)
    test_input = "the website for the lab is collectiveacuity.com"
    input_map = regex.map(test_input)
    assert input_map[0]['word'] == 'the'
    # print(input_map)
    file_ext = {
        "json": ".+\\.json$",
        "json.gz": ".+\\.json\\.gz$",
        "yaml": ".+\\.ya?ml$",
        "yaml.gz": ".+\\.ya?ml\\.gz$",
        "drep": ".+\\.drep$"
    }
    regex = labRegex(file_ext)
    test_input = 'happy.json.gz'
    input_map = regex.map(test_input)[0]
    assert input_map['json.gz']
    print(input_map)