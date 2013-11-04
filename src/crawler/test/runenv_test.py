
import os
import unittest
import utils as ut
import log_parser as lp
import common as cm
from fpdtest import FPDTest

class RunningEnvTest(FPDTest):
    
    def test_used_binaries(self):
        bins = (cm.CHROME_MOD_BINARY, cm.PHANTOM_BINARY, cm.PHANTOM_MOD_BINARY, 
                cm.CASPER_BINARY, cm.CHROME_DRIVER_BINARY)
        for binary in bins:
            if not os.path.isfile(binary):
                self.fail('Cannot find %s' % binary)
            if not os.access(binary, os.X_OK): # http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
                self.fail('Don\t have execution permission for %s' % binary)
        
    def test_used_packages(self):
        packages = ('xvfb-run', 'mitmdump', 'mysql', cm.CHROME_BINARY)
        for package in packages:
            self.failUnless(ut.is_installed(package), 'Cannot find %s in your system' % package) 
    
    def test_run_dirs(self):
        run_dirs = (cm.BASE_FP_RUN_FOLDER, cm.BASE_FP_JOBS_FOLDER, cm.BASE_FP_LOGS_FOLDER)
        for run_dir in run_dirs:
            self.failUnless(os.path.isdir(run_dir))
    
    def test_phantomjs_should_find_casperjs(self):
        test_url = cm.BASE_TEST_URL + '/font-face/barebones.html'
        self.should_crawl_and_log({'main_js': cm.CASPER_JS_LAZY_HOMEPAGER,
                                  'post_visit_func': lp.parse_log_dump_results,
                                  'timeout': 15}, (test_url,), (), 'Cannot find casperjs module, quitting...')
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()