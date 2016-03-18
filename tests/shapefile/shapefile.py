# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cftt.shapefile import shapeloader


class Tester(unittest.TestCase):

    def setUp(self):
        pass

    def test_ShapeLoader(self):
        l = shapeloader.ShapeLoader()
        l.attr('note', '本データの作成に当たっては、ESRIジャパン株式会社の全国市区町村界データを使用しました。本データの著作権はESRIジャパン株式会社に帰属します。')
        s = l('http://www.esrij.com/cgi-bin/wp/wp-content/uploads/2015/08/japan_ver80.zip')
        self.assertNotEqual(s, None)

    def test_Aggregate(self):
        l = shapeloader.ShapeLoader()
        s = l('http://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-15/N03-150101_13_GML.zip')
        self.assertNotEqual(s.aggregate(), None)

if __name__ == '__main__':
    unittest.main()
