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

## depositsClient
### Import:
labpack.banking.capitalone.depositsClient  
### Description:
a class to manage the capital one bank account starter api 
    
    https://developer.capitalone.com/products/bank-account-starter/documentation/
    
    NOTE:   WIP  
### \__init__
##### 
**Signature:**  
\__init__(self, client_id, client_secret, retrieve_details=True, sandbox=False, requests_handler=None, usage_client=None)
##### 
**Description:**  
the initialization method for the capital one client  
<table>
<thead>
<tr><th>Argument        </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                         </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                                    </td></tr>
<tr><td>client_id       </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with client id registered for app with service               </td></tr>
<tr><td>client_secret   </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with client secret registered for app with service           </td></tr>
<tr><td>retrieve_details</td><td>bool    </td><td>          </td><td>True     </td><td>boolean to automatically retrieve, store and refresh account details</td></tr>
<tr><td>sandbox         </td><td>bool    </td><td>          </td><td>False    </td><td>boolean to send requests to test sandbox                            </td></tr>
<tr><td>requests_handler</td><td>function</td><td>          </td><td>None     </td><td>callable that handles requests errors                               </td></tr>
<tr><td>usage_client    </td><td>function</td><td>          </td><td>None     </td><td>callable that records usage data                                    </td></tr>
</tbody>
</table>
### access_token
##### 
**Signature:**  
access_token(self)
##### 
**Description:**  
a method to acquire an oauth access token  
### account_products
##### 
**Signature:**  
account_products(self)
##### 
**Description:**  
a method to retrieve a list of the account products 

            returns:
            { 
                "error": "",
                "code": 200,
                "method": "GET",
                "url": "https://...",
                "headers": { },
                "json": {
                  "entries": [
                    {
                      "productId": "3000",
                      "productName": "Capital One 360 Savings Account"
                    }
                  ]
                }
            }  
### account_product
##### 
**Signature:**  
account_product(self, product_id)
##### 
**Description:**  
a method to retrieve details about a particular account product 
        
        { 
            "error": "",
            "code": 200,
            "method": "GET",
            "url": "https://...",
            "headers": { },
            "json": {
              "productId": "3300",
              "productName": "Capital One 360 Money Market Account",
              "cdTerms": [
                "12M"
              ],
              "annualPercentageYieldDetails": {
                "annualPercentageYieldType": "simple",
                "annualPercentageYield": 1.4,
                "tieredAnnualPercentageYield": [
                  {
                    "tierDescription": "$0 - $9,999.99",
                    "annualPercentageYield": 1.4
                  }
                ],
                "termBasedAnnualPercentageYield": [
                  {
                    "term": "6M",
                    "annualPercentageYield": 1.2
                  }
                ]
              },
              "disclosures": {
                "productDisclosureUrl": "https://www.capitalone.com/savings-accounts/online-savings-account/disclosures/#360savingsdisclosure",
                "termsAndConditionsUrl": "https://www.capitalone.com/online-money-market-account/disclosures/#360moneymarketagreement",
                "electronicFundTransferDisclosureUrl": "https://www.capitalone.com/cds/online-cds/disclosures/#electronicfundtransferdisclosurestatement",
                "privacyPolicyUrl": "https://www.capitalone.com/savings-accounts/online-savings-account/disclosures/#privacypolicy",
                "wireTransferAgreementUrl": "https://www.capitalone.com/savings-accounts/online-savings-account/disclosures/#wirefundstransferdisclosurestatement",
                "paperlessAgreementUrl": "https://www.capitalone.com/terms_eddn",
                "fraudProtectionAgreementUrl": "https://www.capitalone.com/terms-personal-data",
                "tcpaDisclosureContent": "If number(s) provided above is(are) mobile phone number(s), it is (they are) my mobile phone number(s), by clicking on the button below, I consent to receive autodialed and prerecorded/artificial calls , including texts, relating to my relationship with Capital One (which may include handling, servicing, and billing for any of my accounts). Message and Data rates may apply. You can stop these types of messages by replying STOP in response to a text message, or by following any other instructions contained in the time-sensitive call.\n[Radio button] You can call or text me through automated means\n[Radio button] You can only contact me through non-automated mean"
              }
            }
        }  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>product_id</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### account_application
##### 
**Signature:**  
account_application(self, customer_ip, first_name, last_name, tax_id, date_of_birth, address_line_1, city_name, state_code, postal_code, phone_number, email_address, citizenship_country, employment_status, product_id, funding_amount, account_number, routing_number, backup_withholding=False, phone_type="mobile", accept_tcpa=False, accept_terms=True, address_line_2="", middle_name="", tax_id_type="SSN", secondary_citizenship_country="", job_title="", annual_income=0, cd_term="", funding_type="fundach", account_owner="primary", secondary_application=None)
##### 
**Description:**  
a method to submit application for new account  
<table>
<thead>
<tr><th>Argument                     </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                                     </th></tr>
</thead>
<tbody>
<tr><td>self                         </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                                </td></tr>
<tr><td>customer_ip                  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ip address of applicant                                             </td></tr>
<tr><td>first_name                   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with first name of applicant                                             </td></tr>
<tr><td>last_name                    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with last name of applicant                                              </td></tr>
<tr><td>tax_id                       </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with tax id number of applicant                                          </td></tr>
<tr><td>date_of_birth                </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ISO format of date of birth of applicant                            </td></tr>
<tr><td>address_line_1               </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with first line of street address of applicant                           </td></tr>
<tr><td>city_name                    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of city of address of applicant                                </td></tr>
<tr><td>state_code                   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with code for the state of address of applicant                          </td></tr>
<tr><td>postal_code                  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with postal code of address of applicant                                 </td></tr>
<tr><td>phone_number                 </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with phone number and area code of applicant                             </td></tr>
<tr><td>email_address                </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with email address of applicant                                          </td></tr>
<tr><td>citizenship_country          </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with ISO 3166 alpha-3 country code of citizenship of applicant           </td></tr>
<tr><td>employment_status            </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with employment status of applicant                                      </td></tr>
<tr><td>product_id                   </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with id of account product to apply for                                 </td></tr>
<tr><td>funding_amount               </td><td>float </td><td>Yes       </td><td>0.0      </td><td>float with amount of dollars to initially fund account                          </td></tr>
<tr><td>account_number               </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with pre-existing bank account number of applicant                       </td></tr>
<tr><td>routing_number               </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with aba routing number for bank of pre-existing account of applicant    </td></tr>
<tr><td>backup_withholding           </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to indicate backup withholding on accounts of applicant      </td></tr>
<tr><td>phone_type                   </td><td>str   </td><td>          </td><td>"mobile" </td><td>[optional] string with type of phone of applicant                               </td></tr>
<tr><td>accept_tcpa                  </td><td>bool  </td><td>          </td><td>False    </td><td>boolean to accept to be contacted by citizen one marketing on their phone number</td></tr>
<tr><td>accept_terms                 </td><td>bool  </td><td>          </td><td>True     </td><td>boolean to accept the terms and conditions associated with new account          </td></tr>
<tr><td>address_line_2               </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with second line of address of applicant                      </td></tr>
<tr><td>middle_name                  </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with middle name of applicant                                 </td></tr>
<tr><td>tax_id_type                  </td><td>str   </td><td>          </td><td>"SSN"    </td><td>string with type of tax id of applicant                                         </td></tr>
<tr><td>secondary_citizenship_country</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with ISO 3166 alpha-3 country code of secondary citizenship   </td></tr>
<tr><td>job_title                    </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with job title of applicant                                   </td></tr>
<tr><td>annual_income                </td><td>int   </td><td>          </td><td>0        </td><td>[optional] integer with dollar value of annual income of applicant              </td></tr>
<tr><td>cd_term                      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with term for the cd account product to apply for             </td></tr>
<tr><td>funding_type                 </td><td>str   </td><td>          </td><td>"fundach"</td><td>string with funding method selected by the applicant to fund new account        </td></tr>
<tr><td>account_owner                </td><td>str   </td><td>          </td><td>"primary"</td><td>string with role of applicant who owns pre-existing bank account                </td></tr>
<tr><td>secondary_application        </td><td>dict  </td><td>          </td><td>None     </td><td>dictionary with applicant fields of secondary account holder                    </td></tr>
</tbody>
</table>
### wallet_questions
##### 
**Signature:**  
wallet_questions(self, application_id, customer_ip)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>application_id</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>customer_ip   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### wallet_answers
##### 
**Signature:**  
wallet_answers(self, application_id, customer_ip, answer_dict)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument      </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>application_id</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>customer_ip   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>answer_dict   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### application_details
##### 
**Signature:**  
application_details(self)
##### 
**Description:**  
  

## syncGatewayClient
### Import:
labpack.databases.couchbase.syncGatewayClient  
### Description:
the initialization method for syncGatewayAdmin class  
### \__init__
##### 
**Signature:**  
\__init__(self, bucket_name, database_url, document_schema=None, verbose=False, configs=None)
##### 
**Description:**  
the initialization method for syncGatewayAdmin class  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>bucket_name    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>database_url   </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>document_schema</td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>verbose        </td><td>bool    </td><td>          </td><td>False    </td><td>             </td></tr>
<tr><td>configs        </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### create_view
##### 
**Signature:**  
create_view(self, query_criteria=None, uid="_all_users")
##### 
**Description:**  
a method to add a view to a design document of a uid  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default     </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None        </td><td>                                                       </td></tr>
<tr><td>query_criteria</td><td>dict  </td><td>          </td><td>None        </td><td>dictionary with valid jsonmodel query criteria         </td></tr>
<tr><td>uid           </td><td>str   </td><td>          </td><td>"_all_users"</td><td>[optional] string with uid of design document to update</td></tr>
</tbody>
</table>
### delete_view
##### 
**Signature:**  
delete_view(self, query_criteria=None, uid="_all_users")
##### 
**Description:**  
a method to delete a view associated with a user design doc  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default     </th><th>Description                                              </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None        </td><td>                                                         </td></tr>
<tr><td>query_criteria</td><td>dict  </td><td>          </td><td>None        </td><td>[optional] dictionary with valid jsonmodel query criteria</td></tr>
<tr><td>uid           </td><td>str   </td><td>          </td><td>"_all_users"</td><td>[optional] string with uid of design document to update  </td></tr>
</tbody>
</table>
### list_users
##### 
**Signature:**  
list_users(self)
##### 
**Description:**  
a method to list all the user ids of all users in the bucket  
### save_user
##### 
**Signature:**  
save_user(self, uid, user_password, user_channels=None, user_roles=None, user_views=None, disable_account=False)
##### 
**Description:**  
a method to add or update an authorized user to the bucket  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                  </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                             </td></tr>
<tr><td>uid            </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id to assign to user                             </td></tr>
<tr><td>user_password  </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with password to assign to user                       </td></tr>
<tr><td>user_channels  </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of strings with channels to subscribe to user</td></tr>
<tr><td>user_roles     </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of strings with roles to assign to user      </td></tr>
<tr><td>user_views     </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of query criteria to create as views for user</td></tr>
<tr><td>disable_account</td><td>bool  </td><td>          </td><td>False    </td><td>boolean to disable access to records by user                 </td></tr>
</tbody>
</table>
### load_user
##### 
**Signature:**  
load_user(self, uid)
##### 
**Description:**  
a method to retrieve the account details of a user in the bucket  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                     </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                </td></tr>
<tr><td>uid       </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of user in bucket</td></tr>
</tbody>
</table>
### delete_user
##### 
**Signature:**  
delete_user(self, uid, delete_views=True)
##### 
**Description:**  
a method to retrieve the account details of a user in the bucket  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                               </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                          </td></tr>
<tr><td>uid         </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of user in bucket          </td></tr>
<tr><td>delete_views</td><td>bool  </td><td>          </td><td>True     </td><td>boolean to remove indices attached to user</td></tr>
</tbody>
</table>
### create_session
##### 
**Signature:**  
create_session(self, uid, duration=0)
##### 
**Description:**  
a method to create a session token for the user  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>uid       </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of user in bucket                       </td></tr>
<tr><td>duration  </td><td>int   </td><td>          </td><td>0        </td><td>integer with number of seconds to last (default: 24hrs)</td></tr>
</tbody>
</table>
### delete_session
##### 
**Signature:**  
delete_session(self, session_id)
##### 
**Description:**  
a method to create a session token for the user  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                   </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                              </td></tr>
<tr><td>session_id</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of user session token in bucket</td></tr>
</tbody>
</table>
### delete_sessions
##### 
**Signature:**  
delete_sessions(self, uid)
##### 
**Description:**  
a method to delete all session tokens associated with a user  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                     </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                </td></tr>
<tr><td>uid       </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of user in bucket</td></tr>
</tbody>
</table>
### exists
##### 
**Signature:**  
exists(self, doc_id, rev_id="")
##### 
**Description:**  
a method to determine if document exists  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                        </td></tr>
<tr><td>doc_id    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of document in bucket                    </td></tr>
<tr><td>rev_id    </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with revision id of document in bucket</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, query_criteria=None, uid="_all_users", all_versions=False, previous_id="")
##### 
**Description:**  
a generator method for retrieving documents from the bucket  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default     </th><th>Description                                                  </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None        </td><td>                                                             </td></tr>
<tr><td>query_criteria</td><td>dict  </td><td>          </td><td>None        </td><td>[optional] dictionary with valid jsonmodel query criteria    </td></tr>
<tr><td>uid           </td><td>str   </td><td>          </td><td>"_all_users"</td><td>[optional] string with uid of design document to update      </td></tr>
<tr><td>all_versions  </td><td>bool  </td><td>          </td><td>False       </td><td>boolean to include previous revisions in query               </td></tr>
<tr><td>previous_id   </td><td>str   </td><td>          </td><td>""          </td><td>[optional] string with id of the last doc in a previous query</td></tr>
</tbody>
</table>
### create
##### 
**Signature:**  
create(self, doc_details)
##### 
**Description:**  
a method to create a new document in the collection  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>doc_details</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with document details and user id value</td></tr>
</tbody>
</table>
### read
##### 
**Signature:**  
read(self, doc_id, rev_id="")
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument  </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>doc_id    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>rev_id    </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
</tbody>
</table>
### update
##### 
**Signature:**  
update(self, doc_details)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>doc_details</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, doc_id, rev_id)
##### 
**Description:**  
a method to mark a document for deletion  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                             </td></tr>
<tr><td>doc_id    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with id of document in bucket         </td></tr>
<tr><td>rev_id    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with revision id of document in bucket</td></tr>
</tbody>
</table>
### purge
##### 
**Signature:**  
purge(self, doc_ids)
##### 
**Description:**  
a method to remove docs from the collection  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>doc_ids   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string or list of strings with document ids to purge</td></tr>
</tbody>
</table>
### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove the entire bucket from the database  
### export
##### 
**Signature:**  
export(self)
##### 
**Description:**  
  

## sqlClient
### Import:
labpack.databases.sql.sqlClient  
### Description:
a class of methods for storing json valid records in a sql database  
### \__init__
##### 
**Signature:**  
\__init__(self, table_name, database_url, record_schema, rebuild=True, verbose=False)
##### 
**Description:**  
the initialization method for the sqlClient class  
<table>
<thead>
<tr><th>Argument     </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self         </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>table_name   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name for table of records                  </td></tr>
<tr><td>database_url </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with unique resource identifier to database     </td></tr>
<tr><td>record_schema</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with jsonmodel valid schema for records     </td></tr>
<tr><td>rebuild      </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to rebuild table with schema changes</td></tr>
<tr><td>verbose      </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable database logging to stdout</td></tr>
</tbody>
</table>
### exists
##### 
**Signature:**  
exists(self, primary_key)
##### 
**Description:**  
a method to determine if record exists  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                      </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                 </td></tr>
<tr><td>primary_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with primary key of record</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, query_criteria=None, order_criteria=None)
##### 
**Description:**  
a generator method to list records in table which match query criteria  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                     </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                </td></tr>
<tr><td>query_criteria</td><td>dict  </td><td>          </td><td>None     </td><td>dictionary with schema dot-path field names and query qualifiers</td></tr>
<tr><td>order_criteria</td><td>list  </td><td>          </td><td>None     </td><td>list of single keypair dictionaries with field names to order by</td></tr>
</tbody>
</table>
### create
##### 
**Signature:**  
create(self, record_details)
##### 
**Description:**  
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
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                  </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                             </td></tr>
<tr><td>record_details</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with record fields</td></tr>
</tbody>
</table>
### read
##### 
**Signature:**  
read(self, primary_key)
##### 
**Description:**  
a method to retrieve the details for a record in the table  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                      </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                 </td></tr>
<tr><td>primary_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with primary key of record</td></tr>
</tbody>
</table>
### update
##### 
**Signature:**  
update(self, new_details, old_details=None)
##### 
**Description:**  
a method to upsert changes to a record in the table  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>new_details</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary with updated record fields            </td></tr>
<tr><td>old_details</td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with original record fields</td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, primary_key)
##### 
**Description:**  
a method to delete a record in the table  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                      </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                 </td></tr>
<tr><td>primary_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with primary key of record</td></tr>
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
export(self, sql_client, merge_rule="skip", coerce=False)
##### 
**Description:**  
a method to export all the records in table to another table  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                  </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                             </td></tr>
<tr><td>sql_client</td><td>type  </td><td>Yes       </td><td>None     </td><td>class object with sql client methods                         </td></tr>
<tr><td>merge_rule</td><td>str   </td><td>          </td><td>"skip"   </td><td>string with name of rule to adopt for pre-existing records   </td></tr>
<tr><td>coerce    </td><td>bool  </td><td>          </td><td>False    </td><td>boolean to enable migration even if table schemas don't match</td></tr>
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
send_message(self, user_id, message_text, message_style="", button_list=None, small_buttons=True, persist_buttons=False, link_preview=True)
##### 
**Description:**  
a method to send a message using telegram api  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                        </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                   </td></tr>
<tr><td>user_id        </td><td>int   </td><td>Yes       </td><td>0        </td><td>integer with id of telegram user                                   </td></tr>
<tr><td>message_text   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with message to user                                        </td></tr>
<tr><td>message_style  </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with style to apply to text, only 'markdown'     </td></tr>
<tr><td>button_list    </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of string to include as buttons in message         </td></tr>
<tr><td>small_buttons  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to resize buttons to single line                </td></tr>
<tr><td>persist_buttons</td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to keep buttons around after exiting            </td></tr>
<tr><td>link_preview   </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to open up a preview window of a link in message</td></tr>
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

## pollyClient
### Import:
labpack.speech.aws.polly.pollyClient  
### Description:
a class of methods for interacting with AWS Polly API  
### \__init__
##### 
**Signature:**  
\__init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True, usage_client=None)
##### 
**Description:**  
a method for initializing the connection to AWS Polly  
<table>
<thead>
<tr><th>Argument    </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                          </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                     </td></tr>
<tr><td>access_id   </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with access_key_id from aws IAM user setup    </td></tr>
<tr><td>secret_key  </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with secret_access_key from aws IAM user setup</td></tr>
<tr><td>region_name </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name of aws region                       </td></tr>
<tr><td>owner_id    </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with aws account id                           </td></tr>
<tr><td>user_name   </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name of user access keys are assigned to </td></tr>
<tr><td>verbose     </td><td>bool    </td><td>          </td><td>True     </td><td>boolean to enable process messages                   </td></tr>
<tr><td>usage_client</td><td>function</td><td>          </td><td>None     </td><td>callable object to track resource usage              </td></tr>
</tbody>
</table>
### synthesize
##### 
**Signature:**  
synthesize(self, message_text, voice_id="Nicole", output_format="mp3", sample_rate="22050", stream_response=False)
##### 
**Description:**  
a method to synthesize speech from text  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                     </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                </td></tr>
<tr><td>message_text   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with text to synthesize                  </td></tr>
<tr><td>voice_id       </td><td>str   </td><td>          </td><td>"Nicole" </td><td>string with name of voice id in AWS polly to use</td></tr>
<tr><td>output_format  </td><td>str   </td><td>          </td><td>"mp3"    </td><td>string with file type of audio output           </td></tr>
<tr><td>sample_rate    </td><td>str   </td><td>          </td><td>"22050"  </td><td>string with the audio frequency specified in Hz </td></tr>
<tr><td>stream_response</td><td>bool  </td><td>          </td><td>False    </td><td>boolean to return a StreamingBody object        </td></tr>
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
a class of methods for managing file storage on local device in app data 

        NOTE:   appdataClient is designed to store byte data, so encoding (or 
                decoding) different types of file types must be handled by the
                application prior (or after) data is saved (or loaded)  
### \__init__
##### 
**Signature:**  
\__init__(self, collection_name="", prod_name="", org_name="", root_path="")
##### 
**Description:**  
initialization method of appdata client class  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                               </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                                          </td></tr>
<tr><td>collection_name</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of collection to store records                </td></tr>
<tr><td>prod_name      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of application product                        </td></tr>
<tr><td>org_name       </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of organization behind product                </td></tr>
<tr><td>root_path      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with path to root of collections (defaults to user home)</td></tr>
</tbody>
</table>
### exists
##### 
**Signature:**  
exists(self, record_key)
##### 
**Description:**  
a method to determine if a record exists in collection  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                         </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key of record</td></tr>
</tbody>
</table>
### save
##### 
**Signature:**  
save(self, record_key, record_data, overwrite=True, secret_key="")
##### 
**Description:**  
a method to create a record in the collection folder  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>record_key </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name to assign to record (see NOTES below)</td></tr>
<tr><td>record_data</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>byte data for record body                             </td></tr>
<tr><td>overwrite  </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite records with same name</td></tr>
<tr><td>secret_key </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with key to encrypt data            </td></tr>
</tbody>
</table>
### load
##### 
**Signature:**  
load(self, record_key, secret_key="")
##### 
**Description:**  
a method to retrieve byte data of appdata record  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of record            </td></tr>
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
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>path_filters</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary or list of dictionaries with query criteria</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, prefix="", delimiter="", filter_function=None, max_results=1, reverse_search=True, previous_key="")
##### 
**Description:**  
a method to list keys in the collection  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>prefix         </td><td>str     </td><td>          </td><td>""       </td><td>string with prefix value to filter results                     </td></tr>
<tr><td>delimiter      </td><td>str     </td><td>          </td><td>""       </td><td>string with value which results must not contain (after prefix)</td></tr>
<tr><td>filter_function</td><td>function</td><td>          </td><td>None     </td><td>(positional arguments) function used to filter results         </td></tr>
<tr><td>max_results    </td><td>int     </td><td>          </td><td>1        </td><td>integer with maximum number of results to return               </td></tr>
<tr><td>reverse_search </td><td>bool    </td><td>          </td><td>True     </td><td>boolean to search keys in reverse alphanumeric order           </td></tr>
<tr><td>previous_key   </td><td>str     </td><td>          </td><td>""       </td><td>string with key in collection to begin search after            </td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, record_key)
##### 
**Description:**  
a method to delete a file  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                        </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of file</td></tr>
</tbody>
</table>
### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove collection and all records in the collection  
### export
##### 
**Signature:**  
export(self, storage_client, overwrite=True)
##### 
**Description:**  
a method to export all the records in collection to another platform  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                             </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                        </td></tr>
<tr><td>storage_client</td><td>type  </td><td>Yes       </td><td>None     </td><td>class object with storage client methods</td></tr>
<tr><td>overwrite     </td><td>bool  </td><td>          </td><td>True     </td><td>                                        </td></tr>
</tbody>
</table>

## _s3Client
### Import:
labpack.storage.aws.s3._s3Client  
### Description:
a class of methods for interacting with AWS Simple Storage Service  
### \__init__
##### 
**Signature:**  
\__init__(self, access_id, secret_key, region_name, owner_id, user_name, verbose=True)
##### 
**Description:**  
a method for initializing the connection to S3  
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
### list_buckets
##### 
**Signature:**  
list_buckets(self)
##### 
**Description:**  
a method to retrieve a list of buckets on s3  
### create_bucket
##### 
**Signature:**  
create_bucket(self, bucket_name, access_control="private", version_control=False, log_destination=None, lifecycle_rules=None, tag_list=None, notification_settings=None, region_replication=None, access_policy=None)
##### 
**Description:**  
a method for creating a bucket on AWS S3  
<table>
<thead>
<tr><th>Argument             </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self                 </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>bucket_name          </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                                     </td></tr>
<tr><td>access_control       </td><td>str   </td><td>          </td><td>"private"</td><td>string with type of access control policy                      </td></tr>
<tr><td>version_control      </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable versioning of records             </td></tr>
<tr><td>log_destination      </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with bucket name and prefix of log bucket</td></tr>
<tr><td>lifecycle_rules      </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of dictionaries with rules for aging data      </td></tr>
<tr><td>tag_list             </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of dictionaries with key and value for tag     </td></tr>
<tr><td>notification_settings</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of dictionaries with notification details      </td></tr>
<tr><td>region_replication   </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with replication settings (WIP)          </td></tr>
<tr><td>access_policy        </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with policy for user access (WIP)        </td></tr>
</tbody>
</table>
### read_bucket
##### 
**Signature:**  
read_bucket(self, bucket_name)
##### 
**Description:**  
a method to retrieve properties of a bucket in s3  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description               </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                          </td></tr>
<tr><td>bucket_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket</td></tr>
</tbody>
</table>
### update_bucket
##### 
**Signature:**  
update_bucket(self, bucket_name, access_control="private", version_control=False, log_destination=None, lifecycle_rules=None, tag_list=None, notification_settings=None, region_replication=None, access_policy=None)
##### 
**Description:**  
a method for updating the properties of a bucket in S3  
<table>
<thead>
<tr><th>Argument             </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self                 </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>bucket_name          </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                                     </td></tr>
<tr><td>access_control       </td><td>str   </td><td>          </td><td>"private"</td><td>string with type of access control policy                      </td></tr>
<tr><td>version_control      </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable versioning of records             </td></tr>
<tr><td>log_destination      </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with bucket name and prefix of log bucket</td></tr>
<tr><td>lifecycle_rules      </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of dictionaries with rules for aging data      </td></tr>
<tr><td>tag_list             </td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of dictionaries with key and value for tag     </td></tr>
<tr><td>notification_settings</td><td>list  </td><td>          </td><td>None     </td><td>[optional] list of dictionaries with notification details      </td></tr>
<tr><td>region_replication   </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with replication settings (WIP)          </td></tr>
<tr><td>access_policy        </td><td>dict  </td><td>          </td><td>None     </td><td>[optional] dictionary with policy for user access (WIP)        </td></tr>
</tbody>
</table>
### delete_bucket
##### 
**Signature:**  
delete_bucket(self, bucket_name)
##### 
**Description:**  
a method to delete a bucket in s3 and all its contents  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description               </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                          </td></tr>
<tr><td>bucket_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket</td></tr>
</tbody>
</table>
### list_records
##### 
**Signature:**  
list_records(self, bucket_name, prefix="", delimiter="", max_results=1000, starting_key="")
##### 
**Description:**  
a method for retrieving a list of the versions of records in a bucket  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>bucket_name </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                                     </td></tr>
<tr><td>prefix      </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with value limiting results to key prefix    </td></tr>
<tr><td>delimiter   </td><td>str   </td><td>          </td><td>""       </td><td>string with value which results must not contain (after prefix)</td></tr>
<tr><td>max_results </td><td>int   </td><td>          </td><td>1000     </td><td>[optional] integer with max results to return                  </td></tr>
<tr><td>starting_key</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with key value to continue search with       </td></tr>
</tbody>
</table>
### list_versions
##### 
**Signature:**  
list_versions(self, bucket_name, prefix="", delimiter="", max_results=1000, starting_key="", starting_version="")
##### 
**Description:**  
a method for retrieving a list of the versions of records in a bucket  
<table>
<thead>
<tr><th>Argument        </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                   </th></tr>
</thead>
<tbody>
<tr><td>self            </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                              </td></tr>
<tr><td>bucket_name     </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                                    </td></tr>
<tr><td>prefix          </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with value limiting results to key prefix   </td></tr>
<tr><td>delimiter       </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with value limiting results to key delimiter</td></tr>
<tr><td>max_results     </td><td>int   </td><td>          </td><td>1000     </td><td>[optional] integer with max results to return                 </td></tr>
<tr><td>starting_key    </td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with key value to continue search with      </td></tr>
<tr><td>starting_version</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with version id to continue search with     </td></tr>
</tbody>
</table>
### create_record
##### 
**Signature:**  
create_record(self, bucket_name, record_key, record_data, record_metadata=None, record_mimetype="", record_encoding="", overwrite=True)
##### 
**Description:**  
a method for adding a record to an S3 bucket  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                            </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                       </td></tr>
<tr><td>bucket_name    </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name of bucket                             </td></tr>
<tr><td>record_key     </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name of key (path) for record              </td></tr>
<tr><td>record_data    </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>byte data for record                                   </td></tr>
<tr><td>record_metadata</td><td>dict    </td><td>          </td><td>None     </td><td>[optional] dictionary with metadata to attach to record</td></tr>
<tr><td>record_mimetype</td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with content mimetype of record data </td></tr>
<tr><td>record_encoding</td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with content encoding of record data </td></tr>
<tr><td>overwrite      </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite any existing record    </td></tr>
</tbody>
</table>
### read_headers
##### 
**Signature:**  
read_headers(self, bucket_name, record_key, record_version="", version_check=False)
##### 
**Description:**  
a method for retrieving the headers of a record from s3  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>bucket_name   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                        </td></tr>
<tr><td>record_key    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key value of record                   </td></tr>
<tr><td>record_version</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with aws id of version of record</td></tr>
<tr><td>version_check </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable current version check</td></tr>
</tbody>
</table>
### read_record
##### 
**Signature:**  
read_record(self, bucket_name, record_key, record_version="", version_check=False)
##### 
**Description:**  
a method for retrieving data of record from AWS S3  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>bucket_name   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                        </td></tr>
<tr><td>record_key    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of key (path) for record         </td></tr>
<tr><td>record_version</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with aws id of version of record</td></tr>
<tr><td>version_check </td><td>bool  </td><td>          </td><td>False    </td><td>[optional] boolean to enable current version check</td></tr>
</tbody>
</table>
### delete_record
##### 
**Signature:**  
delete_record(self, bucket_name, record_key, record_version="")
##### 
**Description:**  
a method for deleting an object record in s3  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                       </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                  </td></tr>
<tr><td>bucket_name   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                        </td></tr>
<tr><td>record_key    </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key value of record                   </td></tr>
<tr><td>record_version</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with aws id of version of record</td></tr>
</tbody>
</table>
### export_records
##### 
**Signature:**  
export_records(self, bucket_name, export_path="", overwrite=True)
##### 
**Description:**  
a method to export all the records from a bucket to local files  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>bucket_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                                     </td></tr>
<tr><td>export_path</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with path to root directory for record dump  </td></tr>
<tr><td>overwrite  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite existing files matching records</td></tr>
</tbody>
</table>
### import_records
##### 
**Signature:**  
import_records(self, bucket_name, import_path="", overwrite=True)
##### 
**Description:**  
a method to importing records from local files to a bucket  
<table>
<thead>
<tr><th>Argument   </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>bucket_name</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of bucket                                     </td></tr>
<tr><td>import_path</td><td>str   </td><td>          </td><td>""       </td><td>                                                               </td></tr>
<tr><td>overwrite  </td><td>bool  </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite existing files matching records</td></tr>
</tbody>
</table>

## s3Client
### Import:
labpack.storage.aws.s3.s3Client  
### Description:
a class of methods to manage file storage on AWS S3  
### \__init__
##### 
**Signature:**  
\__init__(self, access_id, secret_key, region_name, owner_id, user_name, collection_name="", prod_name="", org_name="", access_control="private", version_control=False, log_destination=None, lifecycle_rules=None, tag_list=None, notification_settings=None, region_replication=None, access_policy=None, verbose=True)
##### 
**Description:**  
  
<table>
<thead>
<tr><th>Argument             </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description  </th></tr>
</thead>
<tbody>
<tr><td>self                 </td><td>object  </td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>access_id            </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>secret_key           </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>region_name          </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>owner_id             </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>user_name            </td><td>NoneType</td><td>Yes       </td><td>None     </td><td>             </td></tr>
<tr><td>collection_name      </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>prod_name            </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>org_name             </td><td>str     </td><td>          </td><td>""       </td><td>             </td></tr>
<tr><td>access_control       </td><td>str     </td><td>          </td><td>"private"</td><td>             </td></tr>
<tr><td>version_control      </td><td>bool    </td><td>          </td><td>False    </td><td>             </td></tr>
<tr><td>log_destination      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>lifecycle_rules      </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>tag_list             </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>notification_settings</td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>region_replication   </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>access_policy        </td><td>NoneType</td><td>          </td><td>None     </td><td>             </td></tr>
<tr><td>verbose              </td><td>bool    </td><td>          </td><td>True     </td><td>             </td></tr>
</tbody>
</table>
### exists
##### 
**Signature:**  
exists(self, record_key)
##### 
**Description:**  
a method to determine if a record exists in collection  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                         </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key of record</td></tr>
</tbody>
</table>
### save
##### 
**Signature:**  
save(self, record_key, record_data, overwrite=True, secret_key="")
##### 
**Description:**  
a method to create a file in the collection folder on S3  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>record_key </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name to assign to record (see NOTES below)</td></tr>
<tr><td>record_data</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>byte data for record body                             </td></tr>
<tr><td>overwrite  </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite records with same name</td></tr>
<tr><td>secret_key </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with key to encrypt data            </td></tr>
</tbody>
</table>
### load
##### 
**Signature:**  
load(self, record_key, secret_key="")
##### 
**Description:**  
a method to retrieve byte data of an S3 record  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of record            </td></tr>
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
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>path_filters</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary or list of dictionaries with query criteria</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, prefix="", delimiter="", filter_function=None, max_results=1, previous_key="")
##### 
**Description:**  
a method to list keys in the collection  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                              </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                         </td></tr>
<tr><td>prefix         </td><td>str     </td><td>          </td><td>""       </td><td>string with prefix value to filter results               </td></tr>
<tr><td>delimiter      </td><td>str     </td><td>          </td><td>""       </td><td>string with value results must not contain (after prefix)</td></tr>
<tr><td>filter_function</td><td>function</td><td>          </td><td>None     </td><td>(positional arguments) function used to filter results   </td></tr>
<tr><td>max_results    </td><td>int     </td><td>          </td><td>1        </td><td>integer with maximum number of results to return         </td></tr>
<tr><td>previous_key   </td><td>str     </td><td>          </td><td>""       </td><td>string with key in collection to begin search after      </td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, record_key)
##### 
**Description:**  
a method to delete a record from S3  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                         </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key of record</td></tr>
</tbody>
</table>
### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove collection and all records in the collection  
### export
##### 
**Signature:**  
export(self, storage_client, overwrite=True)
##### 
**Description:**  
a method to export all the records in collection to another platform  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                             </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                        </td></tr>
<tr><td>storage_client</td><td>type  </td><td>Yes       </td><td>None     </td><td>class object with storage client methods</td></tr>
<tr><td>overwrite     </td><td>bool  </td><td>          </td><td>True     </td><td>                                        </td></tr>
</tbody>
</table>

## dropboxClient
### Import:
labpack.storage.dropbox.dropboxClient  
### Description:
a class of methods to manage file storage on Dropbox API  
### \__init__
##### 
**Signature:**  
\__init__(self, access_token, collection_name="")
##### 
**Description:**  
a method to initialize the dropboxClient class  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                      </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                 </td></tr>
<tr><td>access_token   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with oauth2 access token for users account</td></tr>
<tr><td>collection_name</td><td>str   </td><td>          </td><td>""       </td><td>                                                 </td></tr>
</tbody>
</table>
### exists
##### 
**Signature:**  
exists(self, record_key)
##### 
**Description:**  
a method to determine if a record exists in collection  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                         </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key of record</td></tr>
</tbody>
</table>
### save
##### 
**Signature:**  
save(self, record_key, record_data, overwrite=True, secret_key="")
##### 
**Description:**  
a method to create a record in the collection folder  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>record_key </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name to assign to record (see NOTES below)</td></tr>
<tr><td>record_data</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>byte data for record body                             </td></tr>
<tr><td>overwrite  </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite records with same name</td></tr>
<tr><td>secret_key </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with key to encrypt data            </td></tr>
</tbody>
</table>
### load
##### 
**Signature:**  
load(self, record_key, secret_key="")
##### 
**Description:**  
a method to retrieve byte data of appdata record  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of record            </td></tr>
<tr><td>secret_key</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string used to decrypt data</td></tr>
</tbody>
</table>
### conditional_filter
##### 
**Signature:**  
conditional_filter(self, path_filters)
##### 
**Description:**  
a method to construct a conditional filter function for list method  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>path_filters</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary or list of dictionaries with query criteria</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, prefix="", delimiter="", filter_function=None, max_results=1, previous_key="")
##### 
**Description:**  
a method to list keys in the dropbox collection  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>prefix         </td><td>str     </td><td>          </td><td>""       </td><td>string with prefix value to filter results                     </td></tr>
<tr><td>delimiter      </td><td>str     </td><td>          </td><td>""       </td><td>string with value which results must not contain (after prefix)</td></tr>
<tr><td>filter_function</td><td>function</td><td>          </td><td>None     </td><td>(positional arguments) function used to filter results         </td></tr>
<tr><td>max_results    </td><td>int     </td><td>          </td><td>1        </td><td>integer with maximum number of results to return               </td></tr>
<tr><td>previous_key   </td><td>str     </td><td>          </td><td>""       </td><td>string with key in collection to begin search after            </td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, record_key)
##### 
**Description:**  
a method to delete a file  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                        </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of file</td></tr>
</tbody>
</table>
### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove all records in the collection

        NOTE:   this method removes all the files in the collection, but the
                collection folder itself created by oauth2 cannot be removed.
                only the user can remove the app folder  
### export
##### 
**Signature:**  
export(self, storage_client, overwrite=True)
##### 
**Description:**  
a method to export all the records in collection to another platform  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                             </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                        </td></tr>
<tr><td>storage_client</td><td>type  </td><td>Yes       </td><td>None     </td><td>class object with storage client methods</td></tr>
<tr><td>overwrite     </td><td>bool  </td><td>          </td><td>True     </td><td>                                        </td></tr>
</tbody>
</table>

## driveClient
### Import:
labpack.storage.google.drive.driveClient  
### Description:
a class of methods to manage file storage on Google Drive API  
### \__init__
##### 
**Signature:**  
\__init__(self, access_token, collection_name="")
##### 
**Description:**  
a method to initialize the driveClient class  
<table>
<thead>
<tr><th>Argument       </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                         </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                    </td></tr>
<tr><td>access_token   </td><td>str   </td><td>Yes       </td><td>""       </td><td>string with oauth2 access token for users account   </td></tr>
<tr><td>collection_name</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string with name of collection for import</td></tr>
</tbody>
</table>
### exists
##### 
**Signature:**  
exists(self, record_key)
##### 
**Description:**  
a method to determine if a record exists in collection  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description              </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                         </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with key of record</td></tr>
</tbody>
</table>
### save
##### 
**Signature:**  
save(self, record_key, record_data, overwrite=True, secret_key="")
##### 
**Description:**  
a method to create a record in the collection folder  
<table>
<thead>
<tr><th>Argument   </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self       </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>record_key </td><td>str     </td><td>Yes       </td><td>""       </td><td>string with name to assign to record (see NOTES below)</td></tr>
<tr><td>record_data</td><td>NoneType</td><td>Yes       </td><td>None     </td><td>byte data for record body                             </td></tr>
<tr><td>overwrite  </td><td>bool    </td><td>          </td><td>True     </td><td>[optional] boolean to overwrite records with same name</td></tr>
<tr><td>secret_key </td><td>str     </td><td>          </td><td>""       </td><td>[optional] string with key to encrypt data            </td></tr>
</tbody>
</table>
### load
##### 
**Signature:**  
load(self, record_key, secret_key="")
##### 
**Description:**  
a method to retrieve byte data of appdata record  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                           </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                      </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of record            </td></tr>
<tr><td>secret_key</td><td>str   </td><td>          </td><td>""       </td><td>[optional] string used to decrypt data</td></tr>
</tbody>
</table>
### conditional_filter
##### 
**Signature:**  
conditional_filter(self, path_filters)
##### 
**Description:**  
a method to construct a conditional filter function for list method  
<table>
<thead>
<tr><th>Argument    </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                                           </th></tr>
</thead>
<tbody>
<tr><td>self        </td><td>object</td><td>Yes       </td><td>None     </td><td>                                                      </td></tr>
<tr><td>path_filters</td><td>dict  </td><td>Yes       </td><td>None     </td><td>dictionary or list of dictionaries with query criteria</td></tr>
</tbody>
</table>
### list
##### 
**Signature:**  
list(self, prefix="", delimiter="", filter_function=None, max_results=1, previous_key="")
##### 
**Description:**  
a method to list keys in the google drive collection  
<table>
<thead>
<tr><th>Argument       </th><th>Type    </th><th>Required  </th><th>Default  </th><th>Description                                                    </th></tr>
</thead>
<tbody>
<tr><td>self           </td><td>object  </td><td>Yes       </td><td>None     </td><td>                                                               </td></tr>
<tr><td>prefix         </td><td>str     </td><td>          </td><td>""       </td><td>string with prefix value to filter results                     </td></tr>
<tr><td>delimiter      </td><td>str     </td><td>          </td><td>""       </td><td>string with value which results must not contain (after prefix)</td></tr>
<tr><td>filter_function</td><td>function</td><td>          </td><td>None     </td><td>(positional arguments) function used to filter results         </td></tr>
<tr><td>max_results    </td><td>int     </td><td>          </td><td>1        </td><td>integer with maximum number of results to return               </td></tr>
<tr><td>previous_key   </td><td>str     </td><td>          </td><td>""       </td><td>string with key in collection to begin search after            </td></tr>
</tbody>
</table>
### delete
##### 
**Signature:**  
delete(self, record_key)
##### 
**Description:**  
a method to delete a file  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                        </td></tr>
<tr><td>record_key</td><td>str   </td><td>Yes       </td><td>""       </td><td>string with name of file</td></tr>
</tbody>
</table>
### remove
##### 
**Signature:**  
remove(self)
##### 
**Description:**  
a method to remove all records in the collection

        NOTE:   this method removes all the files in the collection, but the
                collection folder itself created by oauth2 cannot be removed.
                only the user can remove access to the app folder  
### export
##### 
**Signature:**  
export(self, storage_client, overwrite=True)
##### 
**Description:**  
a method to export all the records in collection to another platform  
<table>
<thead>
<tr><th>Argument      </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                             </th></tr>
</thead>
<tbody>
<tr><td>self          </td><td>object</td><td>Yes       </td><td>None     </td><td>                                        </td></tr>
<tr><td>storage_client</td><td>type  </td><td>Yes       </td><td>None     </td><td>class object with storage client methods</td></tr>
<tr><td>overwrite     </td><td>bool  </td><td>          </td><td>True     </td><td>                                        </td></tr>
</tbody>
</table>
