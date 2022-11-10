from telethon import TelegramClient as BaseTelegramClient

from dotenv import dotenv_values

env = dotenv_values()


class TelegramClient(BaseTelegramClient):
    def __init__(self, *args, **kwargs):
        kwargs['session'] = kwargs.get('session', 'src/telegram/sessions/teacher-assist')
        kwargs['api_id'] = kwargs.get('api_id', env['TG_CLIENT_API_ID'])
        kwargs['api_hash'] = kwargs.get('api_hash', env['TG_CLIENT_API_HASH'])
        super(TelegramClient, self).__init__(*args, **kwargs)
