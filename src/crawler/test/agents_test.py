# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import agents as ag
import common as cm
import fileutils as fu
import webutils as wu
import shutil
from log import wl_log
from fpdtest import FPDTest
import log_parser as lp
from functools import partial


class AgentTest(FPDTest):

    def setUp(self):
        self.dirs_to_remove = []
        
    def tearDown(self):
        for out_dir in self.dirs_to_remove:
            print 'Removing:', out_dir
            shutil.rmtree(out_dir)
        
    def create_job_folder(self):
        out_dir = ag.create_job_folder()
        self.dirs_to_remove.append(out_dir)
        return out_dir
    
    def test_logger(self):
        new_logger = partial(ag.logger_fn, wl_log)
        new_logger('info', 'Can we?')
        
    def test_prep_base_folder(self):
        ag.prep_run_folder()
        self.assert_(os.path.isdir(cm.BASE_FP_RUN_FOLDER), 'Cannot create base folder')
        self.assert_(os.path.isdir(cm.BASE_FP_JOBS_FOLDER), 'Cannot create jobs folder')
        self.assert_(os.path.isdir(cm.BASE_FP_LOGS_FOLDER), 'Cannot create logs folder')
        
    def test_should_create_job_folder(self):
        out_dir = self.create_job_folder()
        self.assert_(os.path.isdir(out_dir), 'Cannot create job folder')
    
    def test_job_folder_should_be_writable(self):
        out_dir = self.create_job_folder()
        self.assert_(os.path.isdir(out_dir), 'Cannot create job folder')
        out_file = os.path.join(out_dir, 'some.log')
        
        file_content = '123456789'
        fu.write_to_file(out_file, file_content)
        self.assert_(os.path.isfile(out_file), 'Cannot create file in job folder')
        self.assert_(file_content == fu.read_file(out_file), 'Cannot create file in job folder')

    
    @unittest.skip("long test")
    def test_casper_clicker_should_click_fp_related_links(self):
        urls = ('http://jsbin.com/izofav/2',)
        expected_strs = ('Clicked!', 'login', 'register')
        self.should_crawl_and_log({'main_js': cm.CASPER_JS_CLICKER,
                                  'post_visit_func': lp.parse_log_dump_results,
                                  'timeout': 210},
                                 urls, expected_strs)
    
    def test_default_settings(self):
        urls = (cm.BASE_TEST_URL + "font-face/font-face-names.html",)
        expected_strs = ('FontFaceName', 'Georgia', 'Tahoma', 'Arial')
        self.should_crawl_and_log({}, urls, expected_strs)

    
    def test_mod_phantom_should_log_unicode_font_names(self):
        self.should_crawl_and_log(ag.AGENT_CFG_PHANTOM_MOD_HOME_PAGE, 
                                  (cm.BASE_TEST_URL + "font-face/font-face-unicode.html",), 
                                  ['>>>FPLOG CSSFontFace::getFontData FontFaceName->微软雅 ',
                                   '>>>FPLOG CSSFontFace::getFontData 微软->微软雅黑',
                                   '>>>FPLOG CSSFontSelector::getFontData Arial',
                                   '>>>FPLOG CSSFontSelector::getFontData Nonexistent',
                                   '>>>FPLOG CSSFontSelector::getFontData Font1',
                                   '>>>FPLOG CSSFontFace::getFontData Font1->Georgia',
                                   '>>>FPLOG CSSFontFace::getFontData Tahoma->LocalFontTahomeRepl'], 
                                  [])        
    
    def test_mod_phantom_should_capture_font_loads(self):
        urls = (cm.BASE_TEST_URL + 'font-face/fonts.html',)
        expected_strs = ('Arial', 'Tahoma')
        self.should_crawl_and_log({'main_js': cm.CASPER_JS_LAZY_HOMEPAGER,
                                  'post_visit_func': lp.parse_log_dump_results,
                                  'timeout': 10}, 
                                 urls, expected_strs)
    
   
    def test_init_headless_agent(self):
        ha = ag.HeadlessAgent()
        cr_job = ag.CrawlJob(ha)
    
        crawl_agent_cfg = {
                   'main_js' : cm.CASPER_JS_LAZY_HOMEPAGER,
                   'cmd_line_options' : ag.PHANTOM_COMMON_OPTIONS,
                   'timeout' : 20,
                   'screenshot' : True,
                   'post_visit_func': lp.parse_log_dump_results
                   }
        
        ha = ag.HeadlessAgent()
        ha.setOptions(crawl_agent_cfg)
        limit = 3
        cr_job_cfg = {
                  'desc': 'Visit top %s sites and use fontconfig\'s debugging facilities to collect data.' % limit,
                  'max_parallel_procs': 20,
                  'crawl_agent': ha,
                  'urls':  wu.gen_url_list(limit)
                  }
        
        cr_job.setOptions(cr_job_cfg)
        
        ag.run_crawl(cr_job)
        self.dirs_to_remove.append(os.path.realpath(cr_job.job_dir))
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
