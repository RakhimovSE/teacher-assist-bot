import re
from datetime import datetime

import pytz
from babel.dates import get_timezone_location, format_date, format_time, format_timedelta

from gcsa.event import Event


def is_match(text, pattern=r'^[A-Za-z_][0-9A-Za-z_]*$'):
    """Check if variable has proper naming convention"""
    return bool(re.search(pattern, text))


def get_args(event: Event):
    args = {}
    lines = (event.description or '').split('\n')
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2 and is_match(parts[0]):
            args[parts[0]] = parts[1]
    return args


def get_reminder_text(event: Event, locale='ru_RU', is_formal=True):
    event_tz = pytz.timezone(event.timezone)
    start_dt = event.start.replace(tzinfo=None).astimezone(event_tz)
    now = datetime.now(tz=event_tz)
    day = format_timedelta(start_dt - now, add_direction=True, locale=locale)
    date = format_date(start_dt, format='d MMMM', locale=locale)
    time = format_time(start_dt, format='short', locale=locale)
    tz_city = get_timezone_location(event_tz, locale=locale, return_city=True)
    lines = [
        'Добрый день!' if is_formal else 'Привет!',
        f'У нас по плану занятие {day} ({date} в {time}, время {tz_city})',
        'Всё в силе?',
    ]
    return '\n'.join(lines)
