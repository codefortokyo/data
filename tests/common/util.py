# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class Tester(unittest.TestCase):

    def setUp(self):
        pass

    def test_const(self):
        from cftt.common.util import const
        f = const(1)
        self.assertTrue(hasattr(f, '__call__'))
        self.assertEqual(1, f(123214))
        self.assertEqual(1, f('ABC'))
        self.assertEqual(1, f(a=1, b=2))

    def test_gen_id(self):
        from cftt.common.util import gen_id
        i1 = gen_id()
        i2 = gen_id()
        self.assertNotEqual(i1, i2)
        self.assertNotEqual(i1, None)
        self.assertEqual(len(i1), 22)
        self.assertTrue(isinstance(i1, basestring))

    def test_is_map(self):
        from cftt.common.util import is_map
        self.assertTrue(is_map({}))
        self.assertFalse(is_map([]))
        self.assertFalse(is_map('abc'))

    def test_is_string(self):
        from cftt.common.util import is_string
        self.assertTrue(is_string('にほんご'))
        self.assertTrue(is_string(u'1234'))
        self.assertTrue(is_string('全角'.decode('utf-8')))
        self.assertFalse(is_string([]))

    def test_is_array(self):
        from cftt.common.util import is_array
        self.assertTrue(is_array([]))
        self.assertFalse(is_array({}))
        self.assertFalse(is_array('abc'))

    def test_is_callable(self):
        from cftt.common.util import is_callable
        self.assertTrue(is_callable(lambda x: x))
        self.assertTrue(is_callable(self.test_is_callable))
        self.assertFalse(is_callable((lambda x: x)(1)))

    def test_is_readable(self):
        from StringIO import StringIO
        from cftt.common.util import is_readable
        self.assertTrue(is_readable(StringIO('AAAAA')))
        self.assertTrue(is_readable(sys.stdin))
        self.assertFalse(is_readable('AAAA'))

    def test_is_writable(self):
        from StringIO import StringIO
        from cftt.common.util import is_writable
        self.assertTrue(is_writable(StringIO()))
        self.assertTrue(is_writable(sys.stdout))
        self.assertFalse(is_writable('&&&&'))

    def test_safe_encode(self):
        from cftt.common.util import safe_encode
        self.assertEqual('日本語', safe_encode('日本語'))
        self.assertEqual('日本語', safe_encode('日本語'.decode('utf-8')))

    def test_safe_decode(self):
        from cftt.common.util import safe_decode
        s = '日本語'.decode('utf-8')
        self.assertEqual(s, safe_decode('日本語'))
        self.assertEqual(s, safe_decode('日本語'.decode('utf-8')))

    def test_cons_array(self):
        from cftt.common.util import cons_array
        x = [1, 2, 3]
        self.assertTrue(len(cons_array(x, tuple)), 3)
        self.assertTrue(isinstance(cons_array(x, list), list))

    def test_cons_map(self):
        from cftt.common.util import cons_map
        x = [('a', 1), ('b', 2)]
        self.assertTrue(isinstance(cons_map(x, dict), dict))

    def test_dt2ts(self):
        from datetime import datetime
        from cftt.common.util import dt2ts
        ts = 1458900572523
        dt = datetime.strptime('2016/03/25 19:09:32.523',
                               '%Y/%m/%d %H:%M:%S.%f')
        self.assertTrue(isinstance(dt2ts(datetime.now()), int))
        self.assertEqual(ts, dt2ts(dt))

    def test_ts2dt(self):
        from datetime import datetime
        from cftt.common.util import ts2dt
        ts = 1458900572523
        dt = datetime.strptime('2016/03/25 19:09:32.523',
                               '%Y/%m/%d %H:%M:%S.%f')
        self.assertTrue(isinstance(ts2dt(ts), datetime))
        self.assertEqual(ts2dt(ts), dt)

    def test_is_url(self):
        from cftt.common.util import is_url
        self.assertTrue(is_url('http://somewhere.to'))
        self.assertTrue(is_url('https://somewhere.to'))
        self.assertTrue(is_url('http://somewhere.to/dir'))
        self.assertTrue(is_url('http://somewhere.to/dir?search'))
        self.assertTrue(is_url('http://somewhere.to/dir?s=e&a=r&c=h'))
        self.assertTrue(is_url('http://somewhere.to/dir?s=e&a#anch'))
        self.assertTrue(is_url('http://somewhere.to/dir#anc?s=e&a'))
        self.assertFalse(is_url('/Users/someone/Documents/data.x'))
        self.assertFalse(is_url('data.x'))
        self.assertTrue(is_url('http://192.168.0.1:8000'))

    def test_rec_apply(self):
        from cftt.common.util import rec_apply
        res = rec_apply(int, ['1', {'a': '2'}],
                        condition=lambda x: isinstance(x, basestring),
                        apply_to_key=False)
        self.assertTrue(isinstance(res[0], int))
        self.assertTrue(isinstance(res[1]['a'], int))
        self.assertTrue(isinstance(res, list))
        self.assertTrue(isinstance(res[1], dict))

    def test_rec_decode(self):
        from cftt.common.util import rec_decode
        res = rec_decode(['a', u'b', 'あ', 'い'.decode('utf-8'), 1])
        self.assertTrue(all(map(lambda x: isinstance(x, unicode), res[:4])))
        self.assertTrue(isinstance(res[4], int))

    def test_rec_encode(self):
        from cftt.common.util import rec_encode
        res = rec_encode(['a', u'b', 'あ', 'い'.decode('utf-8'), 1])
        self.assertTrue(all(map(lambda x: isinstance(x, str), res[:4])))
        self.assertTrue(isinstance(res[4], int))

    def test_rec_str2dt(self):
        from datetime import datetime
        from cftt.common.util import rec_str2dt
        res = rec_str2dt(['2016/03/25 19:09:32',
                         {'a': '2016/03/25 19:09:32'},
                         'non-datetime string',
                          u'2016/03/25 19:09:32'])
        self.assertTrue(isinstance(res[0], datetime))
        self.assertTrue(isinstance(res[1]['a'], datetime))
        self.assertTrue(isinstance(res[2], str))
        self.assertTrue(isinstance(res[3], datetime))

    def test_rec_dt2str(self):
        from datetime import datetime
        from cftt.common.util import rec_dt2str
        res = rec_dt2str([datetime.strptime('2016/03/25 19:09:32',
                                            '%Y/%m/%d %H:%M:%S'),
                          {'a': '2016/03/25 19:09:32',
                           'b': datetime.now()},
                          123,
                          u'string'])
        self.assertTrue(isinstance(res[0], basestring))
        self.assertTrue(isinstance(res[1]['a'], basestring))
        self.assertTrue(isinstance(res[1]['b'], basestring))
        self.assertTrue(isinstance(res[2], int))
        self.assertTrue(isinstance(res[3], basestring))


if __name__ == '__main__':
    unittest.main()
