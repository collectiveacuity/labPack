# Packages

## ssl.py
### Import:
labpack.authentication.ssl  
### Description:
a package of methods for managing ssl authentication  
### generate_keystore
##### 
**Signature:**  
generate_keystore(key_alias, key_folder="./", root_cert="", truststore="", password="", organization="", organization_unit="", locality="", country="", key_size=2048, verbose=True, overwrite=False)
##### 
**Description:**  
a function to generate a keystore and cert files for self-signed ssl authentication  
<table>
<thead>
<tr><th>Argument         </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>key_alias        </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>key_folder       </td><td>str     </td><td>          </td><td>&quot;./&quot;     </td><td>             </td></tr>
<tr><td>root_cert        </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>truststore       </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>password         </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>organization     </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>organization_unit</td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>locality         </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>country          </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>key_size         </td><td>int     </td><td>          </td><td>2048     </td><td>             </td></tr>
<tr><td>verbose          </td><td>bool    </td><td>          </td><td>True     </td><td>             </td></tr>
<tr><td>overwrite        </td><td>bool    </td><td>          </td><td>False    </td><td>             </td></tr>
</tbody>
</table>

## drep.py
### Import:
labpack.compilers.drep  
### Description:
  
### dump
##### 
**Signature:**  
dump(json_input, secret_key)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>json_input</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
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

## encoding.py
### Import:
labpack.compilers.encoding  
### Description:
a package for encoding/decoding record data from ext type  
### decode_data
##### 
**Signature:**  
decode_data(file_name, byte_data, mimetype="", secret_key="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>file_name </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>byte_data </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>mimetype  </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>secret_key</td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
</tbody>
</table>
### encode_data
##### 
**Signature:**  
encode_data(file_name, python_object, mimetype="", secret_key="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument     </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>file_name    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>python_object</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>mimetype     </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
<tr><td>secret_key   </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>             </td></tr>
</tbody>
</table>

## filters.py
### Import:
labpack.compilers.filters  
### Description:
a package of methods to compile search filters  
### positional_filter
##### 
**Signature:**  
positional_filter(positional_filters, title="")
##### 
**Description:**  
a method to construct a conditional filter function to test positional arguments  
<table>
<thead>
<tr><th>Argument          </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>positional_filters</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary or list of dictionaries with query criteria</td></tr>
<tr><td>title             </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>string with name of function to use instead           </td></tr>
</tbody>
</table>

## git.py
### Import:
labpack.compilers.git  
### Description:
  
### merge_diff
##### 
**Signature:**  
merge_diff(target, source, output="")
##### 
**Description:**  
a method to merge the non-conflicting diffs between two files
        
        method retrieves the results from `git diff --no-index target source`
        and adds to target the lines from additions found in source. diff
        results which would subtract lines from target are ignored.
        
        PLEASE NOTE:    method makes no check to ensure that target, source
                        or output are valid paths  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>target    </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to file for target data                   </td></tr>
<tr><td>source    </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to file for source data                   </td></tr>
<tr><td>output    </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with path to file to save output of merge</td></tr>
</tbody>
</table>

## json.py
### Import:
labpack.compilers.json  
### Description:
a package of methods to merge two or more json documents preserving order  
### merge_json
##### 
**Signature:**  
merge_json(*sources, output="")
##### 
**Description:**  
method for merging two or more json files

    this method walks the parse tree of json data to merge the fields
    found in subsequent sources into the data structure of the initial source. 
    any number of sources can be added to the source args, but only new fields
    from subsequent sources will be added. to overwrite values in the initial
    source instead, it suffices to simply reverse the order of the sources

    PLEASE NOTE:    since there is no way to uniquely identify list items between
                    two json documents, items are not added to existing lists.

    PLEASE NOTE:    however, lists are transversed in order to evaluate keys of 
                    nested dictionaries using the first item of any subsequent list
                    as a model for the scope
    
    PLEASE NOTE:    this method makes no checks to ensure the file path of the 
                    sources exist nor the folder path to any output  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                       </th></tr>
</thead>
<tbody>
<tr><td>*sources  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                                                  </td></tr>
<tr><td>output    </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with path to save the combined json data to file</td></tr>
</tbody>
</table>
### walk_data
##### 
**Signature:**  
walk_data(target, source)
##### 
**Description:**  
method to recursively walk parse tree and merge source into target  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>target    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>source    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
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
<tr><td>root_path      </td><td>str     </td><td>          </td><td>&quot;./&quot;     </td><td>             </td></tr>
</tbody>
</table>

## yaml.py
### Import:
labpack.compilers.yaml  
### Description:
a package of methods to merge two or more yaml documents preserving order & comments  
### get_comments_map
##### 
**Signature:**  
get_comments_map(self, key, default=None)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>key       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>default   </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### get_comments_seq
##### 
**Signature:**  
get_comments_seq(self, idx, default=None)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>idx       </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>default   </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### merge_yaml
##### 
**Signature:**  
merge_yaml(*sources, output="")
##### 
**Description:**  
method for merging two or more yaml strings

    this method walks the parse tree of yaml data to merge the fields
    (and comments) found in subsequent sources into the data structure of the
    initial sources. any number of sources can be added to the source args, but
    only new fields and new comments from subsequent sources will be added. to
    overwrite the values in the initial source, it suffices to simply reverse 
    the order of the sources

    PLEASE NOTE:    since there is no way to uniquely identify list items between
                    two yaml documents, items are not added to existing lists.
                    the overwrite rule also has no effect on items in lists

    PLEASE NOTE:    however, lists are transversed in order to evaluate comments
                    and keys of nested dictionaries using the first item of any
                    subsequent list as a model for the scope

    PLEASE NOTE:    the way that ruamel.yaml keeps track of multi-line comments
                    can create odd results for comments which appear at the start
                    or the end of lists and dictionaries when new fields and comments 
                    are added. it is best to restrict comments to the start of lists
                    and dictionaries.

    PLEASE NOTE:    this method makes no checks to ensure the file path of the 
                    sources exist nor the folder path to any output  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                       </th></tr>
</thead>
<tbody>
<tr><td>*sources  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                                                  </td></tr>
<tr><td>output    </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with path to save the combined yaml data to file</td></tr>
</tbody>
</table>
### merge_yaml_strings
##### 
**Signature:**  
merge_yaml_strings(*sources, output="")
##### 
**Description:**  
method for merging two or more yaml strings

    this method walks the parse tree of yaml data to merge the fields
    (and comments) found in subsequent sources into the data structure of the
    initial sources. any number of sources can be added to the source args, but
    only new fields and new comments from subsequent sources will be added. to
    overwrite the values in the initial source, it suffices to simply reverse 
    the order of the sources

    PLEASE NOTE:    since there is no way to uniquely identify list items between
                    two yaml documents, items are not added to existing lists.

    PLEASE NOTE:    however, lists are transversed in order to evaluate comments
                    and keys of nested dictionaries using the first item of any
                    subsequent list as a model for the scope

    PLEASE NOTE:    the way that ruamel.yaml keeps track of multi-line comments
                    can create odd results for comments which appear at the start
                    or the end of lists and dictionaries when new fields and comments 
                    are added. it is best to restrict comments to the start of lists
                    and dictionaries.  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>*sources  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>output    </td><td>str     </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with type of output: &#x27;&#x27; [default], io</td></tr>
</tbody>
</table>
### walk_data
##### 
**Signature:**  
walk_data(target, source)
##### 
**Description:**  
method to recursively walk parse tree and merge source into target  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>target    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>source    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## iso_3166.py
### Import:
labpack.datasets.iso_3166  
### Description:
a package of methods for compiling information about ISO 3166 country codes  
### compile_list
##### 
**Signature:**  
compile_list(csv_file="datasets/iso_3166.csv")
##### 
**Description:**  
  
### compile_map
##### 
**Signature:**  
compile_map(key_column="Alpha-3code", csv_list=None)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default      </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>key_column</td><td>str     </td><td>          </td><td>&quot;Alpha-3code&quot;</td><td>             </td></tr>
<tr><td>csv_list  </td><td>NoneType</td><td>          </td><td>None         </td><td>             </td></tr>
</tbody>
</table>
### update_csv
##### 
**Signature:**  
update_csv(csv_url="")
##### 
**Description:**  
  

## iso_3166_2_US.py
### Import:
labpack.datasets.iso_3166_2_US  
### Description:
a package of methods for compiling information about ISO 3166 2 US state codes  
### compile_list
##### 
**Signature:**  
compile_list(csv_file="datasets/iso_3166_2_US.csv")
##### 
**Description:**  
  
### compile_map
##### 
**Signature:**  
compile_map(key_column="USPS", csv_list=None)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>key_column</td><td>str     </td><td>          </td><td>&quot;USPS&quot;   </td><td>             </td></tr>
<tr><td>csv_list  </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### update_csv
##### 
**Signature:**  
update_csv(csv_url="")
##### 
**Description:**  
  

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
<tr><td>secret_key    </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>[optional] string used to decrypt data</td></tr>
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
<tr><td>secret_key</td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string used to encrypt data</td></tr>
</tbody>
</table>

## requests.py
### Import:
labpack.handlers.requests  
### Description:
  
### handle_requests
##### 
**Signature:**  
handle_requests(request_object, uptime_url="www.google.com")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default         </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>request_object</td><td>NoneType</td><td>Yes       </td><td>None            </td><td>             </td></tr>
<tr><td>uptime_url    </td><td>str     </td><td>          </td><td>&quot;www.google.com&quot;</td><td>             </td></tr>
</tbody>
</table>
### requestsHandler
##### 
**Signature:**  
requestsHandler(self, uptime_url="www.google.com", requests_handler="handle_requests", response_handler=None, verbose=False)
##### 
**Description:**  
the initialization method for the requestsHandler class object  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default          </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None             </td><td>                                                           </td></tr>
<tr><td>uptime_url      </td><td>str     </td><td>          </td><td>&quot;www.google.com&quot; </td><td>[optional] string with url to test availability of internet</td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>&quot;handle_requests&quot;</td><td>[optional] callable method which accepts a Request object  </td></tr>
<tr><td>response_handler</td><td>function</td><td>          </td><td>None             </td><td>[optional] callable method which accepts a Response object </td></tr>
<tr><td>verbose         </td><td>bool    </td><td>          </td><td>False            </td><td>boolean to enable print out of status                      </td></tr>
</tbody>
</table>

## data.py
### Import:
labpack.mapping.data  
### Description:
  
### clean_data
##### 
**Signature:**  
clean_data(input_value)
##### 
**Description:**  
a function to transform a value into a json or yaml valid datatype  
### reconstruct_dict
##### 
**Signature:**  
reconstruct_dict(dot_paths, values)
##### 
**Description:**  
a method for reconstructing a dictionary from the values along dot paths  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>dot_paths </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>values    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### segment_path
##### 
**Signature:**  
segment_path(dot_path)
##### 
**Description:**  
a function to separate the path segments in a dot_path key  
### transform_data
##### 
**Signature:**  
transform_data(function, input_data)
##### 
**Description:**  
a function to apply a function to each value in a nested dictionary  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>function  </td><td>function</td><td>Yes       </td><td>None     </td><td>callable function with a single input of any datatype</td></tr>
<tr><td>input_data</td><td>dict    </td><td>Yes       </td><td>None     </td><td>dictionary or list with nested data to transform     </td></tr>
</tbody>
</table>
### walk_data
##### 
**Signature:**  
walk_data(input_data)
##### 
**Description:**  
a generator function for retrieving data in a nested dictionary  

## comparison.py
### Import:
labpack.parsing.comparison  
### Description:
a package of methods to generate the differences between two data architectures  
### compare_records
##### 
**Signature:**  
compare_records(new_record, old_record)
##### 
**Description:**  
a method to generate the differences between two data architectures  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>new_record</td><td>list  </td><td>Yes       </td><td>None     </td><td>set, list or dictionary with new details of an item</td></tr>
<tr><td>old_record</td><td>list  </td><td>Yes       </td><td>None     </td><td>set, list or dictionary with old details of an item</td></tr>
</tbody>
</table>

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
<tr><td>session_header </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with name of session token header key       </td></tr>
<tr><td>secret_key     </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with secret key to json web token encryption</td></tr>
</tbody>
</table>
### validate_request_content
##### 
**Signature:**  
validate_request_content(request_content, request_model, request_component="body")
##### 
**Description:**  
a method to validate the content fields of a flask request  
<table>
<thead>
<tr><th>Argument         </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>request_content  </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with content fields to validate        </td></tr>
<tr><td>request_model    </td><td>object</td><td>Yes       </td><td>None     </td><td>object with jsonmodel class properties            </td></tr>
<tr><td>request_component</td><td>str   </td><td>          </td><td>&quot;body&quot;   </td><td>string with name of component of request evaluated</td></tr>
</tbody>
</table>

## grammar.py
### Import:
labpack.parsing.grammar  
### Description:
  
### join_words
##### 
**Signature:**  
join_words(word_list, operator="and", quotes=False)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>word_list </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>operator  </td><td>str     </td><td>          </td><td>&quot;and&quot;    </td><td>             </td></tr>
<tr><td>quotes    </td><td>bool    </td><td>          </td><td>False    </td><td>             </td></tr>
</tbody>
</table>
### section_text
##### 
**Signature:**  
section_text(text_string, max_characters=500, continue_text="...")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>text_string   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>max_characters</td><td>int     </td><td>          </td><td>500      </td><td>             </td></tr>
<tr><td>continue_text </td><td>str     </td><td>          </td><td>&quot;...&quot;    </td><td>             </td></tr>
</tbody>
</table>

## shell.py
### Import:
labpack.parsing.shell  
### Description:
a package of functions for parsing STDOUT and STDERR  
### convert_table
##### 
**Signature:**  
convert_table(shell_output, delimiter="\t|\s{", }', output="dict")
##### 
**Description:**  
a method to convert a STDOUT shell table into a python data structure  
<table>
<thead>
<tr><th>Argument    </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>shell_output</td><td>str     </td><td>Yes       </td><td>&quot;&quot;       </td><td>string from STDOUT with headers                            </td></tr>
<tr><td>delimiter   </td><td>str     </td><td>          </td><td>&quot;\t|\s{&quot; </td><td>string with regex pattern delimiting headers               </td></tr>
<tr><td>}&#x27;          </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>output      </td><td>str     </td><td>          </td><td>&quot;dict&quot;   </td><td>string with type of structure to output (dict, list or csv)</td></tr>
</tbody>
</table>

## performlab.py
### Import:
labpack.performance.performlab  
### Description:
  
### repeat
##### 
**Signature:**  
repeat(function, kwargs, title, count, verbose=True)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>function  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>kwargs    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
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
  
### describe_ip
##### 
**Signature:**  
describe_ip(ip_address, source="whatismyip")
##### 
**Description:**  
a method to get the details associated with an ip address  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default     </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>ip_address</td><td>NoneType</td><td>Yes       </td><td>None        </td><td>             </td></tr>
<tr><td>source    </td><td>str     </td><td>          </td><td>&quot;whatismyip&quot;</td><td>             </td></tr>
</tbody>
</table>
### get_ip
##### 
**Signature:**  
get_ip(source="aws")
##### 
**Description:**  
a method to get current public ip address of machine  

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
<tr><td>model_path   </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to jsonmodel valid model data </td></tr>
<tr><td>file_path    </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to local configuration file   </td></tr>
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
<tr><td>file_path  </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to settings file                         </td></tr>
<tr><td>module_name</td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with name of module containing file path</td></tr>
<tr><td>secret_key </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with key to decrypt drep file           </td></tr>
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
<tr><td>file_path  </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to file to remove                              </td></tr>
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
<tr><td>file_path     </td><td>str   </td><td>Yes       </td><td>&quot;&quot;       </td><td>string with path to settings file                 </td></tr>
<tr><td>record_details</td><td>list  </td><td>Yes       </td><td>None     </td><td>list or dictionary with record details            </td></tr>
<tr><td>overwrite     </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to overwrite existing file data</td></tr>
<tr><td>secret_key    </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with key to decrypt drep file   </td></tr>
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
