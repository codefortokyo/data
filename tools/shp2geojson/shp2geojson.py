# -*- coding: utf-8 -*-

import sys;

import collections;

from shapely.geometry import shape, mapping;
from shapely.ops import cascaded_union;
import fiona;
from fiona.crs import to_string;
import json;

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

class shapeAggregator(object):
  def __init__(self):
    self.__key = lambda s,x: x.keys();
    self.__filter = lambda s,x: True;
    self.__prop = lambda s,p: {k:p[0][k] if k in p[0] else None for k in s.__key(s,p[0])};
    self.__geom = lambda s,g: mapping(cascaded_union(g));
    self.__features = None;
  def keys(self, k):
    if self.__features is not None:
      raise Exception('can\'t change key during aggregation');
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

def mainFunc(shpAggr):
  import argparse

  parser = argparse.ArgumentParser(description='shape files to geojson.');
  parser.add_argument('files', nargs='+');
  parser.add_argument('-o', '--output', action='store', dest='out', help='output file name (default: stdout)');

  args = parser.parse_args();

  crs = None;
  with fiona.drivers():
    for fn in args.files:
      with fiona.open(fn) as source:
        crs = to_string(source.crs);
        for s in source:
          shpAggr.add(s);
    if args.out is None:
      sys.stdout.write(json.dumps({'type': 'FeatureCollection','features': recApply(shpAggr.aggregate(),lambda x:x.encode('utf-8'),condition=lambda x:isinstance(x,unicode)),'crs': crs}, ensure_ascii=False));
    else:
      with open(args.out, 'w') as o:
        o.write(json.dumps({'type': 'FeatureCollection','features': recApply(shpAggr.aggregate(),lambda x:x.encode('utf-8'),condition=lambda x:isinstance(x,unicode)),'crs': crs}, ensure_ascii=False));


if __name__ == '__main__':
  mainFunc(shapeAggregator());
