__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

from labpack.activity.moves import *

if __name__ == '__main__':

# import dependencies & configs
    from pprint import pprint
    from time import time, sleep
    from labpack.records.settings import load_settings
    from labpack.handlers.requests import handle_requests
    moves_config = load_settings('../../cred/moves.yaml')

# test oauth construction
    from labpack.authentication.oauth2 import oauth2Client
    oauth_kwargs = {
        'client_id': moves_config['oauth_client_id'],
        'client_secret': moves_config['oauth_client_secret'],
        'redirect_uri': moves_config['oauth_redirect_uri'],
        'auth_endpoint': moves_config['oauth_auth_endpoint'],
        'token_endpoint': moves_config['oauth_token_endpoint'],
        'request_mimetype': moves_config['oauth_request_mimetype'],
        'requests_handler': handle_requests
    }
    moves_oauth = oauth2Client(**oauth_kwargs)

# test generate url
    url_kwargs = {
        'service_scope': moves_config['oauth_service_scope'].split(),
        'state_value': 'unittest_%s' % str(time())
    }
    auth_url = moves_oauth.generate_url(**url_kwargs)
    assert auth_url.find('code') > 0

# retrieve access token
    from labpack.storage.appdata import appdataClient
    log_client = appdataClient(collection_name='Logs', prod_name='Fitzroy')
    path_filters = [{
        0: {'discrete_values': ['knowledge']},
        1: {'discrete_values': ['tokens']},
        2: {'discrete_values':['moves']}
    }]
    token_list = log_client.list(log_client.conditionalFilter(path_filters), reverse_search=True)
    token_details = log_client.read(token_list[0])

# test access token renewal
#     new_details = moves_oauth.renew_token(token_details['refresh_token'])
#     token_details.update(**new_details['json'])
#     new_key = 'knowledge/tokens/moves/%s/%s.yaml' % (token_details['user_id'], token_details['expires_at'])
#     log_client.create(new_key, token_details)

# retrieve activities list
    access_token = token_details['access_token']
    service_scope = token_details['service_scope']
    moves_client = movesClient(access_token, service_scope)
    activities_list = moves_client.list_activities()
    assert isinstance(activities_list['json'], list)

# retrieve use profile and construct test kwargs
    profile_details = moves_client.get_profile()
    first_date = profile_details['json']['profile']['firstDate']
    timezone_offset = profile_details['json']['profile']['currentTimeZone']['offset']
    prior_dt = time() - (40 * 24 * 3600)
    next_dt = prior_dt + (30 * 24 * 60 * 60 + 1)
    track_dt = prior_dt + (6 * 24 * 60 * 60 + 1)
    empty_kwargs = {
        'timezone_offset': timezone_offset,
        'first_date': first_date
    }
    from copy import deepcopy
    start_kwargs = deepcopy(empty_kwargs)
    start_kwargs['start'] = prior_dt
    end_kwargs = deepcopy(empty_kwargs)
    end_kwargs['end'] = prior_dt
    both_kwargs = deepcopy(start_kwargs)
    both_kwargs['end'] = next_dt
    story_kwargs = deepcopy(empty_kwargs)
    story_kwargs['track_points'] = True

# # test individual methods
#     details = moves_client.get_summary(**empty_kwargs)
#     assert isinstance(activities_list['json'], list)
#     details = moves_client.get_activities(**start_kwargs)
#     assert isinstance(activities_list['json'], list)
#     details = moves_client.get_places(**end_kwargs)
#     assert isinstance(activities_list['json'], list)
#     details = moves_client.get_places(**both_kwargs)
#     assert isinstance(activities_list['json'], list)
#     details = moves_client.get_storyline(**story_kwargs)
#     assert isinstance(activities_list['json'], list)
#
# # test all data retrieval methods
#     test_list = [ moves_client.get_summary, moves_client.get_places, moves_client.get_activities ]
#     kwargs_list = [ empty_kwargs, start_kwargs, end_kwargs, both_kwargs ]
#     for test in test_list:
#         for kwargs in kwargs_list:
#             details = test(**kwargs)
#             assert isinstance(details['json'], list)
#             sleep(.2)
#     for kwargs in kwargs_list:
#         new_kwargs = deepcopy(kwargs)
#         new_kwargs['track_points'] = True
#         if 'start' in new_kwargs and 'end' in new_kwargs:
#             new_kwargs['end'] = track_dt
#         details = moves_client.get_storyline(**new_kwargs)
#         assert isinstance(details['json'], list)
#         sleep(.2)
#
# # test recent location
#     current_dt = time()
#     yesterday_dt = time() - (24 * 60 * 60)
#     details = moves_client.get_places(timezone_offset, first_date, yesterday_dt, current_dt)
#     sorted_days = sorted(details['json'], key=lambda k: k['date'])
#     recent_day = sorted_days.pop()
#     sorted_segments = sorted(recent_day['segments'], key=lambda k: k['endTime'])
#     recent_segment = sorted_segments.pop()
#     from labpack.records.time import labDT
#     last_dt = labDT.fromISO(recent_segment['endTime']).humanFriendly()
#     last_place = 'somewhere'
#     if 'name' in recent_segment['place']:
#         last_place = 'at the %s' % recent_segment['place']['name']
#     print('At %s, you were %s.' % (last_dt, last_place))
#
# # test track points
#     current_dt = time()
#     yesterday_dt = time() - (24 * 60 * 60)
#     story_kwargs = {
#         'timezone_offset': timezone_offset,
#         'first_date': first_date,
#         'start': yesterday_dt,
#         'end': current_dt,
#         'track_points': True
#     }
#     details = moves_client.get_storyline(**story_kwargs)
#     sorted_days = sorted(details['json'], key=lambda k: k['date'])
#     tracked_segment = {}
#     for day in sorted_days:
#         stop = False
#         sorted_segments = sorted(day['segments'], key=lambda k: k['endTime'])
#         for segment in sorted_segments:
#             found = False
#             if 'activities' in segment.keys():
#                 for activity in segment['activities']:
#                     if 'trackPoints' in activity.keys():
#                         if activity['trackPoints']:
#                             found = True
#                             stop = True
#                             break
#                 if found:
#                     tracked_segment = segment
#                     break
#         if stop:
#             break
#     print(tracked_segment['activities'][0])