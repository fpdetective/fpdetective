import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import commands
import common as cm
import agents as ag
import utils as ut
from fpdtest import FPDTest

TEST_TIMEOUT = 10

user_path = os.path.expanduser

class Test(FPDTest):

    def setUp(self):
        self.log_file = '/tmp/browser_test.log' 
        
    def tearDown(self):
        if os.path.lexists(self.log_file):
            os.unlink(self.log_file)
            
    def test_modchrome_should_log_access_to_navigator_props(self):
        cr = ag.ChromeAgent().setOptions(ag.AGENT_CFG_CHROME_LAZY).setOptions({'timeout':TEST_TIMEOUT})
        expected = ('DOMMimeType::suffixes', 'DOMMimeType::description', 'DOMMimeType::enabledPlugin', 'DOMMimeTypeArray::item',
                        'DOMMimeType::suffixes:swf', 'DOMMimeType::description:Shockwave Flash', '::javaEnabled',
                        'onURL', 'onJSURL')
        self.should_log_access_to_navigator_props(cr.__dict__, expected)
    
    def test_modphantomjs_should_log_access_to_navigator_props(self):
        ph = ag.HeadlessAgent().setOptions(ag.AGENT_CFG_PHANTOM_MOD_HOME_PAGE).setOptions({'timeout':TEST_TIMEOUT})
        self.should_log_access_to_navigator_props(ph.__dict__)
    
    def should_log_access_to_navigator_props(self, browser_cfg, expected_log_strs=()):
        test_url = cm.BASE_TEST_URL + 'crawler/browserfp.html'
        cmd = ag.get_visit_cmd(browser_cfg, '', self.log_file, test_url)
        print 'Visit cmd: ', cmd
        
        status, output = commands.getstatusoutput(cmd) # Run the command
        
        if status and status != ag.ERR_CMD_TIMEDOUT: # 31744 is timeout
            self.fail('Error while visiting %s w/ command: %s: (%s) %s' % (test_url, cmd, status, output))
        
        expected_strs = ('FPLOG ', 'Navigator', 'Screen::height', 'Screen::width', '::appCodeName', '::appName',
                        '::userAgent', '::appVersion', '::cookieEnabled', '::language', '::mimeTypes', 
                        '::platform', '::plugins', '::product', '::productSub', '::userAgent', 
                        '::vendor','::vendorSub',  'Screen::availHeight', 'Screen::availLeft', 
                        'Screen::availTop', 'Screen::availWidth', 'Screen::colorDepth', 'Screen::height', 'Screen::pixelDepth', 'Screen::width',
                        'DOMMimeTypeArray::length',  
                        '/fpbase/src/crawler/test/files/crawler/browserfp.html')        
        
        self.assert_all_patterns_in_file(self.log_file, expected_strs+expected_log_strs)
    
    def test_SUID_sandbox(self):
        log_file = self.new_temp_file('/tmp/chrome.log')
        url = cm.BASE_TEST_URL + "font-face/font-face-names.html"
        unexpected_strs = ('FATAL:browser_main_loop.cc', 'Running without the SUID sandbox')
        expected_strs = ('FPLOG',)
        
        cmd='timeout 10 xvfb-run --auto-servernum %s --disable-setuid-sandbox --enable-logging=stderr --v=1 --vmodule=frame=1 \
            --user-data-dir=/tmp/temp_profile%s --disk-cache-dir=/tmp/tmp_cache%s %s 2>&1 | tee %s' %\
            (cm.CHROME_MOD_BINARY, ut.rand_str(), ut.rand_str(), url, log_file)
        
        ut.run_cmd(cmd)
        
        self.assert_all_patterns_not_in_file(log_file, unexpected_strs)
        self.assert_all_patterns_in_file(log_file, expected_strs)
   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
