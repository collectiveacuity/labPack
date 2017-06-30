# Packages

## drep.py
### Import:
labpack.compilers.drep  
### Description:
  
### dump
##### 
**Signature:**  
dump(map_input, secret_key)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>map_input </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>secret_key</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### load
##### 
**Signature:**  
load(encrypted_data, secret_key)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>encrypted_data</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>secret_key    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## objects.py
### Import:
labpack.compilers.objects  
### Description:
  
### retrieve_function
##### 
**Signature:**  
retrieve_function(function_string, global_scope=None, root_path="./")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>function_string</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>global_scope   </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>root_path      </td><td>str     </td><td>          </td><td>"./"     </td><td>             </td></tr>
</tbody>
</table>

## cryptolab.py
### Import:
labpack.encryption.cryptolab  
### Description:
  
### decrypt
##### 
**Signature:**  
decrypt(encrypted_data, secret_key)
##### 
**Description:**  
uses cryptography module to decrypt byte data
        cipher: AES (128 bit block_size)
        hash: sha512
        key size: 256 bit (first 32 bytes of secret key hash)
        vector size: 128 bit (next 16 bytes of secret key hash)
        padding: PKCS7
        cipher mode: CBC
        backend: openssl 1.0.2a  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>encrypted_data</td><td>bytes </td><td>Yes       </td><td>None     </td><td>bytes with data to decrypt            </td></tr>
<tr><td>secret_key    </td><td>str   </td><td>Yes       </td><td>""       </td><td>[optional] string used to decrypt data</td></tr>
</tbody>
</table>
### encrypt
##### 
**Signature:**  
encrypt(byte_data, secret_key="")
##### 
**Description:**  
uses cryptography module to encrypt byte data
        cipher: AES (128 bit block_size)
        hash: sha512
        key size: 256 bit (first 32 bytes of secret key hash)
        vector size: 128 bit (next 16 bytes of secret key hash)
        padding: PKCS7
        cipher mode: CBC
        backend: openssl 1.0.2a

        NOTE:   if secret_key is left blank,
                method generates a 32 byte hexadecimal string  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>byte_data </td><td>bytes </td><td>Yes       </td><td>None     </td><td>bytes with data to encrypt            </td></tr>
<tr><td>secret_key</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string used to encrypt data</td></tr>
</tbody>
</table>

## requests.py
### Import:
labpack.handlers.requests  
### Description:
  
### handle_requests
##### 
**Signature:**  
handle_requests(request_object)
##### 
**Description:**  
  

## conversion.py
### Import:
labpack.parsing.conversion  
### Description:
a package of functions to convert data architecture formats  
### camelcase_to_lowercase
##### 
**Signature:**  
camelcase_to_lowercase(camelcase_input, python_input=None)
##### 
**Description:**  
a function to recursively convert data with camelcase key names into lowercase keys  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                        </th></tr>
</thead>
<tbody>
<tr><td>camelcase_input</td><td>list  </td><td>Yes       </td><td>None     </td><td>list or dictionary with camelcase keys                             </td></tr>
<tr><td>python_input   </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list or dictionary with default lowercase keys in output</td></tr>
</tbody>
</table>
### lowercase_to_camelcase
##### 
**Signature:**  
lowercase_to_camelcase(python_input, camelcase_input=None)
##### 
**Description:**  
a function to recursively convert data with lowercase key names into camelcase keys  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                        </th></tr>
</thead>
<tbody>
<tr><td>python_input   </td><td>list  </td><td>Yes       </td><td>None     </td><td>[optional] list or dictionary with default camelcase keys in output</td></tr>
<tr><td>camelcase_input</td><td>list  </td><td>          </td><td>None     </td><td>list or dictionary with lowercase keys                             </td></tr>
</tbody>
</table>

## flask.py
### Import:
labpack.parsing.flask  
### Description:
  
### extract_request_details
##### 
**Signature:**  
extract_request_details(request_object, session_object=None)
##### 
**Description:**  
a method for extracting request details from request and session objects

        NOTE:   method is also a placeholder funnel for future validation
                processes, request logging, request context building and
                counter-measures for the nasty web  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>request_object</td><td>object</td><td>Yes       </td><td>None     </td><td>request object generated by flask from request route</td></tr>
<tr><td>session_object</td><td>object</td><td>          </td><td>None     </td><td>session object generated by flask from client cookie</td></tr>
</tbody>
</table>
### extract_session_details
##### 
**Signature:**  
extract_session_details(request_headers, session_header, secret_key)
##### 
**Description:**  
a method to extract and validate jwt session token from request headers  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>request_headers</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with header fields from request         </td></tr>
<tr><td>session_header </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of session token header key       </td></tr>
<tr><td>secret_key     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with secret key to json web token encryption</td></tr>
</tbody>
</table>
### validate_request_content
##### 
**Signature:**  
validate_request_content(request_content, request_model)
##### 
**Description:**  
a method to validate the content fields of a flask request  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                               </th></tr>
</thead>
<tbody>
<tr><td>request_content</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with content fields to validate</td></tr>
<tr><td>request_model  </td><td>object</td><td>Yes       </td><td>None     </td><td>object with jsonmodel class properties    </td></tr>
</tbody>
</table>

## grammar.py
### Import:
labpack.parsing.grammar  
### Description:
  
### join_words
##### 
**Signature:**  
join_words(word_list)
##### 
**Description:**  
  

## performlab.py
### Import:
labpack.performance.performlab  
### Description:
  
### repeat
##### 
**Signature:**  
repeat(function, title, count, verbose=True)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>function  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>title     </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>count     </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>verbose   </td><td>bool    </td><td>          </td><td>True     </td><td>             </td></tr>
</tbody>
</table>

## randomlab.py
### Import:
labpack.randomization.randomlab  
### Description:
  
### random_binary
##### 
**Signature:**  
random_binary(length)
##### 
**Description:**  
  
### random_bytes
##### 
**Signature:**  
random_bytes(length)
##### 
**Description:**  
  
### random_characters
##### 
**Signature:**  
random_characters(character_set, length)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument     </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>character_set</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>length       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### random_double
##### 
**Signature:**  
random_double(low, high)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>low       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>high      </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### random_fraction
##### 
**Signature:**  
random_fraction()
##### 
**Description:**  
  
### random_integer
##### 
**Signature:**  
random_integer(low, high)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>low       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>high      </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### random_number
##### 
**Signature:**  
random_number(length)
##### 
**Description:**  
  
### random_object
##### 
**Signature:**  
random_object()
##### 
**Description:**  
  
### random_shuffle
##### 
**Signature:**  
random_shuffle(item_list)
##### 
**Description:**  
  

## ip.py
### Import:
labpack.records.ip  
### Description:
  
### get_ip
##### 
**Signature:**  
get_ip(source="aws")
##### 
**Description:**  
a method to get current localhost public ip address  

## settings.py
### Import:
labpack.records.settings  
### Description:
  
### compile_settings
##### 
**Signature:**  
compile_settings(model_path, file_path, ignore_errors=False)
##### 
**Description:**  
a method to compile configuration values from different sources

        NOTE:   method searches the environment variables, a local
                configuration path and the default values for a jsonmodel
                object for valid configuration values. if an environmental
                variable or key inside a local config file matches the key
                for a configuration setting declared in the jsonmodel schema,
                its value will be added to the configuration file as long
                as the value is model valid. SEE jsonmodel module.

        NOTE:   the order of assignment:
                    first:  environment variable
                    second: configuration file
                    third:  default value
                    fourth: empty value

        NOTE:   method is guaranteed to produce a full set of top-level keys  
<table>
<thead>
<tr><th>Argument     </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                    </th></tr>
</thead>
<tbody>
<tr><td>model_path   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to jsonmodel valid model data </td></tr>
<tr><td>file_path    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to local configuration file   </td></tr>
<tr><td>ignore_errors</td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to ignore any invalid values</td></tr>
</tbody>
</table>
### ingest_environ
##### 
**Signature:**  
ingest_environ(model_path="")
##### 
**Description:**  
a method to convert environment variables to a python dictionary  
### load_settings
##### 
**Signature:**  
load_settings(file_path, module_name="", secret_key="")
##### 
**Description:**  
a method to load data from json valid files  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                               </th></tr>
</thead>
<tbody>
<tr><td>file_path  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to settings file                         </td></tr>
<tr><td>module_name</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of module containing file path</td></tr>
<tr><td>secret_key </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with key to decrypt drep file           </td></tr>
</tbody>
</table>
### remove_settings
##### 
**Signature:**  
remove_settings(file_path, retry_count=10, remove_dir=False)
##### 
**Description:**  
a method to remove a file using a child process

        http://www.petercollingridge.co.uk/blog/running-multiple-processes-python
        https://docs.python.org/3.5/library/multiprocessing.html  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                     </th></tr>
</thead>
<tbody>
<tr><td>file_path  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to file to remove                              </td></tr>
<tr><td>retry_count</td><td>int   </td><td>          </td><td>10       </td><td>integer with number of attempts to remove before error is thrown</td></tr>
<tr><td>remove_dir </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to remove empty parent directories           </td></tr>
</tbody>
</table>
### save_settings
##### 
**Signature:**  
save_settings(file_path, record_details, overwrite=False, secret_key="")
##### 
**Description:**  
a method to save dictionary typed data to a local file  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>file_path     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to settings file                 </td></tr>
<tr><td>record_details</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with record details                    </td></tr>
<tr><td>overwrite     </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to overwrite existing file data</td></tr>
<tr><td>secret_key    </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with key to decrypt drep file   </td></tr>
</tbody>
</table>

## barrel.py
### Import:
labpack.storage.barrel  
### Description:
  
### main
##### 
**Signature:**  
main(args)
##### 
**Description:**  
  
### retrieve_values
##### 
**Signature:**  
retrieve_values(file_path)
##### 
**Description:**  
  
### store_values
##### 
**Signature:**  
store_values(file_path, data)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>file_path </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>data      </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
