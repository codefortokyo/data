# -*- coding: utf-8 -*-

import sys
import os
import collections

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
    """Return True if x is iterable and not basestring, False otherwise.

    :param x: object
    """
    return (isinstance(x, collections.Iterable) and not
            isinstance(x, basestring))


def is_readable(x):
    """Return True if x.read() is possible, False otherwise.

    :param x: object
    """
    return hasattr(x, 'read') and hasattr(x.read, '__call__')


def is_writable(x):
    """Return True if x.write() is possible, False otherwise.

    :param x: object
    """
    return hasattr(x, 'write') and hasattr(x.write, '__call__')


def safe_encode(x, encoding='utf-8'):
    """Return encoded string of x if x is a unicode, x otherwise.

    :param x: object
    """
    if isinstance(x, unicode):
        return x.encode(encoding)
    return x


def safe_decode(x, encoding='utf-8'):
    """Return decoded string if x is a str, x otherwise.

    :param x: object
    """
    if isinstance(x, str):
        return x.decode(encoding)
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
    """datetime型をtimestampに変換する

    :param dt: datetime型
    """
    return int(time.mktime(dt.timetuple()) * 1000) + (dt.microsecond / 1000)


def ts2dt(ts):
    """整数で表されたtimestampをdatetime型に変換する

    :param ts: 整数
    """
    return datetime.fromtimestamp(
        int(ts) / 1000).replace(microsecond=int(ts) % 1000 * 1000)


def is_url(x):
    """xがURLのパターンにマッチすればTrue、そうでなければFalseを返す

    :param x: basestring
    """
    return re.match(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', x) is not None


def rec_apply(f, x, condition=const(True), is_map=is_map,
              is_array=is_array, apply_to_key=True,
              default_map=dict, default_array=list):
    """xに対して再帰的にfを適用する。conditionで適用するかどうかの判定ができる。

    :param f: 一つの引数を取る関数
    :param x: 任意のオブジェクト
    :param condition: 一つの引数を取り、真偽値を返す関数
    :param is_map: 辞書系オブジェクトかどうか判定する関数
    :param is_array: イテレータオブジェクトかどうか判定する
    :param apply_to_key: 辞書系オブジェクトのkeyにも関数を適用するかどうかの真偽値
    :param default_map: 辞書系オブジェクトを構築する際に、元の型が維持できなかった場合に
        用いられる辞書系オブジェクトのコンストラクタ
    :param default_array: リスト系オブジェクトを構築する際に、元の型が維持できなかった場合に
        用いられるリストオブジェクトのコンストラクタ
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
    """xに対して再帰的にx.decode(encoding)を掛ける

    :param x: 任意のオブジェクト
    :param encoding: エンコーディング。デフォルトはutf-8
    """
    return rec_apply(lambda y: y.decode(encoding), x,
                     condition=lambda y: isinstance(y, str))


def rec_encode(x, encoding='utf-8'):
    """xに対して再帰的にx.encode(encoding)を掛ける

    :param x: 任意のオブジェクト
    :param encoding: エンコーディング。デフォルトはutf-8
    """
    return rec_apply(lambda y: y.encode(encoding), x,
                     condition=lambda y: isinstance(y, unicode))


def rec_str2dt(x, timeFormat='%Y/%m/%d %H:%M:%S'):
    """xに対して再帰的にdatetime.strptime(x, timeFormat)を掛ける

    :param x: 任意のオブジェクト
    :param timeFormat: フォーマット。デフォルトは'%Y/%m/%d %H:%M:%S'
    """
    def f(y):
        try:
            return datetime.strptime(y, timeFormat)
        except:
            return y
    return rec_apply(f, x, condition=is_string)


def rec_dt2str(x, timeFormat='%Y/%m/%d %H:%M:%S'):
    """xに対して再帰的にx.strftime(timeFormat)を掛ける

    :param x: 任意のオブジェクト
    :param timeFormat: フォーマット。デフォルトは'%Y/%m/%d %H:%M:%S'
    """
    return rec_apply(lambda y: y.strftime(timeFormat), x,
                     condition=lambda y: isinstance(y, datetime))
