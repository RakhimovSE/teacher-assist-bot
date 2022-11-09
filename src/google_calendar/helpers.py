import re


def is_match(text: str, pattern=r'^[A-Za-z_][0-9A-Za-z_]*$'):
    """Check if variable has proper naming convention"""
    return bool(re.search(pattern, text))
