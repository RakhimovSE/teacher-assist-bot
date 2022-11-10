from datetime import datetime

import pytz
from babel.dates import get_timezone_location, format_date, format_time, format_timedelta
from gcsa.event import Event as BaseEvent

from src.google_calendar.helpers import is_match, replace_tz


class Event(BaseEvent):
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.init()

    def init(self):
        self.args = self.__get_args()
        self.locale = 'ru' if self.args.get('locale', 'ru') else 'en'
        self.is_informal = self.args.get('appeal') == 'informal'
        self.tz = pytz.timezone(self.timezone)

    def __get_args(self):
        args = {}
        lines = (self.description or '').split('\n')
        for line in lines:
            parts = line.split('=')
            if len(parts) == 2 and is_match(parts[0]):
                args[parts[0]] = parts[1]
        return args

    @property
    def is_upcoming(self):
        start_dt = replace_tz(self.start, self.tz)
        return (start_dt - datetime.now(tz=self.tz)).total_seconds() > 0

    def get_reminder_text(self):
        start_dt = replace_tz(self.start, self.tz)
        now = datetime.now(tz=pytz.utc)
        day = format_timedelta(
            start_dt - now,
            granularity='minute',
            add_direction=True,
            locale=self.locale
        )
        date = format_date(start_dt, format='d MMMM', locale=self.locale)
        time = format_time(start_dt, format='short', locale=self.locale)
        tz_city = get_timezone_location(start_dt, locale=self.locale, return_city=True)
        lines = [
            'Привет!' if self.is_informal else 'Добрый день!',
            f'У нас по плану занятие {day} ({date} в {time}, время {tz_city})',
            'Всё в силе?',
        ]
        return '\n'.join(lines)
