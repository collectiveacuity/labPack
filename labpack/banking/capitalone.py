__author__ = 'rcj1492'
__created__ = '2017.10'
__license__ = 'MIT'

# TODO: generalize requests based response handler classes
class depositsHandler(object):

    ''' handles responses from capital one deposits api and usage data '''

    _class_fields = {
        'schema': {
            'rate_limits': [
                {'requests': 24000, 'period': 24 * 3600 }
            ]
        }
    }

    def __init__(self, usage_client=None):

        '''
            initialization method for deposits handler class
            
        :param usage_client: callable that records usage data
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct initial methods
        self.rate_limits = self.fields.schema['rate_limits']
        self.usage_client = usage_client
    
    # construct error map
        self.error_map = { 
            429: "The request has been rejected because of rate limiting -- you've sent too many requests in a given amount of time.",
            500: "General server error.",
            502: "Internal connection failure.",
            503: "The server is unavailable due to heavy traffic or maintenance."
        }

    def handle(self, response, error_map=None):

    # construct default response details
        details = {
            'method': response.request.method,
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers
        }
    
    # create request specific error map
        if not error_map or not isinstance(error_map, dict):
            error_map = {}
        for key, value in self.error_map.items():
            error_map[key] = value

    # handle different codes
        if details['code'] in (200, 201, 202):
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()

        return details
    
class depositsClient(object):
    
    _class_fields = {
        'schema': {
            'client_id': 'abcdefghijkl0123456789mnopqrstuvwxyz',
            'client_secret': 'ABCDEFGHIJKL0123456789MNOPQRSTUVWXYZ',
            'requests_handler': 'labpack.handlers.requests.handle_requests',
            'usage_client': '',
            'additional_fields': {},
            'product_id': 0
        }
    }
    
    def __init__(self, client_id, client_secret, get_details=True, sandbox=False, requests_handler=None, usage_client=None):
        
        ''' the initialization method for the capital one client

        :param client_id: string with client id registered for app with service
        :param client_secret: string with client secret registered for app with service
        :param get_details: boolean to automatically retrieve, store and refresh account details
        :param sandbox: boolean to send requests to test sandbox
        :param requests_handler: callable that handles requests errors
        :param usage_client: callable that records usage data
        '''

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'client_id': client_id,
            'client_secret': client_secret,
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct class properties
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
        self.token_endpoint = 'https://api.capitalone.com/oauth2/token'
        self.deposits_endpoint = 'https://api.capitalone.com/deposits/'
        if sandbox:
            self.token_endpoint = 'https://api-sandbox.capitalone.com/oauth2/token'
            self.deposits_endpoint = 'https://api-sandbox.capitalone.com/deposits/'
        self.access_token = None
        self.expires_at = 0

    # construct handlers
        self.requests_handler = requests_handler
        self.response_handler = depositsHandler(usage_client)

    def access_token(self):

        ''' a method to acquire an oauth access token '''

        title = '%s.access_token' % self.__class__.__name__
    
    # import dependencies
        from time import time
        import requests

    # construct request kwargs
        request_kwargs = {
            'url': self.token_endpoint,
            'data': {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
        }

    # send request
        try:
            current_time = time()
            response = requests.post(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'POST'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

        response_details = self.response_handler.handle(response)

        if response_details['json']:
            self.access_token = response_details['json']['access_token']
            expires_in = response_details['json']['expires_in']
            self.expires_at = current_time + expires_in
            
        return self.access_token

    def _requests(self, url, method='GET', headers=None, params=None, data=None, errors=None):

        ''' a helper method for relaying requests from client to api '''

        from time import time
        import requests

    # validate access token
        if not self.access_token:
            self.access_token()
    
    # refresh token
        current_time = time()
        if current_time > self.expires_at:
            self.access_token()

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': { 'Authorization': 'Bearer %s' % self.access_token },
            'params': {},
            'data': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)
        if data:
            request_kwargs['data'].update(data)

    # send request
        if method == 'POST':
            try:
                response = requests.post(**request_kwargs)
            except Exception:
                if self.requests_handler:
                    request_kwargs['method'] = 'POST'
                    request_object = requests.Request(**request_kwargs)
                    return self.requests_handler(request_object)
                else:
                    raise
        elif method == 'GET':
            try:
                response = requests.get(**request_kwargs)
            except Exception:
                if self.requests_handler:
                    request_kwargs['method'] = 'GET'
                    request_object = requests.Request(**request_kwargs)
                    return self.requests_handler(request_object)
                else:
                    raise
        else:
            raise ValueError('_request(method='') must be either GET or POST')

    # handle response
        response_details = self.response_handler.handle(response, errors)
        
        return response_details
    
    def account_products(self):
        
        ''' a method to retrieve a list of the account products 

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
        '''

        title = '%s.account_products' % self.__class__.__name__
        
    # construct url
        url = self.deposits_endpoint + 'account-products'
    
    # send request
        details = self._requests(url)

        return details
    
    def account_product(self, product_id):
        
        ''' a method to retrieve details about a particular account product 
        
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
        '''
    
        title = '%s.account_product' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'product_id': product_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # construct url
        url = self.deposits_endpoint + 'account-products/%s' % product_id
    
    # construct method specific errors
        error_map = { 
            404: 'Not Found. No products found for the provided productId.'
        }

    # send request
        details = self._requests(url, errors=error_map)

        return details

# TODO retrieve account product details at init    
    def get_details(self):
        
        pass
    
    def account_application(self, customer_ip, first_name, last_name, tax_id, date_of_birth, address_line_1, city_name, state_code, postal_code, phone_number, email_address, citizenship_country, employment_status, product_id, funding_amount, account_number, routing_number, backup_withholding=False, phone_type='mobile', accept_tcpa=False, accept_terms=True, address_line_2='', middle_name='', tax_id_type='SSN', secondary_citizenship_country='', job_title='', annual_income=0, cd_term='', funding_type='fundach', account_owner='primary', secondary_application=None):

        '''
            a method to submit application for new account
            
        :param customer_ip: string with ip address of applicant
        :param first_name: string with first name of applicant
        :param last_name: string with last name of applicant
        :param tax_id: string with tax id number of applicant
        :param date_of_birth: string with ISO format of date of birth of applicant
        :param address_line_1: string with first line of street address of applicant
        :param city_name: string with name of city of address of applicant
        :param state_code: string with code for the state of address of applicant
        :param postal_code: string with postal code of address of applicant
        :param phone_number: 
        :param email_address: 
        :param citizenship_country: 
        :param employment_status: 
        :param product_id: 
        :param funding_amount: 
        :param account_number: 
        :param routing_number: 
        :param backup_withholding: 
        :param phone_type: 
        :param accept_tcpa: 
        :param accept_terms: 
        :param address_line_2: 
        :param middle_name: string with middle name of applicant
        :param tax_id_type: 
        :param secondary_citizenship_country: 
        :param job_title: 
        :param annual_income: 
        :param cd_term: 
        :param funding_type: 
        :param account_owner: 
        :param secondary_application: 
        :return: dictionary with successful response details in ['json'] key
        
        "customer_ip": "123.456.789.0",
        "first_name": "tom",
        "last_name": "curtiss,
        "middle_name": "",
        "tax_id": "123456789",
        "tax_id_type": "SSN",
        "date_of_birth": "2017-10-10",
        "address_line_1": "1 Cloud Drive",
        "city_name": "Server Farm",
        "state_code": "VA",
        "postal_code": "10101"
        
            "components": {
                ".tax_id": { 
                    "must_contain": [ "\d{3}\-?\d{2}\-?\d{4}" ]
                },
                ".date_of_birth": {
                    "must_contain": [ "\d{4}\-?\d{2}\-?\d{2}" ]
                },
                ".phone_type": {
                    "discrete_values": ['mobile', 'home', 'work']
                },
                ".tax_id_type": {
                    "discrete_values": [ 'SSN', 'ITIN' ]
                },
                ".employment_status": {
                    "discrete_values": [ 'Employed', 'Self-Employed', 'Retired', 'Student', 'Unemployed' ]
                },
                ".product_id": {
                    "discrete_values": [ 3000, 3300, 3500 ]
                },
                ".funding_type": {
                    "discrete_values": [ 'fundach' ]
                },
                ".funding_amount": {
                    "min_value": 0.01
                },
                ".account_owner": {
                    "discrete_values": [ 'primary', 'secondary', 'both' ]
                }
            }
        response details:
        { 
            "error": "",
            "code": 200,
            "method": "GET",
            "url": "https://...",
            "headers": { },
            "json": { }
        }
        '''
    
        title = '%s.account_application' % self.__class__.__name__
        
        from copy import deepcopy
        
    # validate general inputs
        input_fields = {
            'customer_ip': customer_ip
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # validate other fields
        app_fields = {
            'address_line_1': address_line_1
        }
        for key, value in app_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct url
        url = self.deposits_endpoint + 'account-application'
    
    # construct method specific errors
        error_map = { 
            404: 'Not Found. No products found for the provided productId.'
        }

    # construct headers
        headers_kwargs = {
            'Customer-IP-Address': customer_ip
        }

    # construct applicant list
        applicant_list = []
        applicants = [ 'primary' ]
        if secondary_application:
            applicants.append('secondary')
    
    # iterate over applicants
        for applicant in applicants:
        
        # substitute in secondary application fields
            if applicant == 'secondary':
                app_fields = secondary_application
                for key, value in app_fields.items():
                    object_title = '%s(%s=%s)' % (title, key, str(value))
                    self.fields.validate(value, '.%s' % key, object_title)  

        # construct applicant kwargs
            applicant_kwargs = {
                'applicantRole': applicant,
                'firstName': app_fields['first_name'],
                'lastName': app_fields['last_name'],
                'homeAddress': {
                    'addressLine1': app_fields['address_line_1'],
                    'city': app_fields['city_name'],
                    'stateCode': app_fields['state_code'],
                    'postalCode': app_fields['postal_code']
                },
                'tax_id_type': app_fields['tax_id_type'],
            }

        # add optional middle name and second address
            if app_fields['middle_name']:
                applicant_kwargs['middleName'] = app_fields['middle_name']
        
        # add tax id
            if len(app_fields['tax_id']) < 10:
                tax_id_temp = app_fields['tax_id']
                tax_string = tax_id_temp[0:3] + '-' + tax_id[3:5] + '-' + tax_id[5:]
            else:
                tax_string = tax_id
            applicant_kwargs['taxId'] = tax_string
            
        # add annual income field
            if app_fields['annual_income']:
                income_category = 250000
                income_list = [ { 50000: 25000 }, { 100000: 75000 }, { 150000: 125000 }, { 250000: 200000 } ]
                for level in income_list:
                    key, value = next(iter(level.items()))
                    if app_fields['annual_income'] > int(key):
                        continue
                    elif int(key) != 25000:
                        income_category = int(value)
                        break
                applicant_kwargs['annualIncome'] = income_category
    
        # add phone number fields
            phone_kwargs = {
                'phoneNumber': app_fields['phone_number'],
                'acceptedTcpa': app_fields['accept_tcpa']
            }
            if phone_type == 'mobile':
                applicant_kwargs['mobilePhoneNumber'] = phone_kwargs
            elif phone_type == 'home':
                applicant_kwargs['homePhoneNumber'] = phone_kwargs
            elif phone_type == 'work':
                applicant_kwargs['workPhoneNumber'] = phone_kwargs

        # add applicant fields to data kwargs
            applicant_copy = deepcopy(applicant_kwargs)
            applicant_list.append(applicant_copy)
    
    # construct data fields
        data_kwargs = {
            'applicants': applicant_list,
            'productId': product_id
        }
        
    # add cd term
        if product_id == 3500:
            if not cd_term:
                raise IndexError('%s(cd_term=0) must not be empty if product_id=3500')
            else:
                data_kwargs['cdTerm'] = cd_term
        
    # add funding details
        funding_details = {
            'fundingType': funding_type,
            'fundingAmount': funding_amount,
            'externalAccountDetails': {
                'accountNumber': account_number,
                'bankABANumber': routing_number,
                'accountOwnership': account_owner
            }
        }
        data_kwargs['fundingDetails'] = funding_details
    
    # add terms and conditions
        term_details = {
            'acceptAccountDisclosures': accept_terms,
            'acceptPaperlessAgreement': accept_terms,
            'acceptFraudProtection': accept_terms
        }
        data_kwargs['termsAndConditions'] = term_details
        
    # send request
        details = self._requests(url, method='POST', headers=headers_kwargs, data=data_kwargs, errors=error_map)

        return details