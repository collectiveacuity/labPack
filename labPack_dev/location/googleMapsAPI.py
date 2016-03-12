__author__ = 'rcj1492'
__created__ = '2015.11'

'''
https://github.com/googlemaps/google-maps-services-python
https://developers.google.com/maps/documentation/
https://developers.google.com/maps/documentation/geocoding/intro
'''

import json
from urllib.request import urlopen
from urllib.parse import urlencode
from timeit import default_timer as timer

class GoogleConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to Google Maps API with %s request.' % message
        super(GoogleConnectionError, self).__init__(text)
        self.errors = errors

class mapInputs(object):

    __name__ = 'mapInputs'

    def __init__(self, map_rules):

        title = self.__name__ + '.__init__()'

        if not isinstance(map_rules, dict):
            raise TypeError('%s map_rules input must be a dictionary.' % title)
        self.rules = map_rules

    def gpsCoordinates(self, latitude, longitude, title=''):
        if not isinstance(latitude, float):
            raise TypeError('%s latitude input must be a float.' % title)
        elif not isinstance(longitude, float):
            raise TypeError('%s longitude input must be a float.' % title)
        return latitude, longitude

    def timestamp(self, timestamp, title=''):
        if not isinstance(timestamp, float) and not isinstance(timestamp, int):
            raise TypeError('%s timestamp input must be an epoch timestamp.' % title)

    def proximity(self, proximity, title=''):
        max_distance = 50000
        if not isinstance(proximity, int):
            raise TypeError('%s proximity input must be an integer.' % title)
        elif not proximity > 0:
            raise ValueError('%s proximity input must be greater than 0.' % title)
        elif proximity > max_distance:
            raise ValueError('%s proximity input cannot be more than %s' % (title, max_distance))
        return proximity

    def locationTypes(self, type_list, title=''):
        req_list = self.rules['locationTypes']
        if not isinstance(type_list, list):
            raise TypeError('%s types input must be a list.' % title)
        for i in range(len(type_list)):
            if not isinstance(type_list[i], str):
                raise TypeError('%s types list item [%s] must be a string.' % (title, i))
            elif type_list[i] not in req_list:
                raise ValueError('%s types list item [%s] is not a valid Google location type.' % (title, i))
        return type_list

    def geocodeTypes(self, type_list, title=''):
        req_list = self.rules['geocodeTypes']
        if not isinstance(type_list, list):
            raise TypeError('%s types input must be a list.' % title)
        for i in range(len(type_list)):
            if not isinstance(type_list[i], str):
                raise TypeError('%s types list item [%s] must be a string.' % (title, i))
            elif type_list[i] not in req_list:
                raise ValueError('%s types list item [%s] is not a valid Google geocode location type.' % (title, i))
        return type_list

class googleMaps(object):

    '''
        a class of methods to retrieve location information from Google Maps API
    '''

    __name__ = 'googleMaps'

    def __init__(self, app_key, map_rules):

        title = self.__name__ + '.__init__()'

        if not isinstance(app_key, str):
            raise TypeError('%s app_key input must be a string.' & title)
        elif not isinstance(map_rules, dict):
            raise TypeError('%s.__init__() map_rules input must be a dictionary.' % self.__name__)
        self.appKey = app_key
        self.input = mapInputs(map_rules)
        self.endpoints = {
            'timezone': 'https://maps.googleapis.com/maps/api/timezone/json',
            'elevation': 'https://maps.googleapis.com/maps/api/elevation/json',
            'nearbysearch': 'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
            'placedetails': 'https://maps.googleapis.com/maps/api/place/details/json',
            'textsearch': 'https://maps.googleapis.com/maps/api/place/textsearch/json',
            'geocode': 'https://maps.googleapis.com/maps/api/geocode/json'
        }

    def timeZoneID(self, latitude, longitude, timestamp=0, benchmark=False):

        '''
        :param latitude: float from GPS latitude
        :param longitude: float from GPS longitude
        :param timestamp: [optional] float or int with epoch timestamp
        :param benchmark: [optional] boolean to report response time
        :return: string with timezone
        '''

        title = self.__name__ + '.timeZoneID()'

    # validate inputs
        self.input.gpsCoordinates(latitude, longitude, title)
        if timestamp:
            self.input.timestamp(timestamp, title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'location': str(latitude) + ',' + str(longitude)
        }
        if timestamp:
            url_params['timestamp'] = int(timestamp)
        get_url = self.endpoints['timezone'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        response_dict = json.loads(response.read().decode("utf-8"))
        time_zone = response_dict['timeZoneId']
        return time_zone

    def elevation(self, latitude, longitude, benchmark=False):

        '''
        :param latitude: float from GPS latitude
        :param longitude: float from GPS longitude
        :param benchmark: [optional] boolean to report response time
        :return: float with elevation in meters
        '''

        title = self.__name__ + '.elevation()'

    # validate inputs
        self.input.gpsCoordinates(latitude, longitude, title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'locations': str(latitude) + ',' + str(longitude)
        }
        get_url = self.endpoints['elevation'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        response_dict = json.loads(response.read().decode("utf-8"))
        elevation = response_dict['results'][0]['elevation']
        return elevation

    def placeList(self, latitude, longitude, proximity=50, keywords=None, types=None, benchmark=False):

        '''
        :param latitude: float from GPS latitude
        :param longitude: float from GPS longitude
        :param proximity: [optional] integer with radius to refine search for places
        :param keywords: [optional] string with words to refine search for places
        :param types: [optional] list with place types to refine search for places
        :param benchmark: [optional] boolean to report response time
        :return: list of google place dictionaries

        https://developers.google.com/places/supported_types
        '''

        title = self.__name__ + '.placeList()'

    # validate inputs
        self.input.gpsCoordinates(latitude, longitude, title)
        self.input.proximity(proximity, title)
        if keywords:
            if not isinstance(keywords, str):
                raise TypeError('%s keywords input must be a string.' % title)
        if types:
            self.input.locationTypes(types, title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'location': str(latitude) + ',' + str(longitude),
            'radius': proximity
        }
        if keywords:
            url_params['keyword'] = keywords
        if types:
            type_string = ''
            for type in types:
                if type_string:
                    type_string += '|'
                type_string += type
            url_params['types'] = type_string
        get_url = self.endpoints['nearbysearch'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        place_list = []
        response_dict = json.loads(response.read().decode("utf-8"))
        if response_dict['results']:
            for result in response_dict['results']:
                details = {
                    'placeID': result['place_id'],
                    'placeName': '',
                    'placeVicinity': '',
                    'placeIcon': '',
                    'placeTypes': []
                }
                if 'name' in result:
                    details['placeName'] = result['name']
                if 'vicinity' in result:
                    details['placeVicinity'] = result['vicinity']
                if 'icon' in result:
                    details['placeIcon'] = result['icon']
                if 'types' in result:
                    details['placeTypes'] = result['types']
                place_list.append(details)
        return place_list

    def placeDetails(self, place_id, benchmark=False):

        '''
        :param place_id: string with Google ID for a place
        :param benchmark: [optional] boolean to report response time
        :return: dictionary with place details
        '''

        title = self.__name__ + '.placeDetails()'

    # validate inputs
        if not isinstance(place_id, str):
            raise TypeError('%s place_id input must be a string.' % title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'placeid': place_id
        }
        get_url = self.endpoints['placedetails'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        response_dict = json.loads(response.read().decode("utf-8"))
        details = {}
        if response_dict['result']:
            details = {
                'fullAddress': '',
                'streetNumber': '',
                'streetName': '',
                'city': '',
                'region': '',
                'postalCode': '',
                'country': '',
                'placeID': place_id,
                'placeName': '',
                'placeIcon': '',
                'placeTypes': [],
                'phoneNumber': '',
                'placeUrl': '',
                'googleUrl': response_dict['result']['url'],
                'latitude': response_dict['result']['geometry']['location']['lat'],
                'longitude': response_dict['result']['geometry']['location']['lng']
            }
            for component in response_dict['result']['address_components']:
                if 'street_number' in component['types']:
                    details['streetNumber'] = component['long_name']
                if 'route' in component['types']:
                    details['streetName'] = component['long_name']
                if 'locality' in component['types']:
                    details['city'] = component['long_name']
                if 'administrative_area_level_1' in component['types']:
                    details['region'] = component['long_name']
                if 'country' in component['types']:
                    details['country'] = component['long_name']
                if 'postal_code' in component['types']:
                    details['postalCode'] = component['long_name']
            if 'icon' in response_dict['result']:
                details['placeIcon'] = response_dict['result']['icon']
            if 'name' in response_dict['result']:
                details['placeName'] = response_dict['result']['name']
            if 'types' in response_dict['result']:
                details['placeTypes'] = response_dict['result']['types']
            if 'website' in response_dict['result']:
                details['placeUrl'] = response_dict['result']['website']
            if 'formatted_address' in response_dict['result']:
                details['fullAddress'] = response_dict['result']['formatted_address']
            if 'international_phone_number' in response_dict['result']:
                details['phoneNumber'] = response_dict['result']['international_phone_number']
            elif 'formatted_phone_number' in response_dict['result']:
                details['phoneNumber'] = response_dict['result']['formatted_phone_number']

        return details

    def placeGPS(self, address_string, benchmark=False):

        '''
        :param address_string: string with address details
        :param benchmark: [optional] boolean to report response time
        :return: tuple with latitude and longitude floats
        '''

        title = self.__name__ + '.placeGPS()'

    # validate inputs
        if not isinstance(address_string, str):
            raise TypeError('%s address_string input must be a string.' % title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'query': address_string
        }
        get_url = self.endpoints['textsearch'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        response_dict = json.loads(response.read().decode("utf-8"))
        latitude = None
        longitude = None
        if response_dict['results']:
            latitude = response_dict['results'][0]['geometry']['location']['lat']
            latitude = float("{0:.7f}".format(latitude))
            longitude = response_dict['results'][0]['geometry']['location']['lng']
            longitude = float("{0:.7f}".format(longitude))

        return latitude, longitude

    def addressList(self, latitude, longitude, types=None, benchmark=False):

        '''
        :param latitude: float from GPS latitude
        :param longitude: float from GPS longitude
        :param types: [optional] list with geocode types to refine search for addresses
        :param benchmark: [optional] boolean to report response time
        :return: list of address dictionaries

        https://developers.google.com/maps/documentation/geocoding/intro
        '''

        title = self.__name__ + '.addressList()'

    # validate inputs
        self.input.gpsCoordinates(latitude, longitude, title)
        if types:
            self.input.geocodeTypes(types, title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'latlng': str(latitude) + ',' + str(longitude)
        }
        if types:
            type_string = ''
            for type in types:
                if type_string:
                    type_string += '|'
                type_string += type
            url_params['location_type'] = type_string
        get_url = self.endpoints['geocode'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        address_list = []
        response_dict = json.loads(response.read().decode("utf-8"))
        if response_dict['results']:
            for result in response_dict['results']:
                details = {
                    'placeID': '',
                    'fullAddress': '',
                    'placeTypes': [],
                    'streetNumber': '',
                    'streetName': '',
                    'neighborhood': '',
                    'city': '',
                    'region': '',
                    'postalCode': '',
                    'country': ''
                }
                lat = result['geometry']['location']['lat']
                details['latitude'] = float("{0:.7f}".format(lat))
                long = result['geometry']['location']['lng']
                details['longitude'] = float("{0:.7f}".format(long))
                if 'place_id' in result:
                    details['placeID'] = result['place_id']
                if 'formatted_address' in result:
                    details['fullAddress'] = result['formatted_address']
                if 'types' in result:
                    details['placeTypes'] = result['types']
                for component in result['address_components']:
                    if 'street_number' in component['types']:
                        details['streetNumber'] = component['long_name']
                    if 'route' in component['types']:
                        details['streetName'] = component['long_name']
                    if 'neighborhood' in component['types']:
                        details['neighborhood'] = component['long_name']
                    if 'locality' in component['types']:
                        details['city'] = component['long_name']
                    if 'administrative_area_level_1' in component['types']:
                        details['region'] = component['long_name']
                    if 'country' in component['types']:
                        details['country'] = component['long_name']
                    if 'postal_code' in component['types']:
                        details['postalCode'] = component['long_name']
                address_list.append(details)
        return address_list

    def geocodeGPS(self, address_string, benchmark=False):

        '''
        :param address_string: string with address details
        :param benchmark: [optional] boolean to report response time
        :return: tuple with latitude and longitude floats
        '''

        title = self.__name__ + '.geocodeGPS()'

    # validate inputs
        if not isinstance(address_string, str):
            raise TypeError('%s address_string input must be a string.' % title)

    # create url request parameters
        url_params = {
            'key': self.appKey,
            'address': address_string
        }
        get_url = self.endpoints['geocode'] + '?' + urlencode(url_params)

    # send request
        try:
            t0 = timer()
            response = urlopen(get_url)
            t1 = timer()
            if benchmark:
                print(title + ': ' + str(t1 - t0) + ' seconds')
        except:
            raise GoogleConnectionError(title + ' urlopen()')

    # construct result from response
        response_dict = json.loads(response.read().decode("utf-8"))
        latitude = None
        longitude = None
        if response_dict['results']:
            latitude = response_dict['results'][0]['geometry']['location']['lat']
            latitude = float("{0:.7f}".format(latitude))
            longitude = response_dict['results'][0]['geometry']['location']['lng']
            longitude = float("{0:.7f}".format(longitude))

        return latitude, longitude

    def unitTests(self):
        assert self.timeZoneID(40.727516, -74.005722, 1448155180, True)
        assert self.elevation(40.727516, -74.005722, True)
        assert self.placeList(40.727516, -74.005722, proximity=20, keywords='wework', types=['restaurant', 'establishment'], benchmark=True)
        assert self.placeDetails('ChIJD9hlR41ZwokR7VM-8_Ereb0', True)
        assert self.placeGPS('175 Varick Street, NY, NY 10014', True)
        assert self.geocodeGPS('175 Varick Street, NY, NY 10014', True)
        assert self.addressList(40.727516, -74.005722, types=['ROOFTOP'], benchmark=True)
        return self

# TODO: directions
# TODO: speed limits
# TODO: distance matrix (travel distance and time)

