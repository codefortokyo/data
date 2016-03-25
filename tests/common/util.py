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
        self.assertTrue(hasattr(f, '__call__'))
        self.assertEqual(1, f(123214))
        self.assertEqual(1, f('ABC'))
        self.assertEqual(1, f(a=1, b=2))

    def test_gen_id(self):
        i1 = util.gen_id()
        i2 = util.gen_id()
        self.assertNotEqual(i1, i2)
        self.assertNotEqual(i1, None)
        self.assertEqual(len(i1), 22)
        self.assertTrue(isinstance(i1, basestring))

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
        x = [1, 2, 3]
        self.assertTrue(len(util.cons_array(x, tuple)), 3)
        self.assertTrue(isinstance(util.cons_array(x, list), list))

    def test_cons_map(self):
        x = [('a', 1), ('b', 2)]
        self.assertTrue(isinstance(util.cons_map(x, dict), dict))

    def test_dt2ts(self):
        from datetime import datetime
        ts = 1458900572523
        dt = datetime.strptime('2016/03/25 19:09:32.523',
                               '%Y/%m/%d %H:%M:%S.%f')
        self.assertTrue(isinstance(util.dt2ts(datetime.now()), int))
        self.assertEqual(ts, util.dt2ts(dt))

    def test_ts2dt(self):
        from datetime import datetime
        ts = 1458900572523
        dt = datetime.strptime('2016/03/25 19:09:32.523',
                               '%Y/%m/%d %H:%M:%S.%f')
        self.assertTrue(isinstance(util.ts2dt(ts), datetime))
        self.assertEqual(util.ts2dt(ts), dt)

    def test_is_url(self):
        self.assertTrue(util.is_url('http://somewhere.to'))
        self.assertTrue(util.is_url('https://somewhere.to'))
        self.assertTrue(util.is_url('http://somewhere.to/dir'))
        self.assertTrue(util.is_url('http://somewhere.to/dir?search'))
        self.assertTrue(util.is_url('http://somewhere.to/dir?s=e&a=r&c=h'))
        self.assertTrue(util.is_url('http://somewhere.to/dir?s=e&a#anch'))
        self.assertTrue(util.is_url('http://somewhere.to/dir#anc?s=e&a'))
        self.assertFalse(util.is_url('/Users/someone/Documents/data.x'))
        self.assertFalse(util.is_url('data.x'))
        self.assertTrue(util.is_url('http://192.168.0.1:8000'))


if __name__ == '__main__':
    unittest.main()
