import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import utils as ut
import common as cm
import webutils as wu
import dbutils as dbu
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
            self.failUnless(os.path.isdir(run_dir), 'Cannot find dir: %s' % run_dir)
    
    def test_alexa_list(self):
        os.path.isfile(wu.ALEXA_TOP1M_PATH)
    
    def test_mysql(self):
        self.should_not_raise('MySQL Error: cannot connect to default DB', dbu.mysql_init_db)
        self.should_not_raise('MySQL Error: cannot connect to test DB (fp_detective_test)', dbu.mysql_init_db, 'fp_detective_test')
    
    def test_apache(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
