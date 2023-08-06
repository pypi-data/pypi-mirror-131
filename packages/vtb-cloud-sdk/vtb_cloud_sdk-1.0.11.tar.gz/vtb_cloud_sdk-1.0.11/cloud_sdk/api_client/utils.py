import collections
from typing import Union

import pytz
from datetime import datetime, date


# noinspection PyPep8Naming
def datetime_to_str(dt: Union[datetime, date, str], microseconds=False, timezone=False) -> str:
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DATETIME_FORMAT_MS = "%Y-%m-%dT%H:%M:%S.%f"

    if isinstance(dt, datetime):
        if not microseconds:
            dt = dt.replace(microsecond=0)
        if dt.tzinfo:
            dt = dt.replace(tzinfo=pytz.utc)
        fmt = DATETIME_FORMAT_MS if microseconds else DATETIME_FORMAT
        if timezone:
            fmt += "%z"
        return dt.strftime(fmt)
    elif isinstance(dt, date):
        return dt.isoformat()

    return dt


def make_list(value, delimiter=','):
    if isinstance(value, str):
        return value
    if isinstance(value, collections.Iterable):
        return delimiter.join(value)
    return value


def parse_date(value):
    import dateutil.parser

    if value is not None:
        value = dateutil.parser.parse(value).replace(tzinfo=dateutil.tz.tzutc())
    return value
