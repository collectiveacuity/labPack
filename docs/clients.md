# Clients

## movesClient
### Import:
labpack.activity.moves.movesClient  
### Description:
a class of methods for retrieving user data from moves api  
### \__init__
##### 
**Signature:**  
\__init__(self, access_token, service_scope, usage_client=None, requests_handler=None)
##### 
**Description:**  
initialization method for moves client class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                              </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                         </td></tr>
<tr><td>access_token    </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with access token for user provided by moves oauth</td></tr>
<tr><td>service_scope   </td><td>dict    </td><td>Yes       </td><td>None     </td><td>dictionary with service type permissions                 </td></tr>
<tr><td>usage_client    </td><td>function</td><td>          </td><td>None     </td><td>callable that records usage data                         </td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>callable that handles requests errors                    </td></tr>
</tbody>
</table>
### list_activities
##### 
**Signature:**  
list_activities(self)
##### 
**Description:**  
a method to retrieve the details for all activities currently supported  
### get_profile
##### 
**Signature:**  
get_profile(self)
##### 
**Description:**  
a method to retrieve profile details of user  
### get_summary
##### 
**Signature:**  
get_summary(self, timezone_offset, first_date, start=0.0, end=0.0)
##### 
**Description:**  
a method to retrieve summary details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>timezone_offset</td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with timezone offset from user profile details     </td></tr>
<tr><td>first_date     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ISO date from user profile details firstDate   </td></tr>
<tr><td>start          </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with starting datetime for daily summaries</td></tr>
<tr><td>end            </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with ending datetime for daily summaries  </td></tr>
</tbody>
</table>
### get_activities
##### 
**Signature:**  
get_activities(self, timezone_offset, first_date, start=0.0, end=0.0)
##### 
**Description:**  
a method to retrieve activity details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>timezone_offset</td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with timezone offset from user profile details     </td></tr>
<tr><td>first_date     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ISO date from user profile details firstDate   </td></tr>
<tr><td>start          </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with starting datetime for daily summaries</td></tr>
<tr><td>end            </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with ending datetime for daily summaries  </td></tr>
</tbody>
</table>
### get_places
##### 
**Signature:**  
get_places(self, timezone_offset, first_date, start=0.0, end=0.0)
##### 
**Description:**  
a method to retrieve place details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>timezone_offset</td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with timezone offset from user profile details     </td></tr>
<tr><td>first_date     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ISO date from user profile details firstDate   </td></tr>
<tr><td>start          </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with starting datetime for daily summaries</td></tr>
<tr><td>end            </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with ending datetime for daily summaries  </td></tr>
</tbody>
</table>
### get_storyline
##### 
**Signature:**  
get_storyline(self, timezone_offset, first_date, start=0.0, end=0.0, track_points=False)
##### 
**Description:**  
a method to retrieve storyline details for a period of time

        NOTE: start and end must be no more than 30 days, 1 second apart

        NOTE: if track_points=True, start and end must be no more than 6 days, 1 second apart  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                     </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                </td></tr>
<tr><td>timezone_offset</td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with timezone offset from user profile details          </td></tr>
<tr><td>first_date     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ISO date from user profile details firstDate        </td></tr>
<tr><td>start          </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with starting datetime for daily summaries     </td></tr>
<tr><td>end            </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with ending datetime for daily summaries       </td></tr>
<tr><td>track_points   </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to provide detailed tracking of user movement</td></tr>
</tbody>
</table>

## iamClient
### Import:
labpack.authentication.aws.iam.iamClient  
### Description:
a class of methods for interacting with the AWS Identity & Access Management

        https://boto3.readthedocs.org/en/latest/  
### \__init__
##### 
**Signature:**  
\__init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True)
##### 
**Description:**  
a method for initializing the connection to AW IAM  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                     </td></tr>
<tr><td>access_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with access_key_id from aws IAM user setup    </td></tr>
<tr><td>secret_key </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with secret_access_key from aws IAM user setup</td></tr>
<tr><td>region_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of aws region                       </td></tr>
<tr><td>owner_id   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with aws account id                           </td></tr>
<tr><td>user_name  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of user access keys are assigned to </td></tr>
<tr><td>verbose    </td><td>bool  </td><td>          </td><td>True     </td><td>boolean to enable process messages                   </td></tr>
</tbody>
</table>
### list_certificates
##### 
**Signature:**  
list_certificates(self)
##### 
**Description:**  
a method to retrieve a list of server certificates  
### read_certificate
##### 
**Signature:**  
read_certificate(self, certificate_name)
##### 
**Description:**  
a method to retrieve the details about a server certificate  
<table>
<thead>
<tr><th>Argument        </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>certificate_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of server certificate</td></tr>
</tbody>
</table>
### list_roles
##### 
**Signature:**  
list_roles(self)
##### 
**Description:**  
a method to retrieve a list of server certificates  

## oauth2Client
### Import:
labpack.authentication.oauth2.oauth2Client  
### Description:
the initialization method for oauth2 client class  
### \__init__
##### 
**Signature:**  
\__init__(self, client_id, client_secret, auth_endpoint, token_endpoint, redirect_uri, request_mimetype="", status_endpoint="", requests_handler=None, error_map=None)
##### 
**Description:**  
the initialization method for oauth2 client class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                        </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                                   </td></tr>
<tr><td>client_id       </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with client id registered for app with service              </td></tr>
<tr><td>client_secret   </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with client secret registered for app with service          </td></tr>
<tr><td>auth_endpoint   </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with service endpoint for authorization code requests       </td></tr>
<tr><td>token_endpoint  </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with service endpoint for token post requests               </td></tr>
<tr><td>redirect_uri    </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with url for redirect callback registered with service      </td></tr>
<tr><td>request_mimetype</td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with mimetype for token post requests            </td></tr>
<tr><td>status_endpoint </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with service endpoint to retrieve status of token</td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>[optional] callable that handles requests errors                   </td></tr>
<tr><td>error_map       </td><td>dict    </td><td>          </td><td>None     </td><td>[optional] dictionary with key value strings for service error msgs</td></tr>
</tbody>
</table>
### generate_url
##### 
**Signature:**  
generate_url(self, service_scope=None, state_value="", additional_fields=None)
##### 
**Description:**  
a method to generate an authorization url to oauth2 service for client  
<table>
<thead>
<tr><th>Argument         </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                             </th></tr>
</thead>
<tbody>
<tr><td>self             </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                        </td></tr>
<tr><td>service_scope    </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list with scope of permissions for agent     </td></tr>
<tr><td>state_value      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with unique identifier for callback   </td></tr>
<tr><td>additional_fields</td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with key value strings for service</td></tr>
</tbody>
</table>
### get_token
##### 
**Signature:**  
get_token(self, auth_code)
##### 
**Description:**  
a method to retrieve an access token from an oauth2 authorizing party  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                 </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                            </td></tr>
<tr><td>auth_code </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with code provided by client redirect</td></tr>
</tbody>
</table>
### renew_token
##### 
**Signature:**  
renew_token(self, refresh_token)
##### 
**Description:**  
a method to renew an access token from an oauth2 authorizing party  
<table>
<thead>
<tr><th>Argument     </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>refresh_token</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## mailgunClient
### Import:
labpack.email.mailgun.mailgunClient  
### Description:
a class of methods for managing email with mailgun api  
### \__init__
##### 
**Signature:**  
\__init__(self, api_key, email_key, account_domain, usage_client=None, requests_handler=None)
##### 
**Description:**  
initialization method for mailgun client class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                   </td></tr>
<tr><td>api_key         </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with api key provided by mailgun            </td></tr>
<tr><td>email_key       </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with email validation key provide by mailgun</td></tr>
<tr><td>account_domain  </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with domain from which to send email        </td></tr>
<tr><td>usage_client    </td><td>function</td><td>          </td><td>None     </td><td>callable that records usage data                   </td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>callable that handles requests errors              </td></tr>
</tbody>
</table>
### send_email
##### 
**Signature:**  
send_email(self, recipient_list, sender_email, sender_name, email_subject, content_text="", content_html="", tracking_tags=None, cc_list=None, bcc_list=None, delivery_time=0.0)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>recipient_list</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>sender_email  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>sender_name   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>email_subject </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>content_text  </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>content_html  </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>tracking_tags </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>cc_list       </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>bcc_list      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>delivery_time </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
</tbody>
</table>
### validate_email
##### 
**Signature:**  
validate_email(self, email_address)
##### 
**Description:**  
a method to validate an email address  
<table>
<thead>
<tr><th>Argument     </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                          </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object</td><td>Yes       </td><td>None     </td><td>                                     </td></tr>
<tr><td>email_address</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with email address to validate</td></tr>
</tbody>
</table>

## mandrillClient
### Import:
labpack.email.mandrill.mandrillClient  
### Description:
a class of methods for sending emails through the mandrill api  
### \__init__
##### 
**Signature:**  
\__init__(self, api_key, allow_fees=False, usage_client=None, requests_handler=None)
##### 
**Description:**  
a method to initialize the mandrill client class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                           </td></tr>
<tr><td>api_key         </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with api key generated by mandrill  </td></tr>
<tr><td>allow_fees      </td><td>bool    </td><td>          </td><td>False    </td><td>[optional] boolean to allow additional fees</td></tr>
<tr><td>usage_client    </td><td>function</td><td>          </td><td>None     </td><td>callable that records usage data           </td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>callable that handles requests errors      </td></tr>
</tbody>
</table>
### send_email
##### 
**Signature:**  
send_email(self, recipient_list, sender_email, sender_name, email_subject, content_text="", content_html="", tracking_tags=None, cc_list=None, bcc_list=None, delivery_time=0.0)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>recipient_list</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>sender_email  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>sender_name   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>email_subject </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>content_text  </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>content_html  </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>tracking_tags </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>cc_list       </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>bcc_list      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>delivery_time </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
</tbody>
</table>

## meetupClient
### Import:
labpack.events.meetup.meetupClient  
### Description:
a class of methods for managing user events, groups and profile on Meetup API  
### \__init__
##### 
**Signature:**  
\__init__(self, access_token, service_scope, usage_client=None, requests_handler=None)
##### 
**Description:**  
initialization method for meetup client class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                               </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                          </td></tr>
<tr><td>access_token    </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with access token for user provided by meetup oauth</td></tr>
<tr><td>service_scope   </td><td>dict    </td><td>Yes       </td><td>None     </td><td>dictionary with service type permissions                  </td></tr>
<tr><td>usage_client    </td><td>function</td><td>          </td><td>None     </td><td>[optional] callable that records usage data               </td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>[optional] callable that handles requests errors          </td></tr>
</tbody>
</table>
### get_member_brief
##### 
**Signature:**  
get_member_brief(self, member_id=0)
##### 
**Description:**  
a method to retrieve member profile info  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                     </td></tr>
<tr><td>member_id </td><td>int   </td><td>          </td><td>0        </td><td>[optional] integer with member id from member profile</td></tr>
</tbody>
</table>
### get_member_profile
##### 
**Signature:**  
get_member_profile(self, member_id)
##### 
**Description:**  
a method to retrieve member profile details  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                               </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                          </td></tr>
<tr><td>member_id </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with member id from member profile</td></tr>
</tbody>
</table>
### update_member_profile
##### 
**Signature:**  
update_member_profile(self, brief_details, profile_details)
##### 
**Description:**  
a method to update user profile details on meetup  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                               </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                          </td></tr>
<tr><td>brief_details  </td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with member brief details with updated values  </td></tr>
<tr><td>profile_details</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with member profile details with updated values</td></tr>
</tbody>
</table>
### list_member_topics
##### 
**Signature:**  
list_member_topics(self, member_id)
##### 
**Description:**  
a method to retrieve a list of topics member follows  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>member_id </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with meetup member id</td></tr>
</tbody>
</table>
### list_member_groups
##### 
**Signature:**  
list_member_groups(self, member_id)
##### 
**Description:**  
a method to retrieve a list of meetup groups member belongs to  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>member_id </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with meetup member id</td></tr>
</tbody>
</table>
### list_member_events
##### 
**Signature:**  
list_member_events(self, upcoming=True)
##### 
**Description:**  
a method to retrieve a list of events member attended or will attend  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>upcoming  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to filter list to only future events</td></tr>
</tbody>
</table>
### get_member_calendar
##### 
**Signature:**  
get_member_calendar(self, max_results=0)
##### 
**Description:**  
a method to retrieve the upcoming events for all groups member belongs to  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                   </td></tr>
<tr><td>max_results</td><td>int   </td><td>          </td><td>0        </td><td>[optional] integer with number of events to include</td></tr>
</tbody>
</table>
### list_groups
##### 
**Signature:**  
list_groups(self, topics=None, categories=None, text="", country_code="", latitude=0.0, longitude=0.0, location="", radius=0.0, zip_code="", max_results=0, member_groups=True)
##### 
**Description:**  
a method to find meetup groups based upon a number of filters  
<table>
<thead>
<tr><th>Argument     </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                       </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                                  </td></tr>
<tr><td>topics       </td><td>list    </td><td>          </td><td>None     </td><td>[optional] list of integer meetup ids for topics                  </td></tr>
<tr><td>categories   </td><td>NoneType</td><td>          </td><td>None     </td><td>                                                                  </td></tr>
<tr><td>text         </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with words in groups to search                  </td></tr>
<tr><td>country_code </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with two character country code                 </td></tr>
<tr><td>latitude     </td><td>float   </td><td>          </td><td>0.0      </td><td>[optional] float with latitude coordinate at center of geo search </td></tr>
<tr><td>longitude    </td><td>float   </td><td>          </td><td>0.0      </td><td>[optional] float with longitude coordinate at center of geo search</td></tr>
<tr><td>location     </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with meetup location name fields to search      </td></tr>
<tr><td>radius       </td><td>float   </td><td>          </td><td>0.0      </td><td>[optional] float with distance from center of geographic search   </td></tr>
<tr><td>zip_code     </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with zip code of geographic search              </td></tr>
<tr><td>max_results  </td><td>int     </td><td>          </td><td>0        </td><td>[optional] integer with number of groups to include               </td></tr>
<tr><td>member_groups</td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to include groups member belongs to            </td></tr>
</tbody>
</table>
### get_group_details
##### 
**Signature:**  
get_group_details(self, group_url="", group_id=0)
##### 
**Description:**  
a method to retrieve details about a meetup group  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                        </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                   </td></tr>
<tr><td>group_url </td><td>str   </td><td>          </td><td>""       </td><td>string with meetup urlname of group</td></tr>
<tr><td>group_id  </td><td>int   </td><td>          </td><td>0        </td><td>int with meetup id for group       </td></tr>
</tbody>
</table>
### list_group_events
##### 
**Signature:**  
list_group_events(self, group_url, upcoming=True)
##### 
**Description:**  
a method to retrieve a list of upcoming events hosted by group  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>group_url </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname field of group              </td></tr>
<tr><td>upcoming  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to filter list to only future events</td></tr>
</tbody>
</table>
### list_group_members
##### 
**Signature:**  
list_group_members(self, group_url, max_results=0)
##### 
**Description:**  
a method to retrieve a list of members for a meetup group  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>group_url  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for group                </td></tr>
<tr><td>max_results</td><td>int   </td><td>          </td><td>0        </td><td>[optional] integer with number of members to include</td></tr>
</tbody>
</table>
### get_event_details
##### 
**Signature:**  
get_event_details(self, group_url, event_id)
##### 
**Description:**  
a method to retrieve details for an event  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                         </td></tr>
<tr><td>group_url </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for host group</td></tr>
<tr><td>event_id  </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with meetup id for event         </td></tr>
</tbody>
</table>
### list_event_attendees
##### 
**Signature:**  
list_event_attendees(self, group_url, event_id)
##### 
**Description:**  
a method to retrieve attendee list for event from meetup api  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                         </td></tr>
<tr><td>group_url </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for host group</td></tr>
<tr><td>event_id  </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with meetup id for event         </td></tr>
</tbody>
</table>
### get_venue_details
##### 
**Signature:**  
get_venue_details(self, venue_id)
##### 
**Description:**  
a method to retrieve venue details from meetup api  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                    </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                               </td></tr>
<tr><td>venue_id  </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer for meetup id for venue</td></tr>
</tbody>
</table>
### list_locations
##### 
**Signature:**  
list_locations(self, latitude=0.0, longitude=0.0, zip_code="", city_name="", max_results=0)
##### 
**Description:**  
a method to retrieve location address details based upon search parameters  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                       </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                  </td></tr>
<tr><td>latitude   </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with latitude coordinate at center of geo search </td></tr>
<tr><td>longitude  </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with longitude coordinate at center of geo search</td></tr>
<tr><td>zip_code   </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with zip code of geographic search              </td></tr>
<tr><td>city_name  </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of city for search                    </td></tr>
<tr><td>max_results</td><td>int   </td><td>          </td><td>0        </td><td>[optional] integer with number of groups to include               </td></tr>
</tbody>
</table>
### join_group
##### 
**Signature:**  
join_group(self, group_url, membership_answers=None)
##### 
**Description:**  
a method to add member to a meetup group  
<table>
<thead>
<tr><th>Argument          </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                              </th></tr>
</thead>
<tbody>
<tr><td>self              </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                         </td></tr>
<tr><td>group_url         </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for group                     </td></tr>
<tr><td>membership_answers</td><td>list  </td><td>          </td><td>None     </td><td>list with question id and answer for group join questions</td></tr>
</tbody>
</table>
### leave_group
##### 
**Signature:**  
leave_group(self, group_url, member_id, exit_comment="")
##### 
**Description:**  
a method to remove group from meetup member profile  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                           </td></tr>
<tr><td>group_url   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for group       </td></tr>
<tr><td>member_id   </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with member id from member profile </td></tr>
<tr><td>exit_comment</td><td>str   </td><td>          </td><td>""       </td><td>string with comment to leave with organizer</td></tr>
</tbody>
</table>
### join_topics
##### 
**Signature:**  
join_topics(self, member_id, topics)
##### 
**Description:**  
a method to add topics to member profile details on meetup  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                               </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                          </td></tr>
<tr><td>member_id </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with member id from member profile</td></tr>
<tr><td>topics    </td><td>list  </td><td>Yes       </td><td>None     </td><td>list of integer meetup ids for topics     </td></tr>
</tbody>
</table>
### leave_topics
##### 
**Signature:**  
leave_topics(self, member_id, topics)
##### 
**Description:**  
a method to remove topics from member profile details on meetup  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                               </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                          </td></tr>
<tr><td>member_id </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with member id from member profile</td></tr>
<tr><td>topics    </td><td>list  </td><td>Yes       </td><td>None     </td><td>list of integer meetup ids for topics     </td></tr>
</tbody>
</table>
### join_event
##### 
**Signature:**  
join_event(self, group_url, event_id, additional_guests=0, attendance_answers=None, payment_service="", payment_code="")
##### 
**Description:**  
a method to create an rsvp for a meetup event  
<table>
<thead>
<tr><th>Argument          </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self              </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>group_url         </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for group                       </td></tr>
<tr><td>event_id          </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with meetup id for event                           </td></tr>
<tr><td>additional_guests </td><td>int   </td><td>          </td><td>0        </td><td>[optional] integer with number of additional guests        </td></tr>
<tr><td>attendance_answers</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list with id & answer for event survey questions</td></tr>
<tr><td>payment_service   </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of payment service to use      </td></tr>
<tr><td>payment_code      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with token to authorize payment          </td></tr>
</tbody>
</table>
### leave_event
##### 
**Signature:**  
leave_event(self, group_url, event_id)
##### 
**Description:**  
a method to rescind an rsvp to a meetup event  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                         </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                    </td></tr>
<tr><td>group_url </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with meetup urlname for group</td></tr>
<tr><td>event_id  </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with meetup id for event    </td></tr>
</tbody>
</table>

## telegramBotClient
### Import:
labpack.messaging.telegram.telegramBotClient  
### Description:
a class of methods for interacting with telegram bot api  
### \__init__
##### 
**Signature:**  
\__init__(self, bot_id, access_token, requests_handler=None)
##### 
**Description:**  
initialization method for moves client class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>bot_id          </td><td>int     </td><td>Yes       </td><td>0        </td><td>integer with telegram id number for bot                        </td></tr>
<tr><td>access_token    </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with access token for bot provided by telegram botfather</td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>callable that handles requests errors                          </td></tr>
</tbody>
</table>
### get_me
##### 
**Signature:**  
get_me(self)
##### 
**Description:**  
a method to retrieve details about the bot from telegram api  
### get_updates
##### 
**Signature:**  
get_updates(self, last_update=0)
##### 
**Description:**  
a method to retrieve messages for bot from telegram api  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                    </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                               </td></tr>
<tr><td>last_update</td><td>int   </td><td>          </td><td>0        </td><td>integer with update id of last message received</td></tr>
</tbody>
</table>
### get_route
##### 
**Signature:**  
get_route(self, file_id)
##### 
**Description:**  
a method to retrieve route information for file on telegram api  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                    </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                               </td></tr>
<tr><td>file_id   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of file in a message send to bot</td></tr>
</tbody>
</table>
### get_file
##### 
**Signature:**  
get_file(self, file_route, file_name="")
##### 
**Description:**  
a method to retrieve data for a file housed on telegram api  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>file_route</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with route to file endpoint on telegram api</td></tr>
<tr><td>file_name </td><td>str   </td><td>          </td><td>""       </td><td>                                                  </td></tr>
</tbody>
</table>
### send_message
##### 
**Signature:**  
send_message(self, user_id, message_text, message_style="", button_list=None, small_buttons=True, persist_buttons=False)
##### 
**Description:**  
a method to send a message using telegram api  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                   </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                              </td></tr>
<tr><td>user_id        </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with id of telegram user                              </td></tr>
<tr><td>message_text   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with message to user                                   </td></tr>
<tr><td>message_style  </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with style to apply to text, only 'markdown'</td></tr>
<tr><td>button_list    </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of string to include as buttons in message    </td></tr>
<tr><td>small_buttons  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to resize buttons to single line           </td></tr>
<tr><td>persist_buttons</td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to keep buttons around after exiting       </td></tr>
</tbody>
</table>
### send_photo
##### 
**Signature:**  
send_photo(self, user_id, photo_id="", photo_path="", photo_url="", caption_text="", button_list=None, small_buttons=True, persist_buttons=False)
##### 
**Description:**  
a method to send a photo using telegram api  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                               </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                          </td></tr>
<tr><td>user_id        </td><td>int     </td><td>Yes       </td><td>0        </td><td>integer with id of telegram user                          </td></tr>
<tr><td>photo_id       </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with id of file stored with telegram api</td></tr>
<tr><td>photo_path     </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with local path to file                 </td></tr>
<tr><td>photo_url      </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with url of file                        </td></tr>
<tr><td>caption_text   </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with caption to add to photo            </td></tr>
<tr><td>button_list    </td><td>NoneType</td><td>          </td><td>None     </td><td>                                                          </td></tr>
<tr><td>small_buttons  </td><td>bool    </td><td>          </td><td>True     </td><td>                                                          </td></tr>
<tr><td>persist_buttons</td><td>bool    </td><td>          </td><td>False    </td><td>                                                          </td></tr>
</tbody>
</table>
### send_voice
##### 
**Signature:**  
send_voice(self, user_id, voice_id="", voice_path="", voice_url="", caption_text="", button_list=None, small_buttons=True, persist_buttons=False)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>user_id        </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>voice_id       </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>voice_path     </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>voice_url      </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>caption_text   </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>button_list    </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>small_buttons  </td><td>bool    </td><td>          </td><td>True     </td><td>             </td></tr>
<tr><td>persist_buttons</td><td>bool    </td><td>          </td><td>False    </td><td>             </td></tr>
</tbody>
</table>

## twilioClient
### Import:
labpack.messaging.twilio.twilioClient  
### Description:
send an SMS from the Twilio account to phone number  
### \__init__
##### 
**Signature:**  
\__init__(self, account_sid, auth_token, twilio_phone)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument    </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>account_sid </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>auth_token  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>twilio_phone</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### send_message
##### 
**Signature:**  
send_message(self, phone_number, message_text)
##### 
**Description:**  
send an SMS from the Twilio account to phone number  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                   </td></tr>
<tr><td>phone_number</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with phone number with country and area code</td></tr>
<tr><td>message_text</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with message text                           </td></tr>
</tbody>
</table>

## apschedulerClient
### Import:
labpack.platforms.apscheduler.apschedulerClient  
### Description:
initialization method for apschedulerClient class  
### \__init__
##### 
**Signature:**  
\__init__(self, scheduler_url, requests_handler=None)
##### 
**Description:**  
initialization method for apschedulerClient class  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                     </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                </td></tr>
<tr><td>scheduler_url   </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with url of scheduler service            </td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>[optional] callable for handling requests errors</td></tr>
</tbody>
</table>
### get_info
##### 
**Signature:**  
get_info(self)
##### 
**Description:**  
  
### list_jobs
##### 
**Signature:**  
list_jobs(self, argument_filters=None)
##### 
**Description:**  
a method to list jobs in the scheduler  
<table>
<thead>
<tr><th>Argument        </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>argument_filters</td><td>list  </td><td>          </td><td>None     </td><td>list of query criteria dictionaries for class argument keys</td></tr>
</tbody>
</table>
### add_date_job
##### 
**Signature:**  
add_date_job(self, id, function, args=None, kwargs=None, dt=0.0, name="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>id        </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>function  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>args      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>kwargs    </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>dt        </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
<tr><td>name      </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
</tbody>
</table>
### add_interval_job
##### 
**Signature:**  
add_interval_job(self, id, function, interval, args=None, kwargs=None, start=0.0, end=0.0, name="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>id        </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>function  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>interval  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>args      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>kwargs    </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>start     </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
<tr><td>end       </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
<tr><td>name      </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
</tbody>
</table>
### add_cron_job
##### 
**Signature:**  
add_cron_job(self, id, function, month=None, day=None, weekday=None, hour=None, minute=None, second=None, args=None, kwargs=None, start=0.0, end=0.0, name="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>id        </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>function  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>month     </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>day       </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>weekday   </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>hour      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>minute    </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>second    </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>args      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>kwargs    </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>start     </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
<tr><td>end       </td><td>float   </td><td>          </td><td>0.0      </td><td>             </td></tr>
<tr><td>name      </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
</tbody>
</table>
### delete_job
##### 
**Signature:**  
delete_job(self, id)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>id        </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## ec2Client
### Import:
labpack.platforms.aws.ec2.ec2Client  
### Description:
a class of methods for interacting with AWS Elastic Computing Cloud

        https://boto3.readthedocs.org/en/latest/  
### \__init__
##### 
**Signature:**  
\__init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True)
##### 
**Description:**  
a method for initializing the connection to EC2  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                     </td></tr>
<tr><td>access_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with access_key_id from aws IAM user setup    </td></tr>
<tr><td>secret_key </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with secret_access_key from aws IAM user setup</td></tr>
<tr><td>region_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of aws region                       </td></tr>
<tr><td>owner_id   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with aws account id                           </td></tr>
<tr><td>user_name  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of user access keys are assigned to </td></tr>
<tr><td>verbose    </td><td>bool  </td><td>          </td><td>True     </td><td>boolean to enable process messages                   </td></tr>
</tbody>
</table>
### check_instance_state
##### 
**Signature:**  
check_instance_state(self, instance_id, wait=True)
##### 
**Description:**  
method for checking the state of an instance on AWS EC2  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                     </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of instance                       </td></tr>
<tr><td>wait       </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to wait for instance while pending</td></tr>
</tbody>
</table>
### check_instance_status
##### 
**Signature:**  
check_instance_status(self, instance_id, wait=True)
##### 
**Description:**  
a method to wait until AWS instance reports an OK status  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                               </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                          </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string of instance id on AWS                              </td></tr>
<tr><td>wait       </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to wait for instance while initializing</td></tr>
</tbody>
</table>
### list_instances
##### 
**Signature:**  
list_instances(self, tag_values=None)
##### 
**Description:**  
a method to retrieve the list of instances on AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>tag_values</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of tag values</td></tr>
</tbody>
</table>
### read_instance
##### 
**Signature:**  
read_instance(self, instance_id)
##### 
**Description:**  
a method to retrieving the details of a single instances on AWS EC2  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                 </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                            </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string of instance id on AWS</td></tr>
</tbody>
</table>
### tag_instance
##### 
**Signature:**  
tag_instance(self, instance_id, tag_list)
##### 
**Description:**  
a method for adding or updating tags on an AWS instance  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                   </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                              </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string of instance id on AWS  </td></tr>
<tr><td>tag_list   </td><td>list  </td><td>Yes       </td><td>None     </td><td>list of single key-value pairs</td></tr>
</tbody>
</table>
### create_instance
##### 
**Signature:**  
create_instance(self, image_id, pem_file, group_ids, instance_type, volume_type="gp2", ebs_optimized=False, instance_monitoring=False, iam_profile="", tag_list=None, auction_bid=0.0)
##### 
**Description:**  
a method for starting an instance on AWS EC2  
<table>
<thead>
<tr><th>Argument           </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                 </th></tr>
</thead>
<tbody>
<tr><td>self               </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                            </td></tr>
<tr><td>image_id           </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with aws id of image for instance                    </td></tr>
<tr><td>pem_file           </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to pem file to access image                </td></tr>
<tr><td>group_ids          </td><td>list  </td><td>Yes       </td><td>None     </td><td>list with aws id of security group(s) to attach to instance </td></tr>
<tr><td>instance_type      </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with type of instance resource to use                </td></tr>
<tr><td>volume_type        </td><td>str   </td><td>          </td><td>"gp2"    </td><td>string with type of on-disk storage                         </td></tr>
<tr><td>ebs_optimized      </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to activate ebs optimization             </td></tr>
<tr><td>instance_monitoring</td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to active instance monitoring            </td></tr>
<tr><td>iam_profile        </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of iam instance profile role    </td></tr>
<tr><td>tag_list           </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of single key-pair tags for instance        </td></tr>
<tr><td>auction_bid        </td><td>float </td><td>          </td><td>0.0      </td><td>[optional] float with dollar amount to bid for instance hour</td></tr>
</tbody>
</table>
### delete_instance
##### 
**Signature:**  
delete_instance(self, instance_id)
##### 
**Description:**  
method for removing an instance from AWS EC2  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                 </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                            </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string of instance id on AWS</td></tr>
</tbody>
</table>
### check_image_state
##### 
**Signature:**  
check_image_state(self, image_id, wait=True)
##### 
**Description:**  
method for checking the state of an image on AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>image_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of image                       </td></tr>
<tr><td>wait      </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to wait for image while pending</td></tr>
</tbody>
</table>
### list_images
##### 
**Signature:**  
list_images(self, tag_values=None)
##### 
**Description:**  
a method to retrieve the list of images of account on AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>tag_values</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of tag values</td></tr>
</tbody>
</table>
### read_image
##### 
**Signature:**  
read_image(self, image_id)
##### 
**Description:**  
a method to retrieve the details of a single image on AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                           </td></tr>
<tr><td>image_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of image</td></tr>
</tbody>
</table>
### tag_image
##### 
**Signature:**  
tag_image(self, image_id, tag_list)
##### 
**Description:**  
a method for adding or updating tags on an AWS instance  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                    </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                               </td></tr>
<tr><td>image_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of instance </td></tr>
<tr><td>tag_list  </td><td>list  </td><td>Yes       </td><td>None     </td><td>list of tags to add to instance</td></tr>
</tbody>
</table>
### create_image
##### 
**Signature:**  
create_image(self, instance_id, image_name, tag_list=None)
##### 
**Description:**  
method for imaging an instance on AWS EC2  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of running instance           </td></tr>
<tr><td>image_name </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name to give new image               </td></tr>
<tr><td>tag_list   </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of resources tags to add to image</td></tr>
</tbody>
</table>
### delete_image
##### 
**Signature:**  
delete_image(self, image_id)
##### 
**Description:**  
method for removing an image from AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                   </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                              </td></tr>
<tr><td>image_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of instance</td></tr>
</tbody>
</table>
### import_image
##### 
**Signature:**  
import_image(self, image_id, region_name)
##### 
**Description:**  
a method to import an image from another AWS region

            https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html

            REQUIRED: aws credentials must have valid access to both regions  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>image_id   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of source image    </td></tr>
<tr><td>region_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS region of source image</td></tr>
</tbody>
</table>
### export_image
##### 
**Signature:**  
export_image(self, image_id, region_name)
##### 
**Description:**  
a method to add a copy of an image to another AWS region

            https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html

            REQUIRED: iam credentials must have valid access to both regions  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>image_id   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string of AWS id of image to be copied</td></tr>
<tr><td>region_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string of AWS region to copy image to </td></tr>
</tbody>
</table>
### list_keypairs
##### 
**Signature:**  
list_keypairs(self)
##### 
**Description:**  
a method to discover the list of key pairs on AWS  
### list_subnets
##### 
**Signature:**  
list_subnets(self, tag_values=None)
##### 
**Description:**  
a method to discover the list of subnets on AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>tag_values</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of tag values</td></tr>
</tbody>
</table>
### read_subnet
##### 
**Signature:**  
read_subnet(self, subnet_id)
##### 
**Description:**  
a method to retrieve the details about a subnet  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                 </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                            </td></tr>
<tr><td>subnet_id </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of subnet</td></tr>
</tbody>
</table>
### list_security_groups
##### 
**Signature:**  
list_security_groups(self, tag_values=None)
##### 
**Description:**  
a method to discover the list of security groups on AWS EC2  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>tag_values</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of tag values</td></tr>
</tbody>
</table>
### read_security_group
##### 
**Signature:**  
read_security_group(self, group_id)
##### 
**Description:**  
a method to retrieve the details about a security group  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                         </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                    </td></tr>
<tr><td>group_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of security group</td></tr>
</tbody>
</table>
### cleanup
##### 
**Signature:**  
cleanup(self)
##### 
**Description:**  
a method for removing instances and images in unusual states  

## sshClient
### Import:
labpack.platforms.aws.ssh.sshClient  
### Description:
a class of methods to run commands on an active AWS instance

        NOTE:   Make sure that VPC rules allow SSH access to your local IP
        NOTE:   SCP protocol requires SCP installed on Remote Host  
### \__init__
##### 
**Signature:**  
\__init__(self, instance_id, pem_file, access_id, secret_key, region_name, owner_id, user_name, login_name="", verbose=True)
##### 
**Description:**  
a method for initializing the SSH connection parameters to the EC2 instance  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                     </td></tr>
<tr><td>instance_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with AWS id of instance                       </td></tr>
<tr><td>pem_file   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to keypair pem file                 </td></tr>
<tr><td>access_id  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with access_key_id from aws IAM user setup    </td></tr>
<tr><td>secret_key </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with secret_access_key from aws IAM user setup</td></tr>
<tr><td>region_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of aws region                       </td></tr>
<tr><td>owner_id   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with aws account id                           </td></tr>
<tr><td>user_name  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of user access keys are assigned to </td></tr>
<tr><td>login_name </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of login user            </td></tr>
<tr><td>verbose    </td><td>bool  </td><td>          </td><td>True     </td><td>boolean to enable process messages                   </td></tr>
</tbody>
</table>
### terminal
##### 
**Signature:**  
terminal(self, confirmation=True)
##### 
**Description:**  
method to open an SSH terminal inside AWS instance  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>confirmation</td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to prompt keypair confirmation</td></tr>
</tbody>
</table>
### script
##### 
**Signature:**  
script(self, commands, synopsis=True)
##### 
**Description:**  
a method to run a list of shell command scripts on AWS instance  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                   </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                              </td></tr>
<tr><td>commands  </td><td>list  </td><td>Yes       </td><td>None     </td><td>list of strings with shell commands to pass through connection</td></tr>
<tr><td>synopsis  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to simplify progress messages to one line  </td></tr>
</tbody>
</table>
### put
##### 
**Signature:**  
put(self, local_path, remote_path="", overwrite=False, synopsis=True)
##### 
**Description:**  
a method to copy a folder or file from local device to AWS instance  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                 </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                            </td></tr>
<tr><td>local_path </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to folder or file on local host            </td></tr>
<tr><td>remote_path</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with path to copy contents on remote host </td></tr>
<tr><td>overwrite  </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable file overwrite on remote host  </td></tr>
<tr><td>synopsis   </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to simplify progress messages to one line</td></tr>
</tbody>
</table>
### get
##### 
**Signature:**  
get(self, remote_path, local_path="", overwrite=False, synopsis=True)
##### 
**Description:**  
a method to copy a folder or file from AWS instance to local device  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                 </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                            </td></tr>
<tr><td>remote_path</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to copy contents on remote host            </td></tr>
<tr><td>local_path </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with path to folder or file on local host </td></tr>
<tr><td>overwrite  </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable file overwrite on remote host  </td></tr>
<tr><td>synopsis   </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to simplify progress messages to one line</td></tr>
</tbody>
</table>
### responsive
##### 
**Signature:**  
responsive(self, port=80, timeout=600)
##### 
**Description:**  
a method for waiting until web server on AWS instance has restarted  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                        </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                   </td></tr>
<tr><td>port      </td><td>int   </td><td>          </td><td>80       </td><td>integer with port number to check                  </td></tr>
<tr><td>timeout   </td><td>int   </td><td>          </td><td>600      </td><td>integer with number of seconds to continue to check</td></tr>
</tbody>
</table>

## dockerClient
### Import:
labpack.platforms.docker.dockerClient  
### Description:
a method to initialize the dockerClient class  
### \__init__
##### 
**Signature:**  
\__init__(self, virtualbox_name="", verbose=False)
##### 
**Description:**  
a method to initialize the dockerClient class  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                    </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                               </td></tr>
<tr><td>virtualbox_name</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of virtualbox image</td></tr>
<tr><td>verbose        </td><td>bool  </td><td>          </td><td>False    </td><td>                                               </td></tr>
</tbody>
</table>
### images
##### 
**Signature:**  
images(self)
##### 
**Description:**  
  
### ps
##### 
**Signature:**  
ps(self)
##### 
**Description:**  
  
### inspect
##### 
**Signature:**  
inspect(self, container_alias="", docker_image="", image_tag="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>container_alias</td><td>str   </td><td>          </td><td>""       </td><td>string with name of container</td></tr>
<tr><td>docker_image   </td><td>str   </td><td>          </td><td>""       </td><td>                             </td></tr>
<tr><td>image_tag      </td><td>str   </td><td>          </td><td>""       </td><td>                             </td></tr>
</tbody>
</table>
### run
##### 
**Signature:**  
run(self, run_script)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>run_script</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### rm
##### 
**Signature:**  
rm(self, container_alias)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>container_alias</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### rmi
##### 
**Signature:**  
rmi(self, image_id)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>image_id  </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### ip
##### 
**Signature:**  
ip(self)
##### 
**Description:**  
  
### command
##### 
**Signature:**  
command(self, sys_command)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description               </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                          </td></tr>
<tr><td>sys_command</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with docker command</td></tr>
</tbody>
</table>
### synopsis
##### 
**Signature:**  
synopsis(self, container_settings)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument          </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                  </th></tr>
</thead>
<tbody>
<tr><td>self              </td><td>object</td><td>Yes       </td><td>None     </td><td>                                             </td></tr>
<tr><td>container_settings</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary returned from dockerConfig.inspect</td></tr>
</tbody>
</table>
### enter
##### 
**Signature:**  
enter(self, container_alias)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>container_alias</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## herokuClient
### Import:
labpack.platforms.heroku.herokuClient  
### Description:
a method to initialize the herokuClient class  
### \__init__
##### 
**Signature:**  
\__init__(self, account_email, auth_token, verbose=True)
##### 
**Description:**  
a method to initialize the herokuClient class  
<table>
<thead>
<tr><th>Argument     </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>account_email</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>auth_token   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>verbose      </td><td>bool    </td><td>          </td><td>True     </td><td>             </td></tr>
</tbody>
</table>
### access
##### 
**Signature:**  
access(self, app_subdomain)
##### 
**Description:**  
a method to validate user can access app  
<table>
<thead>
<tr><th>Argument     </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>app_subdomain</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### deploy_docker
##### 
**Signature:**  
deploy_docker(self, dockerfile_path, virtualbox_name="default")
##### 
**Description:**  
a method to deploy app to heroku using docker  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>dockerfile_path</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>virtualbox_name</td><td>str     </td><td>          </td><td>"default"</td><td>             </td></tr>
</tbody>
</table>
### deploy_app
##### 
**Signature:**  
deploy_app(self, site_folder, runtime_type="")
##### 
**Description:**  
a method to deploy a static html page to heroku using php  
<table>
<thead>
<tr><th>Argument    </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>site_folder </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>runtime_type</td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
</tbody>
</table>

## localhostClient
### Import:
labpack.platforms.localhost.localhostClient  
### Description:
a class of methods to interact with the localhost  
### \__init__
##### 
**Signature:**  
\__init__(self)
##### 
**Description:**  
a method to initialize a client class to interact with the localhost  
### app_data
##### 
**Signature:**  
app_data(self, org_name, prod_name)
##### 
**Description:**  
a method to retrieve the os appropriate path to user app data

        # https://www.chromium.org/user-experience/user-data-directory  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                           </td></tr>
<tr><td>org_name  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of product/service creator</td></tr>
<tr><td>prod_name </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of product/service        </td></tr>
</tbody>
</table>
### walk
##### 
**Signature:**  
walk(self, walk_root="", reverse_order=False, previous_file="")
##### 
**Description:**  
a generator method of file paths on localhost from walk of directories  
<table>
<thead>
<tr><th>Argument     </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                      </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                 </td></tr>
<tr><td>walk_root    </td><td>str   </td><td>          </td><td>""       </td><td>string with path from which to root walk of localhost directories</td></tr>
<tr><td>reverse_order</td><td>bool  </td><td>          </td><td>False    </td><td>boolean to determine alphabetical direction of walk              </td></tr>
<tr><td>previous_file</td><td>str   </td><td>          </td><td>""       </td><td>string with path of file after which to start walk               </td></tr>
</tbody>
</table>
### metadata
##### 
**Signature:**  
metadata(self, file_path)
##### 
**Description:**  
a method to retrieve the metadata of a file on the localhost  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                        </td></tr>
<tr><td>file_path </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to file</td></tr>
</tbody>
</table>
### conditional_filter
##### 
**Signature:**  
conditional_filter(self, metadata_filters)
##### 
**Description:**  
a method to construct a conditional filter function for the list method  
<table>
<thead>
<tr><th>Argument        </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                          </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object</td><td>Yes       </td><td>None     </td><td>                                     </td></tr>
<tr><td>metadata_filters</td><td>list  </td><td>Yes       </td><td>None     </td><td>list with query criteria dictionaries</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, filter_function=None, list_root="", max_results=1, reverse_order=False, previous_file="")
##### 
**Description:**  
a method to list files on localhost from walk of directories  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                           </td></tr>
<tr><td>filter_function</td><td>function</td><td>          </td><td>None     </td><td>(keyword arguments) function used to filter results        </td></tr>
<tr><td>list_root      </td><td>str     </td><td>          </td><td>""       </td><td>string with localhost path from which to root list of files</td></tr>
<tr><td>max_results    </td><td>int     </td><td>          </td><td>1        </td><td>integer with maximum number of results to return           </td></tr>
<tr><td>reverse_order  </td><td>bool    </td><td>          </td><td>False    </td><td>boolean to determine alphabetical direction of walk        </td></tr>
<tr><td>previous_file  </td><td>str     </td><td>          </td><td>""       </td><td>string with absolute path of file to begin search after    </td></tr>
</tbody>
</table>

## watsonSpeechClient
### Import:
labpack.speech.watson.watsonSpeechClient  
### Description:
a class of methods to convert speech to text using IBM Watson api 
    
        https://console.ng.bluemix.net/catalog/services/text-to-speech  
### \__init__
##### 
**Signature:**  
\__init__(self, service_username, service_password, requests_handler=None, magic_file="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>service_username</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>service_password</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>requests_handler</td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>magic_file      </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
</tbody>
</table>
### convert_audio
##### 
**Signature:**  
convert_audio(self, file_path, new_mimetype, overwrite=False)
##### 
**Description:**  
a method to convert an audio file into a different codec  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                  </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                             </td></tr>
<tr><td>file_path   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to file on localhost        </td></tr>
<tr><td>new_mimetype</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with mimetype for new file            </td></tr>
<tr><td>overwrite   </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to overwrite existing file</td></tr>
</tbody>
</table>
### transcribe_file
##### 
**Signature:**  
transcribe_file(self, file_path, clip_length=10, compress=True)
##### 
**Description:**  
a method to transcribe the text from an audio file
        
        EXAMPLE: https://github.com/dannguyen/watson-word-watcher  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>file_path  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with path to audio file on localhost         </td></tr>
<tr><td>clip_length</td><td>int   </td><td>          </td><td>10       </td><td>[optional] integer with seconds to divide clips into</td></tr>
<tr><td>compress   </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to convert file to audio/ogg     </td></tr>
</tbody>
</table>
### transcribe_url
##### 
**Signature:**  
transcribe_url(self, file_url, clip_length=0, compress=True)
##### 
**Description:**  
a method to transcribe the text from an audio url  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>file_url   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>clip_length</td><td>int     </td><td>          </td><td>0        </td><td>[optional] integer with seconds to divide clips into</td></tr>
<tr><td>compress   </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to convert file to audio/ogg     </td></tr>
</tbody>
</table>
### transcribe_bytes
##### 
**Signature:**  
transcribe_bytes(self, byte_data, clip_length=0, audio_mimetype="", compress=True)
##### 
**Description:**  
a method to transcribe text from audio byte data  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>byte_data     </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>byte data in buffer with audio data                 </td></tr>
<tr><td>clip_length   </td><td>int     </td><td>          </td><td>0        </td><td>[optional] integer with seconds to divide clips into</td></tr>
<tr><td>audio_mimetype</td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with byte data mimetype           </td></tr>
<tr><td>compress      </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to convert file to audio/ogg     </td></tr>
</tbody>
</table>
### transcribe_stream
##### 
**Signature:**  
transcribe_stream(self, data_stream)
##### 
**Description:**  
a method to perform rolling transcription  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>data_stream</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>

## appdataClient
### Import:
labpack.storage.appdata.appdataClient  
### Description:
a low-level class of methods for managing file storage in local app data

        NOTE:   class is designed to store json valid data nested in a dictionary
                structure. acceptable data types include:
                    boolean
                    integer or float (number)
                    string
                    dictionary
                    list
                    none
                to store other types of data, try first creating an url safe base64
                string using something like:
                    base64.urlsafe_b64encode(byte_data).decode()  
### \__init__
##### 
**Signature:**  
\__init__(self, collection_name="", prod_name="", org_name="")
##### 
**Description:**  
initialization method of appdata client class  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                               </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                          </td></tr>
<tr><td>collection_name</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of collection to store records</td></tr>
<tr><td>prod_name      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of application product        </td></tr>
<tr><td>org_name       </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of organization behind product</td></tr>
</tbody>
</table>
### create
##### 
**Signature:**  
create(self, key_string, body_dict=None, byte_data="", overwrite=True, secret_key="")
##### 
**Description:**  
a method to create a file in the collection folder  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                     </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                </td></tr>
<tr><td>key_string</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name to assign file (see NOTE below)</td></tr>
<tr><td>body_dict </td><td>dict  </td><td>          </td><td>None     </td><td>dictionary with file body details               </td></tr>
<tr><td>byte_data </td><td>str   </td><td>          </td><td>""       </td><td>byte data to save under key string              </td></tr>
<tr><td>overwrite </td><td>bool  </td><td>          </td><td>True     </td><td>boolean to overwrite files with same name       </td></tr>
<tr><td>secret_key</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with key to encrypt body data </td></tr>
</tbody>
</table>
### read
##### 
**Signature:**  
read(self, key_string, secret_key="")
##### 
**Description:**  
a method to retrieve body details from a file  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>key_string</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of file              </td></tr>
<tr><td>secret_key</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string used to decrypt data</td></tr>
</tbody>
</table>
### conditional_filter
##### 
**Signature:**  
conditional_filter(self, path_filters)
##### 
**Description:**  
a method to construct a conditional filter function for class list method  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                          </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                     </td></tr>
<tr><td>path_filters</td><td>list  </td><td>Yes       </td><td>None     </td><td>list with query criteria dictionaries</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, filter_function=None, max_results=1, reverse_search=True, previous_key="")
##### 
**Description:**  
a method to list keys in the collection  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>filter_function</td><td>function</td><td>          </td><td>None     </td><td>(positional arguments) function used to filter results</td></tr>
<tr><td>max_results    </td><td>int     </td><td>          </td><td>1        </td><td>integer with maximum number of results to return      </td></tr>
<tr><td>reverse_search </td><td>bool    </td><td>          </td><td>True     </td><td>boolean to search keys in reverse alphanumeric order  </td></tr>
<tr><td>previous_key   </td><td>str     </td><td>          </td><td>""       </td><td>string with key in collection to begin search after   </td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, key_string)
##### 
**Description:**  
a method to delete a file  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                        </td></tr>
<tr><td>key_string</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of file</td></tr>
</tbody>
</table>
### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove collection and all records in the collection  
