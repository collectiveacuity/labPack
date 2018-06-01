__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

class findClient(object):

    _class_fields = {
        'schema': {
            'group_name': '',
            'server_url': '',
            'password': '',
            'user_id': '',
            'history': 0,
            'port': 0,
            'wifi_fingerprint': [ {
                'mac': '0A:1B:3C:4D:5E:6F',
                'rssi': -2
            }],
            'action': 'track',
            'location_id': ''
        },
        'components': {
            '.history': {
                'integer_data': True,
                'min_value': 1
            },
            '.port': {
                'integer_data': True
            },
            '.wifi_fingerprint[0].rssi': {
                'integer_data': True
            },
            '.action': {
                'discrete_values': [ 'track', 'learn' ]
            },
            '.location_id': {
                'must_not_contain': [ '\s' ]
            }
        }
    }
    
    def __init__(self, group_name, server_url='ml.internalpositioning.com', password=''):

        '''
            a method to initialize a findClient class object

        :param group_name: string with name of group 
        :param server_url: string with url for FIND server
        :param password: [optional] string with password to mosquitto server

        # https://www.internalpositioning.com/api
        '''

        title = '%s.__init__' % self.__class__.__name__
        
    # construct fields
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'group_name': group_name,
            'server_url': server_url,
            'password': password
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        
    # construct class properties
        self.server_url = server_url
        self.endpoint = 'https://%s' % server_url
        self.endpoint_public = 'http://%s' % server_url
        self.group_name = group_name
        self.password = password
        self.positions = {}
        self.locations = {}

    # add regex patterns
        import re
        self.user_pattern = re.compile('location/(.*)$')

    def get_password(self):

        '''
            a method to retrieve the password for the group mosquitto server

        :return: string with group mosquitto server password

        NOTE:   result is added to self.password property 
        '''

        import requests
        url = '%s/mqtt' % self.endpoint
        params = {
            'group': self.group_name
        }
        response = requests.put(url, params=params)
        response_details = response.json()
        self.password = response_details['password']

        return self.password

    def get_locations(self):

        '''
            a method to retrieve all the locations tracked by the model
            
        :return: dictionary with location id keys
        
        NOTE:   results are added to self.locations property
        
        {
            'location.id': {
                '
            }
        }
        '''
        
        import requests
        url = self.endpoint + '/locations'
        params = {
            'group': self.group_name
        }
        response = requests.get(url, params=params)
        response_details = response.json()
        if 'locations' in response_details.keys():
            self.locations = response_details['locations']
            
        return self.locations

    def update_model(self):
        
        '''
             a method to update model with latest training data
             
        :return: True
        '''
        
        import requests
        url = self.endpoint_public + '/calculate'
        params = {
            'group': self.group_name
        }
        response = requests.get(url, params=params)
        response_details = response.json()
        
        return response_details['success']

    def get_position(self, user_id, track=False, confidence=False):

        '''
            a method to retrieve the latest position of a user

        :param user_id: string with id of user
        :param track: [optional] boolean to add user to self.positions
        :param confidence: [optional] boolean to include the data model confidence scores
        :return: dictionaries with position details

        NOTE:   if user does not exist, then location and time are null values

        { 
            'time': 0.0, 
            'location': 'location.id', 
            'id': 'user_id', 
            bayes: {}, # if confidence = True 
            svm: None, # if confidence = True 
            rf: {} # if confidence = True 
        }
        '''

        title = '%s.get_position' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'user_id': user_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
            
    # construct empty response
        position_details = {
            'location': '',
            'time': 0.0,
            'id': user_id
        }

    # construct empty position history
        position_history = []
        
    # compose request
        import requests
        url = self.endpoint + '/location'
        params = {
            'group': self.group_name,
            'user': user_id,
            'n': 1
        }
        response = requests.get(url, params=params)

    # ingest response
        response_details = response.json()
        from labpack.records.time import labDT
        for key in response_details['users'].keys():
            if key == user_id:
                for entry in response_details['users'][key]:
                    if 'time' in entry.keys() and 'location' in entry.keys():
                        time_string = entry['time'] 
                        time_string = time_string.replace(' +0000 UTC', 'Z')
                        time_string = time_string.replace(' ', 'T')
                        time_dt = labDT.fromISO(time_string).epoch()
                        if confidence:
                            for key, value in entry.items():
                                position_details[key] = value
                        position_details['time'] = time_dt
                        position_details['location'] = entry['location']
                        break

        if track:
            stored_position = {
                'location': position_details['location'],
                'time': position_details['time']
            }
            self.positions[user_id] = stored_position

        return position_details

    def get_positions(self, user_id, history=1, confidence=False):
        
        '''
            a method to retrieve the position history of a user
            
        :param user_id: string with id of user
        :param history: [optional] integer with length of previous positions to retrieve
        :param confidence: [optional] boolean to include the data model confidence scores
        :return: list of dictionaries with position details
        
        NOTE:   if user does not exist, then list returns empty
        
        [{ 
            'time': 0.0, 
            'location': 'location.id', 
            'id': 'user_id', 
            bayes: {}, # if confidence = True 
            svm: None, # if confidence = True 
            rf: {} # if confidence = True 
        }]
        '''
    
        title = '%s.get_positions' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'user_id': user_id,
            'history': history
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct empty position history
        position_history = []
        
    # compose request
        import requests
        url = self.endpoint + '/location'
        params = {
            'group': self.group_name,
            'user': user_id,
            'n': history
        }
        response = requests.get(url, params=params)

    # ingest response
        response_details = response.json()
        from labpack.records.time import labDT
        for key in response_details['users'].keys():
            if key == user_id:
                for entry in response_details['users'][key]:
                    position_details = {}
                    if 'time' in entry.keys() and 'location' in entry.keys():
                        time_string = entry['time'] 
                        time_string = time_string.replace(' +0000 UTC', 'Z')
                        time_string = time_string.replace(' ', 'T')
                        time_dt = labDT.fromISO(time_string).epoch()
                        if confidence:
                            for key, value in entry.items():
                                position_details[key] = value
                        position_details['time'] = time_dt
                        position_details['location'] = entry['location']
                        position_history.append(position_details)

        return position_history

    def update_positions(self):

        '''
            a method to update the latest position of all users being tracked 
            
        :return: dictionary with user_id keys and location/time dictionary values
        
        NOTE:   self.players is updated with position details
        
        {
            'user_id': {
                'time': 0.0,
                'location': 'location.id'
            }
        }
        '''
        
    # construct user list
        user_list = []
        for key in self.positions.keys():
            user_list.append(key)

    # return empty result
        if not user_list:
            return self.positions

    # compose request
        import requests
        url = self.endpoint + '/location'

        while user_list:

        # batch requests
            if len(user_list) > 50:
                user_batch = user_list[0:50]
            else:
                user_batch = user_list
            params = {
                'group': self.group_name,
                'users': ','.join(user_batch),
                'n': 1
            }
            response = requests.get(url, params=params)
    
        # ingest response
            response_details = response.json()
            from labpack.records.time import labDT
            if 'users' in response_details.keys():
                for key in response_details['users'].keys():
                    position_details = {}
                    if key in user_batch:
                        for entry in response_details['users'][key]:
                            if 'time' in entry.keys() and 'location' in entry.keys():
                                time_string = entry['time'] 
                                time_string = time_string.replace(' +0000 UTC', 'Z')
                                time_string = time_string.replace(' ', 'T')
                                time_dt = labDT.fromISO(time_string).epoch()
                                position_details = {
                                    'time': time_dt,
                                    'location': entry['location']
                                }
                                break
                        self.positions[key] = position_details

        # slice user list
            if len(user_list) > 50:
                user_list = user_list[50:0]
            else:
                user_list = []

        return self.positions

    def subscribe(self, callable=None, block=False, port=1883):

        '''
            a method to establish a mosquitto socket with server to receive position updates
            
        :param callable: [optional] callable to process the received positions
        :param block: [optional] boolean to block the main thread when method is called
        :param port: [optional] integer with port to connect to
        :return: None
        
        NOTE:   subscribing without a callable will update the self.positions object
                with any user message

        { 
            'time': 0.0, 
            'location': 'location.id', 
            'id': 'user_id', 
            bayes: {}, 
            svm: None, 
            rf: {} 
        }

        # https://www.internalpositioning.com/server/
        '''

        title = '%s.subscribe' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'port': port
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # import dependencies
        import paho.mqtt.client as mqtt

    # define callback on connection event
        def on_connect(client, userdata, flags, rc):

            if rc == 5:
                raise ValueError('MQTT to %s authorization failed.' % self.group_name)

            print("Connected to %s with result code %s" % (self.group_name, rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("%s/location/#" % self.group_name)

    # define callback on a new message event
        def on_message(client, userdata, msg):

            import json
            user_search = self.user_pattern.findall(msg.topic)
            user_id = user_search[0]
            user_location = json.loads(msg.payload.decode())
            user_location['time'] = user_location['time'] / 1000000000
            user_location['id'] = user_id
            if callable:
                callable(user_location)
            else:
                self.positions[user_id] = { 
                    'location': user_location['location'], 
                    'time': user_location['time']
                }

    # instantiate client and configure methods
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(self.group_name, self.password)
        client.connect_async(self.server_url, port, 60)

    # start blocking listener
        if block:
            client.loop_forever()
    # start listener in separate thread
        else:
            client.loop_start()
 
    def publish(self, user_id, wifi_fingerprint, action='track', location_id='', port=1883):

        '''
            a method to publish wifi fingerprint data to a mosquitto server
            
        :param user_id: string with id of user
        :param wifi_fingerprint: list of dictionaries with wifi fields mac and rssi 
        :param action: string with type of action to perform with data (track or learn)
        :param location_id: [optional] string with classifier to add to learning data
        :param port: [optional] integer with port to connect to
        :return: True
        '''
        
        title = '%s.publish' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'user_id': user_id,
            'wifi_fingerprint': wifi_fingerprint,
            'action': action,
            'location_id': location_id,
            'port': port
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
            
    # compose message
        fingerprint_string = ''
        for signal in wifi_fingerprint:
            fingerprint_string += signal['mac'].replace(':','')
            rssi_string = str(signal['rssi']).replace('-','')
            if len(rssi_string) > 2:
                fingerprint_string += ' '
            fingerprint_string += rssi_string

    # compose channel
        topic_string = '%s/track/%s' % (self.group_name, user_id)
        if action == 'learn':
            topic_string = '%s/learn/%s/%s' % (self.group_name, user_id, location_id)

    # send a single message to server
        import paho.mqtt.publish as mqtt_publish
        mqtt_publish.single(
            topic=topic_string,
            payload=fingerprint_string,
            auth={ 'username': self.group_name, 'password': self.password },
            hostname=self.server_url,
            port=port
        )

        return True

if __name__ == '__main__':
    
    from time import time
    from labpack.records.settings import load_settings
    find_cred = load_settings('../../../cred/find.yaml')
    find_client = findClient(
        group_name=find_cred['find_mqtt_group'],
        password=find_cred['find_mqtt_password']
    )

# test password
    password = find_client.get_password()
    assert password == find_cred['find_mqtt_password']

# test locations
    locations = find_client.get_locations()
    print(locations)

# test update model
    assert find_client.update_model()
    
# test positions
    user_id = find_cred['find_mqtt_admin']
    positions = find_client.get_positions(user_id, history=2, confidence=True)
    assert len(positions) == 2

# test position
    position = find_client.get_position(user_id, track=True)
    del position['id']
    position_map = { user_id: position }
    assert position_map == find_client.positions

# test publish
    wifi_fingerprint = find_cred['find_wifi_fingerprint']
    find_client.publish(user_id, wifi_fingerprint)

# test update positions
    find_client.update_positions()
    assert find_client.positions[user_id]
    assert find_client.positions[user_id]['time'] + 5 > time()

# test subscribe
    find_client.subscribe(callable=print, block=True)
