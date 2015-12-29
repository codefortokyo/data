# -*- coding: utf-8 -*-

import json;
import sys;
import os;
import uuid;

__default = {
  'app_host': '0.0.0.0',
  'app_port': 8000,
  'debug': False
};

__attr = {};

__configFileName = '.config.json';
__configFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),__configFileName);


def __export():
  try:
    f = open(__configFilePath, 'w');
    f.write(json.dumps(__attr,sort_keys=True,indent=2));
    f.close();
  except Exception as e:
    print 'config file created';

def __import():
  try:
    f = open(__configFilePath);
    sys.modules[__name__].__attr = json.loads(f.read());
    f.close();
  except Exception as e:
    print e;

def default(key):
  if key not in __default:
    return None;
  if hasattr(__default[key],'__call__'):
    return __default[key]();
  return __default[key];

def isDefined(key):
  return key in __attr;

def attr(*x):
  if len(x) == 0:
    return sys.modules[__name__];
  if len(x) == 1:
    if isinstance(x[0], list):
      return [ attr(key) for key in x[0] ];
    if isinstance(x[0], set):
      return { key: attr(key) for key in x[0] };
    if isinstance(x[0], dict):
      for k,v in x[0].items():
        attr(k,v);
      return sys.modules[__name__];
    if isinstance(x[0], str):
      if x[0] in __attr:
        return __attr[x[0]];
      return default(x[0]);
  if x[1] is None:
    if x[0] in __attr:
      del __attr[x[0]];
    __export();
    return sys.modules[__name__];
  __attr[x[0]] = x[1];
  __export();
  return sys.modules[__name__];

try:
  __import();
except:
  pass;
