'''
Utility functions.
'''

from datetime import datetime, timezone


def timezone_aware(date: datetime) -> datetime:
    '''
    Convert naive to timezone-aware datetime (UTC timezone).

    Parameters:
        date (datetime): Datetime object.
    Returns:
        datetime: A timezone-aware datetime.
    '''

    return date.replace(tzinfo=timezone.utc) if date.tzinfo is None else date


__all__ = [
    'timezone_aware'
]
