__author__ = 'rcj1492'
__created__ = '2015.06'

class MeetupError(Exception):

    def __init__(self, message='', error_dict=None):

        ''' a method to raise meetup api related errors

        :param message:
        :param error_dict:
        '''

        text = '\nBad Request %s' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                for key, value in error_dict.items():
                    self.error[key] = value
        super(MeetupError, self).__init__(text)

class meetupHandler(object):

    ''' handles responses from meetup api and usage data'''

    _class_fields = {
        'schema': {
            'rate_limits': [
                {'requests': 3, 'period': 1}
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

class meetupRegister(object):
    ''' currently must be done manually '''
    def __init__(self, app_settings):
        pass

    def setup(self):
        return self

    def update(self):
        return self

class meetupOAuth(object):

    ''' a class of methods to handle oauth2 authentication with meetup API '''

    _class_fields = {
        'schema': {
            'oauth_endpoint': {
                'web': 'https://api.moves-app.com/oauth/v1',
                'mobile': 'moves://app'
            },
            'token_details': {
                'access_token': '',
                'token_type': '',
                'expires_in': 0,
                'refresh_token': '',
                'user_id': 0
            },
            'token_status': {
                'client_id': '',
                'scope': '',
                'expires_in': 0,
                'user_id': 0
            },
            'client_id': '',
            'client_secret': '',
            'device_type': '',
            'redirect_uri': '',
            'service_scope': ['location'],
            'state_value': '',
            'access_code': ''
        },
        'components': {
            '.device_type': {
                'discrete_values': ['web', 'mobile']
            },
            '.redirect_uri': {
                'must_contain': ['^https://']
            },
            '.service_scope': {
                'unique_values': True,
                'max_size': 2
            },
            '.service_scope[0]': {
                'discrete_values': ['location', 'activity']
            }
        }
    }

    def __init__(self, client_id, client_secret, requests_handler=None):

        ''' initialization method for moves oauth class

        :param client_id: string with client id registered for app with moves api
        :param client_secret: string with client secret registered for app with moves api
        :param requests_handler: callable that handles requests errors
        '''

        # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

        # construct client attributes
        self.client_id = self.fields.validate(client_id, '.client_id')
        self.client_secret = self.fields.validate(client_secret, '.client_secret')

        # construct handlers
        self.meetup_handler = meetupHandler()
        self.requests_handler = requests_handler

class meetupClient(object):

    def __init__(self, access_token):

        ''' initialization method for meetup client class

        :param: access_token
        '''

        pass

    def memberGroups(meetup_user_id, meetup_user_key):
        '''
            function to discover info about a group
            interprets JSON response to GET request to Meetup API for group info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/groups?%s'
        params = {
            'key': meetup_user_key,
            'member_id': str(meetup_user_id)
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def groupInfo(groupID, meetup_user_key):
        '''
            function to discover info about a group
            interprets JSON response to GET request to Meetup API for group info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/groups?%s'
        params = {
            'key': meetup_user_key,
            'group_id': str(groupID)
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def groupEvents(groupID, meetup_user_key):
        '''
            function to discover upcoming events for a group
            interprets JSON response to GET request to Meetup API for group's event list
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/events?%s'
        params = {
            'key': meetup_user_key,
            'group_id': groupID
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def eventInfo(eventID, meetup_user_key):
        '''
            function to discover info about a Meetup event
            interprets JSON response to GET request to Meetup API for event info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            response (mand):
            ['rsvpable'] = true # boolean
            response (optional):
            ['rsvp_rules']['guest_limit'] = 2 # int
            ['fee']['amount'] = 10 # int
            ['fee']['required'] = "1" # string
            ['survey_questions'][0]['id'] = 22529716 # int
            ['survey_guestions'][0]['required'] = false # boolean
            ['survey_questions'][0]['question'] = "What is your name?" # string
            ['yes_rsvp_count'] = 86 # int
            ['rsvp_limit'] = 150 # int
        '''
        meetup_url = 'https://api.meetup.com/2/event/' + str(eventID) + '/?%s'
        params = {
            'key': meetup_user_key,
            'fields': 'rsvpable,rsvp_rules,fee,survey_questions'
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def eventRSVPs(eventID, meetup_user_key):
        '''
            function to check info of all RSVPs to a Meetup event by eventID
            interprets JSON response to GET request to Meetup API for RSVPs status
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            returns:
            ['results'] = list of dictionaries of users
                [0]['member']['member_id'] # int
                [0]['member']['name'] # str
                [0]['rsvp_id'] # int
                [0]['response'] # yes or no
                [0]['member_photo']['highres_link'] # str
            ['meta'] = api responsiveness data
        '''
        meetup_url = 'https://api.meetup.com/2/rsvps?%s'
        params = {
            'key': meetup_user_key,
            'event_id': str(eventID)
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def memberInfo(meetup_user_id, meetup_user_key):
        '''
            function to discover info about a Meetup member
            interprets JSON response to GET request to Meetup API for member info
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            response (mand):
            response (optional):
        '''
        meetup_url = 'https://api.meetup.com/2/member/' + str(meetup_user_id) + '/?%s'
        params = {
            'key': meetup_user_key
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def memberRSVPStatus(rsvpID, meetup_user_key):
        '''
            function to check status of RSVP to a Meetup event by RSVPID
            interprets JSON response to GET request to Meetup API for member RSVP status
            requires:
            RSVPID number for member from a previous event RSVP
            meetup_user_key for member
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        meetup_url = 'https://api.meetup.com/2/rsvp/' + str(rsvpID) + '?%s'
        params = {
            'key': meetup_user_key
        }
        response = urllib.request.urlopen(meetup_url % urllib.parse.urlencode(params))
        return json.loads(response.read().decode("utf-8"))

    def RSVPYes(eventID, meetup_user_key, guests = None):
        '''
            function to RSVP to a Meetup event on behalf of member
            creates a POST to Meetup API to RSVP with member key
            requires:
            event_id of event
            user key of member
            user to be a member of the group
            optional:
            guest limit determined by meetupEventInfo ['rsvp_rules']['guest_limit']
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        params = {
            'event_id': str(eventID),
            'rsvp': 'yes',
            'key': meetup_user_key
        }
        if guests:
            params['guests'] = str(guests)
        else:
            pass
        url = 'https://api.meetup.com/2/rsvp'
        post_params = urllib.parse.urlencode(params).encode('utf-8')
        response = urllib.request.urlopen(url, post_params)
        return json.loads(response.read().decode("utf-8"))

    def RSVPNo(eventID, meetup_user_key):
        '''
            function to decline RSVP to a Meetup event on behalf of member
            creates a POST to Meetup API to RSVP with member key
            requires:
            event_id of event
            user key of member
            user to be a member of the group
            dependencies:
            import json
            import urllib.request
            import urllib.parse
        '''
        params = {
            'event_id': str(eventID),
            'rsvp': 'no',
            'key': meetup_user_key
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        meetup_url = 'https://api.meetup.com/2/rsvp'
        post_argument = urllib.parse.urlencode(params).encode('utf-8')
        response = urllib.request.urlopen(meetup_url, post_argument)
        return json.loads(response.read().decode("utf-8"))

    def memberEventList(meetup_user_id, meetup_user_key, api_throttle, searchDepth=False):
        '''
            returns a chronological list of events in user's Meetup groups
            searchDepth default is all
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            returns list of dictionaries:
            [0]['eventID']
            [0]['eventName']
            [0]['eventURL']
            [0]['eventDT']
            [0]['groupID']
        '''
        member_groups = meetupAPI.memberGroups(meetup_user_id, meetup_user_key)
        member_events = []
        for i in range(0,len(member_groups['results'])):
            t1 = timer()
            try:
                group_events = meetupAPI.groupEvents(member_groups['results'][i]['id'], meetup_user_key)
                if group_events['results']:
                    searchLength = len(group_events['results'])
                    if searchDepth:
                        searchLength = int(searchDepth)
                    else:
                        pass
                    for j in range(0,searchLength):
                        event = {}
                        eventURL = group_events['results'][j]['event_url'].replace('\/', '/')
                        event['eventURL'] = eventURL
                        if isinstance(group_events['results'][j]['id'],int):
                            event['eventID'] = group_events['results'][j]['id']
                        else:
                            event['eventID'] = eventURL[eventURL.find('events/') + 7:\
                                eventURL.rfind('/')]
                        event['eventName'] = group_events['results'][j]['name']
                        event['groupID'] = group_events['results'][j]['group']['id']
                        event['eventDT'] = int(group_events['results'][j]['time']) / 1000
                        member_events.append(event)
                else:
                    pass
            except:
                pass
            t2 = timer()
            time_split = t2 - t1
            wait_time = api_throttle - time_split
            if wait_time > 0:
                time.sleep(wait_time)
        return sorted(member_events, key=lambda k: k['eventDT'])

    def nextRSVP(meetup_user_id, meetup_user_key, api_throttle, searchDepth=False):
        '''
            looks for the next available event in user's Meetup groups & RSVPs for it
            dependencies:
            import json
            import urllib.request
            import urllib.parse
            returns dictionary:
            ['rsvpID']
            ['meetup_user_key']
            ['eventID']
            ['eventName']
            ['eventURL']
            ['eventDT']
            ['groupID']
        '''
        eventFound = False
        eventCounter = 0
        if searchDepth:
            searchDepth = int(searchDepth)
        else:
            searchDepth = 3
        eventList = meetupAPI.memberEventList(meetup_user_id, meetup_user_key, api_throttle, searchDepth)
        eventRSVP = {}
        while not eventFound:
            t1 = timer()
            pE = meetupAPI.eventInfo(eventList[eventCounter]['eventID'], meetup_user_key)
            if not 'rsvp_limit' in pE.keys():
                pE['rsvp_limit'] = 1000000
            if not 'yes_rsvp_count' in pE.keys():
                pE['yes_rsvp_count'] = 0
            if not 'survey_questions' in pE.keys():
                reqQ = False
            else:
                for i in range(0,len(pE['survey_questions'])):
                    if not pE['survey_questions'][i]['required']:
                        reqQ = False
                    else:
                        reqQ = True
                        i = len(pE['survey_questions'])
            if pE['rsvpable'] and pE['yes_rsvp_count'] < pE['rsvp_limit'] and \
                    not 'fees' in pE.keys() and not reqQ:
                try:
                    rsvp = meetupAPI.RSVPYes(eventList[eventCounter]['eventID'], meetup_user_key)
                    eventFound = True
                    eventRSVP['rsvpID'] = rsvp['rsvp_id']
                    eventRSVP['meetup_user_key'] = meetup_user_key
                    eventRSVP['eventID'] = eventList[eventCounter]['eventID']
                    eventRSVP['groupID'] = eventList[eventCounter]['groupID']
                    eventRSVP['eventName'] = eventList[eventCounter]['eventName']
                    eventRSVP['eventDT'] = eventList[eventCounter]['eventDT']
                    eventRSVP['eventURL'] = eventList[eventCounter]['eventURL']
                except:
                    print('RSVP failed')
                    pass
            eventCounter += 1
            t2 = timer()
            time_split = t2 - t1
            wait_time = api_throttle - time_split
            if wait_time > 0:
                time.sleep(wait_time)
        return eventRSVP

    def methodTest(meetup_user_id, meetup_user_key, api_throttle):
        '''
            unit test for the meetup methods
        '''
        urlTitle = 'Meetup API'
        t1 = timer()
        eventRSVP = meetupAPI.nextRSVP(meetup_user_id, meetup_user_key, api_throttle, 3)
        assert meetupAPI.groupInfo(eventRSVP['groupID'], meetup_user_key)
        eventAttendees = meetupAPI.eventRSVPs(eventRSVP['eventID'], meetup_user_key)
        assert meetupAPI.memberInfo(eventAttendees['results'][0]['member']['member_id'], meetup_user_key)
        rsvpStatus = meetupAPI.memberRSVPStatus(eventRSVP['rsvpID'], meetup_user_key)
        if str(rsvpStatus['response']) == 'yes':
            meetupAPI.RSVPNo(eventRSVP['eventID'], meetup_user_key)
            print('Meetup Methods Working')
        else:
            print('failure')
        t2 = timer()
        print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
        return True

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    meetup_config = load_settings('../../../cred/meetup.yaml')
    print(meetup_config)