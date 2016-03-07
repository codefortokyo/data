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

  parser = argparse.ArgumentParser(description='extract properties from the input geojson and dump  into csv.');
  parser.add_argument('-i', '--input', action='store', dest='i', help='input file name (default: stdin)');
  parser.add_argument('-d', '--delimiter', action='store', dest='d', help='delimiter (default: ,)', default=',');
  parser.add_argument('-o', '--output', action='store', dest='o', help='output file name (default: stdout)');

  args = parser.parse_args();

  geojson = None;
  if args.i is not None:
    geojson = manip.geoJson(args.i);
  else:
    geojson = manip.geoJson(sys.stdin);

  header = set();
  for f in geojson:
    header = header.union(f.properties.keys());

  header = list(header);

  if args.o is not None:
    with open(args.o, 'w') as f:
      w = csv.writer(f, delimiter=args.d, lineterminator='\n');
      w.writerow(manip.recEncode(header));
      for g in geojson:
        w.writerow(manip.recEncode( [g.properties[k] if k in g.properties else None for k in header ] ));
  else:
    w = csv.writer(sys.stdout, delimiter=args.d, lineterminator='\n');
    w.writerow(manip.recEncode(header));
    for g in geojson:
      w.writerow(manip.recEncode( [g.properties[k] if k in g.properties else None for k in header ] ));

if __name__ == '__main__':
  mainFunc();
