# Classes

## cassandraSession
### Import:
labpack.databases.cassandra.cassandraSession  
### Description:
a class of methods for creating a session to a cassandra database

    CQL Connector
    https://datastax.github.io/python-driver/getting_started.html
    https://flask-cqlalchemy.readthedocs.io/en/latest/
    https://datastax.github.io/python-driver/cqlengine/third_party.html

    Authentication
    https://datastax.github.io/python-driver/api/cassandra/auth.html#
    https://cassandra.apache.org/doc/latest/operating/security.html#enabling-password-authentication  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, hostname, port=9042, username="", password="", cert_path="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>hostname  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>port      </td><td>int     </td><td>          </td><td>9042     </td><td>             </td></tr>
<tr><td>username  </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>password  </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>cert_path </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
</tbody>
</table>

## cassandraTable
### Import:
labpack.databases.cassandra.cassandraTable  
### Description:
a class of methods for interacting with a table on cassandra

    CQL Connector
    https://datastax.github.io/python-driver/getting_started.html
    https://cassandra.apache.org/doc/latest/cql/dml.html

    NOTE:   WIP  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, keyspace_name, table_name, record_schema, cassandra_session, replication_strategy=None)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument            </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self                </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>keyspace_name       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>table_name          </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>record_schema       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>cassandra_session   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>replication_strategy</td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## DatastoreTable
### Import:
labpack.databases.google.datastore.DatastoreTable  
### Description:
a class to store json valid records as tabular style in google datastore

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
        does not create null values for empty fields. if an empty
        map is declared in the record schema, any data in that field
        of a record is stringified and unindexable.

        the most space efficient setup will not have any indices and
        will use the value of the record id as the main query method
        and/or will allow datastore to generate an id automatically
        
        LIMITS:
        https://cloud.google.com/datastore/docs/concepts/limits
        
        REFERENCES:
        https://googleapis.dev/python/datastore/latest/index.html 
        https://cloud.google.com/datastore/docs/concepts/entities  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, datastore_client, table_name, record_schema, indices=None, default_values=False, verbose=False)
##### 
**Description:**  
the initialization method for the sqlClient class  
<table>
<thead>
<tr><th>Argument        </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>datastore_client</td><td>object</td><td>Yes       </td><td>None     </td><td>datastore.Client object                                </td></tr>
<tr><td>table_name      </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with name for table of records                  </td></tr>
<tr><td>record_schema   </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with jsonmodel valid schema for records     </td></tr>
<tr><td>indices         </td><td>list  </td><td>          </td><td>None     </td><td>list of strings with fields to index                   </td></tr>
<tr><td>default_values  </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to add default values to records    </td></tr>
<tr><td>verbose         </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable database logging to stdout</td></tr>
</tbody>
</table>

### exists
##### 
**Signature:**  
exists(self, record_id)
##### 
**Description:**  
a method to determine if record exists  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                          </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                     </td></tr>
<tr><td>record_id </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with id associated with record</td></tr>
</tbody>
</table>

### list
##### 
**Signature:**  
list(self, filter=None, sort=None, limit=100, cursor="", ids_only=False)
##### 
**Description:**  
a method to retrieve records using criteria evaluated on table indexes

        NOTE:   only fields which have been added to the indices argument at object
                construction can be queried in-memory by Datastore and if an index
                is added after records are in the database, records previously added
                to the datastore are not automatically added to the index. to make
                sure that all records are properly indexed, you must run
                _update_indices
                WARNING: although _update_indices is an optimized SCAN of Datastore,
                it could be very costly

        NOTE:   composite indices allow for more complex queries in-memory
                but must be registered with Datastore using gcloud client
                and specified as index.yaml in app root and built before 
                https://cloud.google.com/datastore/docs/concepts/indexes  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                   </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                              </td></tr>
<tr><td>filter    </td><td>dict  </td><td>          </td><td>None     </td><td>dictionary of dot path field name and jsonmodel query criteria</td></tr>
<tr><td>sort      </td><td>list  </td><td>          </td><td>None     </td><td>list of single key-pair dictionaries with dot path field names</td></tr>
<tr><td>limit     </td><td>int   </td><td>          </td><td>100      </td><td>integer with number of results to return                      </td></tr>
<tr><td>cursor    </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>string base64 url safe encoded with location of last result   </td></tr>
<tr><td>ids_only  </td><td>bool  </td><td>          </td><td>False    </td><td>boolean to enable return of only ids (reduces &#x27;read&#x27; use to 1)</td></tr>
</tbody>
</table>

### create
##### 
**Signature:**  
create(self, record)
##### 
**Description:**  
a method to create a new record in the table

            NOTE:   this class uses the id field as the primary key for all records
                    if record includes an id field that is an integer, float
                    or string, then it will be used as the primary key. 

            NOTE:   if the id field is missing, a unique 24 character url safe 
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
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>record    </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with record fields</td></tr>
</tbody>
</table>

### read
##### 
**Signature:**  
read(self, record_id)
##### 
**Description:**  
a method to retrieve the details for a record in the table  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>record_id </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string or number with unique identifier of record</td></tr>
</tbody>
</table>

### update
##### 
**Signature:**  
update(self, record)
##### 
**Description:**  
a method to update an existing record  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>record    </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with record fields</td></tr>
</tbody>
</table>

### delete
##### 
**Signature:**  
delete(self, record_id)
##### 
**Description:**  
a method to delete an existing record  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>record_id </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string or number with unique identifier of record</td></tr>
</tbody>
</table>

### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove all records in table  

### export
##### 
**Signature:**  
export(self, datastore_table, merge_rule="skip", coerce=False)
##### 
**Description:**  
TODO a method to export all the records to another datastore table  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>datastore_table</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>merge_rule     </td><td>str     </td><td>          </td><td>&quot;skip&quot;   </td><td>             </td></tr>
<tr><td>coerce         </td><td>bool    </td><td>          </td><td>False    </td><td>             </td></tr>
</tbody>
</table>

## SQLSession
### Import:
labpack.databases.sql.SQLSession  
### Description:
the initialization method for the SQLSession class  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, database_url, verbose=False)
##### 
**Description:**  
the initialization method for the SQLSession class  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>database_url</td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with unique resource identifier to database     </td></tr>
<tr><td>verbose     </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable database logging to stdout</td></tr>
</tbody>
</table>

## SQLTable
### Import:
labpack.databases.sql.SQLTable  
### Description:
a class to store json valid records in a sql database 
    
    REFERENCES:
    https://docs.sqlalchemy.org/en/13/core/tutorial.html  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, sql_session, table_name, record_schema, rebuild=True, default_values=False, verbose=False)
##### 
**Description:**  
the initialization method for the SQLTable class  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>sql_session   </td><td>object</td><td>Yes       </td><td>None     </td><td>sql.SQLSession object                                  </td></tr>
<tr><td>table_name    </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with name for table of records                  </td></tr>
<tr><td>record_schema </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with jsonmodel valid schema for records     </td></tr>
<tr><td>rebuild       </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to rebuild table with schema changes</td></tr>
<tr><td>default_values</td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to add default values to records    </td></tr>
<tr><td>verbose       </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable database logging to stdout</td></tr>
</tbody>
</table>

### exists
##### 
**Signature:**  
exists(self, record_id)
##### 
**Description:**  
a method to determine if record exists  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>record_id </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string or number with unique identifier of record</td></tr>
</tbody>
</table>

### list
##### 
**Signature:**  
list(self, filter=None, sort=None, limit=100, cursor="", ids_only=False)
##### 
**Description:**  
a method to retrieve records from table which match query criteria  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                   </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                              </td></tr>
<tr><td>filter    </td><td>dict  </td><td>          </td><td>None     </td><td>dictionary of dot path field name and jsonmodel query criteria</td></tr>
<tr><td>sort      </td><td>list  </td><td>          </td><td>None     </td><td>list of single key-pair dictionaries with dot path field names</td></tr>
<tr><td>limit     </td><td>int   </td><td>          </td><td>100      </td><td>integer with number of results to return                      </td></tr>
<tr><td>cursor    </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>string form of integer with offset to continue query          </td></tr>
<tr><td>ids_only  </td><td>bool  </td><td>          </td><td>False    </td><td>boolean to enable return of only ids (reduces &#x27;read&#x27; use to 1)</td></tr>
</tbody>
</table>

### create
##### 
**Signature:**  
create(self, record)
##### 
**Description:**  
a method to create a new record in the table 

            NOTE:   this class uses the id key as the primary key for all records
                    if record includes an id field that is an integer, float
                    or string, then it will be used as the primary key. if the id
                    field is missing, a random 64 bit integer (if a number) or a
                    unique 24 character url safe string (if a string) will be 
                    created for the id field and included in the record

            NOTE:   record fields which do not exist in the record_schema or whose
                    value do not match the requirements of the record_schema
                    will throw an InputValidationError

            NOTE:   lists fields are pickled before they are saved to disk and
                    are not possible to search using sql query statements. it is
                    recommended that lists be stored instead as separate tables

            NOTE:   if a map field is declared as empty in the record_schema, then
                    all record fields inside it will be pickled before the
                    record is saved to disk and are not possible to search  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>record    </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with record fields</td></tr>
</tbody>
</table>

### read
##### 
**Signature:**  
read(self, record_id)
##### 
**Description:**  
a method to retrieve the details for a record in the table  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>record_id </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string or number with unique identifier of record</td></tr>
</tbody>
</table>

### update
##### 
**Signature:**  
update(self, updated, original=None)
##### 
**Description:**  
a method to update changes to a record in the table  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>updated   </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with updated record fields            </td></tr>
<tr><td>original  </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with original record fields</td></tr>
</tbody>
</table>

### delete
##### 
**Signature:**  
delete(self, record_id)
##### 
**Description:**  
a method to delete a record in the table  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>record_id </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string or number with unique identifier of record</td></tr>
</tbody>
</table>

### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove the entire table 

        :return string with status message  

### export
##### 
**Signature:**  
export(self, sql_table, merge_rule="skip", coerce=False)
##### 
**Description:**  
a method to export all the records in table to another sql table  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                             </td></tr>
<tr><td>sql_table </td><td>type  </td><td>Yes       </td><td>None     </td><td>class object with sql table methods                          </td></tr>
<tr><td>merge_rule</td><td>str   </td><td>          </td><td>&quot;skip&quot;   </td><td>string with name of rule to adopt for pre-existing records   </td></tr>
<tr><td>coerce    </td><td>bool  </td><td>          </td><td>False    </td><td>boolean to enable migration even if table schemas don&#x27;t match</td></tr>
</tbody>
</table>

## labMagic
### Import:
labpack.parsing.magic.labMagic  
### Description:
initialization method for labMagic class  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, magic_file="")
##### 
**Description:**  
initialization method for labMagic class  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                   </td></tr>
<tr><td>magic_file</td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with local path to magic.mgc file</td></tr>
</tbody>
</table>

### analyze
##### 
**Signature:**  
analyze(self, file_path="", file_url="", byte_data=None)
##### 
**Description:**  
a method to determine the mimetype and extension of a file from its byte data  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                         </td></tr>
<tr><td>file_path </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with local path to file</td></tr>
<tr><td>file_url  </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with url of file       </td></tr>
<tr><td>byte_data </td><td>NoneType</td><td>          </td><td>None     </td><td>[optional] byte data from a file         </td></tr>
</tbody>
</table>

## labRegex
### Import:
labpack.parsing.regex.labRegex  
### Description:
instantiates class with a regular expression dictionary  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self, regex_schema, override=False)
##### 
**Description:**  
instantiates class with a regular expression dictionary  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>regex_schema</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with regular expression name, pattern key-pairs     </td></tr>
<tr><td>override    </td><td>bool  </td><td>          </td><td>False    </td><td>boolean to ignore value errors raised from regex name conflicts</td></tr>
</tbody>
</table>

### map
##### 
**Signature:**  
map(self, string_input, n_grams=1)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument    </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>string_input</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>n_grams     </td><td>int     </td><td>          </td><td>1        </td><td>             </td></tr>
</tbody>
</table>

## labID
### Import:
labpack.records.id.labID  
### Description:
a class of methods for uniquely identifying objects

        build-in methods:
            self.uuid: uuid1 uuid object
            self.id12: 12 character base 64 url safe string of posix time
            self.id24: 24 character base 64 url safe string of md5 hash of uuid1
            self.id36: 36 character base 64 url safe string of sha1 hash of uuid1
            self.id48: 48 character base 64 url safe string of sha256 hash of uuid1
            self.mac: string of mac address of device
            self.epoch: current posix epoch timestamp with micro second resolution
            self.iso: current iso utc datetime string
            self.datetime: current python datetime  

### \_\_init__
##### 
**Signature:**  
\_\_init__(self)
##### 
**Description:**  
a method to initialize a unique ID based upon the UUID1 method  

## labDT
### Import:
labpack.records.time.labDT  
### Description:
a class of methods for datetime conversion

    for list of timezones:
        https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones
    for list of datetime directives:
        https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior  

### new
##### 
**Signature:**  
new(cls)
##### 
**Description:**  
a method to generate the current datetime as a labDT object  

### zulu
##### 
**Signature:**  
zulu(self)
##### 
**Description:**  
a method to report ISO UTC datetime string from a labDT object

        NOTE: for timezone offset string use .isoformat() instead  

### epoch
##### 
**Signature:**  
epoch(self)
##### 
**Description:**  
a method to report posix epoch timestamp from a labDT object  

### rfc2822
##### 
**Signature:**  
rfc2822(self)
##### 
**Description:**  
a method to report a RFC-2822 Compliant Date from a labDT object

            https://tools.ietf.org/html/rfc2822.html#page-14  

### pyLocal
##### 
**Signature:**  
pyLocal(self, time_zone="")
##### 
**Description:**  
a method to report a python datetime from a labDT object  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                 </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                            </td></tr>
<tr><td>time_zone </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with timezone to report in</td></tr>
</tbody>
</table>

### jsLocal
##### 
**Signature:**  
jsLocal(self, time_zone="")
##### 
**Description:**  
a method to report a javascript string from a labDT object  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                 </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                            </td></tr>
<tr><td>time_zone </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with timezone to report in</td></tr>
</tbody>
</table>

### humanFriendly
##### 
**Signature:**  
humanFriendly(self, time_zone="", include_day=True, include_time=True)
##### 
**Description:**  
a method to report a human friendly string from a labDT object  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                 </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                            </td></tr>
<tr><td>time_zone   </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with timezone to report in</td></tr>
<tr><td>include_day </td><td>bool  </td><td>          </td><td>True     </td><td>                                            </td></tr>
<tr><td>include_time</td><td>bool  </td><td>          </td><td>True     </td><td>                                            </td></tr>
</tbody>
</table>

### fromEpoch
##### 
**Signature:**  
fromEpoch(cls, epoch_time)
##### 
**Description:**  
a method for constructing a labDT object from epoch timestamp  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                     </th></tr>
</thead>
<tbody>
<tr><td>cls       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                </td></tr>
<tr><td>epoch_time</td><td>float   </td><td>Yes       </td><td>0.0      </td><td>number with epoch timestamp info</td></tr>
</tbody>
</table>

### fromISO
##### 
**Signature:**  
fromISO(cls, iso_string)
##### 
**Description:**  
a method for constructing a labDT object from a timezone aware ISO string  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                 </th></tr>
</thead>
<tbody>
<tr><td>cls       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                            </td></tr>
<tr><td>iso_string</td><td>str     </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with date and time info in ISO format</td></tr>
</tbody>
</table>

### fromPython
##### 
**Signature:**  
fromPython(cls, python_datetime)
##### 
**Description:**  
a method for constructing a labDT from a python datetime with timezone info  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                       </th></tr>
</thead>
<tbody>
<tr><td>cls            </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                  </td></tr>
<tr><td>python_datetime</td><td>object  </td><td>Yes       </td><td>None     </td><td>datetime object with timezone info</td></tr>
</tbody>
</table>

### fromJavascript
##### 
**Signature:**  
fromJavascript(cls, javascript_datetime)
##### 
**Description:**  
a method to construct labDT from a javascript datetime string  
<table>
<thead>
<tr><th>Argument           </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>cls                </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>javascript_datetime</td><td>str     </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with datetime info in javascript formatting</td></tr>
</tbody>
</table>

### fromPattern
##### 
**Signature:**  
fromPattern(cls, datetime_string, datetime_pattern, time_zone, require_hour=True)
##### 
**Description:**  
a method for constructing labDT from a strptime pattern in a string
            https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            iso_pattern: '%Y-%m-%dT%H:%M:%S.%f%z'
            human_friendly_pattern: '%A, %B %d, %Y %I:%M:%S.%f%p'  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                   </th></tr>
</thead>
<tbody>
<tr><td>cls             </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                              </td></tr>
<tr><td>datetime_string </td><td>str     </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with date and time info                </td></tr>
<tr><td>datetime_pattern</td><td>str     </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with python formatted pattern          </td></tr>
<tr><td>time_zone       </td><td>str     </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with timezone info                     </td></tr>
<tr><td>require_hour    </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to disable hour requirement</td></tr>
</tbody>
</table>
