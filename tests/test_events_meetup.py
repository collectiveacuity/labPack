__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'

from labpack.events.meetup import *

if __name__ == '__main__':

# import dependencies & configs
    from pprint import pprint
    from time import time
    from labpack.records.settings import load_settings
    meetup_config = load_settings('../../cred/meetup.yaml')

# test oauth construction
    meetup_oauth = meetupOAuth(meetup_config['oauth_client_id'], meetup_config['oauth_client_secret'])

# test generate url
    auth_url = meetup_oauth.generate_url(meetup_config['oauth_redirect_uri'], meetup_config['oauth_service_scope'].split(), state_value='unittest')
    assert auth_url.find('oauth2') > 0

# retrieve access token
    from labpack.storage.appdata import appdataClient
    log_client = appdataClient(collection_name='Logs', prod_name='Fitzroy')
    path_filters = [{0: {'discrete_values': ['knowledge']}, 1: {'discrete_values': ['tokens']}, 2: {'discrete_values':['meetup']}}]
    token_list = log_client.list(log_client.conditionalFilter(path_filters), reverse_search=True)
    token_details = log_client.read(token_list[0])

# test access token renewal
    new_details = meetup_oauth.renew_token(token_details['refresh_token'])
    token_details.update(**new_details['json'])
    new_key = 'knowledge/tokens/meetup/%s/%s.yaml' % (token_details['user_id'], token_details['expires_at'])
    log_client.create(new_key, token_details)

# test client construction
    meetup_client = meetupClient(token_details['access_token'], token_details['service_scope'])

# test member profile, settings, topics, groups and events
#     profile_details = meetup_client.get_member_brief()
#     member_id = int(profile_details['json']['id'])
#     assert isinstance(profile_details['json']['id'], str)
#     profile_details = meetup_client.get_member_profile(member_id)
#     assert isinstance(profile_details['json']['id'], int)
#     member_topics = meetup_client.list_member_topics(member_id)
#     assert isinstance(member_topics['json'][0]['id'], int)
#     member_groups = meetup_client.list_member_groups(member_id)
#     assert member_groups['json'][5]['group']['name']
#     if len(member_groups['json']) <= 200:
#         assert len(member_groups['json']) == profile_details['json']['stats']['groups']
#     member_events = meetup_client.list_member_events()
#     assert isinstance(member_events['json'], list)

# test member calendar, event attendees & other member profile, settings, topics & groups
#     event_details = meetup_client.get_member_calendar(max_results=10)
#     group_url = event_details['json'][0]['group']['urlname']
#     event_id = int(event_details['json'][0]['id'])
#     event_attendees = meetup_client.list_event_attendees(group_url, event_id)
#     member_id = event_attendees['json'][0]['member']['id']
#     profile_details = meetup_client.get_member_brief(member_id)
#     assert profile_details['json']['joined']
#     profile_details = meetup_client.get_member_profile(member_id)
#     assert 'bio' in profile_details['json']['privacy'].keys()
#     member_topics = meetup_client.list_member_topics(member_id)
#     assert isinstance(member_topics['json'], list)
#     member_groups = meetup_client.list_member_groups(member_id)
#     assert isinstance(member_groups['json'], list)

# test event, venue and group details and list group events
#     event_details = meetup_client.get_member_calendar(max_results=10)
#     group_url = event_details['json'][0]['group']['urlname']
#     event_id = int(event_details['json'][0]['id'])
#     venue_id = event_details['json'][0]['venue']['id']
#     group_id = int(event_details['json'][0]['group']['id'])
#     group_details = meetup_client.get_group_details(group_id=group_id)
#     assert group_details['json']['next_event']['id']
#     print(group_details['json']['join_info'])
#     group_events = meetup_client.list_group_events(group_url)
#     assert group_events['json'][0]['created']
#     event_details = meetup_client.get_event_details(group_url, event_id)
#     assert event_details['json']['event_hosts'][0]['id']
#     venue_details = meetup_client.get_venue_details(venue_id)
#     assert venue_details['json']['name']

# test list groups, group members and locations
#     list_kwargs = {
#         'categories': [34],
#         'latitude': 40.75,
#         'longitude': -73.98,
#         'radius': 1.0,
#         'max_results': 5
#     }
#     group_list = meetup_client.list_groups(**list_kwargs)
#     assert group_list['json'][0]['organizer']['id']
#     group_url = group_list['json'][0]['urlname']
#     group_members = meetup_client.list_group_members(group_url, max_results=5)
#     assert group_members['json'][0]['group_profile']['created']
#     list_kwargs = {
#         'zip_code': '94203',
#         'max_results': 1
#     }
#     meetup_locations = meetup_client.list_locations(**list_kwargs)
#     assert meetup_locations['json'][0]['city'] == 'Sacramento'

# test join and leave group
#     member_profile = meetup_client.get_member_brief()
#     member_id = int(member_profile['json']['id'])
#     list_kwargs = {
#         'categories': [34],
#         'latitude': 40.75,
#         'longitude': -73.98,
#         'radius': 2.0,
#         'max_results': 10,
#         'member_groups': False
#     }
#     group_list = meetup_client.list_groups(**list_kwargs)
#     group_url = ''
#     question_id = 0
#     for group in group_list['json']:
#         if not group['join_info']['questions_req'] and group['join_info']['questions']:
#             for question in group['join_info']['questions']:
#                 question_tokens = question['question'].split()
#                 for token in question_tokens:
#                     if token.lower() == 'name':
#                         group_url = group['urlname']
#                         question_id = question['id']
#                         break
#                 if group_url:
#                     break
#         if group_url:
#             break
#     if group_url and question_id:
#         membership_answers = [ { 'question_id': question_id, 'answer_text': 'First Last'}]
#         response = meetup_client.join_group(group_url, membership_answers)
#         print(response['json'])
#         from time import sleep
#         sleep(2)
#         group_url = 'gdgnyc'
#         response = meetup_client.leave_group(group_url, member_id)
#         assert response['code'] == 204

# test join and leave topics
#     member_profile = meetup_client.get_member_brief()
#     member_id = int(member_profile['json']['id'])
#     topic_list = [ 511, 611, 766 ]
#     member_topics = meetup_client.list_member_topics(member_id)
#     topic_set = [x['id'] for x in member_topics['json']]
#     assert len(set(topic_list) - set(topic_set)) == len(topic_list)
#     updated_profile = meetup_client.join_topics(member_id, topic_list)
#     added_topics = []
#     for topic in updated_profile['json']:
#         if topic['id'] in topic_list:
#             added_topics.append(topic['name'])
#     assert len(added_topics) == len(topic_list)
#     from time import sleep
#     sleep(1)
#     updated_profile = meetup_client.leave_topics(member_id, topic_list)
#     assert len(updated_profile['json']) == len(member_topics['json'])

# test update profile
#     member_brief = meetup_client.get_member_brief()
#     member_id = int(member_brief['json']['id'])
#     member_profile = meetup_client.get_member_profile(member_id)
#     member_profile['json']['privacy']['groups'] = 'visible'
#     member_profile['json']['birthday']['year'] = 1991
#     updated_profile = meetup_client.update_member_profile(member_brief['json'], member_profile['json'])
#     assert updated_profile['json']['privacy']['groups'] == 'visible'
#     member_profile['json']['privacy']['groups'] = 'hidden'
#     member_profile['json']['birthday']['year'] = 0
#     updated_profile = meetup_client.update_member_profile(member_brief['json'], member_profile['json'])
#     assert updated_profile['json']['privacy']['groups'] == 'hidden'

# test join and leave event
#     event_details = meetup_client.get_member_calendar(max_results=100)
#     event_id = 0
#     group_url = ''
#     survey_questions = []
#     for event in event_details['json']:
#         if event['fee']['required']:
#             pass
#         elif event['rsvp_limit'] >= event['yes_rsvp_count'] + 1:
#             pass
#         elif not event['rsvp_rules']['guest_limit']:
#             pass
#         elif not event['rsvpable']:
#             pass
#         elif not event['survey_questions']:
#             pass
#         elif event['self']['rsvp']['response'] == 'yes':
#             pass
#         else:
#             group_url = event['group']['urlname']
#             event_id = int(event['id'])
#             survey_questions = event['survey_questions']
#             break
#     if event_id:
#         join_kwargs = {
#             'attendance_answers': [{'question_id': survey_questions[0]['id'], 'answer_text': 'maybe'}],
#             'group_url': group_url,
#             'event_id': event_id,
#             'additional_guests': 1
#         }
#         attendee_details = meetup_client.join_event(**join_kwargs)
#         assert attendee_details['json']['guests'] == 1
#         attendee_details = meetup_client.leave_event(group_url, event_id)
#         assert attendee_details['json']['response'] == 'no'