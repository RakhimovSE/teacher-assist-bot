import asyncio

from telethon import TelegramClient as BaseTelegramClient
from dotenv import dotenv_values

from src.google_calendar import GoogleCalendar, Event

env = dotenv_values()


class TelegramClient(BaseTelegramClient):
    def __init__(self, calendar: GoogleCalendar, *args, **kwargs):
        kwargs['session'] = kwargs.get('session', 'src/telegram/sessions/teacher-assist')
        kwargs['api_id'] = kwargs.get('api_id', env['TG_CLIENT_API_ID'])
        kwargs['api_hash'] = kwargs.get('api_hash', env['TG_CLIENT_API_HASH'])
        super(TelegramClient, self).__init__(*args, **kwargs)
        self.calendar = calendar

    async def send_event_reminders(self):
        return [
            message
            for message in await asyncio.gather(
                *map(self.send_event_reminder, self.calendar.events)
            )
            if message is not None
        ]

    async def send_event_reminder(self, event: Event):
        try:
            return await self.send_message(
                int(event.args['telegram_id']),
                event.get_reminder_text()
            )
        except:
            return None
