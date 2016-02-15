__author__ = 'rcj1492'
__created__ = '2015.11'

def timeZonefromGPS(lat, long, timestamp, google_app_key):
    '''
        GET request to Google Timezone API to find timeZone from GPS location
        includes a performance test of API response time
        https://developers.google.com/maps/documentation/timezone/
        quota: 2500 per day
        throttle: 5 per sec
        dependencies:
        import json
        import urllib.request
        import urllib.parse
    :param lat: string from GPS latitude
    :param long: string from GPS longitude
    :param timestamp: string from epoch timestamp
    :return: string with standard timezone
    '''
    urlTitle = 'Google Map API'
    params = {
        'key': google_app_key,
        'location': str(lat) + "," + str(long),
        'timestamp': str(timestamp)
    }
    url = 'https://maps.googleapis.com/maps/api/timezone/json?%s'
    GET_params = urllib.parse.urlencode(params)
    t1 = timer()
    response = urllib.request.urlopen(url % GET_params)
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    data = json.loads(response.read().decode("utf-8"))
    return data['timeZoneId']
assert timeZonefromGPS(40.727516, -74.005722, time.time(), googleAppKey) == 'America/New_York'

def getGPSfromAddress(address, google_app_key):
    '''
        GET request to Google Places API to find GPS from address info
        includes a performance test of API response time
        https://developers.google.com/places/webservice/search
        quota: 2500 per day
        throttle: 5 per sec
        usage: each request uses 10 calls from quota
        dependencies:
        import json
        import urllib.request
        import urllib.parse
    :param query: string with address details
    :return dictionary with ['lat'] and ['lng']
    '''
    urlTitle = 'Google Map API'
    params = {
        'key': google_app_key,
        'query': str(address)
    }
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?%s'
    GET_params = urllib.parse.urlencode(params)
    t1 = timer()
    response = urllib.request.urlopen(url % GET_params)
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    data = json.loads(response.read().decode("utf-8"))
    return data['results'][0]['geometry']['location']
assert getGPSfromAddress('815 Post Rd Darien, CT 06820', googleAppKey)['lat'] == 41.0787049

def placeIDfromGPS(lat, long, google_app_key, keyword = None, type = None):
    '''
        GET request to Google Places API to placeID from GPS coordinate
        includes a performance test of API response time
        https://developers.google.com/places/webservice/search
        quota: 2500 per day
        throttle: 5 per sec
        usage: each request uses 10 calls from quota
        dependencies:
        import json
        import urllib.request
        import urllib.parse
    :param lat: string
    :param long: string
    :param keyword: string of word search of locations nearby
    :param type: string of location type, multiples separated by pipe
    :return list of results with most relevant first
    '''
    urlTitle = 'Google Map API'
    params = {
        'key': google_app_key,
        'location': str(lat) + "," + str(long),
        'radius': '50' # radius in meters from coordinate to search
    }
    if keyword:
        params['keyword'] = keyword
    if type:
        params['types'] = type
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?%s'
    GET_params = urllib.parse.urlencode(params)
    t1 = timer()
    response = urllib.request.urlopen(url % GET_params)
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    data = json.loads(response.read().decode("utf-8"))
    return data['results']
assert placeIDfromGPS(41.0787049, -73.468918, googleAppKey, type='cafe')[0]['place_id'] == \
       'ChIJrcijEoGgwokRheFOp_lB0Vw'

def placeDetailsfromPlaceID(placeid, google_app_key):
    '''
        GET request to Google Places API for place details from place ID
        includes a performance test of API response time
        https://developers.google.com/places/webservice/search
        quota: 2500 per day
        throttle: 5 per sec
        dependencies:
        import json
        import urllib.request
        import urllib.parse
    :param placeid: string
    :return
    '''
    urlTitle = 'Google Map API'
    params = {
        'key': google_app_key,
        'placeid': placeid
    }
    url = 'https://maps.googleapis.com/maps/api/place/details/json?%s'
    GET_params = urllib.parse.urlencode(params)
    t1 = timer()
    response = urllib.request.urlopen(url % GET_params)
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    data = json.loads(response.read().decode("utf-8"))
    return data['result']
assert placeDetailsfromPlaceID('ChIJrcijEoGgwokRheFOp_lB0Vw', googleAppKey)['name'] == 'Starbucks'
