'''
Created on Oct 22, 2013

@author: gacar
'''
import unittest
from log import wl_log
import commands
from weblabtest import WebLabTest
import os 

TEST_TIMEOUT = 10

######################################################
CHROMIUM_PATH = '~/dev/chromium/src/out/Release/chrome'
######################################################
user_path = os.path.expanduser

class Test(WebLabTest):

    def setUp(self):
        self.log_file = 'chrome_test.log' 
        
    def tearDown(self):
        if os.path.lexists(self.log_file):
            os.unlink(self.log_file)
    
    def should_visit_and_log(self):
        pass
    
    def test_mod_chromium_should_log_navigator_props(self):
        #cd ~/dev/chromium/src/out/Release/;./chrome --enable-logging=stderr --v=1 --user-data-dir=/tmp/temp_profile 2>&1 | tee /tmp/chrome.log; geany /tmp/chrome.log;'
        os.chdir(user_path('~/dev/chromium/src/out/Release/'))
        test_url = 'http://homes.esat.kuleuven.be/~gacar/phtest/index.html'
#        xvfb-run --auto-servernum 
        cmd = 'timeout -k %s %s %s --enable-logging=stderr --v=1 --no-sandbox --disable-metrics\
         --allow-running-insecure-content --ignore-certificate-errors --disk-cache-size=0\
          --user-data-dir=/tmp/temp_profile %s 2>&1 | tee %s' \
          % (TEST_TIMEOUT, TEST_TIMEOUT, CHROMIUM_PATH, test_url, self.log_file)
        
        wl_log.info('>> %s (%s) %s' % (test_url, '?', cmd))
        status, output = commands.getstatusoutput(cmd) # Run the command
        
        if status and status != 31744:
            wl_log.critical('Error while visiting %s(%s) w/ command: %s: (%s) %s' % (test_url, '?', cmd, status, output))
        else:
            wl_log.info(' >> ok %s (%s)' % (test_url, '?'))
        
        WebLabTest.assert_all_patterns_in_file(self, self.log_file, '54646464654')
           
    


if __name__ == "__main__":
    import sys;
    if len(sys.argv) != 2:
        sys.exit("ERROR: Please provide path to Chromium binary")        
    chrome_path = sys.argv[1]
    del sys.argv[1:]
    unittest.main()