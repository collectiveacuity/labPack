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

    _class_fields = {
        'schema': {
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
            },
            'bot_method': 'getMe',
            'method_kwargs': {},
            'file_id': 'AgADAQADqqcIlRwG3Q-cUsx5sAQADqT5y8BAAEgpr3t_b1ajggpr3I4C',
            'file_path': '../../data/test_file.png',
            'file_url': 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
        },
        'components': {
            '.telegram_credentials': {
                'extra_fields': True
            }
        }
    }

    _bot_methods = {
        'schema': {
            'sendPhoto': {
                'chat_id': 0,
                'photo': '',
                'caption': '',
                'disable_notification': False,
                'reply_to_message_id': 0,
                'reply_markup': {}
            }
        },
        'components': {
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
            }
        }
    }

    def __init__(self, bot_settings, telegram_credentials):

    # construct input validation method
        self.fields = jsonModel(self._class_fields)
        self.botMethods = jsonModel(self._bot_methods)

    # construct sub method generator
        file_extensions = {}
        for key, value in self.botMethods.keyMap.items():
            if 'field_metadata' in value.keys():
                meta_data = value['field_metadata']
                if 'file_type' in meta_data.keys() and 'file_extensions' in meta_data.keys():
                    file_extensions[meta_data['file_type']] = labRegex(meta_data['file_extensions'])
        self.ext =  file_extensions

    # validate inputs
        # bot_settings = self.fields.validate(bot_settings, '.bot_settings')
        telegram_credentials = self.fields.validate(telegram_credentials, '.telegram_credentials')

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

    def request(self, bot_method, method_kwargs=None, file_id='', file_path='', file_url=''):

        '''
            a method to make a post request to the telegram bot api

        :param bot_method: string with bot method name
        :param method_kwargs: dictionary with method keyword arguments
        :param file_id: string with telegram file id to use for method
        :param file_path: string with path to file located on localhost
        :param file_url: string with url address of file
        :return: (json valid) dictionary with response (or error)

        bot methods:
        https://core.telegram.org/bots/api#making-requests

        requests documentation:
        https://requests.readthedocs.io/en/master/user/quickstart/
        '''

        title = '%s.request' % self.__class__.__name__

    # validate inputs
        input_kwargs = [bot_method, method_kwargs, file_id, file_path, file_url]
        input_names = ['.bot_method', '.method_kwargs', '.file_id', '.file_path', '.file_url']
        for i in range(len(input_kwargs)):
            if input_kwargs[i]:
                self.fields.validate(input_kwargs[i], input_names[i])

    # construct post request key word arguments
        request_kwargs = {
            'url': '%s%s/%s' % (self.endpoint, self.accessToken, bot_method)
        }

    # add method arguments to request fields
        if method_kwargs:
            request_kwargs['data'] = method_kwargs

    # TODO add method kwargs validation from api documentation

    # retrieve file type for method
        file_type = ''
        component_key = '.' + bot_method
        component_criteria = self.botMethods.keyMap[component_key]
        if 'field_metadata' in component_criteria.keys():
            if 'file_type' in component_criteria['field_metadata'].keys():
                file_type = component_criteria['field_metadata']['file_type']

    # add file to request kwargs
        if file_type:
            if file_id:
                request_kwargs['data'][file_type] = file_id
            elif file_path:
                if not os.path.exists(file_path):
                    raise Exception('%s(file_path=%s}) is not a valid file path.' % (title,file_path))
                request_kwargs['files'] = { file_type: open(file_path, 'rb') }
            elif file_url:
                file_extension = ''
                remote_file = requests.get(file_url)
                file_mapping = self.ext[file_type].map(file_url)[0]
                for key, value in file_mapping.items():
                    if value and isinstance(value, bool):
                        file_extension = '.' + key
                file_buffer = io.BytesIO(remote_file.content)
                file_buffer.name = '%s%s' % (file_type, file_extension)
                request_kwargs['files'] = { file_type: file_buffer }

    # send request
        try:
            response = requests.post(**request_kwargs)
        except:
            raise TelegramConnectionError('%s requests.post()' % title, error_dict=request_kwargs)

    # unwrap and return json response
        json_dict = response.json()

        return json_dict

if __name__ == '__main__':
    from cred.credentialsTelegram import telegramCredentials, photoLists
    user_id = telegramCredentials['admin_id']
    bot_id = telegramCredentials['bot_id']
    photo_path = '../../data/test_file.png'
    photo_url = 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
    bot_settings = {
        'commands': {
            'start': '',
            'help': '',
            'settings': ''
        },
        'first_name': telegramCredentials['bot_name'],
        'id': telegramCredentials['bot_id'],
        'username': telegramCredentials['bot_username']
    }
    request_list = [
        { 'bot_method': 'getMe' },
        { 'bot_method': 'getUpdates', 'method_kwargs': { 'offset': 135205444 } },
        { 'bot_method': 'sendMessage', 'method_kwargs': { 'chat_id': user_id, 'text': 'text me again' } },
        { 'bot_method': 'sendPhoto', 'method_kwargs': { 'chat_id': user_id },
          'file_path': photo_path },
        { 'bot_method': 'sendPhoto', 'method_kwargs': { 'chat_id': user_id },
          'file_id': photoLists[0]['file_id'] },
        { 'bot_method': 'sendPhoto', 'method_kwargs': { 'chat_id': user_id },
          'file_url': photo_url },
    ]

    bot = telegramBotClient(bot_settings=bot_settings, telegram_credentials=telegramCredentials)
    response = bot.request(**request_list[5])
    print(response)
