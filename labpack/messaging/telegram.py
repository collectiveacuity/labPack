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

import io
import os
import requests
from jsonmodel.validators import jsonModel
from labpack.parsing.regex import labRegex

def validate_type(file_name, extension_map):

    title = 'validate_type'

# validate file extension
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
        raise ValueError('%s(file_name=%s) must be one of %s file types.' % (title, file_name, extension_list))

    return file_extension

def get_file(file_url, file_name=''):

    title = 'get_file'

# request file from url
    try:
        remote_file = requests.get(file_url)
    except:
        raise ValueError('%s(%s=%s) is not a valid url.' % (title, file_url, file_url))
    if not file_name:
        file_name = 'file'

# add contents to buffer
    import io
    file_buffer = io.BytesIO(remote_file.content)
    file_buffer.name = '%s' % file_name

    return file_buffer

def load_offset(file_path):

    record_details = {
        'last_update': 0
    }

    from labpack.records.settings import load_settings
    record_details = load_settings(file_path)

    return record_details['last_update']

def save_offset(update_value, file_path):

    if not isinstance(update_value, int):
        raise ValueError('Update value must be an integer')

    record_details = {
        'last_update': update_value
    }

    from labpack.records.settings import save_settings
    return_path = save_settings(record_details, file_path, overwrite=True)

    return return_path

def get_me(bot_id, access_token):

# construct key word arguments
    request_kwargs = {
        'url': 'https://api.telegram.org/bot%s:%s/getMe' % (bot_id, access_token),
    }

# send get update request
    response_object = requests.post(**request_kwargs)
    response = response_object.json()

    return response

def get_updates(bot_id, access_token, last_update=0):

# construct key word arguments
    request_kwargs = {
        'url': 'https://api.telegram.org/bot%s:%s/getUpdates' % (bot_id, access_token),
    }

# add offset to kwargs
    if last_update:
        request_kwargs['data'] = {
            'offset': last_update + 1
        }

# send get update request
    response_object = requests.post(**request_kwargs)
    response = response_object.json()

# construct update list
    update_list = []
    if response['result']:
        for i in range(len(response['result'])):
            update_list.append(response['result'][i])

    return update_list

def send_message(bot_id, access_token, user_id, message_text):

# construct key word arguments
    request_kwargs = {
        'url': 'https://api.telegram.org/bot%s:%s/sendMessage' % (bot_id, access_token),
        'data': {
            'chat_id': user_id,
            'text': message_text
        }
    }

# send message
    response = requests.post(**request_kwargs)

    return response.json()

def send_photo(bot_id, access_token, user_id, photo_path='', photo_id='', photo_url='', caption_text=''):

    title = 'send_photo'

# construct valid file extensions
    extension_map = {
        'jpg': '.+\\.jpg$',
        'jpeg': '.+\\.jpeg$',
        'gif': '.+\\.gif$',
        'png': '.+\\.png$',
        'tif': '.+\\.tif$',
        'bmp': '.+\\.bmp$'
    }

# construct key word arguments
    request_kwargs = {
        'url': 'https://api.telegram.org/bot%s:%s/sendPhoto' % (bot_id, access_token),
        'data': {
            'chat_id': user_id
        }
    }
    if caption_text:
        request_kwargs['data']['caption'] = caption_text

# add photo to request keywords
    if photo_path:
        validate_type(photo_path, extension_map)
        if not os.path.exists(photo_path):
            raise ValueError('%s is not a valid file path.' % photo_path)
        request_kwargs['files'] = { 'photo': open(photo_path, 'rb') }
    elif photo_id:
        request_kwargs['data']['photo'] = photo_id
    elif photo_url:
        file_extension = validate_type(photo_url, extension_map)
        file_buffer = get_file(photo_url, 'photo%s' % file_extension)
        request_kwargs['files'] = { 'photo': file_buffer }
    else:
        raise IndexError('%s(...) requires either a photo_path, photo_id or photo_url argument' % title)

# send welcome message
    response = requests.post(**request_kwargs)

    return response.json()

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

class telegramBotHandler(object):

    def __init__(self):
        pass

    def handle(self, response):

    # construct default response details
        details = {
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers
        }

    # handle different codes
        if details['code'] == 200:
            details['json'] = response.json()
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
            'bot_id': 0,
            'access_token': '',
            'last_update': 0,
            'user_id': 0,
            'user_name': ''
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
        self.endpoint = '%s%s:%s' % (self.fields.schema['api_endpoint'], self.bot_id, self.access_token)

    # construct handlers
        self.requests_handler = requests_handler
        self.telegram_handler = telegramBotHandler()

    def _post_request(self, url, json=None):

        import requests

    # construct request fields
        request_kwargs = {
            'url': url
        }
        if json:
            request_kwargs['json'] = json

    # send request
        try:
            response = requests.post(**request_kwargs)
        except Exception as err:
            if self.requests_handler:
                return self.requests_handler(err)
            else:
                raise

    # handle response
        response_details = response.json()

        return response_details

    def get_me(self):

    # construct request fields
        url = '%s/getMe' % self.endpoint

    # send request
        bot_details = self._post_request(url)

        return bot_details

    def get_updates(self, last_update=0):

        title = '%s.get_updates' % self.__class__.__name__

    # construct request fields
        request_kwargs = {
            'url': '%s/getUpdates' % self.endpoint
        }

    # add offset to kwargs
        if last_update:
            object_title = '%s(last_update=%s)' % (title, str(last_update))
            self.fields.validate(last_update, '.last_update', object_title)
            request_kwargs['data'] = {
                'offset': last_update + 1
            }

    # send request
        response_details = requests.post(**request_kwargs)

    # construct update list
        update_list = []
        if response['result']:
            for i in range(len(response['result'])):
                update_list.append(response['result'][i])

        return update_list

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

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    telegram_cred = load_settings('../../../cred/telegram.yaml')
    bot_id = telegram_cred['telegram_bot_id']
    access_token = telegram_cred['telegram_access_token']
    telegram_bot = telegramBotClient(bot_id, access_token)
    bot_details = telegram_bot.get_me()
    print(bot_details)
    # assert get_me(bot_id, access_token)['result']
    # update_list = get_updates(bot_id, access_token)
    # if update_list:
    #     user_id = update_list[0]['message']['from']['id']
    #     photo_url = 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
    #     # send_photo(bot_id, access_token, user_id, photo_url=photo_url)
