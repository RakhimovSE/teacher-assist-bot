import re

from gcsa.event import Event


def is_match(text, pattern=r'^[A-Za-z_][0-9A-Za-z_]*$'):
    """Check if variable has proper naming convention"""
    return bool(re.search(pattern, text))


def get_event_args(event: Event):
    args = {}
    lines = (event.description or '').split('\n')
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2 and is_match(parts[0]):
            args[parts[0]] = parts[1]
    return args
