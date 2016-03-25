# -*- coding: utf-8 -*-

import sys
import json
from datetime import datetime

from .. common import util
from .. feature.featurecollection import FeatureCollection
from geojsonloader import GeoJSONLoader


def mainFunc(argproc=None, glproc=None, aggrparams=None, fcpostproc=None,
             fpostproc=None):
    import argparse

    parser = argparse.ArgumentParser(description='geojson manipulation.')
    parser.add_argument(
        'input', nargs='*',
        help='''path to geojson file or zip file, URL to resources.
        (default: stdin)'''
    )
    parser.add_argument('-e', '--encode', action='store', dest='encode',
                        help='output encoding (default: utf-8)',
                        default='utf-8')
    parser.add_argument('-o', '--output', action='store', dest='out',
                        help='output file name (default: stdout)')
    parser.add_argument('-a', '--aggregate', action='store_true', dest='aggr',
                        help='aggregate the output (default: False)')

    if argproc is not None:
        argproc(parser)

    args = parser.parse_args()

    gl = GeoJSONLoader(timestamp=util.dt2ts(datetime.now()))
    if glproc is not None:
        glproc(gl, args)

    fc = FeatureCollection()
    if len(args.input) == 0:
        fc = gl(sys.stdin)
    else:
        for i in args.input:
            fc += gl(i)

    if args.aggr:
        if aggrparams is not None:
            fc = fc.aggregate(**aggrparams(args))
        else:
            fc = fc.aggregate()

    if fpostproc is not None:
        for f in fc:
            fpostproc(f, args)

    if fcpostproc is not None:
        fcpostproc(fc, args)

    if args.out is None:
        sys.stdout.write(json.dumps(fc.dump(encoding=args.encode),
                                    ensure_ascii=False))
    else:
        with open(args.out, 'w') as o:
            o.write(json.dumps(fc.dump(encoding=args.encode),
                               ensure_ascii=False))

if __name__ == '__main__':
    mainFunc()
