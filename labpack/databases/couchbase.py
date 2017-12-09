__author__ = 'rcj1492'
__created__ = '2017.12'
__license__ = 'MIT'

# https://developer.couchbase.com/documentation/mobile/1.5/guides/sync-gateway/authorizing-users/index.html
# https://developer.couchbase.com/documentation/mobile/1.5/guides/sync-gateway/config-properties/index.html#1.5/databases-foo_db-server


# sync function
# https://developer.couchbase.com/documentation/mobile/current/guides/sync-gateway/sync-function-api-guide/index.html

# curl http://localhost:4985

# admin_port = '4985'
# db_name = 'lab'
# 
# import requests
# 
# def create_user(user_id, user_password, user_channels=None, user_roles=None):
# 
#     url = 'http://localhost:%s/%s/_user/' % (admin_port, db_name)
#     
#     json_data = {
#         'admin_channels': [ user_id ],
#         'admin_roles': [ user_id ],
#         'name': user_id,
#         'password': user_password,
#         'disabled': False
#     }
#     
#     if user_channels:
#         json_data['admin_channels'].extend(user_channels)
#     if user_roles:
#         json_data['admin_roles'].extend(user_roles)
#     
#     response = requests.post(url, json=json_data)
#     
#     return response.status_code
# 
# def update_user(user_id, user_password, user_channels=None, user_roles=None):
#     
#     url = 'http://localhost:%s/%s/_user/%s' % (admin_port, db_name, user_id)
#     
#     json_data = {
#         'admin_channels': [ user_id ],
#         'admin_roles': [ user_id ],
#         'password': user_password,
#         'disabled': False
#     }
#     
#     if user_channels:
#         json_data['admin_channels'].extend(user_channels)
#     if user_roles:
#         json_data['admin_roles'].extend(user_roles)
#     
#     response = requests.put(url, json=json_data)
#     
#     return response.status_code
#     
# def disable_user(user_id, user_password, user_channels=None, user_roles=None):
#     
#     url = 'http://localhost:%s/%s/_user/%s' % (admin_port, db_name, user_id)
#     
#     json_data = {
#         'admin_channels': [ user_id ],
#         'admin_roles': [ user_id ],
#         'password': user_password,
#         'disabled': True
#     }
#     
#     if user_channels:
#         json_data['admin_channels'].extend(user_channels)
#     if user_roles:
#         json_data['admin_roles'].extend(user_roles)
#     
#     response = requests.put(url, json=json_data)
#     
#     return response.status_code
# 
# def delete_user(user_id):
#     
#     url = 'http://localhost:%s/%s/_user/%s' % (admin_port, db_name, user_id)
#     
#     response = requests.delete(url)
#     
#     return response.status_code
# 
# def get_user(user_id):
#     
#     url = 'http://localhost:%s/%s/_user/%s' % (admin_port, db_name, user_id)
#     
#     response = requests.get(url)
#     
#     return response.json()
# 
# def list_users():
#     
#     url = 'http://localhost:%s/%s/_user/' % (admin_port, db_name)
#     
#     response = requests.get(url)
#     
#     return response.json()
# 
# def create_session(user_id):
#     
#     url = 'http://localhost:%s/%s/_session' % (admin_port, db_name)
#     
#     json_data = {
#         'name': user_id
#     }
#     
#     response = requests.post(url, json=json_data)
#     
#     return response.json()
# 
# def delete_session(session_id):
#     
#    url = 'http://localhost:%s/%s/_session/%s' % (admin_port, db_name, session_id)
#    
#    response = requests.delete(url)
#    
#    return response.status_code
# 
# def delete_sessions(user_id):
#     
#     url = 'http://localhost:%s/%s/_user/%s/_session' % (admin_port, db_name, user_id)
#     
#     response = requests.delete(url)
#     
#     return response.status_code
# 
# def create_design(query_index, json_body):
#     
#     base_url = 'http://localhost:%s/%s/_design/%s' % (admin_port, db_name, query_index)
#     
#     response = requests.put(base_url, json=json_body)
#     
#     return response.status_code
# 
# def create_table_design(user_id, table_name):
# 
#     function_string = 'function(doc, meta) { if (doc.table == "%s" && doc.user_id == "%s") { emit(doc.user_id, doc) } }' % (table_name, user_id)
#     
#     json_body = {
#         "views": {
#             table_name: {
#                 "map": function_string
#             }
#         }
#     }
#     
#     design_doc = read_design('docs')
#     
#     print(design_doc)
#    
# def read_design(query_index):
#     
#     base_url = 'http://localhost:%s/%s/_design/%s' % (admin_port, db_name, query_index)
#     
#     response = requests.get(base_url)
#     
#     return response.json()
# 
#
# 
# def purge_documents(doc_ids):
#     
#     # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/document/post__db___purge
#     
#     if isinstance(doc_ids, str):
#         doc_ids = [ doc_ids ]
#         
#     base_url = 'http://localhost:%s/%s/_purge' % (admin_port, db_name)
#     
#     json_body = {}
#     for doc in doc_ids:
#         json_body[doc] = [ "*" ]
#         
#     response = requests.post(base_url, json=json_body)
#     
#     purged_list = []
#     purged_map = {}
#     response_details = response.json()
#     if 'purged' in response_details.keys():
#         purged_map = response_details['purged']
#     for key in purged_map.keys():
#         purged_list.append(key)
#     
#     return purged_list

'''
alternatives:
https://developer.couchbase.com/documentation/server/4.5/sdk/python/start-using-sdk.html
http://pythonhosted.org/couchbase/index.html
'''
from labpack import __module__
import requests

class syncGatewayClient(object):
    
    # https://developer.couchbase.com/documentation/mobile/current/references/sync-gateway/admin-rest-api/index.html
    _class_fields = {
        'schema': {
            'table_name': '',
            'database_url': '',
            'user_id': '',
            'previous_id': '',
            'doc_id': '',
            'rev_id': '',
            'doc_ids': [ '' ],
            'index_schema': {
                'schema': {}
            },
            'configs': {
                'name': '',
                'bucket': '',
                'pool': '',
                'server': '',
                'allow_empty_password': False,
                'unsupported':{
                    'oidc_test_provider': {},
                    'user_views': {
                      'enabled': False
                    }
                },
                'sync': ''
            }
        },
        'components': {
            '.configs': {
                'extra_fields': True
            },
            '.configs.unsupported': {
                'required_field': False
            },
            '.configs.server': {
                'default_value': 'walrus:/opt/couchbase-sync-gateway/data'
            },
            '.configs.unsupported.oidc_test_provider': {
                'required_field': False,
            },
            '.configs.unsupported.user_views': {
                'required_field': False,
            },
            '.configs.unsupported.user_views.enabled': {
                'default_value': True
            },
            '.configs.sync': {
                'default_value': ''
            },
            '.configs.pool': {
                'default_value': 'default'
            }
        }
    }
    
    def __init__(self, table_name, database_url, index_schema=None, verbose=False, configs=None):

        ''' the initialization method for syncGatewayAdmin class '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/guides/sync-gateway/config-properties/index.html
        
        title = '%s.__init__' % self.__class__.__name__

    # import default sync function
        from os import path
        from importlib.util import find_spec
        module_path = find_spec(__module__).submodule_search_locations[0]
        sync_path = path.join(module_path, 'databases/models/sync_function.js')
        sync_text = open(sync_path).read()
        sync_text = self._clean_js(sync_text)

    # TODO inject data validation into sync text

    # construct fields
        self._class_fields['components']['.configs.sync']['default_value'] = sync_text
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'table_name': table_name,
            'database_url': database_url,
            'index_schema': index_schema,
            'configs': configs
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
    # test connection to db
        try:
            response = requests.get(database_url)
            response = response.json()
            if not 'ADMIN' in response.keys():
                raise Exception('%s(database_url="%s") is not a valid couchbase url.' % (title, database_url))
        except:
            raise Exception('%s(database_url="%s") is not a valid couchbase url.' % (title, database_url))
    
    # construct class properties
        from os import path
        self.table_name = table_name
        self.database_url = database_url
        self.table_url = path.join(database_url, table_name)
        self.admin_access = response['ADMIN']
        
    # construct verbose method
        self.printer_on = True
        def _printer(msg, flush=False):
            if verbose and self.printer_on:
                if flush:
                    print(msg, end='', flush=True)
                else:
                    print(msg)
        self.printer = _printer
    
    # construct index model
        self.model = None
        if index_schema:
            from jsonmodel.validators import jsonModel
            self.model = jsonModel(index_schema)
        else:
            self.model = jsonModel({'schema': { 'user_id': 'abc012XYZ789' }, 'components': {'.': { 'extra_fields': True}}})
        if not 'user_id' in self.model.schema.keys():
            index_schema['schema']['user_id'] = 'abc012XYZ789'
        if not '.' in self.model.components.keys():
            index_schema['components']['.'] = {}
        if not 'extra_fields' in self.model.components['.'].keys():
            index_schema['components']['.']['extra_fields'] = True
            self.model = jsonModel(index_schema)

    # construct configs
        if configs:
            self.configs = configs
        else:
            default_fields = self.fields.ingest(**{})
            self.configs = default_fields['configs']
            self.configs['bucket'] = self.table_name
            self.configs['name'] = self.table_name
        
    # construct lab record generator
        from labpack.records.id import labID
        self.labID = labID
    
    # create db (update config) if none exists
        self._update_table()
    
    def _clean_js(self, js_text):
        
        import re
        comment_regex = re.compile('//.*')
        newline_regex = re.compile('\\n')
        js_text = comment_regex.sub('', js_text)
        js_text = newline_regex.sub('', js_text)
        js_text = " ".join(js_text.split())
        
        return js_text
        
    def _update_table(self):
    
    # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/database/put__db__
    
    # determine existence of table
        table_url = self.table_url + '/'
        response = requests.get(table_url)
        response = response.json()
    
    # create new table
        if not 'db_name' in response.keys():
            if not self.admin_access:
                raise Exception('%s.__init__(table_name="%s") does not exist. Table creation requires admin access.' % (self.__class__.__name__, self.table_name))
            requests.put(table_url, json=self.configs)
            self.printer('Table "%s" created in database.' % self.table_name)
    
    # update configs if there is a change from prior version
        elif self.admin_access:
            config_url = table_url + '_config'
            response = requests.get(config_url)
            response = response.json()
            response['sync'] = self._clean_js(response['sync'])
            from labpack.parsing.comparison import compare_records
            comparison = compare_records(self.configs, response)
            if comparison:
                if len(comparison) > 1:
                    requests.put(config_url, json=self.configs)
                    self.printer('Configuration updated for table "%s".' % self.table_name)
                elif comparison[0]['path']:
                    if comparison[0]['path'][0] != 'allow_empty_password':
                        requests.put(config_url, json=self.configs)
                        self.printer('Configuration updated for table "%s".' % self.table_name)
    
    def _create_index(self, user_id):
    
        ''' a method to create an index in the table to be able to retrieve all documents '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/query/put__db___design__ddoc_
        # https://developer.couchbase.com/documentation/server/3.x/admin/Views/views-writing.html
        
    # compose function string
        function_string = 'function(doc, meta) { if (doc.user_id == "%s") { emit(null, null); } }' % user_id

    # compose json body
        json_body = {
            "views": {
                'all': {
                    "map": function_string
                }
            }
        }

    # compose request url
        url = self.table_url + '/_design/%s' % user_id
    
    # create index if not existing
        response = requests.get(url)
        if response.status_code == 404:
            response = requests.put(url, json=json_body)
        else:
            response_details = response.json()
            if 'all' not in response_details['views'].keys():
                response_details['views']['all'] = { 'map': function_string }
                response = requests.put(url, json=response_details)

        return response.status_code

    def add_user(self, user_id):
        pass
    
    def update_password(self, user_id):
        pass
    
    def disable_user(self, user_id):
        pass
        
    def exists(self, doc_id, rev_id=''):
        
        title = '%s.exists' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'doc_id': doc_id,
            'rev_id': rev_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # send request and construct response
        url = self.table_url + '/%s' % doc_id
        params = None
        if rev_id:
            params = { 'rev': rev_id }
        response = requests.get(url, params=params)
        if not 'error' in response.json():
            return True
        return False

    def list(self, user_id='', query_criteria=None, previous_id=''):
    
        ''' a generator method for retrieving documents from the table '''

        title = '%s.list' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'user_id': user_id,
            'previous_id': previous_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate inputs
        if query_criteria:
            self.model.query(query_criteria)
        else:
            query_criteria = {}

    # determine index to use
        url = self.table_url + '/_all_docs'
        if user_id:
            validate_url = self.table_url + '/_design/%s' % user_id
            response = requests.get(validate_url)
            response = response.json()
            error_message = '%s(user_id="%s") requires a table index. Try: %s._create_index(%s)' % (title, user_id, self.__class__.__name__, user_id)
            if 'error' in response.keys():
                raise Exception(error_message)
            elif not 'all' in response['views'].keys():
                raise Exception(error_message)
            url = self.table_url + '/_design/%s/_view/all' % user_id

    # determine query params
        params = {
            'limit': 101,
            'revs': True
        }
        if previous_id:
            params['startkey'] = previous_id
        break_off = False

    # send request
        while True:
            response = requests.get(url, params=params)

        # report records
            response_details = response.json()

        # TODO fix bug associated with couchbase view declaration
            if not 'rows' in response_details.keys():
                self.printer('BUG: ' + str(response_details))
                break

            else:
                if not response_details['rows']:
                    break
                for i in range(len(response_details['rows'])):
    
                # skip previous key
                    if not 'startkey' in params.keys() or i:
                        row = response_details['rows'][i]
                        doc_details = self.read(row['id'])
                        params['startkey'] = row['id']
    
                    # filter results with query criteria
                        if not doc_details:
                            self.purge(row['id']) # eliminate stranded records
                        else:
                            if query_criteria:
                                if self.model.query(query_criteria, doc_details):
                                    yield doc_details
                            else:
                                yield doc_details
    
                # end if no more results
                    elif len(response_details['rows']) == 1:
                        break_off = True
                        break
            if break_off:
                break

    def create(self, doc_details):

        '''
            a method to create a new document in the collection

        :param doc_details: dictionary with document details and user id value
        :return: dictionary with document details and _id and _rev values
        '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/document/post__db___doc_

        title = '%s.create' % self.__class__.__name__

    # validate input
        doc_details = self.model.validate(doc_details, object_title='%s(doc_details={...}' % title)

    # define url
        url = self.table_url + '/'

    # send request and construct output
        response = requests.post(url, json=doc_details)
        response = response.json()
        doc_details['_id'] = response['id']
        doc_details['_rev'] = response['rev']
    
        return doc_details

    def read(self, doc_id, rev_id=''):
    
        title = '%s.read' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'doc_id': doc_id,
            'rev_id': rev_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # send request and construct response
        url = self.table_url + '/%s' % doc_id
        params = None
        if rev_id:
            params = { 'rev': rev_id }
        response = requests.get(url, params=params)
        response = response.json()
        if 'error' in response.keys():
            response = {}

        return response

    def update(self, doc_details):
        
        title = '%s.update' % self.__class__.__name__
        
    # validate input
        doc_details = self.model.validate(doc_details, object_title='%s(doc_details={...}' % title)
        
    # create json body
        doc_id = ''
        rev_id = ''
        json_body = {}
        for key, value in doc_details.items():
            if key not in ('_id', '_rev'):
                json_body[key] = value
            elif key == '_id':
                doc_id = value
            elif key == '_rev':
                rev_id = value
    
    # validate existence of doc and rev IDs
        if not doc_id or not rev_id:
            raise Exception('%s(doc_details={...} must contain _id and _rev fields.' % title)

    # send request and construct response
        url = self.table_url + '/%s' % doc_id
        params = { 'rev': rev_id }
        response = requests.put(url, params=params, json=json_body)
        response = response.json()
        if 'error' in response.keys():
            doc_details = {}
        else:
            doc_details['_id'] = response['id']
            doc_details['_rev'] = response['rev']

        return doc_details

    def delete(self, doc_id, rev_id):
    
        '''
            a method to mark a document for deletion
            
        :param doc_id: string with id of document in table 
        :param rev_id: string with revision id of document in table
        :return: string with id of deleted document
        '''
        
        title = '%s.delete' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'doc_id': doc_id,
            'rev_id': rev_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
            
    # send request and construct response
        url = self.table_url + '/%s' % doc_id
        params = { 'rev': rev_id }
        response = requests.delete(url, params=params)
        response = response.json()
        if 'error' in response.keys():
            doc_id = ''
        else:
            doc_id = response['id']
        
        return doc_id

    def purge(self, doc_ids):

        '''
            a method to remove docs from the collection
            
        :param doc_ids: string or list of strings with document ids to purge 
        :return: list of strings of doc ids purged
        '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/document/post__db___purge
    
        title = '%s.purge' % self.__class__.__name__
        
    # ingest arguments
        if isinstance(doc_ids, str):
            doc_ids = [ doc_ids ]
        
    # validate inputs
        input_fields = {
            'doc_ids': doc_ids
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct request fields
        url = self.table_url + '/_purge'
        json_body = {}
        for doc in doc_ids:
            json_body[doc] = [ "*" ]
    
    # send request 
        response = requests.post(url, json=json_body)

    # construct output from response
        purged_list = []
        purged_map = {}
        response_details = response.json()
        if 'purged' in response_details.keys():
            purged_map = response_details['purged']
        for key in purged_map.keys():
            purged_list.append(key)
        
        return purged_list
    
    def remove(self):

        '''
            a method to remove the entire table from the database 

        :return: string with confirmation message 
        '''

        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/database/delete__db__

        table_url = self.table_url + '/'
        requests.delete(table_url)
        
        exit_msg = 'Table "%s" removed from database.' % self.table_name
        self.printer(exit_msg)
        
        return exit_msg

    def export(self):
        pass

if __name__ == '__main__':

    database_url = 'http://localhost:4985'
    table_name = 'lab'

    lab_admin = syncGatewayClient(table_name, database_url, verbose=True)
    lab_admin.create({ 'user_id': 'test1', 'test': 'you'})
    lab_admin.create({ 'user_id': 'test1', 'test': 'me' })
    lab_admin.create({ 'user_id': 'test1', 'test': 'them' })
    for doc in lab_admin.list(query_criteria={ '.user_id': { 'equal_to': 'test1' } }):
        if doc:
            doc['test'] = 'us'
            response = lab_admin.update(doc)
            print(response)
            doc_id = response['_id']
            rev_id = response['_rev']
            response = lab_admin.delete(doc_id, rev_id)
            print(response)
            response = lab_admin.purge(doc_id)
            print(response)
