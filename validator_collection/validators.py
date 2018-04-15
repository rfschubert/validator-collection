# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

import decimal as decimal_
import fractions
import io
import math
import os
import re
import uuid as uuid_
import datetime as datetime_

from ast import parse

from validator_collection._compat import numeric_types, datetime_types, date_types, \
    time_types, timestamp_types, tzinfo_types, POSITIVE_INFINITY, NEGATIVE_INFINITY, \
    TimeZone, json, is_py2, is_py3, dict_, float_


URL_REGEX = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"$"
    , re.UNICODE)

EMAIL_REGEX = re.compile(
    r"(?!localhost)[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$"
)

MAC_ADDRESS_REGEX = re.compile(r'^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')

IPV6_REGEX = re.compile(
    '^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)(?:%25(?:[A-Za-z0-9\\-._~]|%[0-9A-Fa-f]{2})+)?$'
)

def uuid(value, allow_empty = False):
    """Validate that ``value`` is a valid :ref:`UUID <python:uuid.UUID>`.

    :param value: The value to validate.
    :type value: :ref:`UUID <python:uuid.UUID>` / :ref:`str <python:str>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` coerced to a :ref:`UUID <python:uuid.UUID>` object / ``None``
    :rtype: :ref:`UUID <python:uuid.UUID>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` cannot be coerced to a :ref:`UUID <python:uuid.UUID>`
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if isinstance(value, uuid_.UUID):
        return value

    try:
        value = uuid_.UUID(value)
    except ValueError:
        raise TypeError('value must be a valid UUID')

    return value


def email(value, allow_empty = False):
    """Validate that ``value`` is a valid email address.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`str <python:str>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid email address or ``None``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, str):
        raise TypeError('value must be a valid string')

    value = value.lower()

    is_valid = EMAIL_REGEX.match(value)

    if not is_valid:
        raise TypeError('value must be a valid email address')

    return value


def url(value, allow_empty = False):
    """Validate that ``value`` is a valid URL.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`str <python:str>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid URL or ``None``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, str):
        raise TypeError('value must be a valid string')

    value = value.lower()

    is_valid = URL_REGEX.match(value)

    if not is_valid:
        raise TypeError('value must be a valid URL')

    return value


def string(value,
           allow_empty = False,
           minimum_length = None,
           maximum_length = None,
           whitespace_padding = False):
    """Validate that ``value`` is a valid string.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum_length: If supplied, indicates the minimum number of characters
      needed to be valid.
    :type minimum_length: :ref:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of characters
      needed to be valid.
    :type maximum_length: :ref:`int <python:int>`

    :param whitespace_padding: If ``True`` and the value is below the
      ``minimum_length``, pad the value with spaces. Defaults to ``False``.
    :type whitespace_padding: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`str <python:str>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid string or ``None``
    :raises ValueError: if ``minimum_length`` is supplied and the length of
      ``value`` is less than ``minimum_length`` and ``whitespace_padding`` is
      ``False``
    :raises ValueError: if ``maximum_length`` is supplied and the length of
      ``value`` is more than the ``maximum_length``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    minimum_length = integer(minimum_length, allow_empty = True)
    maximum_length = integer(maximum_length, allow_empty = True)

    value = str(value)

    if value and maximum_length and len(value) > maximum_length:
        raise ValueError('value (%s) exceeds maximum length')

    if value and minimum_length and len(value) < minimum_length:
        if whitespace_padding:
            value = value.ljust(minimum_length, ' ')
        else:
            raise ValueError('value (%s) is below the minimum length')

    return value


def iterable(value,
             allow_empty = False,
             forbid_literals = (str, bytes),
             minimum_length = None,
             maximum_length = None):
    """Validate that ``value`` is a valid iterable.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param forbid_literals: A collection of literals that will be considered invalid
      even if they are (actually) iterable. Defaults to :ref:`str <python:str>` and
      :ref:`bytes <python:bytes>`.
    :type forbid_literals: iterable

    :param minimum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type minimum_length: :ref:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type maximum_length: :ref:`int <python:int>`

    :returns: ``value`` / ``None``
    :rtype: iterable / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid iterable or ``None``
    :raises ValueError: if ``minimum_length`` is supplied and the length of
      ``value`` is less than ``minimum_length`` and ``whitespace_padding`` is
      ``False``
    :raises ValueError: if ``maximum_length`` is supplied and the length of
      ``value`` is more than the ``maximum_length``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    minimum_length = integer(minimum_length, allow_empty = True)
    maximum_length = integer(maximum_length, allow_empty = True)

    if isinstance(value, forbid_literals) or not hasattr(value, '__iter__'):
        raise TypeError('value must be a valid iterable')

    if value and minimum_length is not None and len(value) < minimum_length:
        raise ValueError('value has fewer items than the minimum length')

    if value and maximum_length is not None and len(value) > maximum_length:
        raise ValueError('value has more items than the maximum length')

    return value


def datetime(value,
             allow_empty = False,
             minimum = None,
             maximum = None):
    """Validate that ``value`` is a valid datetime.

    .. caution::

      If supplying a string, the string needs to be in an ISO-format to pass
      validation. If it is not in an ISO-format, validation will fail.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / :ref:`datetime <python:datetime.datetime>`
      / :ref:`date <python:datetime.date>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :returns: ``value`` / ``None``
    :rtype: :ref:`datetime <python:datetime.datetime>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises ValueError: if ``minimum`` is supplied but ``value`` occurs before ``minimum``
    :raises ValueError: if ``maximum`` is supplied but ``value`` occurs after ``minimum``

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    minimum = datetime(minimum, allow_empty = True)
    maximum = datetime(maximum, allow_empty = True)

    if not isinstance(value, datetime_types):
        raise ValueError('value must be a date object, datetime object, '
                         'ISO-formatted string, '
                         'or POSIX timestamp')
    elif isinstance(value, timestamp_types):
        try:
            value = datetime_.datetime.fromtimestamp(value)
        except ValueError:
            raise ValueError('value must be a date object, datetime object, '
                             'ISO-formatted string, '
                             'or POSIX timestamp')
    elif isinstance(value, str):
        try:
            if 'T' in value:
                value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                value = datetime_.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            try:
                if 'T' in value:
                    value = datetime_.datetime.strptime(value, '%Y/%m/%dT%H:%M:%S')
                else:
                    value = datetime_.datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
            except ValueError:
                try:
                    if 'T' in value:
                        value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                    else:
                        value = datetime_.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        if 'T' in value:
                            value = datetime_.datetime.strptime(value,
                                                                '%Y/%m/%dT%H:%M:%S')
                        else:
                            value = datetime_.datetime.strptime(value,
                                                                '%Y/%m/%d %H:%M:%S')
                    except ValueError:
                        value = date(value)

    if isinstance(value, datetime_.date) and not isinstance(value, datetime_.datetime):
        value = datetime_.datetime(value.year,                                  # pylint: disable=R0204
                                   value.month,
                                   value.day,
                                   0,
                                   0,
                                   0,
                                   0)

    if minimum and value and value < minimum:
        raise ValueError('value (%s) is before the minimum given' % value.isoformat())
    if maximum and value and value > maximum:
        raise ValueError('value (%s) is after the maximum given' % value.isoformat())

    return value


def date(value,
         allow_empty = False,
         minimum = None,
         maximum = None):
    """Validate that ``value`` is a valid date.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / :ref:`datetime <python:datetime.datetime>`
      / :ref:`date <python:datetime.date>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :returns: ``value`` / ``None``
    :rtype: :ref:`date <python:datetime.date>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid value type or ``None``
    :raises ValueError: if ``minimum`` is supplied but ``value`` occurs before ``minimum``
    :raises ValueError: if ``maximum`` is supplied but ``value`` occurs after ``minimum``

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    minimum = date(minimum, allow_empty = True)
    maximum = date(maximum, allow_empty = True)

    if not isinstance(value, date_types):
        raise ValueError('value must be a date object, datetime object, '
                         'ISO-formatted string, '
                         'or POSIX timestamp')
    elif isinstance(value, datetime_.datetime):
        value = value.date()
    elif isinstance(value, timestamp_types):
        try:
            value = datetime_.date.fromtimestamp(value)
        except ValueError:
            raise ValueError('value must be a date object, datetime object, '
                             'ISO-formatted string, '
                             'or POSIX timestamp')
    elif isinstance(value, str):
        try:
            value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            value = value.date()
        except ValueError:
            if ' ' in value:
                value = value.split(' ')[0]
            if 'T' in value:
                value = value.split('T')[0]

            if len(value) != 10:
                raise ValueError('value must be a date object, datetime object, '
                                 'ISO-formatted string, '
                                 'or POSIX timestamp')
            try:
                year = int(value[:4])
                month = int(value[5:7])
                day = int(value[-2:])
                value = datetime_.date(year, month, day)
            except (ValueError, TypeError):
                raise ValueError('value must be a date object, datetime object, '
                                 'ISO-formatted string, '
                                 'or POSIX timestamp')

    if minimum and value and value < minimum:
        raise ValueError('value (%s) is before the minimum given' % value.isoformat())
    if maximum and value and value > maximum:
        raise ValueError('value (%s) is after the maximum given' % value.isoformat())

    return value


def time(value,
         allow_empty = False,
         minimum = None,
         maximum = None):
    """Validate that ``value`` is a valid :ref:`time <python:datetime.time>`.

    .. caution::

      This validator will **always** return the time in UTC. If ``value`` has
      a timezone / UTC offset applied, the validator will coerce the value returned
      back to UTC.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / :ref:`datetime <python:datetime.datetime>`
      / numeric / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :returns: ``value`` in UTC time / ``None``
    :rtype: :ref:`time <python:datetime.time>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid value type or ``None``
    :raises ValueError: if ``minimum`` is supplied but ``value`` occurs before ``minimum``
    :raises ValueError: if ``maximum`` is supplied but ``value`` occurs after ``minimum``

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    minimum = time(minimum, allow_empty = True)
    maximum = time(maximum, allow_empty = True)

    if not isinstance(value, time_types):
        raise ValueError('value must be a datetime object, '
                         'ISO-formatted string, '
                         'or POSIX timestamp')
    elif isinstance(value, datetime_.datetime):
        value = value.time()
    elif isinstance(value, timestamp_types):
        try:
            datetime_value = datetime(value)
            value = datetime_value.time()
        except ValueError:
            raise ValueError('value must be a datetime object, '
                             'ISO-formatted string, '
                             'or POSIX timestamp')
    elif isinstance(value, str):
        try:
            datetime_value = datetime(value)
            print('datetime_value:')
            print(datetime_value)
            value = datetime_value.time()
        except ValueError:
            try:
                if '+' in value:
                    components = value.split('+')
                    is_offset_positive = True
                elif '-' in value:
                    components = value.split('-')
                    is_offset_positive = False
                else:
                    raise ValueError()

                time_string = components[0]
                if len(components) > 1:
                    utc_offset = components[1]
                else:
                    utc_offset = None

                time_components = time_string.split(':')
                hour = int(time_components[0])
                minutes = int(time_components[1])
                seconds = time_components[2]
                if '.' in seconds:
                    second_components = seconds.split('.')
                    seconds = int(second_components[0])
                    microseconds = int(second_components[1])
                else:
                    microseconds = 0

                utc_offset = timezone(utc_offset,
                                      allow_empty = True,
                                      positive = is_offset_positive)

                value = datetime_.time(hour = hour,
                                       minute = minutes,
                                       second = seconds,
                                       microsecond = microseconds,
                                       tzinfo = utc_offset)

            except (ValueError, TypeError, IndexError):
                raise ValueError('value must be a date object, datetime object, '
                                 'ISO-formatted string, '
                                 'or POSIX timestamp')

        if value is not None:
            value = value.replace(tzinfo = None)

    if minimum and value and value < minimum:
        raise ValueError('value (%s) is before the minimum given' % value.isoformat())
    if maximum and value and value > maximum:
        raise ValueError('value (%s) is after the maximum given' % value.isoformat())

    return value


def timezone(value,
             allow_empty = False,
             positive = True):
    """Validate that ``value`` is a valid :ref:`tzinfo <python:datetime.tzinfo>`.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / :ref:`tzinfo <python:datetime.tzinfo>`
      / numeric / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param positive: Indicates whether the ``value`` is positive or negative
      (only has meaning if ``value`` is a string). Defaults to ``True``.
    :type positive: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`tzinfo <python:datetime.tzinfo>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid value type or ``None``

    """
    original_value = value

    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, tzinfo_types):
        raise ValueError('value must be a tzinfo, '
                         'UTC offset in seconds expressed as a number, '
                         'UTC offset expressed as string of form +HH:MM')
    elif isinstance(value, datetime_.datetime):
        value = value.tzinfo
    elif isinstance(value, datetime_.date):
        return None
    elif isinstance(value, datetime_.time):
        return value.tzinfo
    elif isinstance(value, timestamp_types):
        return None
    elif isinstance(value, str):
        if '+' not in value and '-' not in value:
            try:
                datetime_value = datetime(value)
                return datetime_value.tzinfo
            except ValueError:
                raise ValueError('value must be a tzinfo, '
                                 'UTC offset in seconds expressed as a number, '
                                 'UTC offset expressed as string of form +HH:MM')
        elif '-' in value:
            try:
                datetime_value = datetime(value)
                return datetime_value.tzinfo
            except ValueError:
                pass

        if '+' in value and not positive:
            raise ValueError('expected a negative UTC offset but value is positive')
        elif '-' in value and positive:
            raise ValueError('expected a positive UTC offset but value is negative')

        if '+' in value:
            value = value[value.find('+'):]
        elif '-' in value:
            value = value[value.rfind('+'):]

        value = value[1:]

        offset_components = value.split(':')
        if len(offset_components) != 2:
            raise ValueError('value must be a tzinfo, '
                             'UTC offset in seconds expressed as a number, '
                             'UTC offset expressed as string of form +HH:MM')
        hour = int(offset_components[0])
        minutes = int(offset_components[1])

        value = (hour * 60 * 60) + (minutes * 60)
        print(value)

        if not positive:
            value = 0 - value

    if isinstance(value, numeric_types):
        if value > 0:
            positive = True
        elif value < 0:
            positive = False
        elif value == 0:
            return None

        offset = datetime_.timedelta(seconds = value)
        if is_py2:
            value = TimeZone(offset = offset)
        elif is_py3:
            try:
                TimeZone(offset)
            except ValueError:
                raise ValueError('value (%s) cannot exceed +/- 24h' % original_value)
        else:
            raise NotImplementedError()

    return value


def not_empty(value, allow_empty = False):
    """Validate that ``value`` is not empty.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`RequestPayloadError` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``

    :raises RequestPayloadError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if not value and allow_empty:
        return None
    elif not value:
        raise ValueError('value was empty')

    return value


def none(value,
         allow_empty = False,
         coerce_value = False):
    """Validate that ``value`` is ``None``

    .. note::

      If ``coerce_value`` is ``True``, the function will always return ``None``
      even if ``value`` is not *strictly* Python's ``NoneType``.

      If ``coerce_value`` is ``False``, the function will raise an error if
      ``value`` is not strictly Python's ``NoneType``.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty but
      not ``None``. If  ``False``, raises a :ref:`ValueError` if ``value``
      is empty but not ``None``. Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param coerce_value: If ``True``, returns ``None`` regardless of ``value``.
      If ``False``, raises a :ref:`RequestPayloadError` if ``value`` is not ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    return_value = None

    if coerce_value:
        return_value = None
    elif value is not None and not value and allow_empty:
        return_value = None
    elif (value is not None and not value) or value:
        raise ValueError('value must be None')

    return return_value


def decimal(value,
            allow_empty = False,
            minimum = None,
            maximum = None):
    """Validate that ``value`` is a :ref:`Decimal <python:decimal.Decimal>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty but
      not ``None``. If  ``False``, raises a :ref:`ValueError` if ``value``
      is empty but not ``None``. Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is ``None`` and ``allow_empty`` is ``False``
    :raises ValueError: if ``minimum`` is supplied and ``value`` is less than the
      ``minimum``
    :raises ValueError: if ``maximum`` is supplied and ``value`` is more than the
      ``maximum``

    """
    if value is None and allow_empty:
        return None
    elif value is None:
        raise ValueError('value cannot be None')

    if isinstance(value, str):
        try:
            value = decimal_.Decimal(value.strip())
        except decimal_.InvalidOperation:
            raise ValueError('value cannot be converted to a Decimal')
    elif isinstance(value, fractions.Fraction):
        try:
            value = float(value)                                                # pylint: disable=R0204
        except ValueError:
            raise ValueError('value cannot be converted to a Decimal')

    value = numeric(value,
                    allow_empty = False,
                    maximum = maximum,
                    minimum = minimum)

    if not isinstance(value, decimal_.Decimal):
        value = decimal_.Decimal(value)

    return value


def numeric(value,
            allow_empty = False,
            minimum = None,
            maximum = None):
    """Validate that ``value`` is a numeric value.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`RequestPayloadError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is ``None`` and ``allow_empty`` is ``False``
    :raises ValueError: if ``minimum`` is supplied and ``value`` is less than the
      ``minimum``
    :raises ValueError: if ``maximum`` is supplied and ``value`` is more than the
      ``maximum``

    """
    if maximum is None:
        maximum = POSITIVE_INFINITY
    else:
        maximum = numeric(maximum)
    if minimum is None:
        minimum = NEGATIVE_INFINITY
    else:
        minimum = numeric(minimum)

    if value is None and not allow_empty:
        raise ValueError('value cannot be empty')
    elif value is not None:
        if isinstance(value, str):
            try:
                value = float_(value)
            except (ValueError, TypeError):
                raise ValueError('value cannot be coerced to a numeric form')
        elif not isinstance(value, numeric_types):
            raise ValueError('value is not numeric')

    if value is not None and value > maximum:
        raise ValueError('value (%s) exceeds maximum (%s)' % (value, maximum))

    if value is not None and value < minimum:
        raise ValueError('value (%s) less than minimum (%s)' % (value, minimum))

    return value


def integer(value,
            allow_empty = False,
            minimum = None,
            maximum = None,
            base = 10):
    """Validate that ``value`` is an :ref:`int <python:int>`.

    .. note::

      If ``value`` is not already an integer (like a :ref:`float <python:float>`
      or :ref:`Decimal <python:decimal.Decimal>`), the value will be rounded up
      to the nearest integer.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :param base: Indicates the base that is used to determine the integer value.
      The allowed values are 0 and 2–36. Base-2, -8, and -16 literals can be
      optionally prefixed with ``0b/0B``, ``0o/0O/0``, or ``0x/0X``, as with
      integer literals in code. Base 0 means to interpret the string exactly as
      an integer literal, so that the actual base is 2, 8, 10, or 16. Defaults to
      ``10``.

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    value = numeric(value,
                    allow_empty = allow_empty,
                    minimum = minimum,
                    maximum = maximum)

    if value is not None:
        value = int(str(math.ceil(value)), base = base)

    return value


def float(value,
          allow_empty = False,
          minimum = None,
          maximum = None):
    """Validate that ``value`` is a :ref:`float <python:float>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    value = _numeric_coercion(value,
                              coercion_function = float_,
                              allow_empty = allow_empty,
                              minimum = minimum,
                              maximum = maximum)

    return value


def fraction(value,
             allow_empty = False,
             minimum = None,
             maximum = None):
    """Validate that ``value`` is a :ref:`fraction <python:fractions.Fraction>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    value = _numeric_coercion(value,
                              coercion_function = fractions.Fraction,
                              allow_empty = allow_empty,
                              minimum = minimum,
                              maximum = maximum)

    return value


def _numeric_coercion(value,
                      coercion_function = None,
                      allow_empty = False,
                      minimum = None,
                      maximum = None):
    """Validate that ``value`` is numeric and coerce using ``coercion_function``.

    :param value: The value to validate.

    :param coercion_function: The function to use to coerce ``value`` to the desired
      type.
    :type coercion_function: callable

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: the type returned by ``coercion_function``

    :raises ValueError: if ``coercion_function`` is empty
    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if coercion_function is None:
        raise ValueError('coercion_function cannot be empty')
    elif not hasattr(coercion_function, '__call__'):
        raise ValueError('coercion_function must be callable')

    value = numeric(value,
                    allow_empty = allow_empty,
                    minimum = minimum,
                    maximum = maximum)

    if value is not None:
        try:
            value = coercion_function(value)
        except (ValueError, TypeError, AttributeError, SyntaxError):
            raise ValueError('cannot coerce value (%s) to desired type' % value)

    return value


def valid_variable_name(value,
                        allow_empty = False):
    """Validate that the value is a valid Python variable name.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`str <python:str>` or ``None``

    :raises ValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    try:
        parse('%s = None' % value)
    except (SyntaxError, ValueError, TypeError):
        raise ValueError('value (%s) is not a valid variable name' % value)

    return value


def file_exists(value,
                allow_empty = False):
    """Validate that ``value`` is a valid file that exists on the local filesystem.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / ``None``

    :raises ValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises IOError: if ``value`` does not exist
    :raises ValueError: if ``value`` is not a valid file

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    value = path_exists(value)

    if not os.path.isfile(value):
        raise ValueError('value (%s) is not a file')

    return value


def directory_exists(value,
                     allow_empty = False):
    """Validate that ``value`` is a valid directory that exists on the local
    filesystem.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / ``None``

    :raises ValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises IOError: if ``value`` does not exist
    :raises ValueError: if ``value`` is not a valid directory

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    value = path_exists(value)

    if not os.path.isdir(value):
        raise ValueError('value (%s) is not a directory')

    return value


def path_exists(value,
                allow_empty = False):
    """Validate that ``value`` is a path-like object that exists on the local
    filesystem.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / ``None``

    :raises ValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises IOError: if ``value`` does not exist
    :raises ValueError: if ``value`` is not a valid file

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    value = path(value)

    if not os.path.exists(value):
        raise IOError('value (%s) not found' % value)

    return value


def path(value,
         allow_empty = False):
    """Validate that ``value`` is a valid path-like object.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / ``None``

    :raises ValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises IOError: if ``value`` does not exist
    :raises ValueError: if ``value`` is not a valid file

    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if is_py2:
        try:
            os.path.exists(value)
        except TypeError:
            raise ValueError('value (%s) is not a valid path' % value)
    elif is_py3:
        if not isinstance(value, (str, bytes, os.PathLike)):
            raise ValueError('value (%s) is not a valid path' % value)

    return value


def ipv4(value, allow_empty = False):
    """Validate that ``value`` is a valid IP version 4 address.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if not value and allow_empty is False:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    try:
        components = value.split('.')
    except AttributeError:
        raise ValueError('value (%s) is not a valid ipv4' % value)

    if len(components) != 4 or not all(x.isdigit() for x in components):
        raise ValueError('value (%s) is not a valid ipv4' % value)

    for x in components:
        try:
            x = integer(x,
                        minimum = 0,
                        maximum = 255)
        except ValueError:
            raise ValueError('value (%s) is not a valid ipv4' % value)

    return value


def ipv6(value, allow_empty = False):
    """Validate that ``value`` is a valid IP address version 6.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if not value and allow_empty is False:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, str):
        raise ValueError('value (%s) is not a valid ipv6' % value)

    value = value.lower()

    is_valid = IPV6_REGEX.match(value)

    if not is_valid:
        raise ValueError('value (%s) is not a valid ipv6' % value)

    return value


def mac_address(value, allow_empty = False):
    """Validate that ``value`` is a valid MAC address.

    :param value: The value to validate.
    :type value: :ref:`str <python:str>` / ``None``

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is empty. If
      ``False``, raises a :ref:`ValueError <python:ValueError>` if ``value`` is empty.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`str <python:str>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises TypeError: if ``value`` is not a valid URL or ``None``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, str):
        raise ValueError('value must be a valid string')

    if '-' in value:
        value = value.replace('-', ':')

    is_valid = MAC_ADDRESS_REGEX.match(value)

    if not is_valid:
        raise ValueError('value (%s) is not a valid MAC address' % value)

    return value


def dict(value,
         allow_empty = False):
    """Validate that ``value`` is a :ref:`dict <python:dict>`.

    .. hint::

      If ``value`` is a string, this validator will assume it is a JSON
      object and try to convert it into a :ref:`dict <python:dict>`

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`dict <python:dict>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    original_value = value
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if isinstance(value, str):
        try:
            value = json.loads(value)
        except Exception:
            raise ValueError('value (%s) cannot be coerced to a dict)' % original_value)

    if not isinstance(value, dict_):
        raise ValueError('value (%s) is not a dict' % original_value)

    return value


def stringIO(value,
             allow_empty = False):
    """Validate that ``value`` is a :ref:`StringIO <python:io.StringIO>` object.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`StringIO <python:io.StringIO>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, io.StringIO):
        raise ValueError('value is not an io.StringIO object')

    return value


def bytesIO(value,
            allow_empty = False):
    """Validate that ``value`` is a :ref:`BytesIO <python:io.BytesIO>` object.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns ``None`` if ``value`` is ``None``.
      If  ``False``, raises a :ref:`ValueError` if ``value`` is ``None``.
      Defaults to ``False``.
    :type allow_empty: :ref:`bool <python:bool>`

    :returns: ``value`` / ``None``
    :rtype: :ref:`StringIO <python:io.StringIO>` / ``None``

    :raises ValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if not value and not allow_empty:
        raise ValueError('value cannot be empty')
    elif not value:
        return None

    if not isinstance(value, io.BytesIO):
        raise ValueError('value is not a BytesIO')

    return value