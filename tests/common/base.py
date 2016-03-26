# -*- coding: utf-8 -*-


import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class DecodedDictTester(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict()
        self.assertEqual(test._elements, {})
        test = _DecodedDict(((1, 2), ('a', 3)))
        self.assertEqual(test._elements, {u'1': 2, u'a': 3})
        test = _DecodedDict(((1, 2), ('a', 3)), i=1, j=2)
        self.assertEqual(test._elements,
                         {u'1': 2, u'a': 3, u'i': 1, u'j': 2})

    def test__getitem__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict({'a': 1, 'b': (1, 2, 3), 'あ': 3})
        decoded = 'あ'.decode('utf-8')
        self.assertEqual(test['a'], 1)
        self.assertEqual(test[u'a'], 1)
        self.assertEqual(test['b'], (1, 2, 3))
        self.assertEqual(test[('a', 'b')], (1, (1, 2, 3)))
        self.assertEqual(test[decoded], 3)
        self.assertEqual(test['あ'], 3)
        self.assertEqual(test[set(('a', 'あ'))], {'a': 1, decoded: 3})
        self.assertEqual(test[{'k1': 'a', 'k2': 'あ'}], {'k1': 1, 'k2': 3})
        self.assertEqual(test[{'k': ('a', ['a'], set(('a', 'あ')))}],
                         {'k': (1, [1], {'a': 1, decoded: 3})})

    def test__setitem__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict({'a': 1, 'b': (1, 2, 3), 'あ': 3})
        decoded = 'あ'.decode('utf-8')
        self.assertEqual(test._elements['a'], 1)
        self.assertNotIn('c', test._elements)
        test[{'k1': 'a', 'k2': 'c'}] = 4
        self.assertEqual(test._elements['a'], 4)
        self.assertEqual(test._elements['c'], 4)
        test['c'] = None
        self.assertNotIn('c', test._elements)
        test['あ'] = 5
        self.assertEqual(test._elements[decoded], 5)
        test['a'] = ('あ', 'い')
        self.assertEqual(test._elements['a'],
                         (decoded, 'い'.decode('utf-8')))

    def test__delitem__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(a=1, b=2, c=3, d=4, e=5, f=6)
        self.assertEqual(test._elements,
                         dict(a=1, b=2, c=3, d=4, e=5, f=6))
        del test['a']
        self.assertEqual(test._elements,
                         dict(b=2, c=3, d=4, e=5, f=6))
        del test['a']
        self.assertEqual(test._elements,
                         dict(b=2, c=3, d=4, e=5, f=6))
        del test[('b', 'c')]
        self.assertEqual(test._elements,
                         dict(d=4, e=5, f=6))
        del test[{'k': 'f'}]
        self.assertEqual(test._elements,
                         dict(d=4, e=5))

    def test__iter__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(a=1, b=2)
        for x, y in zip(test, dict(a=1, b=2)):
            self.assertEqual(x, y)

    def test__len__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(a=1, b=2)
        self.assertEqual(len(test), 2)
        del test['a']
        self.assertEqual(len(test), 1)

    def test__call__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(a=1, b=2)
        self.assertEqual(test._elements, dict(a=1, b=2))
        self.assertEqual(test('a'), 1)
        self.assertEqual(test(['a', 'b']), [1, 2])
        self.assertEqual(test(('b', 'b')), (2, 2))
        self.assertEqual(test(set(('b', 'a'))), dict(a=1, b=2))
        self.assertEqual(test('b', 'a')._elements, dict(a=1, b='a'))
        self.assertEqual(test(dict(c=0))._elements, dict(a=1, b='a', c=0))
        self.assertEqual(test(dict(c=None))._elements, dict(a=1, b='a'))

    def test__contains__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        self.assertTrue('a' in test)
        self.assertTrue(test.__contains__('a'))
        self.assertTrue('あ' in test)
        self.assertFalse('b' in test)
        self.assertTrue(test.__contains__(('a', 'あ')))
        self.assertFalse(test.__contains__(('a', 'b')))

    def test__keys(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        decoded = 'あ'.decode('utf-8')
        self.assertEqual(set(test.keys()), set((decoded, 'a')))
        del test['あ']
        self.assertEqual(set(test.keys()), set(('a',)))
        test.keys()[0] = 0
        self.assertEqual(test._elements, {'a': 2})

    def test_values(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        decoded = 'あ'.decode('utf-8')
        self.assertEqual(set(test.values()), set((1, 2)))
        del test['あ']
        self.assertEqual(set(test.values()), set((2,)))
        test.values()[0] = 0
        self.assertEqual(test._elements, {'a': 2})

    def test_items(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        decoded = 'あ'.decode('utf-8')
        self.assertEqual(set(test.items()), set(((decoded, 1), ('a', 2))))
        del test['あ']
        self.assertEqual(set(test.items()), set((('a', 2),)))
        test.items()[0] = ('a', 0)
        self.assertEqual(test._elements, {'a': 2})

    def test__eq__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        self.assertTrue(test.__eq__(dict((('あ', 1), ('a', 2)))))
        self.assertFalse(test.__eq__(dict((('あ', 2), ('a', 2)))))
        self.assertTrue(test == dict((('あ', 1), ('a', 2))))
        self.assertFalse(test == dict((('あ', 2), ('a', 2))))

    def test__ne__(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        self.assertFalse(test.__ne__(dict((('あ', 1), ('a', 2)))))
        self.assertTrue(test.__ne__(dict((('あ', 2), ('a', 2)))))
        self.assertFalse(test != dict((('あ', 1), ('a', 2))))
        self.assertTrue(test != dict((('あ', 2), ('a', 2))))

    def test_pop(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        decoded = 'あ'.decode('utf-8')
        self.assertEqual(test.pop(['a', 'x'], 8), 8)
        self.assertEqual(test._elements, {decoded: 1, 'a': 2})
        self.assertEqual(test.pop(['a'], 9), [2])

    def test_get(self):
        from cftt.common.base import _DecodedDict
        test = _DecodedDict(dict((('あ', 1), ('a', 2))))
        self.assertEqual(test.get('a'), test['a'])
        self.assertNotEqual(test.get('x', 0), test['x'])


class BaseAttributeTester(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute()
        self.assertEqual(len(test._attributes), 0)
        test = BaseAttribute(aa=123, bb=234)
        self.assertEqual(len(test._attributes), 2)
        self.assertEqual(test._attributes['aa'], 123)
        self.assertEqual(test._attributes['bb'], 234)

    def test_attr(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute()
        test.attr('id', 'a123')
        self.assertEqual(test, test.attr())
        self.assertEqual(test.attr('id'), test._attributes['id'])
        self.assertEqual(test.attr('id'), 'a123')
        test.attr({'id2': 'b234', 'id3': 345})
        self.assertEqual(test, test.attr())
        self.assertEqual(test.attr('id2'), 'b234')
        self.assertEqual(test.attr('id3'), 345)
        test.attr('id', None)
        self.assertNotIn('id', test._attributes)
        self.assertEqual([345, 'b234', 345],
                         test.attr(['id3', 'id2', 'id3']))
        self.assertEqual({'id2': 'b234', 'id3': 345},
                         test.attr(set(('id2', 'id3'))))
        test.attr('日本語', '日本語')
        decoded = '日本語'.decode('utf-8')
        self.assertIn(decoded, test._attributes)
        self.assertEqual(test.attr(decoded), decoded)
        self.assertEqual(test.attr('日本語'), decoded)
        self.assertIsNone(test.attr('id'))
        test.attr((1, 2), '日本語')
        print test._attributes
        print test.attr((1, 2))

    def test_clear_attributes(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute(aa=123, bb=234)
        self.assertEqual(test._attributes, {'aa': 123, 'bb': 234})
        test.clear_attributes()
        self.assertNotEqual(test._attributes, {'aa': 123, 'bb': 234})
        self.assertNotEqual(test._attributes, {u'aa': 123, u'bb': 234})
        self.assertEqual(test._attributes, {})

    def test_attribute_keys(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute(aa=123, bb=234)
        self.assertEqual(set(test.attribute_keys()), set([u'aa', u'bb']))
        test.attribute_keys()[0] = u'xx'
        self.assertEqual(set(test.attribute_keys()), set([u'aa', u'bb']))

    def test_attribute_values(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute(aa=123, bb=234)
        self.assertEqual(set(test.attribute_values()), set([123, 234]))
        test.attribute_values()[0] = u'xx'
        self.assertEqual(set(test.attribute_values()), set([123, 234]))

    def test_attribute_items(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute(aa=123, bb=234)
        self.assertEqual(test.attribute_items(),
                         dict(((u'aa', 123), (u'bb', 234))))
        test.attribute_items()['aa'] = u'xx'
        self.assertEqual(test.attribute_items(),
                         dict(((u'aa', 123), (u'bb', 234))))

    def test_attributes_getter(self):
        from cftt.common.base import BaseAttribute
        test = BaseAttribute(aa=123, bb=234)
        self.assertEqual(test.attributes,
                         dict(((u'aa', 123), (u'bb', 234))))
        test.attributes['aa'] = u'xx'
        self.assertEqual(test.attributes,
                         dict(((u'aa', 123), (u'bb', 234))))


if __name__ == '__main__':
    unittest.main()
