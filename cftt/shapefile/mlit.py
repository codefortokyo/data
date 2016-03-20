# -*- coding: utf-8 -*-

import getpass

from shp2geojson import mainFunc


def _pr(p):
    fm = {
        "N03_001": "都道府県名",
        "N03_002": "支庁・振興局名",
        "N03_003": "郡・政令都市名",
        "N03_004": "市区町村名",
        "N03_007": "行政区域コード"
    }
    codes = {}
    if 'N03_007' in p:
        if p['N03_007'] is not None:
            codes['都道府県コード'] = p['N03_007'][:2]
            codes['市区町村コード'] = p['N03_007'][2:]
        else:
            codes['都道府県コード'] = None
            codes['市区町村コード'] = None
    return dict({fm[k]: v for k, v in p.items()}, **codes)


def _argparams(parser):
    parser.add_argument('-d', '--dataname', action='store', dest='dataname',
                        help='name of data (default: empty)')
    parser.add_argument('-u', '--username', action='store', dest='username',
                        help='editor name (default: login user name)')
    parser.add_argument('-p', '--publishdate', action='store', dest='pub',
                        help='publish date of this data')
    return parser


def _slparams(args):
    ret = {
        'note': '国土交通省国土政策局「国土数値情報{0}」をもとに{1}が編集・加工'.format(
                (lambda x: '' if x is None else ' ('+x+')')(args.dataname),
                args.username or getpass.getuser()
            ),
        'editor': args.username or getpass.getuser()
    }
    if args.pub is not None:
        ret['publish-date'] = args.pub
    return ret


def _aggrparams(args):
    return {
        'key': lambda f: tuple([f.properties['N03_007']])
    }


def _postproc(f):
    f.properties = _pr(f.properties)

if __name__ == '__main__':
    mainFunc(argparams=_argparams,
             slparams=_slparams,
             aggrparams=_aggrparams,
             postproc=_postproc)
