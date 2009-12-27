#!/usr/bin/python

import re
from backend import DbObj
try:
    from hashlib import md5
except ImportError:
    # Python2.4 fallback
    from md5 import md5

url_re = re.compile("^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?")

class Lookup(object):
    def __init__(self):
        """
        For URL parsing refer to RFC 2396
        http://www.ietf.org/rfc/rfc2396.txt

        For the url http://a.b.c.d.e.f.g/1.html?param=1#Tag the client will try these possible strings:
        a.b.c.d.e.f.g/1.html?param=1#Tag
        a.b.c.d.e.f.g/1.html?param=1
        a.b.c.d.e.f.g/1.html
        a.b.c.d.e.f.g/        
        c.d.e.f.g/1.html?param=1#Tag
        c.d.e.f.g/1.html?param=1
        c.d.e.f.g/1.html
        c.d.e.f.g/
        d.e.f.g/1.html?param=1#Tag
        d.e.f.g/1.html?param=1
        d.e.f.g/1.html
        d.e.f.g/
        e.f.g/1.html?param=1#Tag
        e.f.g/1.html?param=1
        e.f.g/1.html
        e.f.g/
        f.g/1.html?param=1#Tag
        f.g/1.html?param=1
        f.g/1.html
        f.g/

        Refer to http://code.google.com/apis/safebrowsing/ for more details.
        """
        self.backend = DbObj().backend

    def lookup_by_url(self, url):
        """
        Lookup Method by URL.
        """
        self.url = url.lower()
        
        # Break URL into components
        url_components = url_re.match(self.url).groups()

        # Prepare the lookup list as given in the main docstring.
        self.lookup_list = set()
        hostname = url_components[3]
        hostname_comp = hostname.split(".")
        if not hostname_comp:
            raise AttributeError("Invalid URL.")

        for i in xrange(len(hostname_comp) - 1):
            filtered_hostname_comp = ".".join(hostname_comp[i:])
            self.lookup_list.add(filtered_hostname_comp + "/")
            if url_components[4]:
                path = url_components[4].split('/')
                for j in xrange(len(path) + 1):
                    filtered_paths = '/'.join(path[:j])
                    if not '.' in filtered_paths:
                        self.lookup_list.add(filtered_hostname_comp + "%s/" %filtered_paths)
                self.lookup_list.add(filtered_hostname_comp + url_components[4])
                if url_components[5]:
                    self.lookup_list.add(filtered_hostname_comp + ''.join(url_components[4:6]))
                    if url_components[7]:
                        self.lookup_list.add(filtered_hostname_comp + ''.join(url_components[4:6]) + url_components[7])
            
        # Prepare the MD5 hash list for lookups.
        md5_hash_list = []
        for url_comp in self.lookup_list:
            md5_hash_list.append(md5(url_comp).hexdigest())
        return self.backend.lookup_by_md5(md5_hash_list)
              
    # A helper function. Currently unused
    def lookup_by_md5(self, md5_hash):
        """
        Lookup by MD5 hash.
        """
        return self.backend.lookup_by_md5(md5_hash)
