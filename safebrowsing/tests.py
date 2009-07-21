import unittest
from query_lookup import Lookup

class SafebrowsingTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup_obj = Lookup()

    def testLookupList1(self):
        self.lookup_obj.lookup_by_url('http://a.b.c.d.e.f.g/1.html?param=1#Tag')
        lookup_list = ['f.g/1.html?param=1#Tag',
                       'f.g/1.html?param=1',
                       'f.g/1.html',
                       'f.g/',
                       'e.f.g/1.html?param=1#Tag',
                       'e.f.g/1.html?param=1',
                       'e.f.g/1.html',
                       'e.f.g/',
                       'd.e.f.g/1.html?param=1#Tag',
                       'd.e.f.g/1.html?param=1',
                       'd.e.f.g/1.html',
                       'd.e.f.g/',
                       'c.d.e.f.g/1.html?param=1#Tag',
                       'c.d.e.f.g/1.html?param=1',
                       'c.d.e.f.g/1.html',
                       'c.d.e.f.g/',
                       'b.c.e.f.g/1.html?param=1#Tag',
                       'b.c.e.f.g/1.html?param=1',
                       'b.c.e.f.g/1.html',
                       'b.c.e.f.g/',
                       'a.b.c.e.f.g/1.html?param=1#Tag',
                       'a.b.c.e.f.g/1.html?param=1',
                       'a.b.c.e.f.g/1.html',
                       'a.b.c.e.f.g/']
        self.assertEqual(self.lookup_obj.lookup_list, lookup_list)

    def testLookupList2(self):
        self.lookup_obj.lookup_by_url('http://a.b.c.d.e.f.g/1/2.html?param=1#Tag')
        lookup_list = ['f.g/1/2.html?param=1#Tag',
                       'f.g/1/2.html?param=1',
                       'f.g/1/2.html',
                       'f.g/1/',
                       'f.g/',
                       'e.f.g/1/2.html?param=1#Tag',
                       'e.f.g/1/2.html?param=1',
                       'e.f.g/1/2.html',
                       'e.f.g/1/',
                       'e.f.g/',
                       'd.e.f.g/1/2.html?param=1#Tag',
                       'd.e.f.g/1/2.html?param=1',
                       'd.e.f.g/1/2.html',
                       'd.e.f.g/1/',
                       'd.e.f.g/',
                       'c.d.e.f.g/1/2.html?param=1#Tag',
                       'c.d.e.f.g/1/2.html?param=1',
                       'c.d.e.f.g/1/2.html',
                       'c.d.e.f.g/1/',
                       'c.d.e.f.g/',
                       'b.c.d.e.f.g/1/2.html?param=1#Tag',
                       'b.c.d.e.f.g/1/2.html?param=1',
                       'b.c.d.e.f.g/1/2.html',
                       'b.c.d.e.f.g/1/',
                       'b.c.d.e.f.g/',
                       'a.b.c.d.e.f.g/1/2.html?param=1#Tag',
                       'a.b.c.d.e.f.g/1/2.html?param=1',
                       'a.b.c.d.e.f.g/1/2.html',
                       'a.b.c.d.e.f.g/1/',
                       'a.b.c.d.e.f.g/',
                       'a.b.c.d.e.f.g/1/2.html?param=1#Tag',
                       'a.b.c.d.e.f.g/1/2.html?param=1',
                       'a.b.c.d.e.f.g/1/2.html',
                       'a.b.c.d.e.f.g/1/',
                       'a.b.c.d.e.f.g/',
                       'a.b.c.d.e.f.g/1/2.html?param=1#Tag',
                       'a.b.c.d.e.f.g/1/2.html?param=1',
                       'a.b.c.d.e.f.g/1/2.html',
                       'a.b.c.d.e.f.g/1/',
                       'a.b.c.d.e.f.g/',]
        self.assertEqual(self.lookup_obj.lookup_list, lookup_list)

if __name__ == '__main__':
    unittest.main()
