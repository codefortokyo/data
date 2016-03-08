# -*- coding: utf-8 -*-

import sys;
import os;

sys.path.insert(0, os.path.dirname(__file__));

import util;

import json;
import urllib2;

import collections;

from shapely.geometry import shape, mapping;
from shapely.ops import cascaded_union;

class feature(object):
  """feature オブジェクト。
  """
  def __init__(self, d):
    """feature オブジェクトの初期化
    :param d: 初期化するためのデータ。load 関数に準ずる
    """
    super(feature, self).__init__();
    self.load(d);
  def construct(self, geom, prop, attr):
    """feature オブジェクトを構成する
    :param geom: shape オブジェクト
    :param prop: Mapping オブジェクト
    :param attr: Mapping オブジェクト
    """

  def load(self, d):
    """feature オブジェクトを d から構成する
    :param d: 'geometry', 'properties' を持つMappingオブジェクトかfeatureインスタンス
    """
    if isinstance(d, feature):
      self.__geometry = d.__geometry;
      self.__attributes = d.__attributes;
      self.__properties = d.__properties;
    else:


class geoJson(object):
  """geoJson オブジェクト。
  """
  def __init__(self, d):
    """geoJson オブジェクトのコンストラクタ
    :param d: 初期化するためのデータ。load 関数に準ずる
    """
    super(geoJson, self).__init__();
    self.__attributes = {};
    self.__features = [];
    self.load(d);
  def load(self, d, clear=True):
    """d から geoJson をロードする関数。
    d に文字列を渡すと、URL だった場合はその URL からダウンロードしたものを、ファイル名だった場合はそのファイルを読み込む。
    d に read 可能なオブジェクトを渡すと、それを read したものを読み込む。
    d に辞書型オブジェクトを渡すと、それをgeojsonだと解釈して読み込みを試みる。'features'属性が必要。
    """
    if isinstance(d, collections.Mapping):
