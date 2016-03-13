# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cftt.common import util


class Tester(unittest.TestCase):

    def setUp(self):
        pass

    def test_const(self):
        f = util.const(1)
        self.assertEqual(1, f(123214))
        self.assertEqual(1, f('ABC'))
        self.assertEqual(1, f(a=1, b=2))

    def test_gen_id(self):
        i1 = util.gen_id()
        i2 = util.gen_id()
        self.assertNotEqual(i1, i2)

    def test_is_map(self):
        self.assertTrue(util.is_map({}))
        self.assertFalse(util.is_map([]))
        self.assertFalse(util.is_map('abc'))

    def test_is_string(self):
        self.assertTrue(util.is_string('にほんご'))
        self.assertTrue(util.is_string(u'1234'))
        self.assertTrue(util.is_string('全角'.decode('utf-8')))
        self.assertFalse(util.is_string([]))

    def test_is_array(self):
        self.assertTrue(util.is_array([]))
        self.assertFalse(util.is_array({}))
        self.assertFalse(util.is_array('abc'))

    def test_is_callable(self):
        self.assertTrue(util.is_callable(lambda x: x))
        self.assertTrue(util.is_callable(self.test_is_callable))
        self.assertFalse(util.is_callable((lambda x: x)(1)))

    def test_is_readable(self):
        from StringIO import StringIO
        self.assertTrue(util.is_readable(StringIO('AAAAA')))
        self.assertTrue(util.is_readable(sys.stdin))
        self.assertFalse(util.is_readable('AAAA'))

    def test_is_writable(self):
        from StringIO import StringIO
        self.assertTrue(util.is_writable(StringIO()))
        self.assertTrue(util.is_writable(sys.stdout))
        self.assertFalse(util.is_writable('&&&&'))

    def test_safe_encode(self):
        self.assertEqual('日本語', util.safe_encode('日本語'))
        self.assertEqual('日本語', util.safe_encode('日本語'.decode('utf-8')))

    def test_safe_decode(self):
        s = '日本語'.decode('utf-8')
        self.assertEqual(s, util.safe_decode('日本語'))
        self.assertEqual(s, util.safe_decode('日本語'.decode('utf-8')))

    def test_cons_array(self):
        pass

    def test_cons_map(self):
        pass


if __name__ == '__main__':
    unittest.main()
