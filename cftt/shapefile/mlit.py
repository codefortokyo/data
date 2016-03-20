# -*- coding: utf-8 -*-

import sys
import json

from shapeloader import ShapeLoader
from .. feature.featurecollection import FeatureCollection

field_map = {
    "N03_001": "都道府県名",
    "N03_002": "支庁・振興局名",
    "N03_003": "郡・政令都市名",
    "N03_004": "市区町村名",
    "N03_007": "行政区域コード"
}

note_format = '国土交通省国土政策局「国土数値情報{0}」をもとに{1}が編集・加工'


def mainFunc():
    import argparse
    import getpass

    parser = argparse.ArgumentParser(description='shape files to geojson.')
    parser.add_argument('input', nargs='+')
    parser.add_argument('-d', '--dataname', action='store', dest='dataname',
                        help='name of data (default: empty)')
    parser.add_argument('-e', '--encode', action='store', dest='encode',
                        help='encoding (default: utf-8)', default='utf-8')
    parser.add_argument('-a', '--author', action='store', dest='author',
                        help='author name (default: login user name)')
    parser.add_argument('-o', '--output', action='store', dest='out',
                        help='output file name (default: stdout)')

    args = parser.parse_args()

    note = note_format.format(
        (lambda x: '' if x is None else ' ('+x+')')(args.dataname),
        args.author or getpass.getuser()
    )

    sl = ShapeLoader(note=note)
    fc = FeatureCollection(*map(lambda x: sl(x), args.input))

    if args.out is None:
        sys.stdout.write(json.dumps(fc.dump(encode=args.encode),
                                    ensure_ascii=False))
    else:
        with open(args.out, 'w') as o:
            o.write(json.dumps(fc.dump(encode=args.encode),
                               ensure_ascii=False))


if __name__ == '__main__':
    mainFunc()
