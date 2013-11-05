import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import webutils as wu 
import common as cm
from fpdtest import FPDTest

class WebUtilsTest(FPDTest):
    
    def setUp(self):
        self.pub_suffix = wu.PublicSuffix()
        self.data_url =  'data:image/png;base64,iVBORw0KGgoAAAAN===' # junk
        
    def tearDown(self):
        pass
    
    def test_read_url(self):
        page_html = wu.read_url('http://www.google.com')
        self.assertIn('<html', page_html, "Cannot find html tag")        
  
    def test_read_file_url(self):
        page_html = wu.read_url(cm.BASE_TEST_URL + 'crawler/barebones.html')
        self.assertIn('<html', page_html, "Cannot find html tag")        

    def test_strip_url_scheme(self):
        domain = 'abcdef.com'
        url1 = 'http://' + domain 
        url2 = 'https://' + domain
        url3 =  'https://' + domain + '/a/b/c/http/'
        
        
        for url in (domain, url1, url2):
            self.assertEqual(wu.strip_url_scheme(url), domain)
        
        self.failUnless(wu.strip_url_scheme(url3).startswith(domain))
        self.failUnless(wu.strip_url_scheme(self.data_url).startswith('image/png'))
        

    def test_swf_name_from_url(self):
        self.assertEqual('foo.swf', 
                         wu.swf_name_from_url('http://abc.org/foo.swf?param1=1&param2=2'))
        self.assertEqual('bar.swf', 
                         wu.swf_name_from_url('http://abc.org/dir/bar.swf?param1=1&param2=2'))
        # self.assertEqual('bla.swf', wu.swf_name_from_url('http://abc.org/dir/bla.swf/somebase64str/')) TODO: pass this one
    
    def assert_public_suffix(self, url, expected_pub_suffix):
        self.assertEqual(self.pub_suffix.get_public_suffix(url), expected_pub_suffix, 
                         'Cannot get the expected public suffix (%s) for URL %s' % 
                         (expected_pub_suffix, url))
        
    def test_get_public_suffix(self):
        pub_suf_test_urls = ('http://www.foo.org', 
                             'https://www.foo.org',
                             'http://www.subdomain.foo.org',
                             'http://www.subdomain.foo.org:80/subfolder',
                             'https://www.subdomain.foo.org:80/subfolder?param1=4545&param2=54545',
                             'https://www.subdomain.foo.org:80/subfolder/bae654sadfasd==/654sadfasd') 
        for pub_suf_test_url in pub_suf_test_urls:
            self.assert_public_suffix(pub_suf_test_url, 'foo.org')

    def test_gen_url_list(self):
        # TODO: create a test file, remove Alexa dependency.
        
        self.assertEqual(list(wu.gen_url_list(0)), [])
        self.assertEqual(len(list(wu.gen_url_list(10))), 10, 
                         "Cannot read 10 URLs, make sure you've \
                         the CSV file from Alexa in place") # i.e. ALEXA_TOP1M_PATH
                
    def test_get_top_alexa_list_start_stop(self):
        top_50_100 = list(wu.gen_url_list(100, 50))
        self.assertEqual(len(top_50_100), 51)
        
        top_5_10 = list(wu.gen_url_list(10, 5))
        self.assertEqual(len(top_5_10), 6)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
