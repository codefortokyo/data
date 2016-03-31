# -*- coding: utf-8 -*-

import sys
import os
import collections
import tempfile
from datetime import datetime
import time
import re

import shortuuid

shortuuid.set_alphabet(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)


def _print(x):
    """Print x.

    :param x: object
    """
    print x


def _raise(x):
    """Raise x

    :param x: object
    """
    raise x


def gen_id():
    """Return generated short UUID.
    """
    return shortuuid.uuid()


def const(x):
    """Return a function which always returns x

    :param x: object
    """
    return lambda *args, **kwargs: x


def is_map(x):
    """Return True if x is an instance of Mappings, False otherwise.

    :param x: object
    """
    return isinstance(x, collections.Mapping)


def is_string(x):
    """Return True if x is a unicode or a str, False otherwise.

    :param x: object
    """
    return isinstance(x, basestring)


def is_array(x):
    """Return True if x is iterable and not basestring or map, False otherwise.

    :param x: object
    """
    return (isinstance(x, collections.Iterable) and not
            isinstance(x, basestring) and not
            isinstance(x, collections.Mapping))


def is_callable(x):
    """Return True if x is callable, False otherwise.

    :param x: object
    """
    return hasattr(x, '__call__')


def is_readable(x):
    """Return True if x has read method, False otherwise. Don't check about
    IOError.

    :param x: object
    """
    return hasattr(x, 'read') and is_callable(x.read)


def is_writable(x):
    """Return True if x has write method, False otherwise. Don't check about
    IOError

    :param x: object
    """
    return hasattr(x, 'write') and is_callable(x.write)


def safe_encode(x, encoding='utf-8'):
    """Return encoded string of x if x is a unicode, x otherwise.

    :param x: object
    """
    if isinstance(x, unicode):
        return x.encode(encoding)
    return x


def safe_decode(x, encoding=None):
    """Return decoded string if x is a str, x otherwise.

    :param x: object
    """
    if isinstance(x, str):
        if encoding is not None:
            return x.decode(encoding)
        else:
            for enc in ('utf-8', 'cp932', 'euc-jp', 'utf-7', 'shift-jis',
                        'shift-jisx0213', 'shift-jis-2004', 'utf-16',
                        'utf-16-be', 'utf-16-le', 'iso-2022-jp',
                        'euc-jisx0213', 'euc-jis-2004', 'iso-2022-jp-1',
                        'iso-2022-jp-2', 'iso-2022-jp-3', 'iso-2022-jp-ext',
                        'iso-2022-jp-2004'):
                try:
                    return x.decode(enc)
                except:
                    pass
    return x


def cons_array(data, c, default_array=list):
    """Return an instance of c whose elements are data. Return an instance of
    default_array if c cannot take data as an argument for the constructor.

    :param data: tuple of elements
    :param c: class
    :param default_array: class
    """
    try:
        return c(data)
    except:
        return default_array(data)


def cons_map(data, c, default_map=dict):
    """Return an instance of c whose elements are data. Return an instance of
    default_map if c cannot take data as an argument for the constructor.

    :param data: tuple of elements
    :param c: class
    :param default_array: class
    """
    try:
        return c(data)
    except:
        return default_map(data)


def dt2ts(dt):
    """Return timestamp (int) of dt.

    :param dt: datetime
    """
    return int(time.mktime(dt.timetuple()) * 1000) + (dt.microsecond / 1000)


def ts2dt(ts):
    """Return datetime of ts

    :param ts: int
    """
    return datetime.fromtimestamp(
        int(ts) / 1000).replace(microsecond=int(ts) % 1000 * 1000)


def is_url(x):
    """Return if x matches URL expression.

    :param x: basestring
    """
    return re.match(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', x) is not None


def rec_apply(f, x, condition=const(True), is_map=is_map,
              is_array=is_array, apply_to_key=True,
              default_map=dict, default_array=list):
    """Return the same structured data of x but each element is applied f.
    condition is used to check if f should be applied to x. is_map and is_array
    are used to decide if x is container or not. apply_to_key is a flag to
    control if f is applied to the keys of the mapping objects. default_map and
    default_array is used to reconstruct the same structure if the
    reconstruction is failed.

    :param f: one-argument function
    :param x: object
    :param condition: one-argument function
    :param is_map: one-argument function
    :param is_array: one-argument function
    :param apply_to_key: one-argument function
    :param default_map: class object of inherit class of mapping
    :param default_array: class object of inherit class of iterable container
    """
    def g(y):
        if is_map(y):
            if apply_to_key:
                return cons_map(((g(k), g(v)) for k, v in y.items()),
                                y.__class__, default_map)
            return cons_map(((k, g(v)) for k, v in y.items()), y.__class__,
                            default_map)
        if is_array(y):
            return cons_array((g(v) for v in y), y.__class__, default_array)
        if condition(y):
            return f(y)
        return y
    return g(x)


def rec_decode(x, encoding='utf-8'):
    """Return the same structured data as `x` but each element is decoded with
    `encoding`.

    :param x: object
    :param encoding: string which specifies encoding (default: utf-8)
    """
    return rec_apply(lambda y: y.decode(encoding), x,
                     condition=lambda y: isinstance(y, str))


def rec_encode(x, encoding='utf-8'):
    """Return the same structured data as `x` but each element is encoded with
    `encoding`.

    :param x: object
    :param encoding: string which specifies encoding (default: utf-8)
    """
    return rec_apply(lambda y: y.encode(encoding), x,
                     condition=lambda y: isinstance(y, unicode))


def rec_str2dt(x, timeFormat='%Y/%m/%d %H:%M:%S'):
    """Return the same structured data as `x` but each string which matches the
    `timeFormat` is casted to datetime object.

    :param x: object
    :param timeFormat: string which specifies time format.
    (default: '%Y/%m/%d %H:%M:%S')
    """
    def f(y):
        try:
            return datetime.strptime(y, timeFormat)
        except:
            return y
    return rec_apply(f, x, condition=is_string, apply_to_key=False)


def rec_dt2str(x, timeFormat='%Y/%m/%d %H:%M:%S'):
    """Return the same structured data as `x` but each datetime object is
    stringified with `timeFormat`.

    :param x: 任意のオブジェクトls
    :param timeFormat: string which specifies time format.
    (default: '%Y/%m/%d %H:%M:%S')
    """
    return rec_apply(lambda y: y.strftime(timeFormat), x,
                     condition=lambda y: isinstance(y, datetime),
                     apply_to_key=False)
