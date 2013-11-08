import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import utils as ut
import common as cm
import webutils as wu
import dbutils as dbu
from fpdtest import FPDTest

class RunEnvTest(FPDTest):
               
    def test_chrome_mod_bin(self):
        self.should_be_executable(cm.CHROME_MOD_BINARY)
        
    def test_phantom_bin(self):
        self.should_be_executable(cm.PHANTOM_BINARY)
        
    def test_phantom_mod_bin(self):
        self.should_be_executable(cm.PHANTOM_MOD_BINARY)
        
    def test_casper_bin(self):
        self.should_be_executable(cm.CASPER_BINARY)
        
    def test_chrome_driver_bin(self):
        self.should_be_executable(cm.CHROME_DRIVER_BINARY)
        
    def test_xvfb_pkg(self):
        self.assert_is_installed('xvfb-run')
 
    def test_mitmdump_pkg(self):
        self.assert_is_installed('mitmdump')
        
    def test_mysql_pkg(self):
        self.assert_is_installed('mysql')
                
    def test_chromium_pkg(self):
        self.assert_is_installed(cm.CHROME_BINARY)
    
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
