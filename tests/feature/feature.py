# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class FeatureTester(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        from cftt.feature.feature import Feature
        test = Feature()
        test2 = Feature()
        test2.load()
        self.assertEqual(test.geometry, test2.geometry)
        self.assertEqual(test.attributes, test2.attributes)
        self.assertEqual(test.properties, test2.properties)
        test = Feature({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [(0, 0)]},
            'properties': {},
            'attr1': 1,
            'attr2': '日本語'
        })
        test2.load({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [(0, 0)]},
            'properties': {},
            'attr1': 1,
            'attr2': '日本語'
        })
        self.assertEqual(test.geometry, test2.geometry)
        self.assertEqual(test.attributes, test2.attributes)
        self.assertEqual(test.properties, test2.properties)
        test3 = Feature({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [(1, 1)]},
            'properties': {'あ': 'い'},
            'attr1': 1,
            'attr2': '日本語'
        })
        test = Feature(test3)
        test2 = Feature(test3)
        self.assertEqual(test.geometry, test2.geometry)
        self.assertEqual(test.attributes, test2.attributes)
        self.assertEqual(test.properties, test2.properties)
        test2.attr('attr3', 3)
        self.assertEqual(test.geometry, test2.geometry)
        self.assertNotEqual(test.attributes, test2.attributes)
        self.assertEqual(test.properties, test2.properties)
        test.property('prop', 3)
        test2.attr('attr3', None)
        self.assertEqual(test.geometry, test2.geometry)
        self.assertEqual(test.attributes, test2.attributes)
        self.assertNotEqual(test.properties, test2.properties)
        test.geometry = test.geometry.buffer(1)
        test.property('prop', None)
        self.assertNotEqual(test.geometry, test2.geometry)
        self.assertEqual(test.attributes, test2.attributes)
        self.assertEqual(test.properties, test2.properties)

    def test_load(self):
        from cftt.feature.feature import Feature
        from shapely.geometry import mapping
        test = Feature()
        test.load()
        self.assertEqual(test.attributes, {})
        self.assertEqual(test.properties, {})
        self.assertIsNone(test.geometry)
        self.assertRaises(KeyError, Feature, {})
        self.assertRaises(Exception, Feature, {'geometry': {}})
        self.assertRaises(KeyError, Feature,
                          {
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [(0, 0)]
                            }
                          })
        self.assertRaises(KeyError, Feature,
                          {
                            'properties': {}
                          })
        test.load({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [(1, 1)]},
            'properties': {'あ': 'い'},
            'attr1': 1,
            'attr2': '日本語'
        })
        self.assertEqual(test.attributes,
                         {'attr1': 1, 'attr2': '日本語'.decode('utf-8')})
        self.assertEqual(test.properties,
                         {'あ'.decode('utf-8'): 'い'.decode('utf-8')})
        self.assertIsNotNone(test.geometry)
        self.assertEqual(mapping(test.geometry),
                         {'type': 'Point', 'coordinates': (1.0, 1.0)})

    def test_dump(self):
        from cftt.feature.feature import Feature
        from shapely.geometry import mapping
        test = Feature()
        self.assertEqual(
            test.dump(),
            {u'geometry': None, u'properties': {}, u'type': u'Feature'}
        )

if __name__ == '__main__':
    unittest.main()
