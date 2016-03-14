# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cftt.shapefile import shapefile


class Tester(unittest.TestCase):

    def setUp(self):
        pass

    def test_ShapeLoader(self):
        s = shapefile.ShapeLoader()('http://osoken.jp/osoken/cft/data/estat/shp_zip/A002005212000DDSWC13101.zip')
        self.assertNotEqual(s, None)

if __name__ == '__main__':
    unittest.main()
