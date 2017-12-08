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

import requests

class syncGatewayAdmin(object):
    
    # https://developer.couchbase.com/documentation/mobile/current/references/sync-gateway/admin-rest-api/index.html
    
    def __init__(self, table_name, database_url, **configs):

        ''' the initialization method for syncGatewayAdmin class '''
        
        title = '%s.__init__' % self.__class__.__name__
        
        self.table_name = table_name
        self.database_url = database_url
        self.table_url = database_url + '/%s' % table_name
        self.configs = {}
        for key, value in configs.items():
            self.configs[key] = value

    # test connection to db
        try:
            response = requests.get(self.database_url)
            response = response.json()
            print(response)
        except:
            raise '%s is not a valid couchbase url.' % database_url
        
    # create db (update config) if none exists
    
    def _update_config(self):
    
    # retrieve config from db
        
    # construct default sync function
    
    # construct default config
    
    # update defaults
    
        pass
    
    def _create_index(self, user_id=''):
    
        ''' a method to create an index in the table to be able to retrieve all documents '''
        
        # https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html#/query/put__db___design__ddoc_
        # https://developer.couchbase.com/documentation/server/3.x/admin/Views/views-writing.html
        
    # compose function string
        function_string = 'function(doc, meta) { emit(null, null); }'
        if user_id:
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
        index = 'all'
        if user_id:
            index = user_id
        url = self.table_url + '/_design/%s' % index
    
    # create index if not existing
        response = requests.get(url)
        if response.status_code == 404:
            response = requests.put(url, json=json_body)
    
        return response.status_code

    def create_user(self, user_id):
        pass
    
    def update_user(self, user_id):
        pass
    
    def exists(self, doc_id):
        
        return True
    
    def create(self, doc_details):
        
        return True
    
    def read(self, doc_id):

        url = self.table_url + '/%s' % doc_id

        response = requests.get(url)
    
        return response.json()

    def update(self, doc_details):
        pass
    
    def delete(self, doc_id):
        pass
    
    def list(self, user_id='', full_document=False):
    
        ''' a generator method '''
        
    # determine index quality
        index = 'all'
        if user_id:
            index = user_id
    
    # construct url
        url = self.table_url + '/_design/%s/_view/all' % index

    # send request
        response = requests.get(url)
    
    # interpret response
        response_details = response.json()
        doc_list = []
        for row in response_details['rows']:
            if full_document:
                doc_details = self.read(row['id'])
                doc_list.append(doc_details)
            else:
                doc_list.append(row['id'])
    
        return doc_list

    
if __name__ == '__main__':
    
    database_url = 'http://localhost:4985'
    table_name = 'lab'
    
    lab_admin = syncGatewayAdmin(table_name, database_url)
    doc_list = lab_admin.list(full_document=True)
    print(doc_list)
