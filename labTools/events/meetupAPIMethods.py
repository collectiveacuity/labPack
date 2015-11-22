__author__ = 'rcj1492'
__created__ = '2015'

# throttle: 3 requests per second

import time
import json
import urllib.request
import urllib.parse
from timeit import default_timer as timer

from cred.credentialsDataProcessor import *


class meetupAPI:
    '''
        a set of methods for interacting with the meetup.com API
        dependencies for json API requests & time splits
        import time
        import json
        import urllib.request
        import urllib.parse
        from timeit import default_timer as timer
        from config.apiCredentials import *
    '''
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
assert meetupAPI.methodTest(meetupUserID, meetupUserKey, meetupAPIThrottle)