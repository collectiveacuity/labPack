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
### \__init__
##### 
**Signature:**  
\__init__(self, hostname, port=9042, username="", password="", cert_path="")
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
<tr><td>username  </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>password  </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>cert_path </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
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
### \__init__
##### 
**Signature:**  
\__init__(self, keyspace_name, table_name, record_schema, cassandra_session, replication_strategy=None)
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

## labMagic
### Import:
labpack.parsing.magic.labMagic  
### Description:
initialization method for labMagic class  
### \__init__
##### 
**Signature:**  
\__init__(self, magic_file="")
##### 
**Description:**  
initialization method for labMagic class  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                   </td></tr>
<tr><td>magic_file</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with local path to magic.mgc file</td></tr>
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
<tr><td>file_path </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with local path to file</td></tr>
<tr><td>file_url  </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with url of file       </td></tr>
<tr><td>byte_data </td><td>NoneType</td><td>          </td><td>None     </td><td>[optional] byte data from a file         </td></tr>
</tbody>
</table>

## labRegex
### Import:
labpack.parsing.regex.labRegex  
### Description:
instantiates class with a regular expression dictionary  
### \__init__
##### 
**Signature:**  
\__init__(self, regex_schema, override=False)
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
### \__init__
##### 
**Signature:**  
\__init__(self)
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
<tr><td>time_zone </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with timezone to report in</td></tr>
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
<tr><td>time_zone </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with timezone to report in</td></tr>
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
<tr><td>time_zone   </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with timezone to report in</td></tr>
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
<tr><td>iso_string</td><td>str     </td><td>Yes       </td><td>""       </td><td>string with date and time info in ISO format</td></tr>
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
<tr><td>javascript_datetime</td><td>str     </td><td>Yes       </td><td>""       </td><td>string with datetime info in javascript formatting</td></tr>
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
<tr><td>datetime_string </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with date and time info                </td></tr>
<tr><td>datetime_pattern</td><td>str     </td><td>Yes       </td><td>""       </td><td>string with python formatted pattern          </td></tr>
<tr><td>time_zone       </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with timezone info                     </td></tr>
<tr><td>require_hour    </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to disable hour requirement</td></tr>
</tbody>
</table>
