# -*- coding: utf-8 -*-

import sys;

import collections;
import json;
import warnings

def mergeWithDict(f, d):
  for k,v in d.items():
    if k not in f:
      f[k] = set();
    if isinstance(v, collections.Iterable) and not isinstance(v, basestring):
      for x in v:
        f[k].add(x);
    else:
      f[k].add(v);

def mainFunc():
  import argparse

  parser = argparse.ArgumentParser(description='filter geojson by property.');
  parser.add_argument('-i', '--input', action='store', dest='i', help='input file name (default: stdin)');
  parser.add_argument('filters', action='append', nargs='+', help='filter file name or python dictionary object');
  parser.add_argument('-o', '--output', action='store', dest='o', help='output file name (default: stdout)');

  args = parser.parse_args();

  filterDict = {};
  for s in reduce(lambda x,y:x+y, args.filters,[]):
    try:
      with open(s, 'r') as f:
        mergeWithDict(filterDict, json.loads(f.read()));
    except Exception as e:
      warnings.warn(str(e));
      try:
        d = eval(s);
        mergeWithDict(filterDict, d);
      except:
        warnings.warn('filter ' + s + ' does not work');
  geojson = None;
  if args.i is not None:
    with open(args.i, 'r') as f:
      geojson = json.loads(f.read());
  else:
    geojson = json.loads(sys.stdin.read());
  reduced = [];
  for f in geojson['features']:
    flg = True;
    for k,v in filterDict.items():
      flg = f['properties'][k] in v;
      if not flg:
        break;
    if flg:
      reduced.append(f);
  geojson['features'] = reduced;
  if args.o is not None:
    with open(args.o, 'w') as f:
      f.write(json.dumps(geojson));
  else:
    sys.stdout.write(json.dumps(geojson));


if __name__ == '__main__':
  mainFunc();
