# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import log_parser as lp
import fileutils as fu
from fpdtest import FPDTest

lp.FONT_LOAD_THRESHOLD = 2

fp_urls = ('http://www.jacklistens.com/websurvey/jslib/pomegranate.js', 
        'http://www.myfreecams.com/mfc2/lib/o-mfccore.js?vcc=13666666',
         'http://tags.master-perf-tools.com/V20test/tagv22.pkmin.js', 
         'https://www.privacytool.org/AnonymityChecker/js/fontdetect.js', 
         'http://device.maxmind.com/js/device.js', 
         'http://ds.bluecava.com/v50/AC/BCAC5.js', 
         'http://inside-graph.com/ig.js',
         'https://coinbase.com/assets/application-773afba0b6ee06b45ba4363a99637610.js',
         'https://d2o7j92jk8qjiw.cloudfront.net/assets/application-773afba0b6ee06b45ba4363a99637610.js' 
         'http://articlebase.com/sbbpg=sbbShell'
         'http://h.online-metrix.net/fp/fp.swf', 
         'http://mpsnare/iesnare.com', 
         'http://sl4.analytics-engine.net/detector/fp.js',
         'http://www.web-aupair.net/sites/default/files/fp/fp.js',
         'http://sl1.analytics-engine.net/fingerprint/add?callback=jsonp138')

class ParserTest(FPDTest):
    
    def test_mark_if_fp(self):
        self.assertTrue(lp.mark_if_fp('foo.com') == 'foo.com') # should return same URL for non-fp
        for fp_url in fp_urls: 
            self.assertTrue(lp.mark_if_fp(fp_url) != fp_url) # should return something different if it finds fp urls
            
    def test_get_index_filename_for_domain_info(self):
        di = lp.DomainInfo()
        di.log_filename = '/tmp/as.log'
        self.assertEqual(lp.get_index_filename_for_domain_info(di), '/tmp/index.html') 

    def test_add_index_html_line(self):
        self.new_temp_file('index.html')
        di = lp.DomainInfo()
        di.log_filename = '/tmp/as.log'
        lp.add_index_html_line(di)
        ind_file = lp.get_index_filename_for_domain_info(di)
        ind_src = fu.read_file(ind_file)
        self.assertTrue('tr' in ind_src, "Cannot find tr in index.html")
        
    def test_close_index_html(self):
        index_filename = 'files/html/results/index.html'
        index_filename = self.abs_test_file_name(index_filename)
        
        # self.new_temp_file(index_filename) # to remove it after test finishes
        table_rows = """<tr><td>1</td><td><a href="/home/user/fpbase/run/jobs/20130420-010404/1-google-com.html">http://google.com/</a></td><td>10</td><td>1</td></tr>
        <tr><td>118</td><td><a href="/home/user/fpbase/run/jobs/20130420-010404/118-google-com-ar.html">http://google.com.ar/</a></td><td>3</td><td>51</td></tr>
        <tr><td>27</td><td><a href="/home/user/fpbase/run/jobs/20130420-010404/27-google-co-uk.html">http://google.co.uk/</a></td><td>1</td><td>11</td></tr>"""
        
        fu.write_to_file(index_filename, table_rows)
        
        lp.close_index_html(index_filename)
        index_src = fu.read_file(index_filename)
        self.assertTrue('<table' in  index_src, 'No table in index.html')
        self.assertTrue('<thead' in  index_src, 'No thead in index.html')
        self.assertTrue('</html>' in  index_src, 'No closing html tag index.html')

        
    def test_get_fp_from_reqs(self):
        for fp_url in fp_urls: 
            self.assertTrue(lp.get_fp_from_reqs([fp_url,]), 'Cannot find fp in %s' % fp_url)
      
        self.assertTrue(lp.get_fp_from_reqs(fp_urls)) # should return something different if it finds fp urls
        self.assertFalse(lp.get_fp_from_reqs(['foo.org', 'foo.com', 'bar.org'])) #

   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
