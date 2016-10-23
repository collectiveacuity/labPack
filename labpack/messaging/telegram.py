__author__ = 'rcj1492'
__created__ = '2016.09'
__license__ = 'MIT'

'''
    classes to interact with telegram bot api
    https://core.telegram.org/bots/api

    python module for bot api
    https://github.com/luckydonald/pytgbot

    python wrapper for telegram cli
    https://github.com/luckydonald/pytg

    telegram cli
    https://github.com/vysheng/tg
'''

import io
import os
import requests
from jsonmodel.validators import jsonModel
from labpack.parsing.regex import labRegex

class TelegramConnectionError(Exception):

    def __init__(self, message='', error_dict=None):

    # TODO create bad connection diagnostics methods

        text = '\nFailure connecting to Telegram Bot API with %s request.' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                self.error = error_dict
        super(TelegramConnectionError, self).__init__(text)

class telegramBotClient(object):

    _class_methods = {
        'schema': {
            '__init__': {
                'bot_settings': {
                    'commands': {
                        'start': '',
                        'help': '',
                        'settings': ''
                    },
                    'first_name': 'Telegram',
                    'id': 123456789,
                    'username': 'TelegramBot',
                    'callback_url': '',
                    'description': '',
                    'about_text': '',
                    'user_pic': ''
                },
                'telegram_credentials': {
                    'access_token': '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
                }
            },
            'request': {
                'bot_method': 'getMe'
            },
            'getMe': {},
            'getUpdates': {
                'offset': 0,
                'limit': 0,
                'timeout': 0
            },
            'setWebhook': {
                'url': '',
                'certificate': ''
            },
            'sendMessage': {
                'chat_id': 123456,
                'text': 'text me again',
                'parse_mode': '',
                'disable_web_page_preview': False,
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'sendPhoto': {
                'chat_id': 123456,
                'photo': 'AgADAQADqqcIlRwG3Q-cUsx5sAQADqT5y8BAAEgpr3t_b1ajggpr3I4C',
                'caption': '',
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'forwardMessage': {
                'chat_id': 123456,
                'from_chat_id': 234567,
                'disable_notification': False,
                'message_id': 567890212
            },
            'sendAudio': {
                'chat_id': 123456,
                'audio': '../data/audio.mp3',
                'caption': '',
                'duration': 0,
                'performer': '',
                'title': '',
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'sendDocument': {
                'chat_id': 123456,
                'document': 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png',
                'caption': '',
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'sendSticker': {
                'chat_id': 123456,
                'document': 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.webp',
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'sendVideo': {
                'chat_id': 123456,
                'video': '../data/video.mp4',
                'caption': '',
                'duration': 0,
                'width': 0,
                'height': 0,
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'sendVoice': {
                'chat_id': 123456,
                'voice': '../data/voice.ogg',
                'caption': '',
                'duration': 0,
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            },
            'sendLocation': {
                'chat_id': 123456,
                'latitude': 45.8742031,
                'longitude': 34.9874612,
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            }
        },
        'components': {
            '.__init__.telegram_credentials': {
                'extra_fields': True
            },
            '.setWebhook': {
                'field_metadata': {
                    'file_type': 'certificate',
                    'file_extensions': {
                        'pem': '.+\\.pem$'
                    }
                }
            },
            '.sendMessage.parse_mode': {
                'discrete_values': [ 'Markdown', 'HTML' ]
            },
            '.sendPhoto': {
                'field_metadata': {
                    'file_type': 'photo',
                    'file_extensions': {
                        'jpg': '.+\\.jpg$',
                        'jpeg': '.+\\.jpeg$',
                        'gif': '.+\\.gif$',
                        'png': '.+\\.png$',
                        'tif': '.+\\.tif$',
                        'bmp': '.+\\.bmp$'
                    }
                }
            },
            '.sendPhoto.caption': {
                'max_length': 200
            },
            '.sendAudio': {
                'field_metadata': {
                    'file_type': 'audio',
                    'file_extensions': {
                        'mp3': '.+\\.mp3$'
                    },
                    'file_size': 50000000
                }
            },
            '.sendAudio.caption': {
                'max_length': 200
            },
            '.sendDocument': {
                'field_metadata': {
                    'file_type': 'document',
                    'file_extensions': {
                        'doc': '.+\\.docx?$'
                    },
                    'file_size': 50000000
                }
            },
            '.sendDocument.caption': {
                'max_length': 200
            },
            '.sendSticker': {
                'field_metadata': {
                    'file_type': 'sticker',
                    'file_extensions': {
                        'webp': '.+\\.webp$'
                    }
                }
            },
            '.sendVideo': {
                'field_metadata': {
                    'file_type': 'video',
                    'file_extensions': {
                        'mp4': '.+\\.mp4$'
                    },
                    'file_size': 50000000
                }
            },
            '.sendVideo.caption': {
                'max_length': 200
            },
            '.sendVoice': {
                'field_metadata': {
                    'file_type': 'voice',
                    'file_extensions': {
                        'ogg': '.+\\.ogg$'
                    },
                    'file_size': 50000000
                }
            },
            '.sendVoice.caption': {
                'max_length': 200
            }
        }
    }

    def __init__(self, bot_settings, telegram_credentials):

    # construct input validation method
        self.fields = jsonModel(self._class_methods)

    # construct file extensions map method
        file_extensions = {}
        for key, value in self.fields.keyMap.items():
            if 'field_metadata' in value.keys():
                meta_data = value['field_metadata']
                if 'file_type' in meta_data.keys() and 'file_extensions' in meta_data.keys():
                    if meta_data['file_type'] and meta_data['file_extensions']:
                        file_extensions[meta_data['file_type']] = labRegex(meta_data['file_extensions'])
        self.ext =  file_extensions

    # construct file source map method
        file_patterns = {
            'file_id': '[\\w-]{52}',
            'file_url': '^https?://',
            'file_path': '\\.'
        }
        self.sources = labRegex(file_patterns)

    # validate inputs
        # bot_settings = self.fields.validate(bot_settings, '.__init__.bot_settings')
        telegram_credentials = self.fields.validate(telegram_credentials, '.__init__.telegram_credentials')

    # construct core methods
        self.accessToken = telegram_credentials['access_token']
        self.endpoint = 'https://api.telegram.org/bot'

    def setup(self):

        botfather_url = 'https://web.telegram.org/#/im?p=@BotFather'
        setup_sequence = [
            'tg://bot_command?command=start',
            'tg://bot_command?command=newbot&bot=BotFather',
            'message with name',
            'message with username',
            'tg://bot_command?command=cancel&bot=BotFather'
        ]

        auth_token = ''

        return self

    def update(self):

        return self

    def parseSource(self, file_string):

        file_source = ''

        file_map = self.sources.map(file_string)[0]
        if file_map['file_url']:
            file_source = 'file_url'
        elif file_map['file_id']:
            file_source = 'file_id'
        elif file_map['file_path']:
            file_source = 'file_path'

        return file_source

    def request(self, bot_method, **kwargs):

        '''
            a method to make a post request to the telegram bot api

        :param bot_method: string with bot method name
        :param **kwargs: additional keyword arguments for bot method
        :return: (json valid) dictionary with response (or error)

        bot methods:
        https://core.telegram.org/bots/api#making-requests

        requests documentation:
        https://requests.readthedocs.io/en/master/user/quickstart/
        '''

        title = '%s.request' % self.__class__.__name__

    # validate inputs
        if bot_method not in self.fields.schema.keys():
            raise ValueError('%s(bot_method=%s) is not a valid telegram api method.' % (title, bot_method))

    # construct post request key word arguments
        request_kwargs = {
            'url': '%s%s/%s' % (self.endpoint, self.accessToken, bot_method),
            'data': {}
        }
        method_key = '.' + bot_method

    # validate keyword arguments
        data_kwargs = {}
        for key, value in kwargs.items():
            argument_key = '%s.%s' % (method_key, key)
            if argument_key in self.fields.keyMap.keys():
                object_title = '%s(%s=%s)' % (title, key, value)
                data_kwargs[key] = self.fields.validate(value, argument_key, object_title)

    # validate requirements
        object_title = '%s(bot_method=%s, **kwargs)' % (title, bot_method)
        self.fields.validate(data_kwargs, method_key, object_title)

    # add keywords to request kwargs
        if data_kwargs:
            request_kwargs['data'] = data_kwargs

    # retrieve file type from arguments
        file_type = ''
        file_value = ''
        for key in self.ext.keys():
            if key in request_kwargs['data'].keys():
                file_type = key
                file_value = request_kwargs['data'][key]
                del request_kwargs['data'][key]

    # add file to request kwargs
        if file_type:
            file_field = self.parseSource(file_value)
            if file_field == 'file_id':
                request_kwargs['data'][file_type] = file_value
            elif file_field == 'file_path':
                if not os.path.exists(file_value):
                    raise ValueError('%s(%s=%s) is not a valid file path.' % (title, file_type, file_value))
                request_kwargs['files'] = { file_type: open(file_value, 'rb') }
            elif file_field == 'file_url':
                file_extension = ''
                try:
                    remote_file = requests.get(file_value)
                except:
                    raise ValueError('%s(%s=%s) is not a valid url.' % (title, file_type, file_value))
                file_mapping = self.ext[file_type].map(file_value)[0]
                extension_list = []
                for key, value in file_mapping.items():
                    if isinstance(value, bool):
                        extension_list.append('.' % key)
                    if value and isinstance(value, bool):
                        file_extension = '.' + key
                if not file_extension:
                    raise ValueError('%s(%s=%s) must be one of %s file types.' % (title, file_type, file_value, extension_list))
                file_buffer = io.BytesIO(remote_file.content)
                file_buffer.name = '%s%s' % (file_type, file_extension)
                request_kwargs['files'] = { file_type: file_buffer }
            else:
                raise IndexError('%s(bot_method=%s) requires a "%s" argument.' % (title, bot_method, file_type))

    # remove data from request if empty
        if not request_kwargs['data']:
            del request_kwargs['data']

    # send request
        try:
            response = requests.post(**request_kwargs)
        except:
            raise TelegramConnectionError('%s requests.post(%s)' % (title, bot_method), error_dict=request_kwargs)

    # unwrap and return json response
        response_dict = response.json()

        return response_dict