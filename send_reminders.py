from src.telegram import TelegramClient
from src.google_calendar import GoogleCalendar


if __name__ == '__main__':
    client = TelegramClient(GoogleCalendar())
    with client:
        client.loop.run_until_complete(client.send_event_reminders())
