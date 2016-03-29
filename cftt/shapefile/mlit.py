# -*- coding: utf-8 -*-

import os
import getpass
import json

from shp2geojson import mainFunc


def _pr(p):
    fm = {}
    with open(os.path.join(os.path.dirname(__file__),
                           'mlitfield.json')) as f:
        fm = json.loads(f.read())
    for k in p:
        if k not in fm:
            fm[k] = k
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


def _slproc(sl, args):
    ret = {
        'note': '国土交通省国土政策局「国土数値情報{0}」をもとに{1}が編集・加工'.format(
                (lambda x: '' if x is None else ' ('+x+')')(args.dataname),
                args.username or getpass.getuser()
            ),
        'editor': args.username or getpass.getuser()
    }
    if args.pub is not None:
        ret['publish-date'] = args.pub
    sl.attr(ret)
    return sl


def _aggrparams(args):
    return {
        'key': lambda f: tuple([f.properties['N03_007']])
        if 'N03_007' in f.properties else tuple(f.properties.keys())
    }


def _postproc(f):
    f.properties = _pr(f.properties)

if __name__ == '__main__':
    mainFunc(argparams=_argparams,
             slproc=_slproc,
             aggrparams=_aggrparams,
             postproc=_postproc)
