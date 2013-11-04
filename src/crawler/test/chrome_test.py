
import unittest
import os
import shutil
import common as cm
import utils as ut
from fpdtest import FPDTest

class mitmcfg:
    outfile = '/tmp/mitmout'
    dmpfile = outfile + '.dmp'   
    outdir = '/tmp/mitmtest'
    
class Test(FPDTest):
    def setUp(self):
        if os.path.isdir(mitmcfg.outdir):
            shutil.rmtree(mitmcfg.outdir)
        os.mkdir(mitmcfg.outdir)
        
    def tearDown(self):
        if os.path.isdir(mitmcfg.outdir):
            #shutil.rmtree(mitmcfg.outdir)
            pass

    @unittest.skip('sdf')
    def test_chrome_clicker_should_find_fpswf_in_register_link(self):
        self.should_crawl_and_find_swfs('http://espn.go.com', expected_strings=(['swf_url', 'occ_string'], 
                ['fp.swf', 'enumerateFonts']), crawler_type='chrome_clicker')
    
    def test_SUID_sandbox(self):
        # log_file = self.new_temp_file('/tmp/chrome.log')
        log_file = '/tmp/chrome.log'
        url = cm.BASE_TEST_URL + "font-face/font-face-names.html"
        unexpected_strs = ('FATAL:browser_main_loop.cc', 'Running without the SUID sandbox')
        expected_strs = ('FPLOG',)
        
        cmd='timeout 10 xvfb-run --auto-servernum %s --disable-setuid-sandbox --enable-logging=stderr --v=1 --vmodule=frame=1 \
        --user-data-dir=/tmp/temp_profile%s --disk-cache-dir=/tmp/tmp_cache%s %s 2>&1 | tee %s' %\
        (cm.CHROME_MOD_BINARY, ut.rand_str(), ut.rand_str(), url, log_file)
        ut.run_cmd(cmd)
        
        self.assert_all_patterns_not_in_file(log_file, unexpected_strs)
        self.assert_all_patterns_in_file(log_file, expected_strs)


    @unittest.skip('sdf')    
    def test_chrome_should_not_click(self):
        cm.BASE_TEST_URL_ONLINE + 'out_links.html'
        self.should_crawl_and_find_swfs('http://homes.esat.kuleuven.be/~gacar/phtest/out_links.html', 
                unexpected_strings=(['swf_url'], ['http://browserspy.dk/flash/fonts.swf']), crawler_type='chrome_lazy')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_launch_chrome_cmd']
    unittest.main()