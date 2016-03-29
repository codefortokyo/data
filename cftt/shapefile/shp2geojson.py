# -*- coding: utf-8 -*-

import sys
import json
from datetime import datetime

from .. common import util
from shapeloader import ShapeLoader
from .. feature.featurecollection import FeatureCollection


def mainFunc(argparams=None, slproc=None, aggrparams=None, postproc=None):
    import argparse

    parser = argparse.ArgumentParser(description='shape files to geojson.')
    parser.add_argument('input', nargs='+',
                        help='path to shape file or zip file, URL to zip file')
    parser.add_argument('-e', '--encode', action='store', dest='encode',
                        help='outencoding (default: utf-8)', default='utf-8')
    parser.add_argument('-o', '--output', action='store', dest='out',
                        help='output file name (default: stdout)')
    parser.add_argument('-a', '--aggregate', action='store_true', dest='aggr',
                        help='aggregate the output (default: False)')

    if argparams is not None:
        argparams(parser)

    args = parser.parse_args()

    sl = ShapeLoader(timestamp=util.dt2ts(datetime.now()))
    if slproc is not None:
        slproc(sl, args)

    fc = FeatureCollection(*map(lambda x: sl(x), args.input))
    if args.aggr:
        if aggrparams is not None:
            fc = fc.aggregate(**aggrparams(args))
        else:
            fc = fc.aggregate()

    if postproc is not None:
        for f in fc:
            f = postproc(f)

    if args.out is None:
        sys.stdout.write(json.dumps(fc.dump(encoding=args.encode),
                                    ensure_ascii=False))
    else:
        with open(args.out, 'w') as o:
            o.write(json.dumps(fc.dump(encoding=args.encode),
                               ensure_ascii=False))

if __name__ == '__main__':
    mainFunc()
