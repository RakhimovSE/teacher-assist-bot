from typing import Union
import re
from datetime import date, datetime


def is_match(text: str, pattern=r'^[A-Za-z_][0-9A-Za-z_]*$'):
    """Check if variable has proper naming convention"""
    return bool(re.search(pattern, text))


def replace_tz(dt: Union[date, datetime], tz):
    dt_with_tz = (
        dt
        if type(dt) == datetime
        else datetime.combine(dt, datetime.min.time())
    )
    return dt_with_tz.replace(tzinfo=None).astimezone(tz)
