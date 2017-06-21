__author__ = 'rcj1492'
__created__ = '2016.09'
__license__ = 'MIT'

from labpack.messaging.telegram import telegramBotClient

class testTelegramBotClient(telegramBotClient):

    def __init__(self, bot_settings, telegram_credentials):
        telegramBotClient.__init__(self, bot_settings, telegram_credentials)

    def unitTests(self):

        from cred.credentialsTelegram import photoLists
        user_id = telegramCredentials['admin_id']
        photo_path = '../data/test_file.png'
        photo_url = 'https://pbs.twimg.com/profile_images/479475632158408704/Zelyz-xr_400x400.png'
        photo_id = photoLists[0]['file_id']
        request_list = [
            {'bot_method': 'getMe'},
            {'bot_method': 'getUpdates', 'offset': 135205444},
            {'bot_method': 'sendMessage', 'chat_id': user_id, 'text': 'text me again' },
            {'bot_method': 'sendPhoto', 'chat_id': user_id, 'photo': photo_path},
            {'bot_method': 'sendPhoto', 'chat_id': user_id, 'photo': photo_id },
            {'bot_method': 'sendPhoto', 'chat_id': user_id, 'photo': photo_url},
        ]
        command_list = {
            'sendPhoto': {'chat_id': user_id, 'file_url': photo_url}
        }
        response = bot.request(**request_list[2])
        print(response)
        # response = bot.sendPhoto(**command_list['sendPhoto'])
        # print(response)

        return self

if __name__ == '__main__':
    from cred.credentialsTelegram import telegramCredentials
    bot_settings = { 'id': telegramCredentials['bot_id'] }
    bot = testTelegramBotClient(bot_settings, telegramCredentials)
    bot.unitTests()