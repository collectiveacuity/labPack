__author__ = 'rcj1492'
__created__ = '2015.06'

class meetupHandler(object):

    ''' handles responses from meetup api and usage data'''

    _class_fields = {
        'schema': {
            'rate_limits': [
                {'requests': 30, 'period': 10}
            ]
        }
    }

    def __init__(self, usage_client=None):

        ''' initialization method for meetup handler class

        :param usage_client: callable that records usage data
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct initial methods
        self.rate_limits = self.fields.schema['rate_limits']
        self.usage_client = usage_client

    def handle(self, response):

    # construct default response details
        details = {
            'method': response.request.method,
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers
        }

    # rate limit headers:
        # https://www.meetup.com/meetup_api/docs/#limits
        # X-RateLimit-Limit
        # X-RateLimit-Remaining
        # X-RateLimit-Reset

    # handle different codes
        if details['code'] == 200 or details['code'] == 201 or details['code'] == 202:
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()

        return details

class meetupRegister(object):
    ''' currently must be done manually '''
    # https://secure.meetup.com/meetup_api/oauth_consumers/
    def __init__(self, app_settings):
        pass

    def setup(self):
        return self

    def update(self):
        return self

class meetupClient(object):

    ''' a class of methods for managing user events, groups and profile on Meetup API '''

    # use labpack.authentication.oauth2.oauth2Client to obtain access token

    _class_fields = {
        'schema': {
            'api_endpoint': 'https://api.meetup.com',
            'access_token': '1350d78219f4dc9ded18c7fbda86a19e',
            'service_scope': ['ageless'],
            'requests_handler': 'labpack.handlers.requests.handle_requests',
            'usage_client': 'labpack.storage.appdata.appdataClient.__init__',
            'member_id': 12345678,
            'group_url': 'myfavoritegroup',
            'group_id': 23456789,
            'event_id': 23454321,
            'venue_id': 123456,
            'max_results': 4,
            'radius': 10.0,
            'topics': [ 123 ],
            'categories': [ 12 ],
            'zip_code': '94203',
            'city_name': 'Sacramento',
            'country_code': 'US',
            'longitude': 12.345678,
            'latitude': 12.345679,
            'text': 'favorite group',
            'location': 'state capital building',
            'membership_answers': [
                {
                    'question_id': 1234567,
                    'answer_text': 'my name'
                }
            ],
            'exit_comment': 'better deal',
            'attendance_answers': [
                {
                    'question_id': 1234567,
                    'answer_text': 'my name'
                }
            ],
            'additional_guests': 0,
            'payment_service': '',
            'payment_code': ''
        },
        'components': {
            '.service_scope': {
                'unique_values': True
            },
            '.service_scope[0]': {
                'discrete_values': ['ageless', 'basic', 'event_management', 'group_edit', 'group_content', 'group_join', 'profile_edit', 'reporting', 'rsvp']
            },
            '.topics[0]': {
                'integer_data': True
            },
            '.categories[0]': {
                'integer_data': True
            },
            '.max_results': {
                'integer_data': True
            },
            '.member_id': {
                'integer_data': True
            },
            '.event_id': {
                'integer_data': True
            },
            '.group_id': {
                'integer_data': True
            },
            '.venue_id': {
                'integer_data': True
            },
            '.radius': {
                'min_value': 0.0,
                'max_value': 100.0
            },
            '.latitude': {
                'min_value': -90.0,
                'max_value': 90.0
            },
            '.longitude': {
                'min_value': -90.0,
                'max_value': 90.0
            },
            '.zip_code': {
                'max_length': 5,
                'min_length': 5,
                'must_contain': [ '\\d{5}' ]
            },
            '.country_code': {
                'max_length': 2,
                'min_length': 2,
                'must_contain': [ '[A-Z]{2}' ]
            },
            '.membership_answers[0].question_id': {
                'integer_data': True
            },
            '.attendance_answers[0].question_id': {
                'integer_data': True
            },
            '.additional_guests': {
                'integer_data': True,
                'min_value': 0
            }
        }
    }

    _class_objects = {
        'profile_brief': {
            'schema': {
                'bio': '',
                'city': '',
                'country': '',
                'id': '',
                'joined': '',
                'lang': '',
                'lat': '',
                'link': '',
                'lon': '',
                'name': '',
                'photo_url': '',
                'state': '',
                'visited': '',
                'zip': ''
            }
        },
        'profile': {
            'schema': {
                'bio': '',
                'birthday': {
                    'day': 0,
                    'month': 0,
                    'year': 0
                },
                'city': '',
                'country': '',
                'gender': '',
                'group_profile': {},
                'id': 0,
                'joined': 0,
                'last_event': {},
                'lat': 0.0,
                'localized_country_name': '',
                'lon': 0.0,
                'messaging_pref': '',
                'name': '',
                'next_event': {},
                'other_services': {
                    'facebook': {'identifier': '', 'url': ''},
                    'linkedin': {'identifier': '', 'url': ''},
                    'twitter': {'identifier': '', 'url': ''}
                },
                'photo': {},
                'privacy': {
                    'bio': '',
                    'groups': '',
                    'topics': '',
                    'facebook': ''
                },
                'self': {},
                'state': '',
                'stats': {
                    'groups': 0,
                    'rsvps': 0,
                    'topics': 0
                },
                'status': ''
            },
            'components': {
                '.': {
                    'extra_fields': True
                },
                '.birthday.day': {
                    'integer_data': True
                },
                '.birthday.month': {
                    'integer_data': True
                },
                '.birthday.year': {
                    'integer_data': True
                },
                '.id': {
                    'integer_data': True
                },
                '.joined': {
                    'integer_data': True
                },
                '.other_services': {
                    'extra_fields': True
                },
                '.other_services.facebook': {
                    'extra_fields': True
                },
                '.other_services.twitter': {
                    'extra_fields': True
                },
                '.other_services.linkedin': {
                    'extra_fields': True
                },
                '.stats.groups': {
                    'integer_data': True
                },
                '.stats.rsvps': {
                    'integer_data': True
                },
                '.stats.topics': {
                    'integer_data': True
                }
            }
        },
        'topic': {
            'schema': {
                'urlkey': 'diningout',
                'lang': 'en_US',
                'id': 713,
                'name': 'Dining Out'
            },
            'components': {
                '.id': {
                    'integer_data': True
                }
            }
        },
        'self': {
            'schema': {
                'actions': [''],
                'common': {
                    'groups': [{}]
                },
                'blocks': False,
                'friends': False
            }
        },
        'group_profile': {
            'schema': {
                'created': 0,
                'answers': [ {
                    'answer': '',
                    'question': '',
                    'question_id': 0
                }],
                'group': {},
                'role': '',
                'status': '',
                'updated': 0,
                'visited': 0
            },
            'components': {
                '.': {
                    'extra_fields': True
                },
                '.created': {
                    'integer_data': True
                },
                '.updated': {
                    'integer_data': True
                },
                '.visited': {
                    'integer_data': True
                }
            }
        },
        'event': {
            'schema': {
                'id': '123456789',
                'name': 'My Favorite Event',
                'created': 1234567890000,
                'updated': 1234567890000,
                'visibility': 'public',
                'status': 'upcoming',
                'time': 1234567890000,
                'utc_offset': -28800000,
                'duration': 11700000,
                'fee': {
                    'accepts': 'paypal',
                    'required': False,
                    'label': 'price',
                    'currency': 'USD',
                    'description': 'per person',
                    'amount': 5.0
                },
                'rsvp_rules': {
                    'close_time': 1234567890000,
                    'closed': False,
                    'guest_limit': 0,
                    'open_time': 1234567890000,
                    'refund_policy': {
                        'days': 3,
                        'notes': '',
                        'policies': [ '' ]
                    },
                    'waitlisting': 'auto'
                },
                'self': {
                    'actions': ['upload_photo'],
                    'rsvp': {
                        'answers': [
                            {
                                'answer': '',
                                'question': "do you like chocolate?",
                                'question_id': 12345678,
                                'updated': 1234567890000
                            }
                        ],
                        'guests': 0,
                        'response': 'yes'
                    }
                },
                'survey_questions': [
                    {
                        'id': 12345678,
                        'question': 'tell me something i want to know'
                    }
                ],
                'rsvp_limit': 200,
                'yes_rsvp_count': 200,
                'waitlist_count': 123,
                'rsvpable': True,
                'rsvpable_after_join': False,
                'description': '<p>A long description</p>',
                'comment_count': 1,
                'how_to_find_us': 'open the door',
                'group': {
                    'created': 1321563802000,
                    'id': 2829432,
                    'join_mode': 'approval',
                    'lat': 40.7599983215332,
                    'lon': -73.97000122070312,
                    'name': 'Data Driven NYC (a FirstMark Event)',
                    'urlname': 'DataDrivenNYC',
                    'who': 'Members'
                },
                'venue': {
                    'address_1': '731 Lexington Av. 7th Floor',
                    'city': 'New York',
                    'country': 'us',
                    'id': 5405082,
                    'lat': 40.761932373046875,
                    'localized_country_name': 'USA',
                    'lon': -73.96805572509766,
                    'name': 'Bloomberg LP',
                    'repinned': False,
                    'state': 'NY',
                    'zip': '10022'
                },
                'event_hosts': [ {
                    'id': 2369792,
                    'name': 'Matt Turck',
                    'photo': {
                        'base_url': 'http://photos4.meetupstatic.com',
                        'highres_link': 'http://photos2.meetupstatic.com/photos/member/1/9/2/4/highres_255546436.jpeg',
                        'id': 255546436,
                        'photo_link': 'http://photos2.meetupstatic.com/photos/member/1/9/2/4/member_255546436.jpeg',
                        'thumb_link': 'http://photos4.meetupstatic.com/photos/member/1/9/2/4/thumb_255546436.jpeg',
                        'type': 'member'
                    }
                } ],
                'short_link': 'http://meetu.ps/e/df6Ju/GlGy/i',
                'link': 'https://www.meetup.com/mygroup/events/123456789/'
            },
            'components': {
                '.created': {
                    'integer_data': True
                },
                '.updated': {
                    'integer_data': True
                },
                '.time': {
                    'integer_data': True
                },
                '.utc_offset': {
                    'integer_data': True
                },
                '.duration': {
                    'integer_data': True
                },
                '.rsvp_limit': {
                    'integer_data': True
                },
                '.yes_rsvp_count': {
                    'integer_data': True
                },
                '.waitlist_count': {
                    'integer_data': True
                },
                '.comment_count': {
                    'integer_data': True
                },
                '.fee': {
                    'extra_fields': True
                },
                '.rsvp_rules': {
                    'extra_fields': True
                },
                '.rsvp_rules.open_time': {
                    'integer_data': True
                },
                '.rsvp_rules.close_time': {
                    'integer_data': True
                },
                '.rsvp_rules.guest_limit': {
                    'integer_data': True
                },
                '.rsvp_rules.refund_policy.days': {
                    'integer_data': True
                },
                '.rsvp_rules.refund_policy': {
                    'extra_fields': True
                },
                '.self': {
                    'extra_fields': True
                },
                '.self.rsvp': {
                    'extra_fields': True
                },
                '.self.rsvp.answers[0]': {
                    'extra_fields': True
                },
                '.self.rsvp.answers[0].question_id': {
                    'integer_data': True
                },
                '.self.rsvp.answers[0].updated': {
                    'integer_data': True
                },
                '.self.rsvp.guests': {
                    'integer_data': True
                },
                '.survey_questions[0]': {
                    'extra_fields': True
                },
                '.survey_questions[0].id': {
                    'integer_data': True
                },
                '.group': {
                    'extra_fields': True
                },
                '.venue': {
                    'extra_fields': True
                },
                '.event_hosts[0]': {
                    'extra_fields': True
                },
                '.event_hosts[0].id': {
                    'integer_data': True
                },
                '.event_hosts[0].photo.id': {
                    'integer_data': True
                },
                '.event_hosts[0].photo': {
                    'extra_fields': True
                }
            }
        },
        'event_group': {
            'schema': {
                'created': 0,
                'id': 0,
                'join_mode': '',
                'lat': 0.0,
                'lon': 0.0,
                'name': '',
                'urlname': '',
                'who': ''
            },
            'components': {
                '.id': {
                    'integer_data': True
                },
                '.created': {
                    'integer_data': True
                }
            }
        },
        'group_brief': {
            'schema': {
                'group_photo': {
                    'base_url': '',
                    'highres_link': '',
                    'id': 0,
                    'photo_link': '',
                    'thumb_link': '',
                    'type': ''
                },
                'id': 0,
                'join_mode': '',
                'key_photo': {
                    'base_url': '',
                    'highres_link': '',
                    'id': 0,
                    'photo_link': '',
                    'thumb_link': '',
                    'type': ''
                },
                'members': 0,
                'name': '',
                'urlname': '',
                'who': ''
            },
            'components': {
                '.id': {
                    'integer_data': True
                },
                '.group_photo': {
                    'extra_fields': True
                },
                '.group_photo.id': {
                    'integer_data': True
                },
                '.key_photo': {
                    'extra_fields': True
                },
                '.key_photo.id': {
                    'integer_data': True
                },
                '.members': {
                    'integer_data': True
                }
            }
        },
        'group': {
            'schema': {
                'category': {
                    'id': 0,
                    'name': '',
                    'shortname': '',
                    'sort_name': ''
                },
                'city': '',
                'country': '',
                'created': 0,
                'description': '',
                'group_photo': {},
                'id': 0,
                'join_info': {
                    'photo_req': False,
                    'questions': [ {
                        'id': 0,
                        'question': ''
                    } ],
                    'questions_req': False
                },
                'join_mode': '',
                'key_photo': {},
                'last_event': {},
                'lat': 0.0,
                'link': '',
                'localized_country_name': '',
                'lon': 0.0,
                'members': 0,
                'membership_dues': {
                    'currency': '',
                    'fee': 0.0,
                    'fee_desc': '',
                    'methods': {
                        'amazon_payment': False,
                        'credit_card': False,
                        'other': False,
                        'paypal': False
                    },
                    'reasons': [ '' ],
                    'reasons_other': '',
                    'refund_policy': {},
                    'required': False,
                    'required_to': '',
                    'self_payment_required': False,
                    'trial_days': 0
                },
                'name': '',
                'next_event': {},
                'organizer': {
                    'bio': '',
                    'id': 0,
                    'name': '',
                    'photo': {}
                },
                'photos': [ {} ],
                'score': 0.0,
                'state': '',
                'timezone': '',
                'urlname': '',
                'visibility': '',
                'who': ''
            },
            'components': {
                '.': {
                    'extra_fields': True
                },
                '.category.id': {
                    'integer_data': True
                },
                '.created': {
                    'integer_data': True
                },
                '.id': {
                    'integer_data': True
                },
                '.members': {
                    'integer_data': True
                },
                '.membership_dues.trial_days': {
                    'integer_data': True
                },
                '.organizer.id': {
                    'integer_data': True
                },
                '.organizer': {
                    'extra_fields': True
                },
            }
        },
        'event_brief': {
            'schema': {
                'id': '',
                'name': '',
                'time': 0,
                'utc_offset': 0,
                'yes_rsvp_count': 0
            },
            'components': {
                '.': {
                    'extra_fields': True
                },
                '.time': {
                    'integer_data': True
                },
                '.utc_offset': {
                    'integer_data': True
                },
                '.yes_rsvp_count': {
                    'integer_data': True
                }
            }
        },
        'photo': {
            'schema': {
                'base_url': '',
                'highres_link': '',
                'id': 0,
                'photo_link': '',
                'thumb_link': '',
                'type': ''
            },
            'components': {
                '.': {
                    'extra_fields': True
                },
                '.id': {
                    'integer_data': True
                }
            }
        },
        'venue': {
            'schema': {
                'address_1': '',
                'address_2': '',
                'address_3': '',
                'city': '',
                'country': '',
                'distance': 0,
                'email': '',
                'fax': '',
                'id': 0,
                'lat': 0.0,
                'localized_country_name': '',
                'lon': 0.0,
                'name': '',
                'phone': '',
                'rating': 0,
                'rating_count': 0,
                'repinned': False,
                'state': '',
                'visibility': 'public',
                'zip': ''
            },
            'components': {
                '.visibility': {
                    'default_value': 'public'
                },
                '.id': {
                    'integer_data': True
                },
                '.distance': {
                    'integer_data': True
                },
                '.rating': {
                    'integer_data': True
                },
                '.rating_count': {
                    'integer_data': True
                }
            }
        },
        'attendee': {
            'schema': {
                'created': 0,
                'event': {},
                'group': {},
                'guests': 0,
                'member': {'bio': '',
                    'event_context': {'host': False},
                    'id': 0,
                    'name': '',
                    'photo': {
                        'base_url': '',
                        'highres_link': '',
                        'id': 0,
                        'photo_link': '',
                        'thumb_link': '',
                        'type': ''
                    },
                    'role': '',
                    'title': ''
                },
                'response': '',
                'updated': 0,
                'venue': {}
            },
            'components': {
                '.': {
                    'extra_fields': True
                },
                '.member': {
                    'extra_fields': True
                },
                '.member.event_context': {
                    'extra_fields': True
                },
                '.created': {
                    'integer_data': True
                },
                '.member.id': {
                    'integer_data': True
                },
                '.updated': {
                    'integer_data': True
                },
                '.guests': {
                    'integer_data': True
                }
            }
        },
        'location': {
            'schema':{
                'city': '',
                'country': '',
                'lat': 0.0,
                'localized_country_name': '',
                'lon': 0.0,
                'name_string': '',
                'state': '',
                'zip': ''
            }
        }
    }

    def __init__(self, access_token, service_scope, usage_client=None, requests_handler=None):

        ''' initialization method for meetup client class

        :param access_token: string with access token for user provided by meetup oauth
        :param service_scope: dictionary with service type permissions
        :param usage_client: [optional] callable that records usage data
        :param requests_handler: [optional] callable that handles requests errors
        '''

        title = '%s.__init__' % self.__class__.__name__

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct class object models
        object_models = {}
        for key, value in self._class_objects.items():
            object_models[key] = jsonModel(value)
        from labpack.compilers.objects import _method_constructor
        self.objects = _method_constructor(object_models)

    # validate inputs
        input_fields = {
            'access_token': access_token,
            'service_scope': service_scope
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct class properties
        self.access_token = access_token
        self.service_scope = service_scope
        self.endpoint = self.fields.schema['api_endpoint']
    
    # construct method handlers
        self.requests_handler = requests_handler
        self.service_handler = meetupHandler(usage_client)
    
    def _get_request(self, url, headers=None, params=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': {'Authorization': 'Bearer %s' % self.access_token},
            'params': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)

    # send request
        try:
            response = requests.get(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'GET'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.service_handler.handle(response)

        return response_details

    def _post_request(self, url, headers=None, params=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': {'Authorization': 'Bearer %s' % self.access_token},
            'params': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)

    # send request
        try:
            response = requests.post(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'POST'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.service_handler.handle(response)

        return response_details

    def _delete_request(self, url, headers=None, params=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': {'Authorization': 'Bearer %s' % self.access_token},
            'params': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)

    # send request
        try:
            response = requests.delete(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'DELETE'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.service_handler.handle(response)

        return response_details

    def _patch_request(self, url, headers=None, params=None):

        import requests

    # construct request kwargs
        request_kwargs = {
            'url': url,
            'headers': {'Authorization': 'Bearer %s' % self.access_token},
            'params': {}
        }
        if headers:
            request_kwargs['headers'].update(headers)
        if params:
            request_kwargs['params'].update(params)

    # send request
        try:
            response = requests.patch(**request_kwargs)
        except Exception:
            if self.requests_handler:
                request_kwargs['method'] = 'PATCH'
                request_object = requests.Request(**request_kwargs)
                return self.requests_handler(request_object)
            else:
                raise

    # handle response
        response_details = self.service_handler.handle(response)

        return response_details

    def _reconstruct_event(self, event_details):

    # handle self key exception for jsonmodel.ingest class method
        self_details = {}
        self_schema = {}
        if 'self' in event_details.keys():
            self_details = event_details['self']
            self_schema = self.objects.event.schema['self']
            del event_details['self']

    # ingest top level object
        event_details = self.objects.event.ingest(**event_details)

    # ingest lower level objects
        event_details['self'] = self.objects.event._ingest_dict(self_details, self_schema, '.self')
        event_details['venue'] = self.objects.venue.ingest(**event_details['venue'])
        event_details['group'] = self.objects.event_group.ingest(**event_details['group'])

        return event_details

    def _reconstruct_group(self, group_details):

    # ingest top level object
        group_details = self.objects.group.ingest(**group_details)

    # ingest lower level objects
        group_details['last_event'] = self.objects.event_brief.ingest(**group_details['last_event'])
        group_details['next_event'] = self.objects.event_brief.ingest(**group_details['next_event'])
        group_details['group_photo'] = self.objects.photo.ingest(**group_details['group_photo'])
        group_details['key_photo'] = self.objects.photo.ingest(**group_details['key_photo'])
        group_details['organizer']['photo'] = self.objects.photo.ingest(**group_details['organizer']['photo'])
        for photo in group_details['photos']:
            photo = self.objects.photo.ingest(**photo)

        return group_details

    def _reconstruct_member(self, member_details):

    # remove self key from details
        self_details = {}
        if 'self' in member_details.keys():
            self_details = member_details['self']
            del member_details['self']

    # ingest top level object
        member_details = self.objects.profile.ingest(**member_details)

    # re-integrate self key
        member_details['self'] = self.objects.self.ingest(**self_details)
        common_groups = []
        for group in member_details['self']['common']['groups']:
            common_groups.append(self.objects.group_brief.ingest(**group))
        member_details['self']['common']['groups'] = common_groups

    # ingest lower level objects
        member_details['group_profile'] = self.objects.group_profile.ingest(**member_details['group_profile'])
        group_details = member_details['group_profile']['group']
        member_details['group_profile']['group'] = self.objects.group_brief.ingest(**group_details)
        member_details['photo'] = self.objects.photo.ingest(**member_details['photo'])

    # ingest last and next event objects
        self_details = {}
        if 'self' in member_details['last_event'].keys():
            self_details = member_details['last_event']['self']
            del member_details['last_event']['self']
        member_details['last_event'] = self.objects.event_brief.ingest(**member_details['last_event'])
        member_details['last_event']['self'] = self.objects.self.ingest(**self_details)
        self_details = {}
        if 'self' in member_details['next_event'].keys():
            self_details = member_details['next_event']['self']
            del member_details['next_event']['self']
        member_details['next_event'] = self.objects.event_brief.ingest(**member_details['next_event'])
        member_details['next_event']['self'] = self.objects.self.ingest(**self_details)

        return member_details

    def _reconstruct_attendee(self, attendee_details):

    # ingest top level object
        attendee_details = self.objects.attendee.ingest(**attendee_details)

    # ingest lower level objects
        attendee_details['group'] = self.objects.group_brief.ingest(**attendee_details['group'])
        attendee_details['event'] = self.objects.event_brief.ingest(**attendee_details['event'])
        attendee_details['venue'] = self.objects.venue.ingest(**attendee_details['venue'])
        photo_details = attendee_details['member']['photo']
        attendee_details['member']['photo'] = self.objects.photo.ingest(**photo_details)

        return attendee_details

    def get_member_brief(self, member_id=0):

        ''' a method to retrieve member profile info

        :param member_id: [optional] integer with member id from member profile
        :return: dictionary with member profile inside [json] key

        member_profile = self.objects.profile_brief.schema
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.get_member_brief' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/members/' % self.endpoint
        params = {
            'member_id': 'self'
        }
        if member_id:
            params['member_id'] = member_id

    # send request
        response_details = self._get_request(url, params=params)

    # construct method output dictionary
        profile_details = {
            'json': {}
        }
        for key, value in response_details.items():
            if not key == 'json':
                profile_details[key] = value

    # parse response
        if response_details['json']:
            if 'results' in response_details['json'].keys():
                if response_details['json']['results']:
                    details = response_details['json']['results'][0]
                    for key, value in details.items():
                        if key != 'topics':
                            profile_details['json'][key] = value
        profile_details['json'] = self.objects.profile_brief.ingest(**profile_details['json'])

        return profile_details

    def get_member_profile(self, member_id):

        ''' a method to retrieve member profile details

        :param member_id: integer with member id from member profile
        :return: dictionary with member profile details inside [json] key

        profile_details = self.objects.profile.schema
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.get_member_profile' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct member id
        if not member_id:
            raise IndexError('%s requires member id argument.' % title)

    # compose request fields
        url = '%s/members/%s' % (self.endpoint, str(member_id))
        params = {
            'fields': 'gender,birthday,last_event,messaging_pref,next_event,other_services,privacy,self,stats'
        }

    # send requests
        profile_details = self._get_request(url, params=params)

    # construct method output
        if profile_details['json']:
            profile_details['json'] = self._reconstruct_member(profile_details['json'])

        return profile_details

    def update_member_profile(self, brief_details, profile_details):

        ''' a method to update user profile details on meetup

        :param brief_details: dictionary with member brief details with updated values
        :param profile_details: dictionary with member profile details with updated values
        :return: dictionary with partial profile details inside [json] key
        '''

        # https://www.meetup.com/meetup_api/docs/members/:member_id/#edit

        title = '%s.update_member_profile' % self.__class__.__name__

        # validate permissions
        if not 'profile_edit' in self.service_scope:
            raise ValueError('%s requires group_join as part of oauth2 service_scope permissions.' % title)

            # validate inputs
        brief_details = self.objects.profile_brief.validate(brief_details)
        profile_details = self.objects.profile.validate(profile_details)

        # construct request fields
        url = '%s/members/%s' % (self.endpoint, str(profile_details['id']))
        params = {
            'bio': profile_details['bio'],
            'bio_privacy': profile_details['privacy']['bio'],
            'fields': 'gender,birthday,last_event,messaging_pref,next_event,other_services,privacy,self,stats',
            'gender': profile_details['gender'],
            'groups_privacy': profile_details['privacy']['groups'],
            'lang': brief_details['lang'].replace('_', '-'),
            'lat': str(profile_details['lat']),
            'lon': str(profile_details['lon']),
            'messaging_pref': profile_details['messaging_pref'],
            'name': profile_details['name'],
            'photo_id': profile_details['photo']['id'],
            'sync_photo': True,
            'topics_privacy': profile_details['privacy']['topics'],
            'zip': brief_details['zip']
        }
        if profile_details['privacy']['facebook']:
            params['facebook_privacy'] = profile_details['privacy']['facebook']
        birthday_value = False
        for key, value in profile_details['birthday'].items():
            if value:
                birthday_value = True
                break
        if not birthday_value:
            params['birthday'] = '-1'
        else:
            birthday_string = ''
            b_day = profile_details['birthday']
            if b_day['day'] and b_day['month']:
                if b_day['month'] < 10:
                    birthday_string += '0'
                birthday_string += str(b_day['month'])
                if b_day['day'] < 10:
                    birthday_string += '0'
                birthday_string += str(b_day['day'])
            birthday_string += str(b_day['year'])
            params['birthday'] = birthday_string

            # send requests
        profile_details = self._patch_request(url, params=params)

        return profile_details

    def list_member_topics(self, member_id):

        ''' a method to retrieve a list of topics member follows

        :param member_id: integer with meetup member id
        :return: dictionary with list of topic details inside [json] key

        topic_details = self.objects.topic.schema
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.list_member_topics' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct member id
        if not member_id:
            raise IndexError('%s requires member id argument.' % title)

    # compose request fields
        url = '%s/members/%s' % (self.endpoint, str(member_id))
        params = {
            'fields': 'topics'
        }

    # send requests
        response_details = self._get_request(url, params=params)

    # construct method output dictionary
        member_topics = {
            'json': []
        }
        for key, value in response_details.items():
            if not key == 'json':
                member_topics[key] = value

    # parse response
        if response_details['json']:
            if 'topics' in response_details['json'].keys():
                for topic in response_details['json']['topics']:
                    member_topics['json'].append(self.objects.topic.ingest(**topic))

        return member_topics

    def list_member_groups(self, member_id):

        ''' a method to retrieve a list of meetup groups member belongs to

        :param member_id: integer with meetup member id
        :return: dictionary with list of group details in [json]

        group_details = self.objects.group_profile.schema
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#get

        title = '%s.list_member_groups' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'member_id': member_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct member id
        if not member_id:
            raise IndexError('%s requires member id argument.' % title)

    # compose request fields
        url = '%s/members/%s' % (self.endpoint, str(member_id))
        params = {
            'fields': 'memberships'
        }

    # send requests
        response_details = self._get_request(url, params=params)

    # construct method output dictionary
        member_groups = {
            'json': []
        }
        for key, value in response_details.items():
            if not key == 'json':
                member_groups[key] = value

    # parse response
        if response_details['json']:
            if 'memberships' in response_details['json'].keys():
                for group in response_details['json']['memberships']['member']:
                    member_groups['json'].append(self.objects.group_profile.ingest(**group))

        return member_groups

    def list_member_events(self, upcoming=True):

        ''' a method to retrieve a list of events member attended or will attend

        :param upcoming: [optional] boolean to filter list to only future events
        :return: dictionary with list of event details inside [json] key

        event_details = self._reconstruct_event({})
        '''

    # https://www.meetup.com/meetup_api/docs/self/events/

    # construct request fields
        url = '%s/self/events' % self.endpoint
        params = {
            'status': 'past',
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable'
        }
        if upcoming:
            params['status'] = 'upcoming'

    # send requests
        response_details = self._get_request(url, params=params)

    # construct method output
        member_events = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                member_events[key] = value
        for event in response_details['json']:
            member_events['json'].append(self._reconstruct_event(event))

        return member_events

    def get_member_calendar(self, max_results=0):

        ''' a method to retrieve the upcoming events for all groups member belongs to

        :param max_results: [optional] integer with number of events to include
        :return: dictionary with list of event details inside [json] key

        event_details = self._reconstruct_event({})
        '''

    # https://www.meetup.com/meetup_api/docs/self/calendar/#list

        title = '%s.get_member_calendar' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'max_results': max_results
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/self/calendar' % self.endpoint
        params = {
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable'
        }
        if max_results:
            params['page'] = str(max_results)

    # send requests
        response_details = self._get_request(url, params=params)

    # construct method output
        member_calendar = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                member_calendar[key] = value
        for event in response_details['json']:
            member_calendar['json'].append(self._reconstruct_event(event))

        return member_calendar

    def list_groups(self, topics=None, categories=None, text='', country_code='', latitude=0.0, longitude=0.0, location='', radius=0.0, zip_code='', max_results=0, member_groups=True):

        ''' a method to find meetup groups based upon a number of filters

        :param topics: [optional] list of integer meetup ids for topics
        :param text: [optional] string with words in groups to search
        :param country_code: [optional] string with two character country code
        :param latitude: [optional] float with latitude coordinate at center of geo search
        :param longitude: [optional] float with longitude coordinate at center of geo search
        :param location: [optional] string with meetup location name fields to search
        :param radius: [optional] float with distance from center of geographic search
        :param zip_code: [optional] string with zip code of geographic search
        :param max_results: [optional] integer with number of groups to include
        :param member_groups: [optional] boolean to include groups member belongs to
        :return: dictionary with list of group details inside [json] key

        group_details = self._reconstruct_group(**{})
        '''

    # https://www.meetup.com/meetup_api/docs/find/groups/

        title = '%s.list_groups' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'categories': categories,
            'topics': topics,
            'text': text,
            'country_code': country_code,
            'latitude': latitude,
            'longitude': longitude,
            'location': location,
            'radius': radius,
            'zip_code': zip_code,
            'max_results': max_results
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/find/groups' % self.endpoint
        params = {
            'fields': 'last_event,next_event,join_info',
            'self_groups': 'include'
        }
        if not member_groups:
            params['self_groups'] = 'exclude'
        if max_results:
            params['page'] = str(max_results)
        if categories:
            params['category'] = ','.join(str(item) for item in categories)
        if topics:
            params['topic_id'] = ','.join(str(item) for item in categories)
        if text:
            params['text'] = text
        if country_code:
            params['country'] = country_code.lower()
        if latitude:
            params['lat'] = str(latitude)
        if longitude:
            params['lon'] = str(longitude)
        if location:
            params['location'] = location
        if radius:
            params['radius'] = str(radius)
        if zip_code:
            params['zip'] = zip_code

    # send request
        response_details = self._get_request(url, params=params)

    # construct method output
        meetup_groups = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                meetup_groups[key] = value
        for group in response_details['json']:
            meetup_groups['json'].append(self._reconstruct_group(group))

        return meetup_groups

    def get_group_details(self, group_url='', group_id=0):

        ''' a method to retrieve details about a meetup group

        :param group_url: string with meetup urlname of group
        :param group_id: int with meetup id for group
        :return: dictionary with group details inside [json] key

        group_details = self._reconstruct_group(**{})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/#get

        title = '%s.get_group_details' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'group_id': group_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        if not group_url and not group_id:
            raise IndexError('%s requires either a group_url or group_id argument.' % title)

    # construct request fields
        if group_id:
            url = '%s/2/groups?fields=last_event,next_event,join_info&group_id=%s' % (self.endpoint, group_id)
        else:
            url = '%s/%s?fields=last_event,next_event,join_info' % (self.endpoint, group_url)

    # send request
        group_details = self._get_request(url)

    # cosntruct method output
        if group_id:
            if 'results' in group_details['json'].keys():
                if group_details['json']['results']:
                    group_details['json'] = self._reconstruct_group(group_details['json']['results'][0])
        else:
            group_details['json'] = self._reconstruct_group(group_details['json'])

        return group_details

    def list_group_events(self, group_url, upcoming=True):

        ''' a method to retrieve a list of upcoming events hosted by group

        :param group_url: string with meetup urlname field of group
        :param upcoming: [optional] boolean to filter list to only future events
        :return: dictionary with list of event details inside [json] key

        event_details = self._reconstruct_event({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/#list

        title = '%s.list_group_events' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events' % (self.endpoint, group_url)
        params = {
            'status': 'past',
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable'
        }
        if upcoming:
            params['status'] = 'upcoming'

    # send request
        response_details = self._get_request(url, params=params)

    # construct method output
        group_events = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                group_events[key] = value
        for event in response_details['json']:
            group_events['json'].append(self._reconstruct_event(event))

        return group_events

    def list_group_members(self, group_url, max_results=0):

        ''' a method to retrieve a list of members for a meetup group

        :param group_url: string with meetup urlname for group
        :param max_results: [optional] integer with number of members to include
        :return: dictionary with list of member details inside [json] key

        member_details = self._reconstruct_member({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/members/#list

        title = '%s.list_group_members' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'max_results': max_results
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/members' % (self.endpoint, group_url)
        params = {
            'fields': 'gender,birthday,last_event,messaging_pref,next_event,other_services,privacy,self,stats'
        }
        if max_results:
            params['page'] = str(max_results)

    # send request
        response_details = self._get_request(url, params=params)

    # reconstruct method output
        group_members = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                group_members[key] = value
        for member in response_details['json']:
            group_members['json'].append(self._reconstruct_member(member))

        return group_members

    def get_event_details(self, group_url, event_id):

        ''' a method to retrieve details for an event

        :param group_url: string with meetup urlname for host group
        :param event_id: integer with meetup id for event
        :return: dictionary with list of event details inside [json] key

        event_details = self._reconstruct_event({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:id/#get

        title = '%s.get_event_details' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'event_id': event_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events/%s' % (self.endpoint, group_url, str(event_id))
        params = {
            'fields': 'comment_count,event_hosts,rsvp_rules,short_link,survey_questions,rsvpable,rsvpable_after_join'
        }

    # send request
        event_details = self._get_request(url, params=params)

    # construct method output
        if event_details['json']:
            event_details['json'] = self._reconstruct_event(event_details['json'])

        return event_details

    def list_event_attendees(self, group_url, event_id):

        ''' a method to retrieve attendee list for event from meetup api

        :param group_url: string with meetup urlname for host group
        :param event_id: integer with meetup id for event
        :return: dictionary with list of attendee details inside [json] key

        attendee_details = self._reconstruct_attendee({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/rsvps/#list

        title = '%s.list_event_attendees' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'event_id': event_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events/%s/rsvps' % (self.endpoint, group_url, str(event_id))

    # send request
        response_details = self._get_request(url)

    # construct method output
        event_attendees = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                event_attendees[key] = value
        for attendee in response_details['json']:
            event_attendees['json'].append(self._reconstruct_attendee(attendee))

        return event_attendees

    def get_venue_details(self, venue_id):

        ''' a method to retrieve venue details from meetup api

        :param venue_id: integer for meetup id for venue
        :return: dictionary with venue details inside [json] key

        venue_details = self.objects.venue.schema
        '''

        title = '%s.get_venue_details' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'venue_id': venue_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/2/venues' % self.endpoint
        params = {
            'venue_id': str(venue_id)
        }

    # send request
        venue_details = self._get_request(url, params=params)

    # reconstruct method output
        if venue_details['json']:
            if 'results' in venue_details['json'].keys():
                if venue_details['json']['results']:
                    details = venue_details['json']['results'][0]
                    venue_details['json'] = self.objects.venue.ingest(**details)

        return venue_details

    def list_locations(self, latitude=0.0, longitude=0.0, zip_code='', city_name='', max_results=0):

        ''' a method to retrieve location address details based upon search parameters

        :param latitude: [optional] float with latitude coordinate at center of geo search
        :param longitude: [optional] float with longitude coordinate at center of geo search
        :param city_name: [optional] string with name of city for search
        :param zip_code: [optional] string with zip code of geographic search
        :param max_results: [optional] integer with number of groups to include
        :return: dictionary with list of location details inside [json] key

        location_details = self.objects.location.schema
        '''

        # https://www.meetup.com/meetup_api/docs/find/locations/

        title = '%s.list_locations' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'latitude': latitude,
            'longitude': longitude,
            'zip_code': zip_code,
            'city_name': city_name,
            'max_results': max_results
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate requirements
        if latitude or longitude:
            if not latitude or not longitude:
                raise IndexError('%s coordinate search requires both latitude and longitude arguments.' % title)

                # construct request fields
        url = '%s/find/locations' % self.endpoint
        params = {}
        if max_results:
            params['page'] = str(max_results)
        if latitude:
            params['lat'] = str(latitude)
        if longitude:
            params['lon'] = str(longitude)
        elif zip_code:
            params['query'] = zip_code
        elif city_name:
            params['query'] = city_name

            # send request
        response_details = self._get_request(url, params=params)

        # construct method output
        meetup_locations = {
            'json': []
        }
        for key, value in response_details.items():
            if key != 'json':
                meetup_locations[key] = value
        for location in response_details['json']:
            meetup_locations['json'].append(location)

        return meetup_locations

    def join_group(self, group_url, membership_answers=None):

        ''' a method to add member to a meetup group

        :param group_url: string with meetup urlname for group
        :param membership_answers: list with question id and answer for group join questions
        :return: dictionary with member profile details inside [json] key

        profile_details = self._reconstruct_member({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/members/#create

        title = '%s.join_group' % self.__class__.__name__

    # validate permissions
        if not 'group_join' in self.service_scope:
            raise ValueError('%s requires group_join as part of oauth2 service_scope permissions.' % title)

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'membership_answers': membership_answers
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/members' % (self.endpoint, group_url)
        params = {}
        if membership_answers:
            for answer in membership_answers:
                key = 'answer_%s' % str(answer['question_id'])
                params[key] = answer['answer_text']

    # send request
        response_details = self._post_request(url, params=params)

    # construct method output
        if response_details['json']:
            response_details['json'] = self._reconstruct_member(response_details['json'])

        return response_details

    def leave_group(self, group_url, member_id, exit_comment=''):

        ''' a method to remove group from meetup member profile

        :param group_url: string with meetup urlname for group
        :param member_id: integer with member id from member profile
        :param exit_comment: string with comment to leave with organizer
        :return: dictionary with code 204 on success
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/members/:member_id/#delete

        title = '%s.leave_group' % self.__class__.__name__

    # validate permissions
        if not 'profile_edit' in self.service_scope:
            raise ValueError('%s requires profile_edit as part of oauth2 service_scope permissions.' % title)

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'member_id': member_id,
            'exit_comment': exit_comment
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/members/%s' % (self.endpoint, group_url, str(member_id))
        params = {}
        if exit_comment:
            params['exit_comment'] = exit_comment

    # send request
        response_details = self._delete_request(url, params=params)

        return response_details

    def join_topics(self, member_id, topics):

        ''' a method to add topics to member profile details on meetup

        :param member_id: integer with member id from member profile
        :param topics: list of integer meetup ids for topics
        :return: dictionary with list of topic details inside [json] key

        topic_details = self.objects.topic.schema
        '''

    # https://www.meetup.com/meetup_api/docs/members/:member_id/#edit

        title = '%s.join_topics' % self.__class__.__name__

    # validate permissions
        if not 'profile_edit' in self.service_scope:
            raise ValueError('%s requires group_join as part of oauth2 service_scope permissions.' % title)

    # validate inputs
        input_fields = {
            'member_id': member_id,
            'topics': topics
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/members/%s' % (self.endpoint, member_id)
        params = {
            'add_topics': ','.join(str(x) for x in topics),
            'fields': 'topics'
        }

    # send requests
        response_details = self._patch_request(url, params=params)

    # construct method output dictionary
        member_topics = {
            'json': []
        }
        for key, value in response_details.items():
            if not key == 'json':
                member_topics[key] = value

    # parse response
        if response_details['json']:
            if 'topics' in response_details['json'].keys():
                for topic in response_details['json']['topics']:
                    member_topics['json'].append(self.objects.topic.ingest(**topic))

        return member_topics

    def leave_topics(self, member_id, topics):

        ''' a method to remove topics from member profile details on meetup

        :param member_id: integer with member id from member profile
        :param topics: list of integer meetup ids for topics
        :return: dictionary with list of topic details inside [json] key

        topic_details = self.objects.topic.schema
        '''

        # https://www.meetup.com/meetup_api/docs/members/:member_id/#edit

        title = '%s.leave_topics' % self.__class__.__name__

    # validate permissions
        if not 'profile_edit' in self.service_scope:
            raise ValueError('%s requires group_join as part of oauth2 service_scope permissions.' % title)

    # validate inputs
        input_fields = {
            'member_id': member_id,
            'topics': topics
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

                # construct request fields
        url = '%s/members/%s' % (self.endpoint, member_id)
        params = {
            'remove_topics': ','.join(str(x) for x in topics),
            'fields': 'topics'
        }

    # send requests
        response_details = self._patch_request(url, params=params)

    # construct method output dictionary
        member_topics = {
            'json': []
        }
        for key, value in response_details.items():
            if not key == 'json':
                member_topics[key] = value

    # construct method output
        if response_details['json']:
            if 'topics' in response_details['json'].keys():
                for topic in response_details['json']['topics']:
                    member_topics['json'].append(self.objects.topic.ingest(**topic))

        return member_topics

    def join_event(self, group_url, event_id, additional_guests=0, attendance_answers=None, payment_service='', payment_code=''):

        ''' a method to create an rsvp for a meetup event

        :param group_url: string with meetup urlname for group
        :param event_id: integer with meetup id for event
        :param additional_guests: [optional] integer with number of additional guests
        :param attendance_answers: [optional] list with id & answer for event survey questions
        :param payment_service: [optional] string with name of payment service to use
        :param payment_code: [optional] string with token to authorize payment
        :return: dictionary with attendee details inside [json] key

        attendee_details = self._reconstruct_attendee({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/rsvps/

        title = '%s.join_event' % self.__class__.__name__

    # validate permissions
        if not 'rsvp' in self.service_scope:
            raise ValueError('%s requires group_join as part of oauth2 service_scope permissions.' % title)

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'event_id': event_id,
            'additional_guests': additional_guests,
            'attendance_answers': attendance_answers,
            'payment_service': payment_service,
            'payment_code': payment_code
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events/%s/rsvps' % (self.endpoint, group_url, event_id)
        params = {
            'response': 'yes'
        }
        if additional_guests:
            params['guests'] = additional_guests
        if attendance_answers:
            for answer in attendance_answers:
                key = 'answer_%s' % str(answer['question_id'])
                params[key] = answer['answer_text']
        if payment_service:
            params['agree_to_refund'] = True
            params['opt_to_pay'] = True

    # send request
        response_details = self._post_request(url, params=params)

    # construct method output
        if response_details['json']:
            response_details['json'] = self._reconstruct_attendee(response_details['json'])

        return response_details
    
    def leave_event(self, group_url, event_id):

        ''' a method to rescind an rsvp to a meetup event

        :param group_url: string with meetup urlname for group
        :param event_id: integer with meetup id for event
        :return: dictionary with attendee details inside [json] key

        attendee_details = self._reconstruct_attendee({})
        '''

    # https://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/rsvps/

        title = '%s.leave_event' % self.__class__.__name__

    # validate permissions
        if not 'rsvp' in self.service_scope:
            raise ValueError('%s requires group_join as part of oauth2 service_scope permissions.' % title)

    # validate inputs
        input_fields = {
            'group_url': group_url,
            'event_id': event_id
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct request fields
        url = '%s/%s/events/%s/rsvps' % (self.endpoint, group_url, event_id)
        params = {
            'response': 'no'
        }

    # send request
        response_details = self._post_request(url, params=params)

    # construct method output
        if response_details['json']:
            response_details['json'] = self._reconstruct_attendee(response_details['json'])

        return response_details
