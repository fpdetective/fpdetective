import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
from fpdtest import FPDTest
import agents as ag
import common as cm

class PhantomDNTTest(FPDTest):
    # TODO add test for screen size
    def test_should_send_DNT_header(self):
        urls = (cm.BASE_TEST_URL + 'crawler/useragent.html', )      
        self.should_crawl_and_log(ag.AGENT_CFG_DNT_PHANTOM_LAZY,
                                 urls, ['"name": "DNT",', '"value": "1"'], # TODO match with multiline regexp 
                                  [])
   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
