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

# TODO: sequence integration for integer IDs

class sqlClient(object):
    
    ''' a class of methods for storing json valid records in a sql database '''
    
    _class_fields = {
        'schema': {
            'table_name': 'User Data',
            'database_url': 'sqlite:///../../data/records.db',
            'merge_rule': 'overwrite',
            'record_schema': {
                'schema': {}
            },
            'old_details': {
                'id': None
            },
            'new_details': {
                'id': None
            },
            'order_criteria': [ { } ]
        },
        'components': {
            '.table_name': {
                'max_length': 255,
                'must_not_contain': ['/', '\\.', '-', '^\d']
            },
            '.merge_rule': {
                'discrete_values': [ 'overwrite', 'skip', 'upsert' ]
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
        
        NOTE:   init will automatically update the table schema if the record schema
                differs from the existing table. in order to change the name of a field
                without losing the data associated with the old name, add the old key 
                name to the field's metadata in the schema declaration:
                components['.new_field']['field_metadata']['replace_key'] = '.old_field'
        
        NOTE:   to create a new database, use a tool SQL Workbench
                https://data36.com/install-sql-workbench-postgresql/
                SET AUTOCOMMIT = ON
                create database mydb
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
    
    # define item key pattern
        import re
        self.item_key = re.compile('\[0\]')

    # TODO add method to create database if not there
    # https://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy
        
    # construct database session
        self.engine = create_engine(database_url, echo=verbose)
        self.session = self.engine.connect()
        self.table_name = table_name
        self.database_name = db_file
        self.database_url = database_url
        self.verbose = verbose
        self.database_dialect = sql_dialect
    
    # verify schema criteria 
        for key, value in self.model.keyMap.items():
            if not self.database_dialect in ('sqlite', 'postgres'):
        # verify max length for string fields for certain sql dialects
                if value['value_datatype'] == 'string':
                    if not 'max_length' in value.keys():
                        raise ValueError('%s database requires a "max_length" be declared for string field %s in record_schema.' % (self.database_dialect, key))
        # verify no null datatype declarations
            if value['value_datatype'] == 'null':
                raise ValueError('%s(record_schema={...}) field %s cannot have the null datatype.' % (title, key))
    
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
    
    # construct table metadata
        from sqlalchemy import Table, MetaData
        metadata = MetaData()
    
    # determine if there is a prior table
        migration_complete = True
        prior_name = self.table_name
        table_pattern = '%s_old_\w{24}' % self.table_name
        table_regex = re.compile(table_pattern)
        self.tables = self.engine.table_names()
        for table in self.tables:
            if table_regex.findall(table):
                prior_name = table
                migration_complete = False
                break
        prior_columns = self._extract_columns(prior_name)
        
    # construct new table object
        add_sequence = False
        current_columns = self._parse_columns()
        if not 'id' in current_columns.keys():
            current_columns['id'] = [ 'id', 'string', '', None ]
            if not self.database_dialect in ('sqlite', 'postgres'):
                current_columns['id'] = [ 'id', 'string', '', 24 ]
            self.record_schema['schema']['id'] = ''
            self.model = jsonModel(self.record_schema)
        elif isinstance(current_columns['id'], int):
            if not current_columns['id']:
                add_sequence = True
        table_args = [ self.table_name, metadata ]
    # TODO add sequence for integer ids
    # http://docs.sqlalchemy.org/en/latest/core/defaults.html#sqlalchemy.schema.Sequence
        column_args = self._construct_columns(current_columns)
        table_args.extend(column_args)
        self.table = Table(*table_args)
    
    # process table updates
        if prior_columns:
        
        # determine columns to add, remove, rename and change properties
            add_columns, remove_columns, rename_columns, retype_columns, resize_columns = self._compare_columns(current_columns, prior_columns)
        
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
            if remove_columns or rename_columns or retype_columns or resize_columns:
                if not rebuild:
                    raise ValueError('%s table in %s database must be rebuilt in order to update to desired record_schema. try: rebuild=True' % (self.table_name, self.database_name))
                else:
                    new_name = self.table_name
                    old_name = '%s_old_%s' % (self.table_name, labID().id24.replace('-','_').lower())
                    if not migration_complete:
                        old_name = prior_name
                    self._rebuild_table(new_name, old_name, current_columns, prior_columns)
            
            elif not migration_complete:
                print('Update of %s table previously interrupted...' % self.table_name)
                self._rebuild_table(self.table_name, prior_name, current_columns, prior_columns)
                
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
    
    # add tables property with list of tables in database
        self.tables = self.engine.table_names()
    
    def _extract_columns(self, table_name):
        
        ''' a method to extract the column properties of an existing table '''
        
        import re
        from sqlalchemy import MetaData, VARCHAR, INTEGER, BLOB, BOOLEAN, FLOAT
        from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, BIT, BYTEA
    
    # retrieve list of tables
        metadata_object = MetaData()
        table_list = self.engine.table_names()
    
    # determine columns
        prior_columns = {}
        if table_name in table_list:
            metadata_object.reflect(self.engine)
            existing_table = metadata_object.tables[table_name]
            for column in existing_table.columns:
                column_type = None
                column_length = None
                if column.type.__class__ == FLOAT().__class__:
                    column_type = 'float'
                elif column.type.__class__ == DOUBLE_PRECISION().__class__: # Postgres
                    column_type = 'float'
                elif column.type.__class__ == INTEGER().__class__:
                    column_type = 'integer'
                elif column.type.__class__ == VARCHAR().__class__:
                    column_length = getattr(column.type, 'length', None)
                    if column_length == 1:
                        if column.primary_key:
                            column_length = None
                    column_type = 'string'
                elif column.type.__class__ == BLOB().__class__:
                    column_type = 'list'
                elif column.type.__class__ in (BIT().__class__, BYTEA().__class__):
                    column_type = 'list'
                elif column.type.__class__ == BOOLEAN().__class__:
                    column_type = 'boolean'
                prior_columns[column.key] = (column.key, column_type, '', column_length)
        
        return prior_columns
        
    def _parse_columns(self):
    
        ''' a helper method for parsing the column properties from the record schema '''
        
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
                    max_length = None
                    if 'max_length' in value.keys():
                        max_length = value['max_length']
                    column_map[record_key] = (record_key, datatype, replace_key, max_length)
        
        return column_map
    
    def _construct_columns(self, column_map):
        
        ''' a helper method for constructing the column objects for a table object '''
        
        from sqlalchemy import Column, String, Boolean, Integer, Float, Binary 
    
        column_args = []
        for key, value in column_map.items():
            record_key = value[0]
            datatype = value[1]
            max_length = value[2]
            if record_key == 'id':
                if datatype in ('string', 'float', 'integer'):
                    if datatype == 'string':
                        if max_length:
                            column_args.insert(0, Column(record_key, String(max_length), primary_key=True))
                        else:
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
                    if max_length:
                        column_args.append(Column(record_key, String(max_length)))
                    else:
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
        
        # print(new_columns)
        # print(old_columns)
        
        add_columns = {}
        remove_columns = {}
        rename_columns = {}
        retype_columns = {}
        resize_columns = {}
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
                if value[3] != old_columns[key][3]:
                    resize_columns[key] = value[3]
        remove_keys = set(old_columns.keys()) - set(new_columns.keys())
        if remove_keys:
            for key in list(remove_keys):
                remove_columns[key] = True
        
        return add_columns, remove_columns, rename_columns, retype_columns, resize_columns

    def _construct_inserts(self, record, new_columns, rename_columns, retype_columns, resize_columns):

        ''' a helper method for constructing the insert kwargs for a record '''

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
        
        # attempt to resize string data 
                if key in resize_columns.keys():
                    max_length = resize_columns[key]
                    try:
                        if len(record_value) > max_length:
                            record_value = record_value[0:max_length]
                    except:
                        record_value = None

                insert_kwargs[key] = record_value

        return insert_kwargs
    
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
        add_columns, remove_columns, rename_columns, retype_columns, resize_columns = self._compare_columns(new_columns, old_columns)
        
    # rename table and recreate table if it doesn't already exist
        table_list = self.engine.table_names()
        if not old_name in table_list:
            self.engine.execute('ALTER TABLE %s RENAME TO %s' % (new_name, old_name))
            new_table.create(self.engine)
     
    # wait for renamed table to be responsive
                
    # migrate records from old to new
        list_statement = old_table.select()
        count = 0
        for record in self.session.execute(list_statement).fetchall():
            create_kwargs = self._construct_inserts(record, new_columns, rename_columns, retype_columns, resize_columns)
            insert_statement = new_table.insert().values(**create_kwargs)
            self.session.execute(insert_statement)
            delete_statement = old_table.delete(old_table.c.id==record.id)
            self.session.execute(delete_statement)
            if not count % 10:
                print('.', end='', flush=True)
            count += 1
        
    # drop old table
        record_list = self.session.execute(list_statement).first()
        if not record_list:
            self.session.close()
            old_table.drop(self.engine)
            self.session = self.engine.connect()
    
    # handle verbosity   
        print(' done.')
        
        return True
    
    def exists(self, primary_key):
        
        '''
            a method to determine if record exists
            
        :param primary_key: string with primary key of record 
        :return: boolean to indicate existence of record
        '''
        
        select_statement = self.table.select(self.table).where(self.table.c.id==primary_key)
        record_object = self.session.execute(select_statement).first()
        if record_object:
            return True
        return False
    
    def list(self, query_criteria=None, order_criteria=None):
        
        '''
            a generator method to list records in table which match query criteria
            
        :param query_criteria: dictionary with schema dot-path field names and query qualifiers
        :param order_criteria: list of single keypair dictionaries with field names to order by 
        :return: generator object with string of primary key
        
        an example of how to construct the query_criteria argument:

        query_criteria = {
            '.path.to.number': {
                'min_value': 4.5
            },
            '.path.to.string': {
                'discrete_values': [ 'pond', 'lake', 'stream', 'brook' ]
            }
        }

        NOTE:   sql only supports a limited number of query conditions and all list
                fields in a record are stored as a blob. this method constructs a
                sql query which contains clauses wherever the query conditions can
                be translated one-to-one into sql keywords and returns the entire
                record of each qualifying record. once sql returns its results, the
                remaining query conditions are applied to the record and only those
                results which match all conditions are yield by the generator. as
                such, depending upon the conditions selected, this method acts more
                or less like a SCAN of the entire database. if no sql supported
                conditions are provided, the method will look through all records.
        
                native SQL supported conditions
                
                float, integer & strings:
                    value_exists
                    equal_to
                    discrete_values
                    excluded_values
                    greater_than
                    less_than
                    max_value
                    min_value
                
                booleans:
                    value_exists
                    equal_to
                    
                lists:
                    value_exists
        
        NOTE:   the full list of all criteria are found in the reference page for the
                jsonmodel module as well as the query-rules.json file included in the
                module. 
                http://collectiveacuity.github.io/jsonModel/reference/#query-criteria
        
        an example of how to construct the order_criteria argument:
        
        order_criteria = [
            { '.path.to.number': 'descend' }, 
            { '.path.to.string': '' }
        ]
        
        NOTE:   results can be ordered either by ascending or descending values. to
                order in ascending order, leave the value for the field empty. any value
                for the field key automatically is interpreted as descending order
        
        '''
        
        title = '%s.list' % self.__class__.__name__
        
        from sqlalchemy import desc as order_desc
        
    # validate inputs
        if query_criteria:
            self.model.query(query_criteria)
        else:
            query_criteria = {}
        if order_criteria:
            object_title = '%s(%s=%s)' % (title, 'order_criteria', str(order_criteria))
            self.fields.validate(order_criteria, '.order_criteria', object_title)
            for i in range(len(order_criteria)):
                criterion = order_criteria[i]
                for key, value in criterion.items():
                    criteria_key = key
                    if key.find('.') != 0:
                        criteria_key = '.%s' % key
                    if criteria_key not in self.model.keyMap.keys():
                        raise ValueError('%s(order_criteria=[...]) item %s key %s does not exist in record_schema.' % (title, i, key))
        else:
            order_criteria = []

    # construct select statement with sql supported conditions
    # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-filter-operators
        select_object = self.table.select()
        for key, value in query_criteria.items():
            record_key = key
            map_key = key
            if key.find('.') == 0:
                record_key = key[1:]
            else:
                map_key = '.%s' % key
            if record_key:
                if self.item_key.findall(record_key):
                    pass
                else:
                    test_value = value
                    if not isinstance(value, dict):
                        test_value = { 'equal_to': value }
                    column_object = getattr(self.table.c, record_key)
                    for k, v in test_value.items():
                        if k == 'value_exists':
                            if self.model.keyMap[map_key]['value_datatype'] in ('string', 'number', 'boolean', 'list'):
                                if v:
                                    select_object = select_object.where(column_object!=None)
                                else:
                                    select_object = select_object.where(column_object==None)
                        else:
                            if self.model.keyMap[map_key]['value_datatype'] in ('string', 'number', 'boolean'):
                                if k == 'equal_to':
                                    select_object = select_object.where(column_object==v)
                                elif k == 'discrete_values':
                                    select_object = select_object.where(column_object.in_(v))
                                elif k == 'excluded_values':
                                    select_object = select_object.where(~column_object.in_(v))
                                elif k == 'greater_than':
                                    select_object = select_object.where(column_object.__gt__(v))
                                elif k == 'less_than':
                                    select_object = select_object.where(column_object.__lt__(v))
                                elif k == 'max_value':
                                    select_object = select_object.where(column_object.__le__(v))
                                elif k == 'min_value':
                                    select_object = select_object.where(column_object.__ge__(v))

    # add order criteria
        for criterion in order_criteria:
            key, value = next(iter(criterion.items()))
            record_key = key
            if key.find('.') == 0:
                record_key = key[1:]
            if record_key:
                if self.item_key.findall(record_key):
                    pass
                else:
                    column_object = getattr(self.table.c, record_key)
                    if value:
                        select_object = select_object.order_by(order_desc(column_object))
                    else:
                        select_object = select_object.order_by(column_object)

    # execute query on database
        # print(select_object)
        for record in self.session.execute(select_object).fetchall():
            record_details = self._reconstruct_record(record)

        # filter results with non-sql supported conditions
            if query_criteria:
                if self.model.query(query_criteria, record_details):
                    yield record_details
            else:
                yield record_details
    
    def create(self, record_details): 
    
        '''
            a method to create a new record in the table 
        
            NOTE:   this class uses the id key as the primary key for all records
                    if record_details includes an id field that is an integer, float
                    or string, then it will be used as the primary key. if the id
                    field is missing, a unique 24 character url safe string will be 
                    created for the id field and included in the record_details
            
            NOTE:   record_details fields which do not exist in the record_model
                    or whose value do not match the requirements of the record_model
                    will throw an InputValidationError
            
            NOTE:   lists fields are pickled before they are saved to disk and
                    are not possible to search using sql query statements. it is
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
            create_kwargs['id'] = self.labID().id24
        elif isinstance(create_kwargs['id'], int):
            if not create_kwargs['id']:
                if not self.model.keyMap['.id']['declared_value']:
        # TODO increment record on sequence
                    pass
                    
    # insert record into table
        insert_statement = self.table.insert().values(**create_kwargs)
        self.session.execute(insert_statement)
        
        return create_kwargs['id']

    def read(self, primary_key):
    
        ''' 
            a method to retrieve the details for a record in the table 
            
        :param primary_key: string with primary key of record 
        :return: dictionary with record fields 
        '''
        
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

    def update(self, new_details, old_details=None):
        
        ''' a method to upsert changes to a record in the table
        
        :param new_details: dictionary with updated record fields
        :param old_details: [optional] dictionary with original record fields 
        :return: list of dictionaries with updated field details
        
        NOTE:   if old_details is empty, method will poll database for the
                most recent version of the record with which to compare the
                new details for changes
        '''
        
        title = '%s.update' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'new_details': new_details,
            'old_details': old_details
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if old_details:
            if new_details['id'] != old_details['id']:
                raise ValueError('%s old_details["id"] value must match new_details["id"]'  % title)
    
    # extract primary key
        primary_key = new_details['id']
    
    # # handle missing id
    #     if not '.id' in self.model.keyMap.keys():
    #         del new_details['id']
    #         if old_details:
    #             del old_details['id']
    
    # validate new details against record model
        new_details = self.model.validate(new_details)
            
    # retrieve old record if not specified
        if not old_details:
            try:
                old_details = self.read(primary_key)
            except:
                raise ValueError('%s new_details["id"] does not exist.' % title)
                
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
                for i in range(len(update['path'])):
                    segment = update['path'][i]
                    if save_path:
                        save_path += '.'
                    save_path += segment
                    if update['action'] == 'DELETE' and i + 1 == len(update['path']):
                        update_kwargs[save_path] = None
                    elif isinstance(current_details[segment], dict):
                        current_details = current_details[segment]
                        continue
                    elif isinstance(current_details[segment], list):
                        update_kwargs[save_path] = pickle.dumps(new_details[segment])
                        break
                    else:
                        update_kwargs[save_path] = None
            
    # send update command
        if update_kwargs:
            update_statement = self.table.update(self.table.c.id==primary_key).values(**update_kwargs)
            self.session.execute(update_statement)
        
        return update_list
    
    def delete(self, primary_key):
        
        ''' 
            a method to delete a record in the table
         
        :param primary_key: string with primary key of record 
        :return: string with status message
        '''
        
        title = '%s.delete' % self.__class__.__name__
    
    # delete object
        delete_statement = self.table.delete(self.table.c.id==primary_key)
        self.session.execute(delete_statement)
    
    # return message
        exit_msg = '%s has been deleted.' % primary_key
        return exit_msg
        
    def remove(self):
        
        ''' 
            a method to remove the entire table 
        
        :return string with status message    
        '''
        
        self.table.drop(self.engine)
        
        exit_msg = '%s table has been removed from %s database.' % (self.table_name, self.database_name)
        self.printer(exit_msg)
        
        return exit_msg

    def export(self, sql_client, merge_rule='skip', coerce=False):

        '''
            a method to export all the records in table to another table

        :param sql_client: class object with sql client methods
        :param merge_rule: string with name of rule to adopt for pre-existing records
        :param coerce: boolean to enable migration even if table schemas don't match
        :return: string with exit message

        NOTE:   available merge rules include: overwrite, skip and upsert
        '''

        title = '%s.export' % self.__class__.__name__

    # validate sql client
        method_list = [ 'list', 'create', 'read', 'update', 'delete', 'remove', 'export', 'exists', '_construct_inserts', '_parse_columns', '_compare_columns', 'table', 'session', 'table_name', 'database_name' ]
        for method in method_list:
            if getattr(sql_client, method, None) == None:
                from labpack.parsing.grammar import join_words
                raise ValueError('%s(sql_client=...) must be a client object with %s methods.' % (title, join_words(method_list)))
    
    # verbosity
        export_name = self.table_name
        import_name = sql_client.table_name
        print('Migrating %s table in %s database to %s table in %s database' % (export_name, self.database_name, import_name, sql_client.database_name), end='', flush=True)

    # determine differences between tables
        export_columns = self._parse_columns()
        import_columns = sql_client._parse_columns()
        add_columns, remove_columns, rename_columns, retype_columns, resize_columns = self._compare_columns(import_columns, export_columns)
        if remove_columns or retype_columns or resize_columns:
            if not coerce:
                raise ValueError("Migration from %s to %s prevented because schemas don't match and data could be lost." % (export_name, import_name))

    # define upsert reconstructor
        def _reconstruct_upsert(update_kwargs):
            record_details = {}
            current_details = record_details
            for key, value in update_kwargs.items():
                record_key = key
                record_value = value
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

    # migrate records from old to new
        list_statement = self.table.select()
        count = 0
        added = 0
        skipped = 0
        upserted = 0
        overwritten = 0
        for record in self.session.execute(list_statement).fetchall():
            record_details = self._reconstruct_record(record)
            primary_key = record_details['id']
            if not sql_client.exists(primary_key):
                create_kwargs = self._construct_inserts(record, import_columns, rename_columns, retype_columns, resize_columns)
                insert_statement = sql_client.table.insert().values(**create_kwargs)
                sql_client.session.execute(insert_statement)
                added += 1
            elif merge_rule == 'overwrite':
                sql_client.delete(primary_key)
                create_kwargs = self._construct_inserts(record, import_columns, rename_columns, retype_columns, resize_columns)
                insert_statement = sql_client.table.insert().values(**create_kwargs)
                sql_client.session.execute(insert_statement)
                overwritten += 1
            elif merge_rule == 'skip':
                skipped += 1
            elif merge_rule == 'upsert':
                update_kwargs = self._construct_inserts(record, import_columns, rename_columns, retype_columns, resize_columns)
                update_details = _reconstruct_upsert(update_kwargs)
                sql_client.update(update_details)
                upserted += 1
            count = added + overwritten + skipped + upserted
            if not count % 10:
                print('.', end='', flush=True)

    # handle verbosity
        print(' done.')

    # report outcome
        plural = ''
        skip_insert = ''
        overwrite_insert = ''
        upsert_insert = ''
        if added != 1:
            plural = 's'
        if skipped > 0:
            skip_plural = ''
            if skipped > 1:
                skip_plural = 's'
            skip_insert = ' %s record%s skipped to avoid overwrite.' % (str(skipped), skip_plural)
        if overwritten > 0:
            overwrite_plural = ''
            if overwritten > 1:
                overwrite_plural = 's'
            overwrite_insert = ' %s record%s overwritten.' % (str(overwritten), overwrite_plural)
        if upserted > 0:
            upsert_plural = ''
            if upserted > 1:
                upsert_plural = 's'
            upsert_insert = ' %s record%s upserted.' % (str(upserted), upsert_plural)
        exit_msg = '%s record%s added to %s.%s%s%s' % (str(added), plural, import_name, skip_insert, overwrite_insert, upsert_insert)
        print(exit_msg)

        return count