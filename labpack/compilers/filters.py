''' a package of methods to compile search filters '''
__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

def positional_filter(positional_filters, title=''):

    ''' 
        a method to construct a conditional filter function to test positional arguments

    :param positional_filters: dictionary or list of dictionaries with query criteria
    :param title: string with name of function to use instead
    :return: callable for filter_function 

    NOTE:   query criteria architecture

            each item in the path filters argument must be a dictionary
            which is composed of integer-value key names that represent the
            index value of the positional segment to test and key values
            with the dictionary of conditional operators used to test the
            string value in the indexed field of the record.

            eg. positional_filters = [ { 0: { 'must_contain': [ '^lab' ] } } ]

            this example filter looks at the first segment of each key string
            in the collection for a string value which starts with the
            characters 'lab'. as a result, it will match both the following:
                lab/unittests/1473719695.2165067.json
                'laboratory20160912.json'

    NOTE:   the filter function uses a query filters list structure to represent
            the disjunctive normal form of a logical expression. a record is
            added to the results list if any query criteria dictionary in the
            list evaluates to true. within each query criteria dictionary, all
            declared conditional operators must evaluate to true.

            in this way, the positional_filters represents a boolean OR operator and
            each criteria dictionary inside the list represents a boolean AND
            operator between all keys in the dictionary.

            each query criteria uses the architecture of query declaration in
            the jsonModel.query method
    
    NOTE:   function function will lazy load a dictionary input

    positional_filters:
    [ { 0: { conditional operators }, 1: { conditional_operators }, ... } ]

    conditional operators:
        "byte_data": false,
        "discrete_values": [ "" ],
        "excluded_values": [ "" ],
        'equal_to': '',
        "greater_than": "",
        "less_than": "",
        "max_length": 0,
        "max_value": "",
        "min_length": 0,
        "min_value": "",
        "must_contain": [ "" ],
        "must_not_contain": [ "" ],
        "contains_either": [ "" ]
    '''

# define help text    
    if not title:
        title = 'positional_filter'
    filter_arg = '%s(positional_filters=[...])' % title

# construct path_filter model
    filter_schema = {
        'schema': {
            'byte_data': False,
            'discrete_values': [ '' ],
            'excluded_values': [ '' ],
            'equal_to': '',
            'greater_than': '',
            'less_than': '',
            'max_length': 0,
            'max_value': '',
            'min_length': 0,
            'min_value': '',
            'must_contain': [ '' ],
            'must_not_contain': [ '' ],
            'contains_either': [ '' ]
        },
        'components': {
            '.discrete_values': {
                'required_field': False
            },
            '.excluded_values': {
                'required_field': False
            },
            '.must_contain': {
                'required_field': False
            },
            '.must_not_contain': {
                'required_field': False
            },
            '.contains_either': {
                'required_field': False
            }
        }
    }
    from jsonmodel.validators import jsonModel
    filter_model = jsonModel(filter_schema)

# lazy load path dictionary
    if isinstance(positional_filters, dict):
        positional_filters = [ positional_filters ]
        
# validate input
    if not isinstance(positional_filters, list):
        raise TypeError('%s must be a list.' % filter_arg)
    for i in range(len(positional_filters)):
        if not isinstance(positional_filters[i], dict):
            raise TypeError('%s item %s must be a dictionary.' % (filter_arg, i))
        for key, value in positional_filters[i].items():
            _key_name = '%s : {...}' % key
            if not isinstance(key, int):
                raise TypeError('%s key name must be an int.' % filter_arg.replace('...', _key_name))
            elif not isinstance(value, dict):
                raise TypeError('%s key value must be a dictionary' % filter_arg.replace('...', _key_name))
            filter_model.validate(value)

# construct segment value model
    segment_schema = { 'schema': { 'segment_value': 'string' } }
    segment_model = jsonModel(segment_schema)

# construct filter function
    def filter_function(*args):
        max_index = len(args) - 1
        for filter in positional_filters:
            criteria_match = True
            for key, value in filter.items():
                if key > max_index:
                    criteria_match = False
                    break
                segment_criteria = { '.segment_value': value }
                segment_data = { 'segment_value': args[key] }
                if not segment_model.query(segment_criteria, segment_data):
                    criteria_match = False
                    break
            if criteria_match:
                return True
        return False

    return filter_function