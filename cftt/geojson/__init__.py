# -*- coding: utf-8 -*-

import sys;
import os;

import json;
import urllib2;

import collections;

from shapely.geometry import shape, mapping;
from shapely.ops import cascaded_union;

class geoJson(object):
  """geoJson オブジェクト。
  """
  def __init__(self, d):
    """geoJson オブジェクトのコンストラクタ
    :param d: 初期化するためのデータ。load 関数に準ずる
    """
    super(geoJson, self).__init__();
    self.load(d);
