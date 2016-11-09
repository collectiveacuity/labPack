__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

from labpack.activity.moves import *

if __name__ == '__main__':

# import configs
    from time import sleep, time
    config_path = '../../../cred/moves.yaml'
    token_path = '../../keys/moves-token.yaml'
    from labpack.records.settings import load_settings, save_settings
    moves_cred = load_settings(config_path)
    moves_token = load_settings(token_path)
    client_id = moves_cred['oauth_client_id']
    client_secret = moves_cred['oauth_client_secret']
    redirect_uri = moves_cred['oauth_redirect_url']
    moves_oauth = movesOAuth(client_id, client_secret)

# test access token renew process
    auth_url = moves_oauth.generate_url('web', redirect_uri, ['location', 'activity'])
    assert auth_url.find('code') > 0
    status_details = moves_oauth.validate_token(moves_token['access_token'])
    old_expiration = status_details['content']['expires_at']
    assert isinstance(old_expiration, int)
    token_details = moves_oauth.renew_token(moves_token['refresh_token'])
    new_token = { 'contact_id': moves_token['contact_id'] }
    new_token.update(token_details['content'])
    print(new_token)
    status_details = moves_oauth.validate_token(new_token['access_token'])
    assert status_details['content']['expires_at'] > old_expiration
    new_token['service_scope'] = status_details['content']['service_scope']
    save_settings(new_token, token_path, overwrite=True)
    sleep(.1)
    moves_token = load_settings(token_path)

# retrieve activities list
    access_token = moves_token['access_token']
    service_scope = moves_token['service_scope']
    moves_client = movesClient(access_token, service_scope)
    activities_list = moves_client.list_activities()
    assert isinstance(activities_list['content'], list)

# retrieve use profile and construct test kwargs
    profile_details = moves_client.get_profile()
    first_date = profile_details['content']['profile']['firstDate']
    timezone_offset = profile_details['content']['profile']['currentTimeZone']['offset']
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

# test individual methods
    details = moves_client.get_summary(**empty_kwargs)
    assert isinstance(activities_list['content'], list)
    details = moves_client.get_activities(**start_kwargs)
    assert isinstance(activities_list['content'], list)
    details = moves_client.get_places(**end_kwargs)
    assert isinstance(activities_list['content'], list)
    details = moves_client.get_places(**both_kwargs)
    assert isinstance(activities_list['content'], list)
    details = moves_client.get_storyline(**story_kwargs)
    assert isinstance(activities_list['content'], list)

# test all data retrieval methods
    test_list = [ moves_client.get_summary, moves_client.get_places, moves_client.get_activities ]
    kwargs_list = [ empty_kwargs, start_kwargs, end_kwargs, both_kwargs ]
    for test in test_list:
        for kwargs in kwargs_list:
            details = test(**kwargs)
            assert isinstance(details['content'], list)
            sleep(.2)
    for kwargs in kwargs_list:
        new_kwargs = deepcopy(kwargs)
        new_kwargs['track_points'] = True
        if 'start' in new_kwargs and 'end' in new_kwargs:
            new_kwargs['end'] = track_dt
        details = moves_client.get_storyline(**new_kwargs)
        assert isinstance(details['content'], list)
        sleep(.2)

# test recent location
    current_dt = time()
    yesterday_dt = time() - (24 * 60 * 60)
    details = moves_client.get_places(timezone_offset, first_date, yesterday_dt, current_dt)
    sorted_days = sorted(details['content'], key=lambda k: k['date'])
    recent_day = sorted_days.pop()
    sorted_segments = sorted(recent_day['segments'], key=lambda k: k['endTime'])
    recent_segment = sorted_segments.pop()
    from labpack.records.time import labDT
    last_dt = labDT.fromISO(recent_segment['endTime']).humanFriendly()
    last_place = 'somewhere'
    if 'name' in recent_segment['place']:
        last_place = 'at the %s' % recent_segment['place']['name']
    print('At %s, you were %s.' % (last_dt, last_place))

# test track points
    current_dt = time()
    yesterday_dt = time() - (24 * 60 * 60)
    story_kwargs = {
        'timezone_offset': timezone_offset,
        'first_date': first_date,
        'start': yesterday_dt,
        'end': current_dt,
        'track_points': True
    }
    details = moves_client.get_storyline(**story_kwargs)
    sorted_days = sorted(details['content'], key=lambda k: k['date'])
    tracked_segment = {}
    for day in sorted_days:
        stop = False
        sorted_segments = sorted(day['segments'], key=lambda k: k['endTime'])
        for segment in sorted_segments:
            found = False
            if 'activities' in segment.keys():
                for activity in segment['activities']:
                    if 'trackPoints' in activity.keys():
                        if activity['trackPoints']:
                            found = True
                            stop = True
                            break
                if found:
                    tracked_segment = segment
                    break
        if stop:
            break
    print(tracked_segment['activities'][0])