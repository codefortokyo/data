# -*- coding: utf-8 -*-

import sys
import os
import unittest
import uuid

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)


class ShapeLoaderTester(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        from cftt.shapefile.shapeloader import ShapeLoader
        test = ShapeLoader()
        s = test()
        self.assertEqual(len(s), 0)
        self.assertEqual(s.attributes, {})
        test.attr('note', 'あ')
        s = test()
        self.assertEqual(s.attributes, {u'note': 'あ'.decode('utf-8')})
        test = ShapeLoader(one=1, two=2)
        s = test({'features': [
            {'type': 'feature',
             'properties': {},
             'geometry': {'type': 'Point', 'coordinates': [0.0, 0.0]}}],
            'three': 3})
        self.assertEqual(s.attributes,
                         {u'one': 1, u'two': 2, u'three': 3})
        self.assertEqual(len(s), 1)

    def test__call__(self):
        from cftt.shapefile.shapeloader import ShapeLoader
        id = uuid.uuid4()
        test = ShapeLoader(id=id)
        s = test()
        self.assertEqual(s.attributes['id'], id)
        self.assertEqual(len(s), 0)
        self.assertEqual(len(s.attributes), 1)
        s = test({'features': [
            {'type': 'feature',
             'properties': {},
             'geometry': {'type': 'Point', 'coordinates': [0.0, 0.0]}}],
            'three': 3})
        self.assertEqual(s.attributes['id'], id)
        self.assertEqual(s.attributes,
                         {u'three': 3, u'id': id})
        self.assertEqual(len(s), 1)
        test.attr('two', 2)
        t = test(s)
        self.assertEqual(s.attributes['id'], id)
        self.assertEqual(s.attributes,
                         {u'three': 3, u'id': id})
        self.assertEqual(len(s), 1)
        self.assertEqual(t.attributes,
                         {u'three': 3, u'id': id, u'two': 2})
        test_data_dir = os.path.join(PROJECT_ROOT, 'test_data')
        shp = os.path.join(test_data_dir, 'shapefile', 'test_uk.shp')
        s = test(shp)
        self.assertEqual(len(s), 48)
        t = test._load_from_shp(shp)
        self.assertEqual(s.attributes, t.attributes)
        self.assertEqual(len(s), len(t))
        zip = os.path.join(test_data_dir, 'test_uk.zip')
        s = test(zip)
        self.assertEqual(len(s), 48)
        t = test._load_from_zip(zip)
        self.assertEqual(s.attributes, t.attributes)
        self.assertEqual(len(s), len(t))
        from cftt.common.asyncfileserver import AsyncFileServer
        with AsyncFileServer():
            url = 'http://localhost:8000/test_data/test_uk.zip'
            s = test(url)
            self.assertEqual(len(s), 48)
            t = test._load_from_url(url)
            self.assertEqual(s.attributes, t.attributes)
            self.assertEqual(len(s), len(t))


if __name__ == '__main__':
    unittest.main()
