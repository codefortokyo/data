# -*- coding: utf-8 -*-

import sys;

import collections;
import json;
import warnings

def mainFunc():
  import argparse

  parser = argparse.ArgumentParser(description='filter geojson by property.');
  parser.add_argument('-i', '--input', action='store', dest='i', help='input file name (default: stdin)');
  parser.add_argument('key', action='store', help='key to join');
  parser.add_argument('dictionary', action='append', nargs='+', help='dictionary file (json) name or python dictionary object');
  parser.add_argument('-o', '--output', action='store', dest='o', help='output file name (default: stdout)');

  args = parser.parse_args();

  joinDict = {};
  for s in reduce(lambda x,y:x+y, args.dictionary,[]):
    try:
      with open(s, 'r') as f:
        joinDict = dict(joinDict, **json.loads(f.read()));
    except Exception as e:
      warnings.warn(str(e));
      try:
        d = eval(s);
        joinDict = dict(joinDict, **d);
      except:
        warnings.warn('dictionary ' + s + ' does not work');

  geojson = None;
  if args.i is not None:
    with open(args.i, 'r') as f:
      geojson = json.loads(f.read());
  else:
    geojson = json.loads(sys.stdin.read());
  for f in geojson['features']:
    if args.key in f['properties']:
      if f['properties'][args.key] in joinDict:
        for k,v in joinDict[f['properties'][args.key]].items():
          f['properties'][k] = v;
  if args.o is not None:
    with open(args.o, 'w') as f:
      f.write(json.dumps(geojson));
  else:
    sys.stdout.write(json.dumps(geojson));

if __name__ == '__main__':
  mainFunc();
