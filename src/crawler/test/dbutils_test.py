# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import dbutils as dbu
from fpdtest import FPDTest
import log_parser as lp
import agents as ag
import shutil

class Test(FPDTest):
        
    def tearDown(self):
        for out_dir in self.dirs_to_remove:
            print 'Removing:', out_dir
            shutil.rmtree(out_dir)
        if self.db_conn:
            self.db_conn.commit()    
            self.db_conn.close()

    def setUp(self):
        self.dirs_to_remove = []
        self.db_conn = dbu.mysql_init_db('fp_detective_test')
        self.domainInfo = lp.DomainInfo() # create a new DomainInfo obj for tests
        
        self.domainInfo.rank = 1
        self.domainInfo.log_filename = '/var/log/syslog'
        self.domainInfo.url = 'http://google.com'
        self.domainInfo.fonts_loaded = ['Arial', 'Tahoma', 'Georgia', '微软雅黑']
        self.domainInfo.fonts_by_origins = {'http://google.com':['arial', 'Tahoma'], 'http://yahoo.com':['Georgia'] }
        self.domainInfo.requests = ['http://google.com', 'http://yahoo.com']
        self.domainInfo.responses = ['http://abc.com', 'http://xyz.com']
        self.domainInfo.num_font_loads = 50
        self.domainInfo.num_offsetWidth_calls = 15
        self.domainInfo.num_offsetHeight_calls = 15
        self.domainInfo.fp_detected = ['iesnare', 'bluecava']
        self.domainInfo.crawl_id = 64654
        self.domainInfo.fpd_logs = ['userAgent', 'appCodeName']
        self.domainInfo.fc_dbg_font_loads = ['Arial', 'Tahoma', 'Georgia', 'someotherfont', '微软雅黑']
        self.domainInfo.log_complete = 1
        
        ha = ag.HeadlessAgent()
        self.crawl_job = ag.CrawlJob(ha)
        self.dirs_to_remove.append(self.crawl_job.job_dir)
        self.crawl_job.urls = ['http://google.com', 'http://yahoo.com']
        self.crawl_job.desc
        
    def test_mysql_init_db(self):
        db_conn = dbu.mysql_init_db()
        self.assertTrue(db_conn, "Cannot initialize connection.")
    
    def assert_db_val_equal(self, db_row, field_name, expected_val):
        db_val = db_row[field_name]
        self.assertEqual(db_val, expected_val, "Database entry (%s) different than expected value (%s)" % (db_val, expected_val))
    
    def test_add_js_info_to_db(self):
        js_info_id = dbu.add_js_info_to_db(self.domainInfo, self.db_conn, 123) # 123 a a fake site_info_id
        js_info = dbu.get_js_info_from_db(self.db_conn, by='id', value=js_info_id)[0]
        
        self.assert_db_val_equal(js_info, 'rank', self.domainInfo.rank)
        self.assert_db_val_equal(js_info, 'num_offsetHeight_calls', self.domainInfo.num_offsetHeight_calls)
        self.assert_db_val_equal(js_info, 'num_offsetWidth_calls', self.domainInfo.num_offsetWidth_calls)
        self.assert_db_val_equal(js_info, 'fpd_logs', ','.join(self.domainInfo.fpd_logs))
        
        #self.assertEqual(test_row['fp_detected'], ' '.join(domainInfo.fp_detected), "fp_detected has changed")
    
    def test_add_site_info_to_db(self):
        site_info_id = dbu.add_site_info_to_db(self.domainInfo, self.db_conn) # insert mock obj to db
        site_info_row = dbu.get_site_info_from_db(self.db_conn, by='id', value=site_info_id)[0] # retrieve inserted obj
        
        self.assert_db_val_equal(site_info_row, 'http_requests', ' '.join(self.domainInfo.requests))
        self.assert_db_val_equal(site_info_row, 'http_responses', ' '.join(self.domainInfo.responses))
        self.assert_db_val_equal(site_info_row, 'crawl_id', self.domainInfo.crawl_id)
        self.assert_db_val_equal(site_info_row, 'url', self.domainInfo.url)
        self.assert_db_val_equal(site_info_row, 'fc_dbg_font_loads', ','.join(self.domainInfo.fc_dbg_font_loads))
        self.assert_db_val_equal(site_info_row, 'num_fc_dbg_font_loads', len(self.domainInfo.fc_dbg_font_loads))
        self.assert_db_val_equal(site_info_row, 'rank', self.domainInfo.rank)
        self.assert_db_val_equal(site_info_row, 'log_complete', self.domainInfo.log_complete)
        
        
    def test_add_crawl_job_to_db(self):
        crawl_job_id = dbu.add_crawl_job_to_db(self.crawl_job, self.db_conn) # insert mock obj to db
        crawl_job_row = dbu.get_crawl_job_from_db(self.db_conn, by='id', value=crawl_job_id)[0] # retrieve inserted obj
        self.assert_db_val_equal(crawl_job_row, 'id', crawl_job_id)
        self.assert_db_val_equal(crawl_job_row, 'num_crawl_urls', self.crawl_job.num_crawl_urls)
        self.assert_db_val_equal(crawl_job_row, 'job_dir_path', self.crawl_job.job_dir)
        self.assert_db_val_equal(crawl_job_row, 'browser_user_agent', self.crawl_job.crawl_agent.user_agent_str)
        self.assert_db_val_equal(crawl_job_row, 'browser_type', self.crawl_job.crawl_agent.type)
        self.assert_db_val_equal(crawl_job_row, 'max_parallel_procs', self.crawl_job.max_parallel_procs)
        self.assert_db_val_equal(crawl_job_row, 'desc', self.crawl_job.desc)
    
    
    @unittest.skip('Skipping')
    def test_sqlite_init_db(self):
        test_db_file = self.new_temp_file('dbtest.sqlite')
        schema = '../swf_schema.sql'
        
        db_conn = dbu.sqlite_init_db(test_db_file, schema)
        db_c = db_conn.cursor()
        
        # can we read sqlite version
        if not db_c.execute('SELECT VERSION()'):
            self.fail("Cannot init db")
        
        db_conn.commit()
        db_conn.close()
              
    @unittest.skip('Skipping')
    def test_init_db_raises(self):

        test_db_file = self.new_temp_file('dbtest.sqlite')
        schema = 'NONEXISTENT654_schema.sql'
        try:
            dbu.sqlite_init_db(test_db_file, schema)
        except:
            pass
        else:
            self.fail("Cannot raise exception for nonexistent schema file")
        
        # can we read sqlite version
    
   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
