# -*- coding: utf-8 -*-

import sys
import os
import unittest
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class ShapeLoaderTester(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        from cftt.shapefile.shapeloader import ShapeLoader
        test = ShapeLoader()
        s = test()
        self.assertEqual(len(s), 0)
        self.assertEqual(s.attr(), {})
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
        


if __name__ == '__main__':
    unittest.main()
