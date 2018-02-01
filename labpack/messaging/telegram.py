__author__ = 'rcj1492'
__created__ = '2016.09'
__license__ = 'MIT'

'''
    python module for bot api
    https://github.com/luckydonald/pytgbot

    python wrapper for telegram cli
    https://github.com/luckydonald/pytg

    telegram cli
    https://github.com/vysheng/tg

    telegram with OAUTH
    http://stackoverflow.com/questions/37264827/telegram-bot-oauth-authorization

    haproxy with ssl pass-thru
    https://serversforhackers.com/using-ssl-certificates-with-haproxy
    http://nginx.2469901.n2.nabble.com/SSL-pass-through-td7583170.html
'''

class TelegramBotError(Exception):

    def __init__(self, message='', error_dict=None):

    # TODO create bad connection diagnostics methods

        text = '\nFailure connecting to Telegram Bot API with %s request.' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                self.error = error_dict
        super(TelegramBotError, self).__init__(text)

# TODO: test all different errors
class telegramBotHandler(object):

    def __init__(self):
        pass

    def handle(self, response):

    # construct default response details
        details = {
            'method': response.request.method,
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers,
        }

    # handle different codes
        if details['code'] == 200:
            details['json'] = response.json()
        elif details['code'] == 403 or details['code'] == 400:
            details['error'] = response.json()['description']
        else:
            details['error'] = response.content.decode()

        return details

class telegramBotRegister(object):

    ''' a class of methods to register a new bot with telegram bot api

    currently must be done manually
    https://core.telegram.org/bots#6-botfather

    botfather_url = 'https://web.telegram.org/#/im?p=@BotFather'
    setup_sequence = [
        'tg://bot_command?command=start',
        'tg://bot_command?command=newbot&bot=BotFather',
        'message with name',
        'message with username',
        'tg://bot_command?command=cancel&bot=BotFather'
    ]
    '''

    def __init__(self, bot_settings):
        pass

    def setup(self):
        return self

    def update(self):
        return self

class telegramBotClient(object):

    ''' a class of methods for interacting with telegram bot api '''

    # https://core.telegram.org/bots/api

    _class_fields = {
        'schema': {
            'api_endpoint': 'https://api.telegram.org/bot',
            'file_endpoint': 'https://api.telegram.org/file/bot',
            'bot_id': 0,
            'access_token': '',
            'max_connections': 0,
            'webhook_url': 'https://mydomain.com/secret_token_value',
            'certificate_id': '',
            'certificate_path': 'path/to/cert.pub',
            'certificate_url': '',
            'last_update': 0,
            'user_id': 0,
            'user_name': '',
            'message_text': 'am i too needy?',
            'message_style': 'markdown',
            'button_list': [ 'yes' ],
            'keypad_type': 'phone',
            'photo_id': '',
            'photo_path': '',
            'photo_url': '',
            'caption_text': '',
            'file_id': '',
            'photo_extensions': {
                'jpg': '.+\\.jpg$',
                'jpeg': '.+\\.jpeg$',
                'gif': '.+\\.gif$',
                'png': '.+\\.png$',
                'tif': '.+\\.tif$',
                'bmp': '.+\\.bmp$'
            },
            'certificate_extensions': {
                'pem': '.+\\.pem$'
            }
        },
        'components': {
            '.bot_id': {
                'integer_data': True
            },
            '.last_update': {
                'integer_data': True
            },
            '.user_id': {
                'integer_data': True
            },
            '.message_style': {
                'discrete_values': [ 'markdown' ]
            },
            '.keypad_type': {
                'discrete_values': [ 'phone', 'calculator' ]
            },
            '.button_list[0]': {
                'max_length': 32
            },
            '.caption_text': {
                'max_length': 200
            },
            '.max_connections': {
                'integer_data': True,
                'max_value': 100,
                'min_value': 1
            }
        }
    }

    def __init__(self, bot_id, access_token, requests_handler=None):

        ''' initialization method for moves client class

        :param bot_id: integer with telegram id number for bot
        :param access_token: string with access token for bot provided by telegram botfather
        :param requests_handler: callable that handles requests errors
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct client attributes
        object_title = '%s.__init__(bot_id=%s)' % (self.__class__.__name__, str(bot_id))
        self.bot_id = self.fields.validate(bot_id, '.bot_id', object_title)
        object_title = '%s.__init__(access_token=%s)' % (self.__class__.__name__, str(access_token))
        self.access_token = self.fields.validate(access_token, '.access_token', object_title)
        self.api_endpoint = '%s%s:%s' % (self.fields.schema['api_endpoint'], self.bot_id, self.access_token)
        self.file_endpoint = '%s%s:%s/' % (self.fields.schema['file_endpoint'], self.bot_id, self.access_token)

    # construct handlers
        self.requests_handler = requests_handler
        self.telegram_handler = telegramBotHandler()

    def _get_data(self, file_url, file_name='', method_title='', argument_title=''):

        ''' a helper method to retrieve data buffer for a file url

        :param file_url: string with url to file
        :param file_name: [optional] string with name to affix to file buffer
        :param method_title: [optional] string with name of class method calling
        :param argument_title: [optional] string with name of method argument key
        :return: byte data buffer with file data
        '''

        # https://docs.python.org/3/library/io.html#io.BytesIO

        import io
        import requests

    # fill empty values
        if not file_name:
            file_name = 'file'
        if not method_title:
            method_title = '%s._get_data' % self.__class__.__name__
        if not argument_title:
            argument_title = 'file_url'

    # request file from url
        try:
            remote_file = requests.get(file_url)
        except requests.exceptions.ConnectionError as err:
            if self.requests_handler:
                return self.requests_handler(err)
            else:
                raise
        except:
            raise ValueError('%s(%s=%s) is not a valid url.' % (method_title, argument_title, file_url))

    # add contents to buffer
        file_buffer = io.BytesIO(remote_file.content)
        file_buffer.name = '%s' % file_name

        return file_buffer

    def _validate_type(self, file_name, extension_map, method_title, argument_title):

        ''' a helper method to validate extension type of file

        :param file_name: string with file name to test
        :param extension_map: dictionary with extensions names and regex patterns
        :param method_title: string with title of feeder method
        :param argument_title: string with title of argument key from feeder method
        :return: string with file extension
        '''

    # validate file extension
        from labpack.parsing.regex import labRegex
        file_extension = ''
        ext_types = labRegex(extension_map)
        file_mapping = ext_types.map(file_name)[0]
        extension_list = []
        for key, value in file_mapping.items():
            if isinstance(value, bool):
                extension_list.append('.%s' % key)
            if value and isinstance(value, bool):
                file_extension = '.%s' + key
        if not file_extension:
            raise ValueError('%s(%s=%s) must be one of %s file types.' % (method_title, argument_title, file_name, extension_list))

        return file_extension

    def _compile_buttons(self, button_list, small_buttons, persist_buttons):

        ''' a helper method to compile buttons to telegram api format

        :param button_list: list of strings with button values
        :param small_buttons: boolean to resize buttons to fit text size
        :param persist_buttons: boolean to keep buttons around after exiting
        :return: string in json serial format
        '''

        import json
        keyboard_list = []
        for item in button_list:
            keyboard_list.append([{'text': item}])
        keyboard_kwargs = {
            'keyboard': keyboard_list,
            'one_time_keyboard': not persist_buttons,
            'resize_keyboard': small_buttons
        }
        json_data = json.dumps(keyboard_kwargs)
        return json_data

    def _compile_keypad(self, keypad_type, persist_buttons):
        
        ''' a helper method to compile keypad buttons to telegram api format

        :param keypad_type: string with type of keypad to emulate
        :param persist_buttons: boolean to keep buttons around after exiting
        :return: string in json serial format
        '''

        import json
        keyboard_list = []
        if keypad_type == 'phone':
            row_list = [ {'text': '1'}, {'text': '2'}, {'text': '3'} ]
            keyboard_list.append(row_list)
            row_list = [ {'text': '4'}, {'text': '5'}, {'text': '6'} ]
            keyboard_list.append(row_list)
            row_list = [ {'text': '7'}, {'text': '8'}, {'text': '9'} ]
            keyboard_list.append(row_list)
            row_list = [ {'text': '*'}, {'text': '0'}, {'text': '#'} ]
            keyboard_list.append(row_list)
        elif keypad_type == 'calculator':
            row_list = [ {'text': '7'}, {'text': '8'}, {'text': '9'}, {'text': '/'} ]
            keyboard_list.append(row_list)
            row_list = [ {'text': '4'}, {'text': '5'}, {'text': '6'}, {'text': '*'} ]
            keyboard_list.append(row_list)
            row_list = [ {'text': '1'}, {'text': '2'}, {'text': '3'}, {'text': '-'} ]
            keyboard_list.append(row_list)
            row_list = [ {'text': '0'}, {'text': '.'}, {'text': '='}, {'text': '+'} ]
            keyboard_list.append(row_list)
        keyboard_kwargs = {
            'keyboard': keyboard_list,
            'one_time_keyboard': not persist_buttons,
            'resize_keyboard': True
        }
        json_data = json.dumps(keyboard_kwargs)
        return json_data

    def _post_request(self, url, data=None, files=None):

        ''' a helper method for sending post requests to telegram api

        https://core.telegram.org/bots/api#making-requests
        https://requests.readthedocs.io/en/master/user/quickstart/

        :param url: string with url for post request
        :param data: [optional] dictionary with data to add to request
        :param files: [optional] byte data to add to request
        :return: dictionary with response details
        '''

        import requests

    # construct request fields
        request_kwargs = {
            'url': url
        }
        if data:
            request_kwargs['data'] = data
        if files:
            request_kwargs['files'] = files

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
        response_details = self.telegram_handler.handle(response)

        return response_details

    def get_me(self):

        ''' a method to retrieve details about the bot from telegram api

        :return: dictionary of response details with bot details in 'json' key

        {
            'headers': { ... },
            'url': 'https://api.telegram.org/bot.../getUpdates',
            'code': 200,
            'error': '',
            'json': {
                'ok': True,
                'result': {
                    'id': 1234567890,
                    'first_name': 'my Bot',
                    'username': 'myBot'
                }
            }
        }
        '''

    # construct request fields
        url = '%s/getMe?test=me' % self.api_endpoint

    # send request
        response_details = self._post_request(url)

        return response_details

    def set_webhook(self, webhook_url, certificate_id='', certificate_path='', certificate_url='', max_connections=40):

        # https://core.telegram.org/bots/self-signed
        
        title = '%s.set_webhook' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'webhook_url': webhook_url,
            'certificate_id': certificate_id,
            'certificate_path': certificate_path,
            'certificate_url': certificate_url,
            'max_connections': max_connections
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # construct request fields
        request_kwargs = {
            'url': '%s/setWebhook' % self.api_endpoint,
            'data': {
                'url': webhook_url,
                'max_connections': max_connections
            }
        }
    
    # construct extension map
        extension_map = self.fields.schema['certificate_extensions']
    
    # add photo to request keywords
        if certificate_path:
            import os
            self._validate_type(certificate_path, extension_map, title, 'certificate_path')
            if not os.path.exists(certificate_path):
                raise ValueError('%s is not a valid file path.' % certificate_path)
            request_kwargs['files'] = { 'certificate': open(certificate_path, 'rb') }
        elif certificate_id:
            request_kwargs['data']['certificate'] = certificate_id
        elif certificate_url:
            file_extension = self._validate_type(certificate_url, extension_map, title, 'certificate_url')
            file_buffer = self._get_data(certificate_url, 'certificate%s' % file_extension, title, 'certificate_url')
            request_kwargs['files'] = { 'certificate': file_buffer }

    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details
    
    def delete_webhook(self):
        
        title = '%s.delete_webhook' % self.__class__.__name__
    
    # construct request fields
        request_kwargs = {
            'url': '%s/setWebhook' % self.api_endpoint
        }    
    
    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details
    
    def get_updates(self, last_update=0):

        ''' a method to retrieve messages for bot from telegram api

        :param last_update: integer with update id of last message received
        :return: dictionary of response details with update list in [json][result]

        {
            'headers': { ... },
            'url': 'https://api.telegram.org/bot.../getUpdates',
            'code': 200,
            'error': '',
            'json': {
                'ok': True,
                'result': [
                    {
                        'update_id': 667652176,
                        'message': {
                            'chat': {
                                'first_name': 'First',
                                'type': 'private',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'text': 'Hey',
                            'from': {
                                'first_name': 'First',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'message_id': 173,
                            'date': 1478729313
                        }
                    },
                    {
                        'update_id': 667652176,
                        'message': {
                            'chat': {
                                'first_name': 'First',
                                'type': 'private',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'caption': 'Interesting song',
                            'photo': [
                                {
                                    'file_id': 'AgADAQ...EC',
                                    'width': 51,
                                    'file_size': 1238,
                                    'height': 90
                                },
                                {
                                    'file_id': 'AgADAQ...Ag',
                                    'width': 180,
                                    'file_size': 13151,
                                    'height': 320
                                },
                                {
                                    'file_id': 'AgADAQ...VC',
                                    'width': 449,
                                    'file_size': 51134,
                                    'height': 800
                                },
                                {
                                    'file_id': 'AgADAQ...AC',
                                    'width': 719,
                                    'file_size': 82609,
                                    'height': 1280
                                }
                            ],
                            'from': {
                                'first_name': 'First',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'message_id': 175,
                            'date': 1478729799
                        }
                    },
                    {
                        'update_id': 667652179,
                        'message': {
                            'chat': {
                                'first_name': 'First',
                                'type': 'private',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'caption': 'Snow in slow mo',
                            'document': {
                                'file_name': 'IMG_0010.MOV',
                                'thumb': {
                                    'file_id': 'AAQB...IC',
                                    'file_size': 2547,
                                    'width': 90,
                                    'height': 50
                                },
                                'file_size': 51588899,
                                'file_id': 'BQAD...QI'
                            }
                            'from': {
                                'first_name': 'First',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'message_id': 176,
                            'date': 1478729313
                        }
                    },
                    {
                        'update_id': 667652180,
                        'message': {
                            'chat': {
                                'first_name': 'First',
                                'type': 'private',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'location': {
                                'latitude': 12.345678,
                                'longitude': -23.456789
                            },
                            'venue': {'
                                location': {
                                    'latitude': 12.345678,
                                    'longitude': -23.456789
                                },
                                'address': '1 Laboratory Rd',
                                'title': 'Collective Acuity Labs',
                                'foursquare_id': '4a...e3'
                            },
                            'from': {
                                'first_name': 'First',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'message_id': 177,
                            'date': 1478729313
                        }
                    },
                    {
                        'update_id': 667652191,
                        'message': {
                            'chat': {
                                'first_name': 'First',
                                'type': 'private',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'voice': {
                                'duration': 3,
                                'mime_type': 'audio/ogg',
                                'file_id': 'AwADAQADAgADXGbcC3hOFYsqDDtKAg',
                                'file_size': 7008
                            },
                            'from': {
                                'first_name': 'First',
                                'id': 1234567890,
                                'last_name': 'Last'
                            },
                            'message_id': 224,
                            'date': 1478729313
                        }
                    }
                ]
            }
        }
        '''

        title = '%s.get_updates' % self.__class__.__name__

    # construct request fields
        request_kwargs = {
            'url': '%s/getUpdates' % self.api_endpoint
        }

    # add offset to kwargs
        if last_update:
            object_title = '%s(last_update=%s)' % (title, str(last_update))
            self.fields.validate(last_update, '.last_update', object_title)
            request_kwargs['data'] = {
                'offset': last_update + 1
            }

    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details

    def get_route(self, file_id):

        ''' a method to retrieve route information for file on telegram api

        :param file_id: string with id of file in a message send to bot
        :return: dictionary of response details with route details in [json][result]
        '''

        title = '%s.get_route' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'file_id': file_id,
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct key word arguments
        request_kwargs = {
            'url': '%s/getFile' % self.api_endpoint,
            'data': {
                'file_id': file_id
            }
        }

    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details

    def get_file(self, file_route, file_name=''):

        ''' a method to retrieve data for a file housed on telegram api

        :param file_route: string with route to file endpoint on telegram api
        :return: byte data stream with file data
        '''

        title = '%s.get_file' % self.__class__.__name__

    # construct file url
        file_url = '%s%s' % (self.file_endpoint, file_route)

    # send request for file data
        data_buffer = self._get_data(file_url, file_name, method_title=title)

        return data_buffer

    def send_message(self, user_id, message_text, message_style='', button_list=None, small_buttons=True, persist_buttons=False, link_preview=True):

        ''' a method to send a message using telegram api

        :param user_id: integer with id of telegram user
        :param message_text: string with message to user
        :param message_style: [optional] string with style to apply to text, only 'markdown'
        :param button_list: [optional] list of string to include as buttons in message
        :param small_buttons: [optional] boolean to resize buttons to single line
        :param persist_buttons: [optional] boolean to keep buttons around after exiting
        :param link_preview: [optional] boolean to open up a preview window of a link in message
        :return: dictionary of response details with message details in [json][result]

        {
            'headers': { ... },
            'url': 'https://api.telegram.org/bot.../sendMessage',
            'code': 200,
            'error': '',
            'json': {
                'ok': True,
                'result': {
                    'chat': {
                        'first_name': 'First',
                        'type': 'private',
                        'id': 1234567890,
                        'last_name': 'Last'
                    },
                    'text': 'text me again',
                    'from': {
                        'first_name': 'my Bot',
                        'id': 987654310,
                        'username': 'myBot'
                    },
                    'message_id': 178,
                    'date': 1478729313
                }
            }
        }
        '''

        title = '%s.send_message' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'user_id': user_id,
            'message_text': message_text,
            'message_style': message_style,
            'button_list': button_list
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct key word arguments
        request_kwargs = {
            'url': '%s/sendMessage' % self.api_endpoint,
            'data': {
                'chat_id': user_id,
                'text': message_text
            }
        }
        if message_style:
            if message_style == 'markdown':
                request_kwargs['data']['parse_mode'] = 'Markdown'
            elif message_style == 'html':
                request_kwargs['data']['parse_mode'] = 'HTML'
        if button_list:
            request_kwargs['data']['reply_markup'] = self._compile_buttons(button_list, small_buttons, persist_buttons)
        # elif keypad_type:
        #     request_kwargs['data']['reply_markup'] = self._compile_keypad(keypad_type, persist_buttons)
        if not link_preview:
            request_kwargs['data']['disable_web_page_preview'] = True

    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details

    def send_photo(self, user_id, photo_id='', photo_path='', photo_url='', caption_text='', button_list=None, small_buttons=True, persist_buttons=False):

        ''' a method to send a photo using telegram api

        :param user_id: integer with id of telegram user
        :param photo_id: [optional] string with id of file stored with telegram api
        :param photo_path: [optional] string with local path to file
        :param photo_url: [optional] string with url of file
        :param caption_text: [optional] string with caption to add to photo
        :return: dictionary of response details with message detail in [json][result]

        {
            'headers': { ... },
            'url': 'https://api.telegram.org/bot.../sendPhoto',
            'code': 200,
            'error': '',
            'json': {
                'ok': True,
                'result': {
                    'chat': {
                        'first_name': 'First',
                        'type': 'private',
                        'id': 1234567890,
                        'last_name': 'Last'
                    },
                    'caption': 'lab logo',
                    'photo': [
                        {
                            'file_id': 'AgADAQ...EC',
                            'width': 51,
                            'file_size': 1238,
                            'height': 90
                        },
                        {
                            'file_id': 'AgADAQ...Ag',
                            'width': 180,
                            'file_size': 13151,
                            'height': 320
                        },
                        {
                            'file_id': 'AgADAQ...VC',
                            'width': 449,
                            'file_size': 51134,
                            'height': 800
                        },
                        {
                            'file_id': 'AgADAQ...AC',
                            'width': 719,
                            'file_size': 82609,
                            'height': 1280
                        }
                    ],
                    'from': {
                        'first_name': 'my Bot',
                        'id': 987654310,
                        'username': 'myBot'
                    },
                    'message_id': 179,
                    'date': 1478729413
                }
            }
        }
        '''

        title = '%s.send_photo' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'user_id': user_id,
            'caption_text': caption_text,
            'photo_id': photo_id,
            'photo_path': photo_path,
            'photo_url': photo_url,
            'button_list': button_list
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct extension map
        extension_map = self.fields.schema['photo_extensions']

    # construct key word arguments
        request_kwargs = {
            'url': '%s/sendPhoto' % self.api_endpoint,
            'data': {
                'chat_id': user_id
            }
        }
        if caption_text:
            request_kwargs['data']['caption'] = caption_text
        if button_list:
            request_kwargs['data']['reply_markup'] = self._compile_buttons(button_list, small_buttons, persist_buttons)

    # add photo to request keywords
        if photo_path:
            import os
            self._validate_type(photo_path, extension_map, title, 'photo_path')
            if not os.path.exists(photo_path):
                raise ValueError('%s is not a valid file path.' % photo_path)
            request_kwargs['files'] = { 'photo': open(photo_path, 'rb') }
        elif photo_id:
            request_kwargs['data']['photo'] = photo_id
        elif photo_url:
            file_extension = self._validate_type(photo_url, extension_map, title, 'photo_url')
            file_buffer = self._get_data(photo_url, 'photo%s' % file_extension, title, 'photo_url')
            request_kwargs['files'] = { 'photo': file_buffer }
        else:
            raise IndexError('%s(...) requires either a photo_path, photo_id or photo_url argument' % title)

    # send request
        response_details = self._post_request(**request_kwargs)

        return response_details

    def send_voice(self, user_id, voice_id='', voice_path='', voice_url='', caption_text='', button_list=None, small_buttons=True, persist_buttons=False):

        return True

if __name__ == '__main__':

    from labpack.records.settings import load_settings, save_settings
    from labpack.handlers.requests import handle_requests
    telegram_config = load_settings('../../../cred/telegram.yaml')
    photo_url = 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
    photo_id = 'AgADAQADsKcxG4RH3Q85DF_-VgGr___A5y8ABVzwsrRBb8xF-wEAAQI'
    photo_path = '../../data/test_photo.png'
    file_path = '../../data/test_voice.ogg'
    update_path = '../../data/telegram-update.json'
    update_id = load_settings(update_path)['last_update']
    bot_id = telegram_config['telegram_bot_id']
    access_token = telegram_config['telegram_access_token']
    user_id = telegram_config['telegram_admin_id']
    telegram_bot = telegramBotClient(bot_id, access_token, requests_handler=handle_requests)
    details = telegram_bot.get_me()
    assert details['json']['result']['id'] == bot_id
    updates_details = telegram_bot.get_updates()
    if updates_details['json']['result']:
        update_list = sorted(updates_details['json']['result'], key=lambda k: k['update_id'])
        offset_details = { 'last_update': update_list[-1]['update_id']}
        save_settings(offset_details, update_path, overwrite=True)
    # details = telegram_bot.send_message(user_id, 'text me again')
    # details = telegram_bot.send_photo(user_id, photo_url=photo_url, caption_text='Lab Logo')
    # details = telegram_bot.send_photo(user_id, photo_id=photo_id)
    # details = telegram_bot.send_photo(user_id, photo_path=photo_path)
    # details = telegram_bot.send_message(user_id, '*Select a Number:*\n\t_1_\n\t\t`2`\n\t\t\t[3](http://collectiveacuity.com)', message_style='markdown')
    # details = telegram_bot.send_message(user_id, 'Select a Number:', button_list=['1','2','3'])
    # details = telegram_bot.send_message(user_id, 'Select a Letter:', button_list=['ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF'], small_buttons=False, persist_buttons=True)
    file_id = 'AwADAQADAwADXGbcCxP7_eEhVMEeAg'
    details = telegram_bot.get_route(file_id)
    file_route = details['json']['result']['file_path']
    file_buffer = telegram_bot.get_file(file_route, file_name='test_voice')
    file_data = file_buffer.getvalue()
    file_name = file_buffer.name
    from labpack.parsing.magic import labMagic
    lab_magic = labMagic('../../data/magic.mgc')
    file_details = lab_magic.analyze(byte_data=file_data)
    save_path = '../../data/%s%s' % (file_name, file_details['extension'])
    with open(save_path, 'wb') as f:
        f.write(file_data)
        f.close()
