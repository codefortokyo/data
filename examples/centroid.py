# -*- coding: utf-8 -*-

import sys
import os
import csv
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from cftt.common.feature import Feature
from cftt.common import util


if __name__ == '__main__':
    """load geojson from standard input,
    compute the centroid of the each feature then output
    it with each properties.
    """
    r = json.loads(sys.stdin.read())
    f = map(lambda x: Feature(x), r['features'])
    for g in f:
        c = g.geometry.centroid
        g.property({'centroid_x': c.x, 'centroid_y': c.y})
    keys = f[0].properties.keys()
    w = csv.writer(sys.stdout, lineterminator='\n')
    w.writerow(util.rec_encode(keys))
    for g in f:
        w.writerow(util.rec_encode(g.property(keys)))
