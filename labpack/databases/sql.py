__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

'''
PLEASE NOTE:    sql package requires the SQLAlchemy module.

(all platforms) pip3 install SQLAlchemy
'''

try:
    from sqlalchemy import create_engine
except:
    import sys
    print('sql package requires the SQLAlchemy module. try: pip3 install SQLAlchemy')
    sys.exit(1)

import pickle
    
class sqlClient(object):
    
    ''' a class of methods for storing records in a sql database '''
    
    _class_fields = {
        'schema': {
            'table_name': 'User Data',
            'database_url': 'sqlite:///../../data/records.db',
            'record_schema': {
                'schema': {}
            },
            'old_details': {
                'id': None
            },
            'new_details': {
                'id': None
            }
        },
        'components': {
            '.table_name': {
                'max_length': 255,
                'must_not_contain': ['/', '^\\.']
            },
            '.record_schema': {
                'extra_fields': True
            },
            '.old_details': {
                'extra_fields': True
            },
            '.new_details': {
                'extra_fields': True
            }
        }
    }
    
    def __init__(self, table_name, database_url, record_schema, rebuild=True, verbose=False):
        
        '''
            the initialization method for the sqlClient class
            
        :param table_name: string with name for table of records
        :param database_url: string with unique resource identifier to database
        :param record_schema: dictionary with jsonmodel valid schema for records
        :param rebuild: [optional] boolean to rebuild table with schema changes 
        :param verbose: [optional] boolean to enable database logging to stdout
        '''
        
        title = '%s.__init__' % self.__class__.__name__
        
    # construct fields
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'table_name': table_name,
            'database_url': database_url,
            'record_schema': record_schema
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # validate database url
        import re
        url_split = re.compile('://+')
        url_error = '%s(database_url="..." must have the format: dialect://user:password@host:port or dialect:///../path/to/local.db' % title
        if not url_split.findall(database_url):
            raise ValueError(url_error)
        sql_dialect, db_path = url_split.split(database_url)
        if sql_dialect == 'sqlite':
            from os import path
            try:
                db_root, db_file = path.split(db_path)
            except:
                raise ValueError(url_error)
            if db_root:
                if not path.exists(db_root):
                    from os import makedirs
                    makedirs(db_root)
        else:
            db_cred, db_file = db_path.split('@')
    
    # construct verbose method
        self.printer_on = True
        def _printer(msg, flush=False):
            if verbose and self.printer_on:
                if flush:
                    print(msg, end='', flush=True)
                else:
                    print(msg)
        self.printer = _printer
        
    # construct record model
        self.record_schema = record_schema
        self.model = jsonModel(record_schema)
                
    # construct database session
        self.engine = create_engine(database_url, echo=verbose)
        self.session = self.engine.connect()
        self.table_name = table_name
        self.database_name = db_file
        self.database_url = database_url
        self.verbose = verbose
    
    # # ORM construct
    #     from sqlalchemy.orm import sessionmaker
    #     from sqlalchemy.ext.declarative import declarative_base
    #     self.engine = create_engine(database_url, echo=verbose)
    #     dbSession = sessionmaker(bind=self.engine)
    #     self.session = dbSession()
    #     self.base = declarative_base()
    #     class RecordObject(self.base):
    #         __tablename__ = table_name
    #         id = Column(String, primary_key=True)
    #     self.base.metadata.create_all(self.engine)
    
    # construct lab id class
        from labpack.records.id import labID
        self.labID = labID
    
    # construct table metadata and prior table properties
        from sqlalchemy import Table, MetaData
        metadata = MetaData()
        prior_columns = self._extract_columns(self.table_name)
        
    # construct new table object
        current_columns = self._parse_columns()
        if not 'id' in current_columns.keys():
            current_columns['id'] = [ 'id', 'string', True, '' ]
            self.record_schema['schema']['id'] = ''
            self.model = jsonModel(self.record_schema)
        table_args = [ self.table_name, metadata ]
        column_args = self._construct_columns(current_columns)
        table_args.extend(column_args)
        self.table = Table(*table_args)
    
    # process table updates
        if prior_columns:
        
        # determine columns to add, remove, rename and change properties
            add_columns, remove_columns, rename_columns, retype_columns = self._compare_columns(current_columns, prior_columns)
        
        # define update functions
        # https://stackoverflow.com/questions/7300948/add-column-to-sqlalchemy-table
            def _add_column(column_key):
                column = getattr(self.table.c, column_key)
                column_name = column.key
                if column_name.find('.') > -1:
                    column_name = '"%s"' % column_name
                column_type = column.type.compile(self.engine.dialect)
                self.engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (self.table_name, column_name, column_type))
        
            def _remove_column(column):
                column_name = column.compile(dialect=self.engine.dialect)
                self.engine.execute('ALTER TABLE %s DROP COLUMN %s' % (self.table_name, column_name))
        
        # update table schema
            if remove_columns or rename_columns or retype_columns:
                if not rebuild:
                    raise ValueError('%s table in %s database must be rebuilt in order to update to desired record_schema. try: rebuild=True' % (self.table_name, self.database_name))
                else:
                    new_name = self.table_name
                    old_name = '%s_old_%s' % (self.table_name, labID().id24.replace('-','_'))
                    self._rebuild_table(new_name, old_name, current_columns, prior_columns)
                    
            elif add_columns:
                column_names = []
                for column_key in add_columns.keys():
                    _add_column(column_key)
                    column_names.append(column_key)
                from labpack.parsing.grammar import join_words
                plural = ''
                if len(column_names) > 1:
                    plural = 's'
                print('%s column%s added to table %s' % (join_words(column_names), plural, self.table_name))
                
    # or create new table
        else:
            self.table.create(self.engine)                    
            print('%s table created in %s database.' % (self.table_name, self.database_name))
    
    def _extract_columns(self, table_name):
        
        ''' a method to extract the column properties of an existing table '''
        
        from sqlalchemy import MetaData, VARCHAR, INTEGER, BLOB, BOOLEAN, FLOAT
        
        metadata_object = MetaData()
        table_list = self.engine.table_names()
        prior_columns = {}
        if table_name in table_list:
            metadata_object.reflect(self.engine)
            existing_table = metadata_object.tables[table_name]
            for column in existing_table.columns:
                column_type = None
                if column.type.__class__ == FLOAT().__class__:
                    column_type = 'float'
                elif column.type.__class__ == INTEGER().__class__:
                    column_type = 'integer'
                elif column.type.__class__ == VARCHAR().__class__:
                    column_type = 'string'
                elif column.type.__class__ == BLOB().__class__:
                    column_type = 'list'
                elif column.type.__class__ == BOOLEAN().__class__:
                    column_type = 'boolean'
                prior_columns[column.key] = (column.key, column_type, '')
        
        return prior_columns
        
    def _parse_columns(self):
    
        ''' a helper method for parsing the column properties from the record schema '''
        
    # define item key pattern
        import re
        self.item_key = re.compile('\[0\]')
    
    # construct column list
        column_map = {}
        for key, value in self.model.keyMap.items():
            record_key = key[1:]
            if record_key:
                if self.item_key.findall(record_key):
                    pass
                else:
                    if value['value_datatype'] == 'map':
                        continue
                    datatype = value['value_datatype']
                    if value['value_datatype'] == 'number':
                        datatype = 'float'
                        if 'integer_data' in value.keys():
                            if value['integer_data']:
                                datatype = 'integer'
                    replace_key = ''
                    if 'field_metadata' in value.keys():
                        if 'replace_key' in value['field_metadata'].keys():
                            if isinstance(value['field_metadata']['replace_key'], str):
                                replace_key = value['field_metadata']['replace_key']
                    column_map[record_key] = (record_key, datatype, replace_key)
        
        return column_map
    
    def _construct_columns(self, column_map):
        
        ''' a helper method for constructing the column objects for a table object '''
        
        from sqlalchemy import Column, String, Boolean, Integer, Float, Binary 
        
        column_args = []
        for key, value in column_map.items():
            record_key = value[0]
            datatype = value[1]
            if record_key == 'id':
                if datatype in ('string', 'float', 'integer'):
                    if datatype == 'string':
                        column_args.insert(0, Column(record_key, String, primary_key=True))
                    elif datatype == 'float':
                        column_args.insert(0, Column(record_key, Float, primary_key=True))
                    elif datatype == 'integer':
                        column_args.insert(0, Column(record_key, Integer, primary_key=True))
                else:
                    raise ValueError('Field "id" in record_schema must be a string, float or integer.')
            else:
                if datatype == 'boolean':
                    column_args.append(Column(record_key, Boolean))
                elif datatype == 'string':
                    column_args.append(Column(record_key, String))
                elif datatype == 'float':
                    column_args.append(Column(record_key, Float))
                elif datatype == 'integer':
                    column_args.append(Column(record_key, Integer))
                elif datatype == 'list':
                    column_args.append(Column(record_key, Binary))
        
        return column_args
        
    def _reconstruct_record(self, record_object):
        
        ''' a helper method for reconstructing record fields from record object '''
        
        record_details = {}
        current_details = record_details
        for key, value in self.model.keyMap.items():
            record_key = key[1:]
            if record_key:
                record_value = getattr(record_object, record_key, None)
                if record_value != None:
                    record_segments = record_key.split('.')
                    for i in range(len(record_segments)):
                        segment = record_segments[i]
                        if i + 1 < len(record_segments):
                            if segment not in record_details.keys():
                                current_details[segment] = {}
                            current_details = current_details[segment]
                        else:
                            if isinstance(record_value, bytes):
                                current_details[segment] = pickle.loads(record_value)
                            else:
                                current_details[segment] = record_value
                    current_details = record_details
                    
        return record_details
    
    def _compare_columns(self, new_columns, old_columns):
        
        ''' a helper method for generating differences between column properties '''
        
        add_columns = {}
        remove_columns = {}
        rename_columns = {}
        retype_columns = {}
        for key, value in new_columns.items():
            if key not in old_columns.keys():
                add_columns[key] = True
                if value[2]:
                    if value[2] in old_columns.keys():
                        rename_columns[key] = value[2]
                        del add_columns[key]
            else:
                if value[1] != old_columns[key][1]:
                    retype_columns[key] = value[1]
        remove_keys = set(old_columns.keys()) - set(new_columns.keys())
        if remove_keys:
            for key in list(remove_keys):
                remove_columns[key] = True
        
        return add_columns, remove_columns, rename_columns, retype_columns
        
    def _rebuild_table(self, new_name, old_name, new_columns, old_columns): 
        
        ''' a helper method for rebuilding table (by renaming & migrating) '''
    
    # verbosity
        print('Rebuilding %s table in %s database' % (self.table_name, self.database_name), end='', flush=True)
        
        from sqlalchemy import Table, MetaData
        metadata_object = MetaData()
    
    # construct old table
        old_table_args = [ old_name, metadata_object ]
        old_column_args = self._construct_columns(old_columns)
        old_table_args.extend(old_column_args)
        old_table = Table(*old_table_args)
    
    # construct new table
        new_table_args = [ new_name, metadata_object ]
        new_column_args = self._construct_columns(new_columns)
        new_table_args.extend(new_column_args)
        new_table = Table(*new_table_args)
    
    # determine differences between tables
        add_columns, remove_columns, rename_columns, retype_columns = self._compare_columns(new_columns, old_columns)
        
    # rename table and recreate table if it doesn't already exist
        table_list = self.engine.table_names()
        if not old_name in table_list:
            self.engine.execute('ALTER TABLE %s RENAME TO %s' % (new_name, old_name))
            new_table.create(self.engine)
    
    # define insert kwarg constructor
        def _construct_inserts(record, new_columns, rename_columns, retype_columns):
            
            insert_kwargs = {}
            
            for key, value in new_columns.items():
            
            # retrieve value for key (or from old key name)
                if key in rename_columns.keys():
                    record_value = getattr(record, rename_columns[key], None)
                else:
                    record_value = getattr(record, key, None)
            
            # attempt to convert datatype
                if record_value:
                    if key in retype_columns.keys():
                        try:
                            old_list = False
                            if isinstance(record_value, bytes):
                                record_value = pickle.loads(record_value)
                                old_list = True
                            if retype_columns[key] == 'boolean':
                                record_value = bool(record_value)
                            elif retype_columns[key] == 'string':
                                if old_list:
                                    record_value = ','.join(record_value)
                                else:
                                    record_value = str(record_value)
                            elif retype_columns[key] == 'integer':
                                if old_list:
                                    record_value = int(record_value[0])
                                else:
                                    record_value = int(record_value)
                            elif retype_columns[key] == 'float':
                                if old_list:
                                    record_value = int(record_value[0])
                                else:
                                    record_value = float(record_value)
                            elif retype_columns[key] == 'list':
                                if isinstance(record_value, str):
                                    record_value = pickle.dumps(record_value.split(','))
                                else:
                                    record_value = pickle.dumps([record_value])
                        except:
                            record_value = None
                
                    insert_kwargs[key] = record_value
            
            return insert_kwargs
            
    # migrate records from old to new
        list_statement = old_table.select()
        count = 0
        for record in self.session.execute(list_statement).fetchall():
            create_kwargs = _construct_inserts(record, new_columns, rename_columns, retype_columns)
            insert_statement = new_table.insert().values(**create_kwargs)
            self.session.execute(insert_statement)
            delete_statement = old_table.delete(old_table.c.id==record.id)
            self.session.execute(delete_statement)
            if not count % 10:
                print('.', end='', flush=True)
            count += 1
            
    # drop old table
        if not self.session.execute(list_statement).first():
            old_table.drop(self.engine)
    
    # handle verbosity   
        print(' done.')
        
        return True
    
    def exists(self, primary_key):
        
        ''' a method to determine if record exists '''
        
        select_statement = self.table.select(self.table).where(self.table.c.id==primary_key)
        record_object = self.session.execute(select_statement).first()
        if record_object:
            return True
        return False
    
    def list(self, query_criteria=None):
        
        '''
            a generator method to list records in table which match query criteria
            
        :param query_criteria: dictionary with schema dot-path field names and query qualifiers 
        :return: generator object with string of primary key
        
        an example of how to construct the query_criteria argument:

        query_criteria = {
            '.path.to.number': {
                'min_value': 4.5
            },
            '.path.to.string': {
                'must_contain': [ '\\regex' ]
            }
        }

        NOTE:   for a full list of operators for query_criteria based upon field
                datatype, see either the query-rules.json file or REFERENCE file for
                the jsonmodel module
                
        # http://collectiveacuity.github.io/jsonModel/reference/#query-criteria
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-filter-operators
        '''
        
        if query_criteria:
            self.model.query(query_criteria)
            
        select_object = self.table.select()
        for key, value in query_criteria.items():
            for k, v in value.items():
                if k == 'discrete_values':
                    column_object = getattr(self.table.c, key[1:])
                    select_object = select_object.where(column_object.in_(v))
        
        print(select_object)
        
        for record in self.session.execute(select_object).fetchall():
            yield record.id
    
    def create(self, record_details): 
    
        '''
            a method to create a new record in the table 
        
            NOTE:   this class uses the id key as the primary key for all records
                    if record_details includes an id field that is an integer, float
                    or string, then it will be used as the primary key. if the id
                    field is missing, a 36 character url safe string will be created
                    for the record and included in the record_details
            
            NOTE:   record_details fields which do not exist in the record_model
                    or whose value do not match the requirements of the record_model
                    will throw an InputValidationError
            
            NOTE:   lists fields are pickled before they are saved to disk and
                    are not possible to search using normal querying. it is
                    recommended that lists be stored instead as separate tables
                    
        :param record_details: dictionary with record fields 
        :return: string with primary key for record
        '''
        
    # validate inputs
        record_details = self.model.validate(record_details)
    
    # add fields to create request
        create_kwargs = {}
        for key, value in self.model.keyMap.items():
            record_key = key[1:]
            if record_key:
                if self.item_key.findall(record_key):
                    pass
                else:
                    if value['value_datatype'] in ('boolean', 'string', 'number'):
                        try:
                            results = self.model._walk(key, record_details)
                            create_kwargs[record_key] = results[0]
                        except:
                            pass
                    elif value['value_datatype'] == 'list':
                        try:
                            results = self.model._walk(key, record_details)
                            create_kwargs[record_key] = pickle.dumps(results[0])
                        except:
                            pass
    
    # add id field if missing     
        if not 'id' in create_kwargs.keys():
            create_kwargs['id'] = self.labID().id36
    
    # insert record into table
        insert_statement = self.table.insert().values(**create_kwargs)
        self.session.execute(insert_statement)
        
        return create_kwargs['id']

    def read(self, primary_key):
    
        ''' a method to retrieve the details for a record in the table '''
        
        title = '%s.read' % self.__class__.__name__
        
    # retrieve record object
        # record_object = self.session.query(self.record).filter_by(id=primary_key).first()
        select_statement = self.table.select(self.table.c.id==primary_key)
        record_object = self.session.execute(select_statement).first()
        if not record_object:
            raise ValueError('%s(primary_key=%s) does not exist.' % (title, primary_key))
        
    # reconstruct record details
        record_details = self._reconstruct_record(record_object)
                    
        return record_details

    def update(self, new_details, old_details):
        
        ''' a method to upsert changes to a record in the table '''
        
        title = '%s.update' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'new_details': new_details,
            'old_details': old_details
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        if new_details['id'] != old_details['id']:
            raise ValueError('%s old_details["id"] value must match new_details["id"]'  % title)
    
    # extract primary key
        primary_key = new_details['id']
        del new_details['id']
        del old_details['id']
    
    # validate new details against record model
        new_details = self.model.validate(new_details)
    
    # determine record differences
        from labpack.parsing.comparison import compare_records
        update_list = compare_records(new_details, old_details)
    
    # construct update keywords
        update_kwargs = {}
        for update in update_list:
            if update['action'] not in ('DELETE', 'REMOVE'):
                current_details = new_details
                save_path = ''
                for segment in update['path']:
                    if save_path:
                        save_path += '.'
                    save_path += segment
                    if isinstance(current_details[segment], dict):
                        current_details = current_details[segment]
                        continue
                    elif isinstance(current_details[segment], list):
                        update_kwargs[save_path] = pickle.dumps(current_details[segment])
                        break
                    else:
                        update_kwargs[save_path] = current_details[segment]
            else:
                current_details = old_details
                save_path = ''
                for segment in update['path']:
                    if save_path:
                        save_path += '.'
                    save_path += segment
                    if isinstance(current_details[segment], dict):
                        current_details = current_details[segment]
                        continue
                    elif isinstance(current_details[segment], list):
                        update_kwargs[save_path] = pickle.dumps(current_details[segment])
                        break
                    else:
                        update_kwargs[save_path] = None
            
    # send update command
        update_statement = self.table.update(self.table.c.id==primary_key).values(**update_kwargs)
        self.session.execute(update_statement)
        
        return primary_key
    
    def delete(self, primary_key):
        
        ''' a method to delete a record in the table '''
        
        title = '%s.delete' % self.__class__.__name__
    
    # delete object
        delete_statement = self.table.delete(self.table.c.id==primary_key)
        self.session.execute(delete_statement)
    
    # return message
        exit_msg = '%s has been deleted.' % primary_key
        return exit_msg
        
    def remove(self):
        
        ''' a method to remove the entire table '''
        
        self.table.drop(self.engine)
        
        exit_msg = '%s table has been removed from %s database.' % (self.table_name, self.database_name)
        return exit_msg

if __name__ == '__main__':
    
    record_schema = {
      'schema': {
        'token_id': '',
        'expires_at': 0.0,
        'service_scope': [''],
        'active': False,
        'address': {
          'number': 0,
          'street': '',
          'city': ''
        },
        'places': ['']
      },
      'components': {
        '.address': {
          'required_field': False
        },
        '.address.number': {
          'integer_data': True
        },
        '.places': {
          'required_field': False
        },
        '.service_scope': {
          'required_field': False
        }
      }
    }
    sql_kwargs = {
        'table_name': 'tokens',
        'database_url': 'sqlite:///../../data/records.db',
        'record_schema': record_schema
    }
    sql_client = sqlClient(**sql_kwargs)
    record_details = { 'token_id': 'unittest', 'places': ['here', 'there'], 'address': {'number': 3, 'city': 'motown' } }
    record_id = sql_client.create(record_details)
    record_details = sql_client.read(record_id)
    print(record_details)
    from copy import deepcopy
    new_details = deepcopy(record_details)
    new_details['address']['street'] = 'construction road'
    new_details['places'].append('everywhere')
    del new_details['address']['number']
    sql_client.update(new_details, record_details)
    print(sql_client.read(record_id))
    for record_id in sql_client.list({'.id':{'discrete_values': ['zZyl9ipT25Id0SfMyvcUUbQts9Br8ONlSjjw']}}):
        print(record_id)
    # exit_msg = sql_client.delete(record_id)
    # print(exit_msg)
    # assert not sql_client.exists(record_id)
    # exit_msg = sql_client.remove()
    # print(exit_msg)