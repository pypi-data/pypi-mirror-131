"""
Date & time utility library

The main assumption is to operate only on tz-aware datetime objects,
provide tools for easy conversion from naive to aware, and operate
on standard `datetime` objects for compatibility reasons.

Arrow library proposed as a replacement for `times` is very good,
especially for chain processing, but have one main disadvantage - Arrow
objects are not compatible with datetimes and can't be used directly.
There is necessary a one or two conversion steps, from datetime to Arrow
and in opposite way to achieve full compatibility.

There is a still room for a library that will manipulate on datetime
objects.

---

This is a library based of `times` package, which is already discontinued.
"""

import calendar
import datetime
import sys
import time
import six

import arrow
import dateutil.parser
import pytz

from .version import VERSION

PY3 = sys.version_info[0] == 3
if PY3:
    string_types = str
else:
    string_types = basestring


__author__ = "Vincent Driessen <vincent@3rdcloud.com>"
__author__ = "Marcin Nowak <marcin.j.nowak@gmail.com>"
__version__ = VERSION


def local_tzname():
    """
    Returns name of local timezone
    """
    return time.tzname[0]


def local_tz():
    """
    Returns local timezone instance
    """
    return pytz.timezone(local_tzname())


def to_universal(local_dt, timezone=None):
    """
    Converts the given datetime or UNIX timestamp to a universal
    datetime, assuming that naive datetimes are stored in UTC.
    Additional timezone argument is used to properly convert naive local_dt.
    """
    if isinstance(local_dt, (int, float)):
        if timezone is not None:
            raise ValueError("Timezone argument illegal when using UNIX timestamps.")
        return from_unix(local_dt)
    elif isinstance(local_dt, string_types):
        local_dt = arrow.get(local_dt).to("UTC").naive
    return from_local(local_dt, timezone)


def from_local(local_dt, timezone=None):
    """Converts the given local datetime to a universal datetime."""
    if not isinstance(local_dt, datetime.datetime):
        raise TypeError("Expected a datetime object")

    if local_dt.tzinfo:
        return local_dt.astimezone(pytz.utc)
    else:
        timezone = timezone or local_tzname()
        return make_aware(local_dt, timezone).astimezone(pytz.utc)


def from_unix(ut):
    """
    Converts a UNIX timestamp, as returned by `time.time()`, to universal
    time.  Assumes the input is in UTC, as `time.time()` does.
    """
    if not isinstance(ut, (int, float)):
        raise TypeError("Expected an int or float value")

    return datetime.datetime.utcfromtimestamp(ut).replace(tzinfo=pytz.utc)


def to_local(dt, timezone):
    """Converts universal datetime to a local representation in given timezone."""
    return make_aware(dt).astimezone(pytz.timezone(timezone))


def to_unix(dt):
    """Converts a datetime object to unixtime"""
    if not isinstance(dt, datetime.datetime):
        raise TypeError("Expected a datetime object")

    return arrow.get(dt).timestamp


def format(dt, timezone, fmt=None):
    """Formats the given universal time for display in the given time zone."""
    local = to_local(dt, timezone)
    if fmt is None:
        return local.isoformat()
    else:
        return local.strftime(fmt)


def now(tz=None, align=None):
    """
    Return tz-aware datetime objects that represents `now()`
    in specified timezone (UTC as default).

    Datetime may be aligned (truncated) to: second, minute, hour, day, month,
    year. (see DateTimeTruncator for details)
    """

    dt = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    if align:

        def truncate_func(x):
            return datetime_truncator.truncate(x, align)

    else:

        def truncate_func(x):
            return x

    if tz:
        try:
            return truncate_func(dt.astimezone(tz))
        except TypeError:
            return truncate_func(dt.astimezone(pytz.timezone(tz)))
    else:
        return truncate_func(dt)


def total_seconds(td):
    """
    Wrapper for timedelta.total_seconds() which is missing in Python 2.6
    Compatible with 2.7+
    """
    try:
        return td.total_seconds()
    except AttributeError:
        return (
            td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6
        ) / 10 ** 6


def make_aware(dt, tz=None):
    """
    Convert naive datetime object to tz-aware
    """
    if tz:
        if isinstance(tz, six.string_types):
            tz = pytz.timezone(tz)
    else:
        tz = pytz.utc
    if dt.tzinfo:
        return dt.astimezone(dt.tzinfo)
    else:
        return tz.localize(dt)


def make_naive(dt, tz=None):
    if tz:
        if isinstance(tz, six.string_types):
            tz = pytz.timezone(tz)
    else:
        tz = pytz.utc
    return dt.astimezone(tz).replace(tzinfo=None)


class DateTimeTruncator(object):
    def __init__(self):
        self.parts = {
            "year": lambda x: x.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            ),
            "month": lambda x: x.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            ),
            "day": lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0),
            "hour": lambda x: x.replace(minute=0, second=0, microsecond=0),
            "minute": lambda x: x.replace(second=0, microsecond=0),
            "second": lambda x: x.replace(microsecond=0),
        }
        # aliases
        self.parts.update(
            {
                "years": self.parts["year"],
                "months": self.parts["month"],
                "days": self.parts["day"],
                "hours": self.parts["hour"],
                "minutes": self.parts["minute"],
                "seconds": self.parts["second"],
            }
        )

    def truncate(self, dt, mode):
        try:
            return self.parts[mode](dt)
        except AttributeError:
            raise AttributeError('Unknown truncate mode "%s"' % mode)


datetime_truncator = DateTimeTruncator()
truncate = datetime_truncator.truncate
tz = pytz.timezone


def parse_datetime(x, timezone=None):
    if isinstance(x, datetime.datetime):
        return make_aware(x, timezone)
    elif isinstance(x, datetime.date):
        return make_aware(datetime.datetime(x.year, x.month, x.day, 0, 0, 0), timezone)
    else:
        return make_aware(dateutil.parser.parse(x), timezone)


def shift(x, days=0, hours=0, minutes=0, seconds=0):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return x + datetime.timedelta(days=days, seconds=total_seconds)


def delta(*args, **kwargs):
    return datetime.timedelta(*args, **kwargs)


def local_date(dt, timezone):
    return dt.astimezone(pytz.timezone(timezone)).date()


def datetime_from_date(date, timezone=None):
    dt = datetime.datetime(*date.timetuple()[:6])
    return make_aware(dt, timezone)


def now_unix(*args, **kwargs):
    return to_unix(now(*args, **kwargs))
