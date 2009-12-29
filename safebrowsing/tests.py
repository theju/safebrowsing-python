import unittest
from query_lookup import Lookup

class SafebrowsingTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup_obj = Lookup()

    def testLookupList1(self):
        self.lookup_obj.lookup_by_url('http://a.b.c.d.e.f.g/1.html?param=1#Tag')
        lookup_list = set(['a.b.c.d.e.f.g/',
                           'a.b.c.d.e.f.g/1.html',
                           'a.b.c.d.e.f.g/1.html?param=1',
                           'a.b.c.d.e.f.g/1.html?param=1#tag',
                           'b.c.d.e.f.g/',
                           'b.c.d.e.f.g/1.html',
                           'b.c.d.e.f.g/1.html?param=1',
                           'b.c.d.e.f.g/1.html?param=1#tag',
                           'c.d.e.f.g/',
                           'c.d.e.f.g/1.html',
                           'c.d.e.f.g/1.html?param=1',
                           'c.d.e.f.g/1.html?param=1#tag',
                           'd.e.f.g/',
                           'd.e.f.g/1.html',
                           'd.e.f.g/1.html?param=1',
                           'd.e.f.g/1.html?param=1#tag',
                           'e.f.g/',
                           'e.f.g/1.html',
                           'e.f.g/1.html?param=1',
                           'e.f.g/1.html?param=1#tag',
                           'f.g/',
                           'f.g/1.html',
                           'f.g/1.html?param=1',
                           'f.g/1.html?param=1#tag',
                           ])
        self.assertEqual(self.lookup_obj.lookup_list, lookup_list)

    def testLookupList2(self):
        self.lookup_obj.lookup_by_url('http://a.b.c.d.e.f.g/1/2/3.html?param=1#Tag')
        lookup_list = set(['a.b.c.d.e.f.g/',
                           'a.b.c.d.e.f.g/1/',
                           'a.b.c.d.e.f.g/1/2/',
                           'a.b.c.d.e.f.g/1/2/3.html',
                           'a.b.c.d.e.f.g/1/2/3.html?param=1',
                           'a.b.c.d.e.f.g/1/2/3.html?param=1#tag',
                           'b.c.d.e.f.g/',
                           'b.c.d.e.f.g/1/',
                           'b.c.d.e.f.g/1/2/',
                           'b.c.d.e.f.g/1/2/3.html',
                           'b.c.d.e.f.g/1/2/3.html?param=1',
                           'b.c.d.e.f.g/1/2/3.html?param=1#tag',
                           'c.d.e.f.g/',
                           'c.d.e.f.g/1/',
                           'c.d.e.f.g/1/2/',
                           'c.d.e.f.g/1/2/3.html',
                           'c.d.e.f.g/1/2/3.html?param=1',
                           'c.d.e.f.g/1/2/3.html?param=1#tag',
                           'd.e.f.g/',
                           'd.e.f.g/1/',
                           'd.e.f.g/1/2/',
                           'd.e.f.g/1/2/3.html',
                           'd.e.f.g/1/2/3.html?param=1',
                           'd.e.f.g/1/2/3.html?param=1#tag',
                           'e.f.g/',
                           'e.f.g/1/',
                           'e.f.g/1/2/',
                           'e.f.g/1/2/3.html',
                           'e.f.g/1/2/3.html?param=1',
                           'e.f.g/1/2/3.html?param=1#tag',
                           'f.g/',
                           'f.g/1/',
                           'f.g/1/2/',
                           'f.g/1/2/3.html',
                           'f.g/1/2/3.html?param=1',
                           'f.g/1/2/3.html?param=1#tag',
                           ])
        self.assertEqual(self.lookup_obj.lookup_list, lookup_list)

    def testHashPresent1(self):
        result = self.lookup_obj.lookup_by_url('http://malware.testing.google.test/testing/malware/')
        self.assertEqual(result, u'M')

    def testHashNotPresent1(self):
        result = self.lookup_obj.lookup_by_url('http://google.com/')
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
