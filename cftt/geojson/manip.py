# -*- coding: utf-8 -*-

import sys;
import os;

import json;

import collections;

from shapely.geometry import shape, mapping;
from shapely.ops import cascaded_union;

def recApply(d, func, condition=lambda x:True, isMap=lambda x:isinstance(x,collections.Mapping), isContainer=lambda x:isinstance(x,collections.Iterable) and not isinstance(x, basestring), applyToKey=True):
  """d に対して func を再帰的に適用する

  :param d: 任意の変数
  :param func: 適用する関数
  :param condition: 関数を適用するかどうか判定する関数
  :param isMap: 辞書系オブジェクトかどうか判定する関数
  :param isContainer: イテレータブル系かどうか判定する関数
  :param applyToKey: 辞書系オブジェクトのキーにも関数を適用するかどうかの真偽値
  """
  if isMap(d):
    if applyToKey:
      return d.__class__( ( (recApply(k,func,condition,isMap,isContainer,applyToKey),recApply(v,func,condition,isMap,isContainer,applyToKey)) for k,v in d.items() ) );
    return d.__class__( ( (k,recApply(v,func,condition,isMap,isContainer,applyToKey)) for k,v in d.items() ) );
  if isContainer(d):
    return d.__class__( ( recApply(v,func,condition,isMap,isContainer,applyToKey) for v in d ) );
  if condition(d):
    return func(d);
  return d;

def recDecode(d):
  """d と同じ構造で、 d の全ての str 要素に対して .decode('utf-8') を掛けたものを返す

  :param d: 任意の変数
  """
  return recApply(d, lambda x:x.decode('utf-8'), lambda x:isinstance(x, str));

def recEncode(d):
  """d と同じ構造で、 d の全ての unicode 要素に対して .encode('utf-8') を掛けたものを返す

  :param d: 任意の変数
  """
  return recApply(d, lambda x:x.encode('utf-8'), lambda x:isinstance(x, unicode));

class feature(object):
  """単一の feature を扱うためのクラス
  """
  def __init__(self, data):
    """feature を構成する

    :param data: 'geometry' と 'properties' を要素に持ったオブジェクト
    """
    self.load(data);
  def load(self, data):
    self.__geometry = shape(data['geometry']);
    self.__properties = recApply(data['properties'],lambda x:x.decode('utf-8'),lambda x:isinstance(x,str));
    self.__attributes = recApply({k:v for k,v in data.items() if k not in set(('geometry','properties','type'))},lambda x:x.decode('utf-8'),lambda x:isinstance(x,str));
    return self;
  def dump(self):
    return dict({'type':'Feature','geometry':mapping(self.__geometry), 'properties':recApply(self.__properties,lambda x:x.encode('utf-8'),lambda x:isinstance(x,unicode))},**recApply(self.__attributes,lambda x:x.encode('utf-8'),lambda x:isinstance(x,unicode)));
  def join(self, d):
    self.__properties = dict(self.__properties,**d);
    return self;
  @property
  def properties(self):
    return self.__properties;
  @property
  def geometry(self):
    return self.__geometry;
  @property
  def attributes(self):
    return self.__attributes;
  def isMatch(self, condition):
    return condition(self.__properties);

class features(object):
  def __init__(self, data):
    self.__data = None;
    self.load(data);
  def load(self, data):
    self.__data = [ feature(d) for d in data ];
    return self;
  def dump(self):
    if self.__data is None:
      return [];
    return [f.dump() for f in self.__data]
  def __iter__(self):
    if self.__data is None:
      raise StopIteration;
    return self.__data.__iter__();

class geoJson(object):
  def __init__(self, data):
    self.__features = None;
    self.__attributes = {};
    if isinstance(data, basestring):
      with open(data,'r') as f:
        self.load(json.loads(f.read()));
    elif hasattr(data, 'read'):
      self.load(json.loads(data.read()));
    else:
      self.load(data);
  def load(self, data):
    self.__attributes = recApply({k:v for k,v in data.items() if k not in set(('type','features'))},lambda x:x.decode('utf-8'),lambda x:isinstance(x,str));
    self.__features = features(data['features']);
    return self;
  def dump(self):
    if self.__features is None:
      return dict({'type': 'FeaturesCollection','features':[]},**recApply(self.__attributes,lambda x:x.encode('utf-8'),lambda x:isinstance(x,unicode)));
    return dict({'type': 'FeaturesCollection','features':self.__features.dump()},**recApply(self.__attributes,lambda x:x.encode('utf-8'),lambda x:isinstance(x,unicode)));
  def __str__(self):
    return json.dumps(self.dump());
  def __iter__(self):
    if self.__features is None:
      raise StopIteration;
    return self.__features.__iter__();
