__author__ = 'rcj1492'
__created__ = '2017.12'
__license__ = 'MIT'

'''
alternatives:
https://developer.couchbase.com/documentation/server/4.5/sdk/python/start-using-sdk.html
http://pythonhosted.org/couchbase/index.html
curl http://localhost:4985
'''

from labpack import __module__
import requests

class syncGatewayClient(object):
    
    # https://developer.couchbase.com/documentation/mobile/current/references/sync-gateway/admin-rest-api/index.html
    
    _class_fields = {
        'schema': {
            'bucket_name': '',
            'database_url': '',
            'uid': '',
            'user_password': '',
            'duration': 0,
            'session_id': '',
            'previous_id': '',
            'doc_id': '',
            'rev_id': '',
            'doc_ids': [ '' ],
            'user_roles': [ '' ],
            'user_channels': [ '' ],
            'record_schema': {
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
            '.duration': {
                'integer_data': True,
                'min_value': 0
            },
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
    
    def __init__(self, bucket_name, database_url, record_schema=None, verbose=False, configs=None):

        ''' the initialization method for syncGatewayAdmin class '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/guides/sync-gateway/config-properties/index.html
        # https://developer.couchbase.com/documentation/mobile/current/guides/sync-gateway/sync-function-api-guide/index.html
        
        title = '%s.__init__' % self.__class__.__name__

    # import default sync function
        from os import path
        from importlib.util import find_spec
        module_path = find_spec(__module__).submodule_search_locations[0]
        sync_path = path.join(module_path, 'databases/models/sync_function.js')
        sync_text = open(sync_path).read()
        sync_text = self._update_js(sync_text, record_schema)

    # construct fields
        self._class_fields['components']['.configs.sync']['default_value'] = sync_text
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'bucket_name': bucket_name,
            'database_url': database_url,
            'record_schema': record_schema,
            'configs': configs
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
    # test connection to db
        self.admin_access = True
        try:
            response = requests.get(database_url)
            response = response.json()
            if not 'ADMIN' in response.keys():
                self.admin_access = False
        except:
            raise Exception('%s(database_url="%s") is not a valid couchbase url.' % (title, database_url))
    
    # construct class properties
        from os import path
        self.bucket_name = bucket_name
        self.database_url = database_url
        self.bucket_url = path.join(database_url, bucket_name)
        
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
        if record_schema:
            from jsonmodel.validators import jsonModel
            self.model = jsonModel(record_schema)
        else:
            self.model = jsonModel({'schema': { 'uid': 'abc012XYZ789' }, 'components': {'.': { 'extra_fields': True}}})
        if not 'uid' in self.model.schema.keys():
            record_schema['schema']['uid'] = 'abc012XYZ789'
        if not '.' in self.model.components.keys():
            record_schema['components']['.'] = {}
        if not 'extra_fields' in self.model.components['.'].keys():
            record_schema['components']['.']['extra_fields'] = True
            self.model = jsonModel(record_schema)

    # construct configs
        if configs:
            self.configs = configs
        else:
            default_fields = self.fields.ingest(**{})
            self.configs = default_fields['configs']
            self.configs['bucket'] = self.bucket_name
            self.configs['name'] = self.bucket_name
        
    # construct lab record generator
        from labpack.records.id import labID
        self.labID = labID
    
    # create db (update config) if none exists
        self._update_bucket()
    
    def _update_js(self, js_text, record_schema=None):

        import re
        comment_regex = re.compile('//.*')
        newline_regex = re.compile('\\n')
        js_text = comment_regex.sub('', js_text)
        js_text = newline_regex.sub('', js_text)
        js_text = " ".join(js_text.split())

     # TODO inject data validation from record schema into js_text
        if record_schema:
            pass

        return js_text

    def _update_bucket(self):
    
    # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/database/put__db__
    
    # determine existence of bucket
        bucket_url = self.bucket_url + '/'
        response = requests.get(bucket_url)
        response = response.json()
    
    # handle login errors
        if 'error' in response.keys():
            if not self.admin_access:
                raise Exception('%s.__init__(bucket_name="%s") error: %s' % (self.__class__.__name__, self.bucket_name, str(response)))
    
    # create new bucket
        if not 'db_name' in response.keys():
            if not self.admin_access:
                raise Exception('%s.__init__(bucket_name="%s") does not exist. Bucket creation requires admin access.' % (self.__class__.__name__, self.bucket_name))
            requests.put(bucket_url, json=self.configs)
            self.printer('Bucket "%s" created in database.' % self.bucket_name)
    
    # update configs if there is a change from prior version
        elif self.admin_access:
            config_url = bucket_url + '_config'
            response = requests.get(config_url)
            response = response.json()
            response['sync'] = self._update_js(response['sync'])
            from labpack.parsing.comparison import compare_records
            comparison = compare_records(self.configs, response)
            if comparison:
                if len(comparison) > 1:
                    requests.put(config_url, json=self.configs)
                    self.printer('Configuration updated for bucket "%s".' % self.bucket_name)
                elif comparison[0]['path']:
                    if comparison[0]['path'][0] != 'allow_empty_password':
                        requests.put(config_url, json=self.configs)
                        self.printer('Configuration updated for bucket "%s".' % self.bucket_name)

    def create_view(self, query_criteria=None, uid='_all_users'):
    
        ''' a method to create a view in the bucket to run a query '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/query/put__db___design__ddoc_
        # https://developer.couchbase.com/documentation/server/3.x/admin/Views/views-writing.html
    
        title = '%s.create_view' % self.__class__.__name__
    
    # catch missing args
        if not query_criteria and not uid:
            raise IndexError('%s requires either a uid or query_criteria argument.' % title)
    
    # create a view of all user documents
        else:
            
        # retrieve the design document for the uid
            url = self.bucket_url + '/_design/%s' % uid
            design_details = {
                'views': {}
            }
            response = requests.get(url)
            if response.status_code in (200, 201):
                design_details = response.json()
        
        # create a view of all docs for the uid
            if not query_criteria:
                if uid == '_all_users':
                    pass
                else:
                    function_string = 'function(doc, meta) { if (doc.uid == "%s") { emit(null, null); } }' % uid
                    design_details['views']['_all_docs'] = { 'map': function_string }
            
        # construct a view for a query criteria
            else:
                
            # determine hashed key for criteria
                import hashlib
                from collections import OrderedDict
                ordered_criteria = OrderedDict(**query_criteria)
                hashed_criteria = hashlib.md5(str(ordered_criteria).encode('utf-8')).hexdigest()
            
            # determine function string for criteria
                uid_insert = 'emit();'
                if uid != '_all_users':
                    uid_insert = 'if (doc.uid == "%s") { emit(); }' % uid
                function_string = 'function(doc, meta) { %s }' % uid_insert
                emit_insert = 'emit(null, ['
                count = 0
                for key in ordered_criteria.keys():
                    if count:
                        emit_insert += ','
                    emit_insert += 'doc%s' % key
                emit_insert += ']);'
                function_string.replace('emit();', emit_insert)
            
            # construct updated design details
                design_details['views'][hashed_criteria] = { 'map': function_string}
            
        # send update of design document
            response = requests.put(url, json=design_details)
        
        return response.status_code

    def delete_view(self, query_criteria=None, uid='_all_users'):
    
        '''
            a method to delete a view associated with a user design doc
            
        :param query_criteria: [optional] dictionary with query criteria to be used in list method
        :param uid: [optional] string with uid of design document to update
        :return: integer with status of operation
        
        NOTE:   if a query_criteria is not specified, then the entire user design doc is removed
                otherwise, the existing design document is updated. 
        '''
    # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/query/delete__db___design__ddoc_
    
        title = '%s.delete_view' % self.__class__.__name__
    
    # handle deleting user design doc
        if not query_criteria:
            url = self.bucket_url + '/_design/%s' % uid
            response = requests.delete(url)
    
    # catch missing args
        elif not uid:
            raise IndexError('%s requires either a uid or query_criteria argument.' % title)
    
    # handle removing a view from a design doc
        else:
            
    # determine hash of query criteria
            import hashlib
            from collections import OrderedDict
            ordered_criteria = OrderedDict(**query_criteria)
            hashed_criteria = hashlib.md5(str(ordered_criteria).encode('utf-8')).hexdigest()       
    
    # determine design document to update
            url = self.bucket_url + '/_design/%s' % uid
    
    # remove view from design document and update
            response = requests.get(url)
            if response.status_code in (200, 201):
                design_details = response.json()
                if hashed_criteria in design_details['views'].keys():
                    del design_details['views'][hashed_criteria]
                    if design_details:
                        response = requests.put(url, json=design_details)
                    else:
                        response = requests.delete(url)
    
        return response.status_code

    def list_users(self):
    
        ''' a method to list all the user ids of all users in the bucket '''
        
    # construct url
        url = self.bucket_url + '/_user/'

    # send request and unwrap response
        response = requests.get(url)
        response = response.json()

        return response

    def save_user(self, uid, user_password, user_channels=None, user_roles=None, user_views=None, disable_account=False):

        '''
            a method to add or update an authorized user to the bucket
            
        :param uid: string with id to assign to user
        :param user_password: string with password to assign to user
        :param user_channels: [optional] list of strings with channels to subscribe to user
        :param user_roles: [optional] list of strings with roles to assign to user
        :param user_views: [optional] list of query criteria to create as views for user
        :param disable_account: boolean to disable access to records by user
        :return: integer with status code of user account creation
        '''

    # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/user/put__db___user__name_
    # https://developer.couchbase.com/documentation/mobile/1.5/guides/sync-gateway/authorizing-users/index.html
    
        title = '%s.save_user' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'uid': uid,
            'user_password': user_password,
            'user_channels': user_channels,
            'user_roles': user_roles
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # construct url
        url = self.bucket_url + '/_user/%s' % uid

    # create default settings
        json_data = {
            'admin_channels': [ uid ],
            'admin_roles': [ uid ],
            'name': uid,
            'password': user_password,
            'disabled': disable_account
        }
    
    # add optional additional channels and roles
        if user_channels:
            json_data['admin_channels'].extend(user_channels)
        if user_roles:
            json_data['admin_roles'].extend(user_roles)

    # send request
        response = requests.put(url, json=json_data)

    # create indices
        if response.status_code in (200, 201):
            self.create_view(uid=uid)
            if user_views:
                for criteria in user_views:
                    self.create_view(query_criteria=criteria, uid=uid)

    # report outcome
        self.printer('User "%s" updated in bucket "%s"' % (uid, self.bucket_name))
        
        return response.status_code

    def load_user(self, uid):
    
        '''
            a method to retrieve the account details of a user in the bucket
            
        :param uid: string with id of user in bucket 
        :return: dictionary with account fields for user
        '''
    
        title = '%s.load_user' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'uid': uid
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # construct url
        url = self.bucket_url + '/_user/%s' % uid
        
    # send request and unwrap response
        response = requests.get(url)
        response = response.json()
    
        return response

    def delete_user(self, uid, delete_views=True):
        
        '''
            a method to retrieve the account details of a user in the bucket
            
        :param uid: string with id of user in bucket
        :param delete_views: boolean to remove indices attached to user
        :return: integer with status of delete operation
        '''
    
        title = '%s.delete_user' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'uid': uid
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # delete any existing sessions
        self.delete_sessions(uid)
    
    # delete any existing views
        if delete_views:
            self.delete_view(uid=uid)
            
    # construct url
        url = self.bucket_url + '/_user/%s' % uid

    # send request
        response = requests.delete(url)
    
    # report outcome
        self.printer('User "%s" removed from bucket "%s"' % (uid, self.bucket_name))
        
        return response.status_code

    def create_session(self, uid, duration=0):

        '''
            a method to create a session token for the user
            
        :param uid: string with id of user in bucket
        :param duration: integer with number of seconds to last (default: 24hrs) 
        :return: dictionary with account fields for user
        '''
    
        title = '%s.create_session' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'uid': uid,
            'duration': duration
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
    # construct request fields
        url = self.bucket_url + '/_session'
        json_data = {
            'name': uid
        }
        if duration:
            json_data['ttl'] = duration
    
    # send request and unwrap response
        response = requests.post(url, json=json_data)
        response = response.json()
    
        return response

    def delete_session(self, session_id):
    
        '''
            a method to create a session token for the user
            
        :param session_id: string with id of user session token in bucket
        :return: integer with status code of operation
        '''
        
        title = '%s.delete_session' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'session_id': session_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct url
        url = self.bucket_url + '/_session/%s' % session_id
        
    # send request
        response = requests.delete(url)
        
        return response.status_code

    def delete_sessions(self, uid):
        
        '''
            a method to delete all session tokens associated with a user
            
        :param uid: string with id of user in bucket
        :return: integer with status code of delete operation
        '''
    
        title = '%s.delete_session' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'uid': uid
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct url
        url = self.bucket_url + '/_user/%s/_session' % uid
    
    # send request
        response = requests.delete(url)

        return response.status_code

    def exists(self, doc_id, rev_id=''):
        
        '''
            a method to determine if document exists
            
        :param doc_id: string with id of document in bucket 
        :param rev_id: [optional] string with revision id of document in bucket
        :return: boolean indicating existence of document
        '''

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
        url = self.bucket_url + '/%s' % doc_id
        params = None
        if rev_id:
            params = { 'rev': rev_id }
        response = requests.get(url, params=params)
        if not 'error' in response.json():
            return True
        return False

    def list(self, query_criteria=None, uid='', previous_id=''):
    
        ''' a generator method for retrieving documents from the bucket '''

        title = '%s.list' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'uid': uid,
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
        url = self.bucket_url + '/_all_docs'
        if uid:
            validate_url = self.bucket_url + '/_design/%s' % uid
            response = requests.get(validate_url)
            response = response.json()
            error_message = '%s(uid="%s") requires a bucket index. Try: %s.create_view(uid="%s")' % (title, uid, self.__class__.__name__, uid)
            if 'error' in response.keys():
                raise Exception(error_message)
            elif not '_all_docs' in response['views'].keys():
                raise Exception(error_message)
            url = self.bucket_url + '/_design/%s/_view/_all_docs' % uid

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

        # break off if reached end of records
            if not 'rows' in response_details.keys():
            # TODO fix bug associated with couchbase view declaration
            #     self.printer('BUG: ' + str(response_details))
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

    # define request fields
        from copy import deepcopy
        new_record = deepcopy(doc_details)
        url = self.bucket_url + '/'

    # send request and construct output
        response = requests.post(url, json=new_record)
        if response.status_code not in (200, 201):
            response = response.json()
            raise Exception('%s() error: %s' % (title, response))
        response = response.json()
        new_record['_id'] = response['id']
        new_record['_rev'] = response['rev']
    
        return new_record

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
        url = self.bucket_url + '/%s' % doc_id
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
        url = self.bucket_url + '/%s' % doc_id
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
            
        :param doc_id: string with id of document in bucket 
        :param rev_id: string with revision id of document in bucket
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
        url = self.bucket_url + '/%s' % doc_id
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
        url = self.bucket_url + '/_purge'
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
            a method to remove the entire bucket from the database 

        :return: string with confirmation message 
        '''

        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/database/delete__db__

        title = '%s.remove' % self.__class__.__name__

    # validate admin access
        if not self.admin_access:
            raise Exception('%s requires admin access.' % title)

    # flush files on server
        if self.configs['server'].find('http:') > -1:
            flush_url = self.configs['server'] + '/pools/%s/buckets/%s/controller/doFlush' % (self.configs['pool'], self.bucket_name)
            response = requests.post(flush_url)
            try:
                print(response.json())
            except:
                print(response.status_code)
    
    # delete bucket from configs
        delete_url = self.bucket_url + '/'
        requests.delete(delete_url)
        
    # report outcome
        exit_msg = 'Bucket "%s" removed from database.' % self.bucket_name
        self.printer(exit_msg)
        
        return exit_msg

    def export(self):
        pass

if __name__ == '__main__':

    from time import time
    database_url = 'http://localhost:4985'
    test_bucket = 'test'
    test_user = 'test1'
    test_password = 'password'
    updated_password = 'newPassW0rd'
    new_user = 'test2'
    new_password = 'password2'
    test_doc = { 'uid': 'test1', 'dt': time(), 'place': 'here' }

# test initialization
    test_admin = syncGatewayClient(test_bucket, database_url, verbose=True)
        
# test user methods
    user_list = test_admin.list_users()
    if not test_user in user_list:
        print('first user created')
        test_admin.save_user(test_user, test_password)
    user_load = test_admin.load_user(test_user)
    print(user_load)

# test document methods
    doc_list = []
    for doc in test_admin.list(uid=test_user):
        doc_list.append(doc)
    if not doc_list:
        print('first record created')
        test_admin.create(test_doc)
    doc_list = []
    for doc in test_admin.list(uid=test_user):
        doc_list.append(doc)
    if len(doc_list) < 2:
        print('second record created')
        test_admin.create(test_doc)
    for doc in test_admin.list(uid=test_user):
        print(doc)
        doc['place'] = 'there'
        test_admin.update(doc)
    for doc in test_admin.list(uid=test_user):
        print(doc)
        test_admin.delete(doc['_id'], doc['_rev'])
        test_admin.purge(doc['_id'])
    doc_list = []
    for doc in test_admin.list(uid=test_user):
        doc_list.append(doc)
    
# test second user
    

# test bucket removal
    test_admin.remove()
    
    # test_admin.create({ 'uid': 'test1', 'test': 'you'})
    # test_admin.create({ 'uid': 'test1', 'test': 'me' })
    # test_admin.create({ 'uid': 'test1', 'test': 'them' })
    # for doc in test_admin.list(query_criteria={ '.uid': { 'equal_to': 'test1' } }):
    #     if doc:
    #         doc['test'] = 'us'
    #         response = test_admin.update(doc)
    #         print(response)
    #         doc_id = response['_id']
    #         rev_id = response['_rev']
    #         response = test_admin.delete(doc_id, rev_id)
    #         print(response)
    #         response = test_admin.purge(doc_id)
    #         print(response)
    #     pass
