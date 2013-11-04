# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
from fpdtest import FPDTest
import agents as ag
import common as cm
from crawler import LINK_LABELS
DEFAULT_TEST_TIMEOUT = 10

LINK_URLS = ['login', 'logon', 'sign', 'register', 'subscri', 'log-in', 'log-on', 'join', 'sell', 'member',
                   'auth', 'account', 'user', 'password', 'store', 'shop', 'my']

# check fp_links.html
expected_url_strings = ['.html#%s' % url_string for url_string in LINK_URLS] # we expect to navigate to these URLs by clicking

# check fp_labels.html
expected_labels = ['\[contains\(text\(\), "%s"' % label for label in LINK_LABELS] # we expect to see these in logs (when we click by label texts)

CASPER_CLICK_LOGS = ['Clicked', 'html#linkx1', 'html#linkx2', 'html#linkx3']
COMMON_CASPER_ERROR_LOGS = ['ReferenceError',]

#@unittest.skip("skipping")    
class CasperTest(FPDTest):
        
    def test_should_click_fp_related_links(self):
        urls = (cm.BASE_TEST_URL + 'crawler/fp_links.html', )
        self.should_crawl_and_log(ag.AGENT_CFG_PHANTOM_MOD_CLICKER, 
                                 urls, expected_url_strings + CASPER_CLICK_LOGS, COMMON_CASPER_ERROR_LOGS)
        
    def test_should_click_fp_related_labels(self):
        urls = (cm.BASE_TEST_URL + 'crawler/fp_labels.html', )
        self.should_crawl_and_log(ag.AGENT_CFG_PHANTOM_MOD_CLICKER,
                                 urls, expected_labels, COMMON_CASPER_ERROR_LOGS)
    
    def test_should_set_the_user_agent(self):
        urls = (cm.BASE_TEST_URL + 'crawler/useragent.html', )
        self.should_crawl_and_log(ag.AGENT_CFG_PHANTOM_MOD_HOME_PAGE,
                                 urls, [r'Mozilla/5.0 \(X11; Linux i686\) AppleWebKit/537.36 \(KHTML, like Gecko\) Chrome/32.0.1673.0 Safari/537.36'], COMMON_CASPER_ERROR_LOGS)
         
    def test_should_not_click_xorigin_links(self):
                
        urls = (cm.BASE_TEST_URL_ONLINE + 'out_links.html', )
        
        self.should_crawl_and_log({'main_js': cm.CASPER_JS_CLICKER,
                                  'post_visit_func': None,
                                  'type': 'clicker',
                                  'timeout': 210}, urls,
                                 ["#should-click", "http://www.esat.kuleuven.be/"],
                                 ['requested: http://google.com/should-not-click', 
                                  'requested: http://yahoo.com/', \
                                  'requested: http://www.kuleuven.be/wieiswie/nl/person'] + COMMON_CASPER_ERROR_LOGS) 
                                    # the last link will test if we click the links from inner pages. We only expected to click link from homepage.

   
   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
