# -*- coding: utf-8 -*-

import sys;

import collections;
import json;
import warnings

import manip;

import csv;
import StringIO;

def mainFunc():
  import argparse

  parser = argparse.ArgumentParser(description='filter geojson by property.');
  parser.add_argument('-i', '--input', action='store', dest='i', help='input file name (default: stdin)');
  parser.add_argument('-d', '--delimiter', action='store', dest='delim', help='delimitor for key string', default=',');
  parser.add_argument('key', action='store', help='key file name or raw string which represents join keys.');
  parser.add_argument('dictionary', action='store', help='dictionary file (json,csv or tsv) name');
  parser.add_argument('-o', '--output', action='store', dest='o', help='output file name (default: stdout)');

  args = parser.parse_args();

  keys = [];
  try:
    with open( args.key, 'r' ) as f:
      if args.key.endswith('.json'):
        d = json.dumps(f.read());
        if isinstance(d, basestring):
          keys = [ d ];
        elif isinstance(d, collections.Iterable):
          keys = [ k for k in d if isinstance(k, basestring) ];
      else:
        keys = csv.reader(f, delimiter=args.delim).next();
  except:
    try:
      keys = csv.reader(StringIO.StringIO(args.key), delimiter=args.delim).next();
    except:
      pass;
  if len(keys)==0:
    warnings.warn('invalid key');
    return;
  keys = manip.recDecode(keys);

  joinDict = {};
  try:
    with open (args.dictionary, 'r') as f:
      d = [];
      if args.dictionary.endswith('.json'):
        d = manip.recDecode(json.dumps(f.read()));
        if isinstance(d, collections.Mapping):
          d = [d];
      else:
        delim = ',';
        if args.dictionary.endswith('.tsv'):
          delim = '\t';
        r = csv.reader(f, delimiter=delim);
        h = r.next();
        d = manip.recDecode([ { k:v for k,v in zip(h,x) } for x in r ]);
      for x in d:
        try:
          key = tuple( x[k] for k in keys );
          joinDict[key] = manip.recApply( { k:v for k,v in x.items() if k not in set(key)}, lambda x:x.decode('utf-8'), lambda x:isinstance(x,str));
        except:
          warnings.warn(str(x) + ' is invalid record');
  except:
    warnings.warn(args.dictionary + ' is invalid');
    return;


  geojson = None;
  if args.i is not None:
    geojson = manip.geoJson(args.i);
  else:
    geojson = manip.geoJson(sys.stdin);

  for f in geojson:
    key = tuple( f.properties[k] if k in f.properties else None for k in keys );
    if key in joinDict:
      f.join(joinDict[key]);

  if args.o is not None:
    with open(args.o, 'w') as f:
      f.write(str(geojson));
  else:
    sys.stdout.write(str(geojson));

if __name__ == '__main__':
  mainFunc();
