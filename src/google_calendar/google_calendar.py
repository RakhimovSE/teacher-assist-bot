from datetime import datetime, timedelta

import pytz
from gcsa.google_calendar import GoogleCalendar as BaseGoogleCalendar
from dotenv import dotenv_values

from src.google_calendar.event import Event

env = dotenv_values()


class GoogleCalendar(BaseGoogleCalendar):
    def __init__(self, *args, **kwargs):
        kwargs['default_calendar'] = kwargs.get('default_calendar', env['GCAL_ID'])
        kwargs['credentials_path'] = kwargs.get('credentials_path', 'src/google_calendar/credentials/credentials.json')
        kwargs['read_only'] = kwargs.get('read_only', True)
        super(GoogleCalendar, self).__init__(*args, **kwargs)

    @property
    def events(self):
        today = datetime.now(tz=pytz.utc)
        tomorrow = today + timedelta(days=1)
        events = []
        for base_event in self[today:tomorrow:'startTime']:
            event: Event = base_event
            event.__class__ = Event
            event.init()
            if event.is_upcoming:
                events.append(event)
        return events
