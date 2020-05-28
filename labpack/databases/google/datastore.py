__author__ = 'rcj1492'
__created__ = '2020.05'
__license__ = '©2020 Collective Acuity'

'''
PLEASE NOTE:    datastore package requires the google cloud datastore module.

(all platforms) pip3 install google-cloud-datastore
'''

try:
    from google.cloud import datastore
except:
    import sys

    print('datastore package requires the google cloud datastore module. try: pip3 install google-cloud-datastore')
    sys.exit(1)

import re
import json
import base64
from labpack.records.id import labID
from jsonmodel.validators import jsonModel


class DatastoreTable(object):

    ''' 
        a class to manage tabular style records in google datastore

        STORAGE:
        https://cloud.google.com/datastore/docs/concepts/storage-size

        each record size is dramatically impacted by the length of:

            1. the name of the table
            2. the id for each record
            3. the name of each field

        as well as the number of indexed fields. each index uses
        storage equal to the combined size of each of the elements above
        plus the value of the field and duplicate it twice... for both
        ascending and descending orders.

        by default, this class requires indices to be specified and 
        does not create null values for empty fields.

        the most space efficient setup will not have any indices and
        will use the value of the record id as the main query method
        and/or will allow datastore to generate an id automatically
        
        LIMITS:
        https://cloud.google.com/datastore/docs/concepts/limits
        
        REFERENCES:
        https://googleapis.dev/python/datastore/latest/index.html 
        https://cloud.google.com/datastore/docs/concepts/entities
    '''

    _class_fields = {
        'schema': {
            'table_name': 'User Data',
            'record_schema': {
                'schema': {}
            },
            'indices': [''],
            'results': 1,
            'batch': 1,
            'cursor': 'aGFwcHk=',
            'old_details': {
                'id': None
            },
            'new_details': {
                'id': None
            },
            'merge_rule': 'overwrite',
            'sort': [{}]
        },
        'components': {
            '.table_name': {
                'max_length': 255,
                'must_not_contain': ['/', '\\.', '-', '^\d', '^__']
            },
            '.results': {
                'greater_than': 0,
                'integer_data': True,
                'max_value': 1000
            },
            '.batch': {
                'greater_than': 0,
                'integer_data': True,
                'max_value': 500
            },
            '.cursor': {
                'byte_data': True
            },
            '.merge_rule': {
                'discrete_values': ['overwrite', 'skip', 'update']
            },
            '.record_schema': {
                'extra_fields': True
            }
        }
    }

    def __init__(self, datastore_client, table_name, record_schema, indices=None, default_values=False, verbose=False):

        title = '%s.__init__' % self.__class__.__name__

        # construct class fields
        self.fields = jsonModel(self._class_fields)

        # validate inputs
        args = {
            'table_name': table_name,
            'record_schema': record_schema,
            'indices': indices
        }
        for key, value in args.items():
            if value:
                titlex = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, titlex)

        # validate client
        if not isinstance(datastore_client, datastore.Client):
            raise ValueError('%s(client=...) must be a google.cloud.datastore.Client object.' % title)

        # construct properties
        self.client = datastore_client
        self.table_name = table_name
        self.record_schema = record_schema
        self.model = jsonModel(record_schema)
        self.kind = table_name
        self.indices = set()
        self.store_indices = set()
        self.default_values = default_values
        self.default = self.model.ingest(**{})

        # construct helper methods
        self.labID = labID
        self.item_key = re.compile('\[0\]')

        # validate indices
        if indices:
            for i in range(len(indices)):
                index = indices[i]
                msg = '%s(indices=[...]) item %s' % (title, i)
                if index.find('.') == 0:
                    raise ValueError('%s must not start with "."')
                dot_index = '.%s' % index
                if not dot_index in self.model.keyMap.keys():
                    raise ValueError('%s must be a key path in record_schema.' % msg)
                self.indices.add(index)
                # correct item path to list path for datastore
                store_key = index
                if self.item_key.findall(index):
                    end = index.find('[0]')
                    store_key = index[0:end]
                self.store_indices.add(store_key)

        # validate id is a number or string
        if '.id' in self.model.keyMap.keys():
            if not self.model.keyMap['.id']['value_datatype'] in ('string', 'number'):
                raise ValueError('%s(record_schema={id:...}) id field must be a string or number.' % title)
        else:
            extra_fields = False
            if 'extra_fields' in self.model.keyMap['.'].keys():
                extra_fields = self.model.keyMap['.']['extra_fields']
            if not extra_fields:
                raise ValueError(
                    '%s(record_schema={...}) must either contain an id field or allow extra fields.' % title)

        # enable json dumps if lists contain datatype other than strings or numbers
        self.enable_json = set()
        self.json_lists = set()
        for key, value in self.model.keyMap.items():
            # check for __key__ name
            if key == '.__key__':
                raise ValueError('%(record_schema) cannot contain field "__key__". Name is a keyword in datastore.')
            # check if field is a list
            if self.item_key.findall(key):
                if value['value_datatype'] not in ('string', 'number'):
                    self.enable_json.add(key)
                    end = key.find('[0]')
                    self.json_lists.add(key[0:end])

        # validate there are no lists in indices if json dumps enabled
        if self.enable_json:
            if self.indices:
                dot_indices = set()
                for index in self.indices:
                    dot_indices.add('.%s' % index)
                unindexable = self.enable_json.intersection(dot_indices)
                if unindexable:
                    from labpack.parsing.grammar import join_words
                    raise ValueError('%s(indices) cannot contain %s. Indices can only contain item key paths for lists of strings or numbers.' % (title, join_words(list(unindexable), operator='or')))

        # construct verbose method
        self.printer_on = True
        def _printer(msg, flush=False):
            if verbose and self.printer_on:
                if flush:
                    print(msg, end='', flush=True)
                else:
                    print(msg)
        self.printer = _printer

    def _rebuild_table(self):
        # TODO method to reformat existing records to conform to new schema
        pass

    def _prepare_record(self, record):

        ''' a helper method for converting a record to column-based fields '''

        fields = {}
        for key, value in self.model.keyMap.items():
            record_key = key[1:]
            if record_key:
                if self.item_key.findall(record_key):
                    pass
                else:
                    if value['value_datatype'] in ('boolean', 'string', 'number'):
                        try:
                            results = self.model._walk(key, record)
                            fields[record_key] = results[0]
                        except:
                            if self.default_values:
                                results = self.model._walk(key, self.default)
                                fields[record_key] = results[0]
                    elif value['value_datatype'] == 'list' and record_key in self.json_lists:
                        try:
                            results = self.model._walk(key, record)
                            fields[record_key] = json.dumps(results[0])
                        except:
                            if self.default_values:
                                results = self.model._walk(key, self.default)
                                fields[record_key] = results[0]
                    elif value['value_datatype'] == 'list':
                        try:
                            results = self.model._walk(key, record)
                            fields[record_key] = results[0]
                        except:
                            if self.default_values:
                                results = self.model._walk(key, self.default)
                                fields[record_key] = results[0]

        # add id field if missing
        uid = self.labID().id24[0:16]
        if not 'id' in fields.keys():
            if '.id' in self.model.keyMap.keys():
                if self.model.keyMap['.id']['value_datatype'] == 'number':
                    integer = False
                    if 'integer_data' in self.model.keyMap['.id'].keys():
                        if self.model.keyMap['.id']['integer_data']:
                            fields['id'] = 0
                            integer = True
                    if not integer:
                        fields['id'] = 0.0
                else:
                    fields['id'] = uid
            else:
                fields['id'] = uid

        return fields

    def _reconstruct_record(self, entity):

        ''' a helper method for reconstructing a record from a datastore entity '''

        details = {
            'id': entity.key._flat_path[-1]
        }
        current = details
        for key, value in self.model.keyMap.items():
            record_key = key[1:]
            if record_key:
                record_value = entity.get(record_key, None)
                if record_value != None:
                    record_segments = record_key.split('.')
                    for i in range(len(record_segments)):
                        segment = record_segments[i]
                        if i + 1 < len(record_segments):
                            if segment not in details.keys():
                                current[segment] = {}
                            current = current[segment]
                        else:
                            if value['value_datatype'] == 'list' and record_key in self.json_lists:
                                current[segment] = json.loads(record_value)
                            else:
                                current[segment] = record_value
                    current = details

        return details

    def _paginate(self, query, iter_func, end_func):

        ''' a method to automatically paginate fetch queries '''

        next_cursor = True
        kwargs = {
            'limit': 100
        }
        count = 0
        while next_cursor:
            query_iter = query.fetch(**kwargs)
            page = next(query_iter.pages)
            for entity in page:
                iter_func(entity)
                count += 1
            next_cursor = query_iter.next_page_token
            if next_cursor:
                kwargs['start_cursor'] = next_cursor

        return end_func(count)

    def _update_indices(self, batch=10):

        ''' a method to update indexing of fields in all records 

        NOTE:   datastore does not automatically index old records, this method
                scans each index and updates the indexing of fields which are
                not indexed. RUN THIS METHOD CAUTIOUSLY
        '''

        title = '%s._update_indices' % self.__class__.__name__

        # validate inputs
        args = {
            'batch': batch
        }
        for key, value in args.items():
            titlex = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, titlex)

        # define empty key sets
        ids = set()
        indices = {}
        for index in self.store_indices:
            indices[index] = set()

        # retrieve all keys
        self.printer('Retrieving ids for table %s' % self.table_name, flush=True)
        query = self.client.query(kind=self.kind)
        query.keys_only()
        next_cursor = True
        kwargs = {
            'limit': 100
        }
        while next_cursor:
            query_iter = query.fetch(**kwargs)
            page = next(query_iter.pages)
            for entity in page:
                ids.add(entity.key._flat_path[-1])
                self.printer('.', flush=True)
            next_cursor = query_iter.next_page_token
            if next_cursor:
                kwargs['start_cursor'] = next_cursor
        self.printer(' done.')

        # for all indices, retrieve index keys
        for index in indices.keys():
            self.printer('Retrieving ids for index %s' % index, flush=True)
            index_query = self.client.query(kind=self.kind)
            index_query.keys_only()
            index_query.order = [index]
            next_cursor = True
            kwargs = {
                'limit': 100
            }
            while next_cursor:
                query_iter = index_query.fetch(**kwargs)
                page = next(query_iter.pages)
                for entity in page:
                    indices[index].add(entity.key._flat_path[-1])
                    self.printer('.', flush=True)
                next_cursor = query_iter.next_page_token
                if next_cursor:
                    kwargs['start_cursor'] = next_cursor
            self.printer(' done.')

        # determine records with all indices
        complete = ids
        for key in indices.keys():
            complete = complete.intersection(indices[key])
        incomplete = list(ids - complete)
        count = len(incomplete)

        # conduct multi get and update
        while True:
            i = batch * -1
            subset = incomplete[i or None:]

            # retrieve a batch of records
            keys = []
            for record_id in subset:
                keys.append(self.client.key(self.kind, record_id))
            records = self.client.get_multi(keys)

            # add indexes to fields
            entities = []
            for entity in records:
                exclusions = set(entity.keys()) - self.store_indices
                kwargs = {'key': entity.key}
                if exclusions:
                    kwargs['exclude_from_indexes'] = list(exclusions)
                updated = datastore.Entity(**kwargs)
                fields = {}
                for key, value in entity.items():
                    fields[key] = value
                updated.update(fields)
                entities.append(updated)
                self.printer('Updating indices for %s.' % entity.key._flat_path[-1])

            # send update request
            self.client.put_multi(entities)

            # pop processed records and break off loop
            incomplete = incomplete[:i or None]
            if len(subset) < batch or not incomplete:
                break

        # report completion and return count
        self.printer('Table %s indices updated.' % self.table_name)
        return count

    def list(self, filter=None, sort=None, results=100, cursor='', ids_only=False):

        '''
            a method to retrieve records using criteria evaluated on table indexes

        NOTE:   only fields which have been added to the indices argument at object
                construction can be queried in-memory by Datastore and if an index
                is added after records are in the database, records previously added
                to the datastore are not automatically added to the index. to make
                sure that all records are properly indexed, you must run
                _update_indices
                WARNING - _update_indices is an optimized SCAN of Datastore
                and could be very costly

        NOTE:   composite indices allow for more complex queries in-memory
                but must be registered with Datastore using gcloud client
                and specified as index.yaml in app root and built before 
                https://cloud.google.com/datastore/docs/concepts/indexes

        :param filter: dictionary of dot path field name and jsonmodel query criteria
        :param sort: list of single key-pair dictionaries with dot path field names
        :param results: integer with number of results to return
        :param cursor: object with place of search sequence for last results for pagination
        :param ids_only: boolean to enable return of only ids (reduces 'read' use to 1)
        :return: list of results

        filter:
        {
            'path.to.field': 'equal to value',
            'path.to.number': {
                'min_value': 4.5
            },
            'path.to.string': {
                'discrete_values': [ 'pond', 'lake', 'stream', 'brook' ]
            }
        }

        NOTE:   datastore only supports a limited number of query conditions and
                only lists of numbers and strings can be queried. this method
                constructs a query which contains clauses wherever the query 
                conditions can be translated one-to-one into datastore filters
                and returns the entire record of each qualifying record. once
                datastore returns its results, the remaining query conditions are
                applied to the records and only those results which match all
                conditions are produced. as such, depending upon the filter criteria
                chosen, this method acts more or less like a SCAN of the entire
                database. if no datastore supported conditions are provided, the
                method will look through all records and impose a large usage cost.
                it is advised to select only filters supported by datastore,
                especially if enabling ids_only option.

                native datastore supported conditions:

                float, integer & strings (including those found in lists):
                    equal_to
                    greater_than
                    less_than
                    max_value
                    min_value

                booleans:
                    equal_to

        NOTE:   the full list of all filter criteria supported by post-processing
                are found in the reference page for the jsonmodel module as well 
                as the query-rules.json file included in the module. 
                http://collectiveacuity.github.io/jsonModel/reference/#query-criteria

        an example of how to construct the sort argument:

        sort = [
            { 'path.to.number': 'descend' }
        ]

        NOTE:   results can be ordered either by ascending or descending values. to
                order in ascending order, leave the value for the field empty. a
                declared value automatically is interpreted as descending order.

        NOTE:   sorts on more than one field require a composite index

        output:
        [ { 'id': '...', 'email': '...', ... }, { ... } ], cursor_string

        output (if ids_only):
        [ 'abc', 'xyz', 'ijk', ... ], cursor_string

        REFERENCES:
            https://cloud.google.com/datastore/docs/concepts/queries
            https://googleapis.dev/python/datastore/latest/queries.html
            https://cloud.google.com/datastore/docs/concepts/queries#inequality_filters_are_limited_to_at_most_one_property
        
        SUB-OPTIMAL SEARCHES (requiring post-process):
            400 Cannot have inequality filters on multiple properties
            400 inequality filter property and first sort order must be the same

        SEARCHES REQUIRING COMPOSITE INDEX:
            400 no matching index found (for = and > on separate properties)
            400 no matching index found (for multiple sort properties)
            400 no matching index found (for = filter and different sort property)
        '''

        title = '%s.list' % self.__class__.__name__

        # validate inputs
        args = {
            'sort': sort,
            'results': results,
            'cursor': cursor
        }
        for key, value in args.items():
            if value:
                titlex = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, titlex)

        # validate filter
        if filter:
            self.model.query(filter)
        else:
            filter = {}

        # validate sort
        if sort:
            for i in range(len(sort)):
                criterion = sort[i]
                msg = '%s(sort=[...]) item %s' % (title, i)
                for key, value in criterion.items():
                    if key.find('.') == 0:
                        raise ValueError('%s key %s must not begin with "."' % (msg, key))
                    elif not key in self.indices:
                        raise ValueError('%s key %s must be indexed in indices.' % (msg, key))
        else:
            sort = []

        # construct default query
        query = self.client.query(kind=self.kind)

        # add filters
        post_process = False
        inequality = ''
        equalities = []
        for key, value in filter.items():

            # handle key filters
            if key == 'id':
                if isinstance(value, dict):
                    for k, v in value.items():
                        eval_key = self.client.key(self.kind, v)
                        if k == 'equal_to':
                            query.key_filter(eval_key, '=')
                            equalities.append(eval_key)
                        elif k == 'greater_than':
                            if not inequality or inequality == eval_key:
                                query.key_filter(eval_key, '>')
                                inequality = 'id'
                            else:
                                post_process = True
                        elif k == 'less_than':
                            if not inequality or inequality == eval_key:
                                query.key_filter(eval_key, '<')
                                inequality = 'id'
                            else:
                                post_process = True
                        elif k == 'max_value':
                            if not inequality or inequality == eval_key:
                                query.key_filter(eval_key, '<=')
                                inequality = 'id'
                            else:
                                post_process = True
                        elif k == 'min_value':
                            if not inequality or inequality == eval_key:
                                query.key_filter(eval_key, '>=')
                                inequality = 'id'
                            else:
                                post_process = True
                        else:
                            post_process = True
                else:
                    eval_key = self.client.key(self.kind, value)
                    query.key_filter(eval_key, '=')
                    equalities.append(eval_key)

            # activate post processing if any filter key not in indices
            elif key not in self.indices:
                post_process = True

            # add filter for each eligible criterion in filter criteria
            elif isinstance(value, dict):
                # correct item path to list path
                store_key = key
                if self.item_key.findall(key):
                    end = key.find('[0]')
                    store_key = key[0:end]
                for k, v in value.items():
                    if k == 'equal_to':
                        query.add_filter(store_key, '=', v)
                        equalities.append(self.client.key(self.kind, store_key))
                    elif k == 'greater_than':
                        if not inequality or inequality == store_key:
                            query.add_filter(store_key, '>', v)
                            inequality = store_key
                        else:
                            post_process = True
                    elif k == 'less_than':
                        if not inequality or inequality == store_key:
                            query.add_filter(store_key, '<', v)
                            inequality = store_key
                        else:
                            post_process = True
                    elif k == 'max_value':
                        if not inequality or inequality == store_key:
                            query.add_filter(store_key, '<=', v)
                            inequality = store_key
                        else:
                            post_process = True
                    elif k == 'min_value':
                        if not inequality or inequality == store_key:
                            query.add_filter(store_key, '>=', v)
                            inequality = store_key
                        else:
                            post_process = True
                    else:
                        post_process = True
            else:
                # correct item path to list path
                store_key = key
                if self.item_key.findall(key):
                    end = key.find('[0]')
                    store_key = key[0:end]
                query.add_filter(store_key, '=', value)
                equalities.append(self.client.key(self.kind, store_key))

        # add sort orders
        order = []
        ordered = []
        for criterion in sort:
            key, value = next(iter(criterion.items()))
            if self.item_key.findall(key) or key in ordered:
                # prevent weird sorting outcomes or double sorting
                pass
            elif value:
                order.append('-%s' % key)
                ordered.append(key)
                # reset query to sort only and post process
                if len(ordered) == 1:
                    if inequality and inequality != key:
                        query = self.client.query(kind=self.kind)
                        post_process = True
            else:
                order.append(key)
                ordered.append(key)
                # reset query to sort only and post process
                if len(ordered) == 1:
                    if inequality and inequality != key:
                        query = self.client.query(kind=self.kind)
                        post_process = True
        if order:
            query.order = order

        # reduce query to ids
        if ids_only and not post_process:
            query.keys_only()

        # construct fetch kwargs
        kwargs = {
            'limit': results
        }
        # convert cursor arg into byte data
        if cursor:
            kwargs['start_cursor'] = base64.urlsafe_b64decode(cursor.encode('utf-8'))

        # fetch results
        results = query.fetch(**kwargs)

        # reconstruct (and further evaluate) records
        records = []
        page = next(results.pages)
        entities = list(page)
        for entity in entities:
            if ids_only and not post_process:
                records.append(entity.key._flat_path[-1])
            elif not post_process:
                records.append(self._reconstruct_record(entity))
            else:
                record = self._reconstruct_record(entity)
                if self.model.query(filter, record):
                    if ids_only:
                        records.append(record['id'])
                    else:
                        records.append(record)

        # determine end cursor
        end_cursor = ''
        next_token = results.next_page_token
        if next_token:
            end_cursor = base64.urlsafe_b64encode(next_token).decode('utf-8')

        return records, end_cursor

    def exists(self, record_id):

        ''' a method to determine if record exists '''

        query = self.client.query(kind=self.kind)
        eval_key = self.client.key(self.kind, record_id)
        query.add_filter('__key__', '=', eval_key)
        query.keys_only()
        result = list(query.fetch())
        if result:
            return True
        return False

    def create(self, record):

        '''
            a method to create a new record in the table

            NOTE:   this class uses the id field as the primary key for all records
                    if record includes an id field that is an integer, float
                    or string, then it will be used as the primary key. 

            NOTE:   if the id field is missing, a unique 16 character url safe 
                    string will be created for the id field and included in the 
                    record. if the id field == 0.0, then datastore will assign a 
                    randomly generated 16 digit numerical id
            
            NOTE:   key length is a significant component of the size of storing a
                    record. the built in datastore id take up 8 bytes while an id
                    string takes up bytes = len(id) + 1. in addition, all keys have
                    an additional 16 byte overhead and the record id is reused for
                    each index twice, once for ascending and once for descending
                    order. 

            NOTE:   record fields which do not exist in the record_schema or 
                    whose value do not match the requirements of the record_schema
                    will throw an InputValidationError

            NOTE:   list fields are stringified using json before they are saved 
                    to the datastore and are not possible to search using query
                    statements. it is recommended that lists be stored instead as
                    separate tables

        :param record: dictionary with record fields 
        :return: string with id for record
        '''

        title = '%s.create' % self.__class__.__name__

        # validate inputs
        details = self.model.validate(record, object_title='%s(record={...})' % title)

        # prepare fields for put request
        fields = self._prepare_record(details)

        # prepare key for datastore
        # https://cloud.google.com/datastore/docs/concepts/entities#assigning_identifiers
        key = None
        record_id = None
        generated = False
        if isinstance(fields['id'], int) or isinstance(fields['id'], float):
            if not fields['id']:
                key = self.client.key(self.kind)
                generated = True
        if not generated:
            record_id = fields['id']
            key = self.client.key(self.kind, record_id)
        del fields['id']

        # prepare record for insertion
        # https://cloud.google.com/datastore/docs/concepts/entities
        exclusions = set(fields.keys()) - self.store_indices
        kwargs = {'key': key}
        if exclusions:
            kwargs['exclude_from_indexes'] = list(exclusions)
        entity = datastore.Entity(**kwargs)
        entity.update(fields)

        # send put request
        self.client.put(entity)

        # return primary key
        if generated:
            record_id = entity.key._flat_path[-1]
        self.printer('Record %s created.' % record_id)

        return record_id

    def read(self, record_id):

        ''' 
            a method to retrieve the details for a record in the table 

        :param record_id: string or number with unique identifier of record
        :return: dictionary with record fields 
        '''

        title = '%s.read' % self.__class__.__name__

        #  retrieve entity
        key = self.client.key(self.kind, record_id)
        entity = self.client.get(key)
        if not entity:
            return {}

        # reconstruct record from entity values
        return self._reconstruct_record(entity)

    def update(self, record):

        ''' a method to update an existing record '''

        title = '%s.update' % self.__class__.__name__

        # validate inputs
        details = self.model.validate(record, object_title='%s(record={...})' % title)

        # validate id
        if not 'id' in details.keys():
            raise ValueError('%s(record) must contain an id field.' % title)
        elif not details['id']:
            raise ValueError('%s(record) id field must not be empty.' % title)

        # prepare record for updating
        fields = self._prepare_record(details)
        uid = fields['id']
        del fields['id']

        # prepare entity
        # https://cloud.google.com/datastore/docs/concepts/entities#updating_an_entity
        key = self.client.key(self.kind, uid)
        exclusions = set(fields.keys()) - self.store_indices
        kwargs = {'key': key}
        if exclusions:
            kwargs['exclude_from_indexes'] = list(exclusions)
        entity = datastore.Entity(**kwargs)
        entity.update(fields)

        # update database
        self.client.put(entity)

        return details

    def delete(self, record_id):

        ''' a method to delete an existing record '''

        key = self.client.key(self.kind, record_id)
        self.client.delete(key)

        msg = 'Record %s deleted.' % record_id
        self.printer(msg)

        return msg

    def remove(self):

        ''' a method to remove all records in table '''

        query = self.client.query(kind=self.kind)
        query.keys_only()

        def iter_func(entity):
            self.client.delete(entity.key)
            self.printer('Record %s deleted.' % entity.key._flat_path[-1])

        def end_func(count):
            self.printer('Table %s empty.' % self.table_name)
            return count

        return self._paginate(query, iter_func, end_func)

    def export(self, dest_table, merge_rule='skip', coerce=False):

        ''' TODO a method to export all the records to another table '''

        # TODO validate methods of destination sql_table

        query = self.client.query(kind=self.kind)
        dest_name = 'new_table'

        def iter_func(entity):
            record = self._reconstruct_record(entity)
            # TODO add record to destination
            self.printer('Record %s copied to %s' % (record['id'], dest_name))

        def end_func(count):
            # TODO report results
            self.printer('Export to %s complete.' % dest_name)
            return count

        return self._paginate(query, iter_func, end_func)


        
