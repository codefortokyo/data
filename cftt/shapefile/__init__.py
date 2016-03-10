# -*- coding: utf-8 -*-

import sys;
import os;

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'));

import util;

import json;
import urllib2;

import collections;

from shapely.geometry import shape, mapping;
from shapely.ops import cascaded_union;
import fiona;
from fiona.crs import to_string;

import collections;

class feature(object):
  """単一の feature を扱うためのクラス
  """
  def __init__(self, data):
    """feature を構成する

    :param data: 'geometry' と 'properties' を属性に持った Mapping オブジェクト
    """
    self.load(data);
  def load(self, data):
    """data を元に feature を構成する

    :param data: 'geometry' と 'properties' を属性に持った Mapping オブジェクト
    """
    self.__geometry = shape(data['geometry']);
    self.__properties = recApply(data['properties'],lambda x:x.decode('utf-8'),lambda x:isinstance(x,str));
    self.__attributes = recApply({k:v for k,v in data.items() if k not in set(('geometry','properties','type'))},lambda x:x.decode('utf-8'),lambda x:isinstance(x,str));
    return self;
  def dump(self):
    """このインスタンスを表す、json.dumpsなどでダンプ可能なオブジェクトを返す
    """
    return dict({'type':'Feature','geometry':mapping(self.__geometry), 'properties':recApply(self.__properties,lambda x:x.encode('utf-8'),lambda x:isinstance(x,unicode))},**recApply(self.__attributes,lambda x:x.encode('utf-8'),lambda x:isinstance(x,unicode)));
  def join(self, d):
    """d のキーヴァリューの組をこのインスタンスの properties に追加する

    :param d: Mapping オブジェクト
    """
    self.__properties = dict(self.__properties,**d);
    return self;
  @property
  def properties(self):
    """このインスタンスの properties オブジェクト自体を返す
    """
    return self.__properties;
  @property
  def geometry(self):
    """このインスタンスの geometry オブジェクト自体を返す
    """
    return self.__geometry;
  @property
  def attributes(self):
    """このインスタンスのその他の属性の Mapping オブジェクトを返す
    """
    return self.__attributes;
  def isMatch(self, condition):
    """このインスタンスの properties が condition に一致しているかどうか返す

    :param condition: 一つの引数（propertiesが渡される）を取る関数
    """
    return condition(self.__properties);

class shapeHandler(collections.Iterable):
  def __init__(self, x):
    super(shapeHandler, self).__init__();
  def load(self, x):
    if isinstance(x, shapeHandler):
      self.__features = x.__features;
    elif

class shapeAggregator(collections.Iterable):
  def __init__(self):
    self.__key = lambda s,x: x.keys();
    self.__filter = lambda s,x: True;
    self.__prop = lambda s,p: {k:p[0][k] if k in p[0] else None for k in s.__key(s,p[0])};
    self.__geom = lambda s,g: mapping(cascaded_union(g));
    self.__features = None;
  def key(self, k):
    """
    """
    if k is not None:
      self.__key = lambda s,x: k;
    return self;
  def prop(self, f):
    if self.__features is not None:
      raise Exception('can\'t change property aggregator during aggregation');
    if f is not None:
      self.__prop = f;
    return self;
  def geom(self, f):
    if self.__features is not None:
      raise Exception('can\'t change geomety aggregator during aggregation');
    if f is not None:
      self.__geom = f;
    return self;
  def filter(self, f):
    if self.__features is not None:
      raise Exception('can\'t change filter during aggregation');
    if f is not None:
      self.__filter = f;
    return self;
  def add(self, f):
    if self.__features is None:
      self.__features = {};
    if self.__filter(self, f):
      t = tuple( f['properties'][k] if k in f['properties'] else None for k in self.__key(self,f['properties']) );
      if t not in self.__features:
        self.__features[t] = {'p': [], 'g': []};
      self.__features[t]['p'].append(f['properties']);
      self.__features[t]['g'].append(shape(f['geometry']));
  def aggregate(self):
    return [ {'id': i+1,'properties': self.__prop(self,v['p']), 'geometry': self.__geom(self,v['g']), 'type': 'Feature'} for i,v in enumerate(self.__features.values()) ];
