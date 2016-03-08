# -*- coding: utf-8 -*-

import sys;
import os;
import collections;

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

def rApply(f, x, condition=const(True), isMapping=isMapping, isIterable=isIterable, applyToKey=True, defaultMapping=dict, defaultSequence=list):
  """xに対して再帰的にfを適用する。conditionで適用するかどうかの判定ができる。
  :param f: 一つの引数を取る関数
  :param x: 任意のオブジェクト
  :param condition: 一つの引数を取り、真偽値を返す関数
  :param isMapping: 辞書系オブジェクトかどうか判定する関数
  :param isIterable:　イテレータオブジェクトかどうか判定する
  :param applyToKey: 辞書系オブジェクトのkeyにも関数を適用するかどうかの真偽値
  :param defaultMapping: 辞書系オブジェクトを構築する際に、元の型が維持できなかった場合に用いられる辞書系オブジェクトのコンストラクタ
  :param defaultSequence: リスト系オブジェクトを構築する際に、元の型が維持できなかった場合に用いられるリストオブジェクトのコンストラクタ
  """
  if isMapping(x):
    if applyToKey:
      try:
        return x.__class__( ( (rApply(f,k,condition,isMapping,isIterable,applyToKey),rApply(f,v,condition,isMapping,isIterable,applyToKey)) for k,v in x.items() ) );
      except:
        return defaultMapping( ( (rApply(f,k,condition,isMapping,isIterable,applyToKey),rApply(f,v,condition,isMapping,isIterable,applyToKey)) for k,v in x.items() ) );
    try:
      return x.__class__( ( (k,rApply(f,v,condition,isMapping,isIterable,applyToKey)) for k,v in x.items() ) );
    except:
      return defaultMapping( ( (k,rApply(f,v,condition,isMapping,isIterable,applyToKey)) for k,v in x.items() ) );
  if isIterable(x):
    try:
      return x.__class__( ( rApply(f,v,condition,isMapping,isIterable,applyToKey) for v in x ) );
    except:
      return defaultSequence( (rApply(f,v,condition,isMapping,isIterable,applyToKey) for v in x ) );
  if condition(x):
    return f(x);
  return x;
