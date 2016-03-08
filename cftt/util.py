# -*- coding: utf-8 -*-

import sys;
import os;
import collections;

from datetime import datetime;
import time;
import re;

import shortuuid;

shortuuid.set_alphabet('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789');

def _print(x):
  """print 文の関数版。

  :param x: 任意のオブジェクト
  """
  print x;

def _raise(x):
  """raise 文の関数版。この関数の中から x　をraise する

  :param x: 任意のオブジェクト
  """
  raise x;

def genId():
  """22文字のUUIDを生成する
  """
  return shortuuid.uuid();

def const(x):
  """常にxを返す関数を返す

  :param x: 任意のオブジェクト
  """
  return lambda *args,**kwargs: x;

def isMapping(x):
  """xが辞書系オブジェクトならTrue、そうでなければFalseを返す

  :param x: 任意のオブジェクト
  """
  return isinstance(x, collections.Mapping);

def isString(x):
  """xがunicode文字列か文字列ならTrue、そうでなければFalseを返す

  :param x: 任意のオブジェクト
  """
  return isinstance(x, basestring);

def isIterable(x):
  """xがiterableであり、文字列系でない場合True、そうでなければFalseを返す

  :param x: 任意のオブジェクト
  """
  return isinstance(x, collections.Iterable) and not isinstance(x, basestring);

def isReadable(x):
  """xがread可能なオブジェクトの場合True、そうでなければFalseを返す

  :param x: 任意のオブジェクト
  """
  return hasattr(x, 'read') and hasattr(x.read, '__call__');

def isWritable(x):
  """xがwrite可能なオブジェクトの場合True、そうでなければFalseを返す

  :param x: 任意のオブジェクト
  """
  return hasattr(x, 'write') and hasattr(x.write, '__call__');

def dt2Ts(dt):
  """datetime型をtimestampに変換する

  :param dt: datetime型
  """
  return int(time.mktime(dt.timetuple())*1000)+(dt.microsecond/1000);

def ts2Dt(ts):
  """整数で表されたtimestampをdatetime型に変換する

  :param ts: 整数
  """
  return datetime.fromtimestamp( int(ts)/1000 ).replace(microsecond=int(ts)%1000*1000);

def isURL(x):
  """xがURLのパターンにマッチすればTrue、そうでなければFalseを返す

  :param x: basestring
  """
  return re.match(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', x) is not None;

def rApply(f, x, condition=const(True), isMapping=isMapping, isIterable=isIterable, applyToKey=True, defaultMapping=dict, defaultSequence=list):
  """xに対して再帰的にfを適用する。conditionで適用するかどうかの判定ができる。

  :param f: 一つの引数を取る関数
  :param x: 任意のオブジェクト
  :param condition: 一つの引数を取り、真偽値を返す関数
  :param isMapping: 辞書系オブジェクトかどうか判定する関数
  :param isIterable: イテレータオブジェクトかどうか判定する
  :param applyToKey: 辞書系オブジェクトのkeyにも関数を適用するかどうかの真偽値
  :param defaultMapping: 辞書系オブジェクトを構築する際に、元の型が維持できなかった場合に用いられる辞書系オブジェクトのコンストラクタ
  :param defaultSequence: リスト系オブジェクトを構築する際に、元の型が維持できなかった場合に用いられるリストオブジェクトのコンストラクタ
  """
  if isMapping(x):
    if applyToKey:
      res = ( (rApply(f,k,condition,isMapping,isIterable,applyToKey),rApply(f,v,condition,isMapping,isIterable,applyToKey)) for k,v in x.items() );
      try:
        return x.__class__( res );
      except:
        return defaultMapping( res );
    try:
      res = ( (k,rApply(f,v,condition,isMapping,isIterable,applyToKey)) for k,v in x.items() );
      return x.__class__( res );
    except:
      return defaultMapping( res );
  if isIterable(x):
    res = ( rApply(f,v,condition,isMapping,isIterable,applyToKey) for v in x );
    try:
      return x.__class__( res );
    except:
      return defaultSequence( res );
  if condition(x):
    return f(x);
  return x;

def rDecode(x, encoding='utf-8'):
  """xに対して再帰的にx.decode(encoding)を掛ける

  :param x: 任意のオブジェクト
  :param encoding: エンコーディング。デフォルトはutf-8
  """
  return rApply(lambda y:y.decode(encoding), x, condition=lambda y:isinstance(y,str));

def rEncode(x, encoding='utf-8'):
  """xに対して再帰的にx.encode(encoding)を掛ける

  :param x: 任意のオブジェクト
  :param encoding: エンコーディング。デフォルトはutf-8
  """
  return rApply(lambda y:y.encode(encoding), x, condition=lambda y:isinstance(y,unicode));

def rStr2Dt(x, timeFormat='%Y/%m/%d %H:%M:%S'):
  """xに対して再帰的にdatetime.strptime(x, timeFormat)を掛ける

  :param x: 任意のオブジェクト
  :param timeFormat: フォーマット。デフォルトは'%Y/%m/%d %H:%M:%S'
  """
  def f(y):
    try:
      return datetime.strptime(y, timeFormat);
    except:
      return y;
  return rApply(f, x, condition=lambda y: isinstance(y, basestring));

def rDt2Str(x, timeFormat='%Y/%m/%d %H:%M:%S'):
  """xに対して再帰的にx.strftime(timeFormat)を掛ける

  :param x: 任意のオブジェクト
  :param timeFormat: フォーマット。デフォルトは'%Y/%m/%d %H:%M:%S'
  """
  return rApply(lambda y:y.strftime(timeFormat), x, condition=lambda y:isinstance(y,datetime));
