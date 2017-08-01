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
            'collection_name': 'User Data',
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
            '.collection_name': {
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
    
    def __init__(self, collection_name, database_url, record_schema, verbose=False):
        
        title = '%s.__init__' % self.__class__.__name__
        
    # construct fields
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'collection_name': collection_name,
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
    
    # construct record model
        self.model = jsonModel(record_schema)
                
    # construct database session
        self.engine = create_engine(database_url, echo=verbose)
        self.session = self.engine.connect()
        self.collection_name = collection_name
        self.database_name = db_file
    
    # # ORM construct
    #     from sqlalchemy.orm import sessionmaker
    #     from sqlalchemy.ext.declarative import declarative_base
    #     self.engine = create_engine(database_url, echo=verbose)
    #     dbSession = sessionmaker(bind=self.engine)
    #     self.session = dbSession()
    #     self.base = declarative_base()
    #     class RecordObject(self.base):
    #         __tablename__ = collection_name
    #         id = Column(String, primary_key=True)
    #     self.base.metadata.create_all(self.engine)
    
    # construct lab id class
        from labpack.records.id import labID
        self.labID = labID
    
    # construct table metadata storage object
        from sqlalchemy import Column, String, Boolean, Integer, Float, Binary, Table, MetaData
        metadata = MetaData()
    
    # define table fields
        import re
        self.list_key = re.compile('\[0\]')
        table_args = [ self.collection_name, metadata, Column('id', String, primary_key=True) ]
        for key, value in self.model.keyMap.items():
            record_key = key[1:]
            if record_key:
                if self.list_key.findall(record_key):
                    pass
                elif record_key == 'id':
                    if value['value_datatype'] == 'string':
                        table_args[2] = Column(record_key, String, primary_key=True)
                    elif value['value_datatype'] == 'number':
                        column_value = Column(record_key, Float, primary_key=True)
                        if 'integer_data' in value.keys():
                            if value['integer_data']:
                                column_value = Column(record_key, Integer, primary_key=True)
                        table_args[2] = column_value
                else:
                    if value['value_datatype'] == 'boolean':
                        table_args.append(Column(record_key, Boolean))
                    elif value['value_datatype'] == 'string':
                        table_args.append(Column(record_key, String))
                    elif value['value_datatype'] == 'number':
                        column_value = Column(record_key, Float)
                        if 'integer_data' in value.keys():
                            if value['integer_data']:
                                column_value = Column(record_key, Integer)
                        table_args.append(column_value)
                    elif value['value_datatype'] == 'list':
                        table_args.append(Column(record_key, Binary))
    
    # TODO, update table with new columns
    # https://sqlalchemy-migrate.readthedocs.io/en/latest/
    # http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table.drop
                        
    # construct table object and add to database
        self.table = Table(*table_args)
        if not self.table.exists(self.engine):
            print('%s table created in %s database.' % (self.collection_name, self.database_name))
            self.table.create(self.engine)
    
    def exists(self, primary_key):
        
        ''' a method to determine if record exists '''
        
        select_statement = self.table.select(self.table).where(self.table.c.id==primary_key)
        record_object = self.session.execute(select_statement).first()
        if record_object:
            return True
        return False
        
    def create(self, record_details): 
    
        '''
            a method to create a new record in the collection 
        
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
                    recommended that lists be stored instead as separate collections
                    
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
                if self.list_key.findall(record_key):
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
    
        ''' a method to retrieve the details for a record in the collection '''
        
        title = '%s.read' % self.__class__.__name__
        
    # retrieve record object
        # record_object = self.session.query(self.record).filter_by(id=primary_key).first()
        select_statement = self.table.select(self.table).where(self.table.c.id==primary_key)
        record_object = self.session.execute(select_statement).first()
        if not record_object:
            raise ValueError('%s(primary_key=%s) does not exist.' % (title, primary_key))
        
    # reconstruct record details
        record_details = { 'id': record_object.id }
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

    def update(self, new_details, old_details):
        
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
        update_statement = self.table.update().where(self.table.c.id==primary_key).values(**update_kwargs)
        self.session.execute(update_statement)
        
        return primary_key
    
    def delete(self, primary_key):
        
        ''' a method to delete a record in the collection '''
        
        title = '%s.delete' % self.__class__.__name__
    
    # delete object
        delete_statement = self.table.delete().where(self.table.c.id==primary_key)
        self.session.execute(delete_statement)
    
    # return message
        exit_msg = '%s has been deleted.' % primary_key
        return exit_msg
        
    def remove(self):
        
        ''' a method to remove the entire collection '''
        
        self.table.drop(self.engine)
        
        exit_msg = '%s table has been removed from %s database.' % (self.collection_name, self.database_name)
        return exit_msg
        
if __name__ == '__main__':
    
    record_schema = {
      'schema': {
        'token_id': '',
        'expires_at': 0,
        'service_scope': '',
        'active': False,
        'address': {
          'number': 0,
          'street': ''
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
        }
      }
    }
    sql_kwargs = {
        'collection_name': 'tokens',
        'database_url': 'sqlite:///../../data/records.db',
        'record_schema': record_schema
    }
    sql_client = sqlClient(**sql_kwargs)
    record_details = { 'token_id': 'unittest', 'places': ['here', 'there'], 'address': {'number': 3 } }
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
    exit_msg = sql_client.delete(record_id)
    print(exit_msg)
    assert not sql_client.exists(record_id)
    exit_msg = sql_client.remove()
    print(exit_msg)