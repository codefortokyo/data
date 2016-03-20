# -*- coding: utf-8 -*-

from .. feature.featurecollection import FeatureCollection

m = {
    "N03_001": "都道府県名",
    "N03_002": "支庁・振興局名",
    "N03_003": "郡・政令都市名",
    "N03_004": "市区町村名",
    "N03_007": "行政区域コード"
}


def mainFunc():
    import argparse

    parser = argparse.ArgumentParser(description='shape files to geojson.')
    parser.add_argument('input', nargs='+')
    parser.add_argument('-o', '--output', action='store', dest='out',
                        help='output file name (default: stdout)')

    args = parser.parse_args()

    fc = reduce(lambda x, y: x + y,
                [FeatureCollection(src) for src in args.input])

    if args.out is None:
        sys.stdout.write(json.dumps(fc.dump(), ensure_ascii=False))
    else:
        with open(args.out, 'w') as o:
            o.write(json.dumps(fc.dump(), ensure_ascii=False))


if __name__ == '__main__':
    mainFunc()
