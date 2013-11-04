
import unittest
import crawler as cr 
import utils as ut
from fpdtest import FPDTest

class ChromeTest(FPDTest):

    def test_crawl_url_timeout(self):
        test_url = "http://jsbin.com/aqexuw/10"
        try:
            ut.timeout(cr.CRAWLER_CLICKER_VISIT_TIMEOUT + 2)
            cr.crawl_url("chrome_clicker", test_url, "")
        except ut.TimeExceededError as texc:
            self.fail("Crawl has timed out %s" % texc)

    def test_is_mailto_link(self):
        non_mailto_hrefs = ("http://abc.com", "http://mailto.com", "https://abc.com", "https://mailto.com:9091", "mailto")  
        mailto_hrefs = ("mailto:abc@def.com", "mailto:abc@gmail.com", "mailto:somebody@somewhere.com")
        for non_mailto_href in non_mailto_hrefs:
            if cr.is_mailto_link(non_mailto_href):
                self.fail("is_mailto_link returned True for a non-mailto link")

        for mailto_href in mailto_hrefs:
            if not cr.is_mailto_link(mailto_href):
                self.fail("is_mailto_link returned False for a mailto link")

    def test_is_external(self):
        non_external_pairs = (("http://abc.com/contact", "http://abc.com"),
                              ("http://abc.com/sub/contact", "https://abc.com"), 
                              ("http://abc.com/sub/contact:8080", "https://abc.com"),
                              ("contact", "http://abc.com"),
                              ("contact", "https://abc.com"),
                              ("contact", "https://abc.com/sub/")
                              )
        
        external_pairs = (("http://abcd.com/contact", "http://abc.com"), 
                              ("http://ab.com/sub/contact", "https://abc.com"), 
                              ("http://xyz.com/sub/contact:8080", "https://abc.com/sub")
                              )
        for non_external_pair in non_external_pairs:
            if cr.is_external(non_external_pair[0], non_external_pair[1]):
                self.fail("is_external returned True for an internal link %s" % non_external_pair[0])

        for external_pair in external_pairs:
            if not cr.is_external(external_pair[0], external_pair[1]):
                self.fail("is_external returned False for an external link %s" % external_pair[0])
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()