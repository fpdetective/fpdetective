
import unittest
import os, re
import fileutils as fu
import agents as ag
import swfutils as swu
import dbutils as dbu
import MySQLdb as mdb

DEFAULT_TEST_CRAWL_TIMEOUT = 10

class FPDTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.files_to_remove = [] # list of files to be removed during class teardown
    
    def should_not_raise(self, msg, fn, *xargs, **kwargs):
        """Ensure that function does not raises an exception when executed with the given args."""
        try:
            fn(*xargs, **kwargs)            
        except:
            self.fail(msg)
        else:
            pass
    
        
    def should_raise(self, msg, fn, *xargs, **kwargs):
        """Ensure that function raises an exception when executed with the given args."""
        try:
            fn(*xargs, **kwargs)            
        except:
            pass
        else:
            self.fail(msg)
                    
    
    def should_raise_for_diff_len_args(self, func, arg1, arg2):
        """Check whether function raises an exception when executed with args of disparate lengths."""
        try:
            func(arg1, arg2)
        except AssertionError:
            pass # OK, that's what we'd expect
        else:
            self.fail("Didn't raise an assertion error for arguments\
                        with different lengths")

    def assert_is_file(self, filename, msg):
        """Check if file exist."""
        self.assertTrue(os.path.isfile(filename), msg)
    
    def assert_pat_in_file(self, filename, pat):
        self.assertTrue(fu.grep_all_in_file(filename, pat), "Cannot find pattern %s in %s" % (pat, filename)) 

    def assert_all_patterns_in_file(self, filename, pats):
        """Assert if all patterns passed are included in the file."""
        if type(pats) == str:
            pats = (pats,)
        txt = fu.read_file(filename)
        for pat in pats:
            res = re.findall(pat, txt)
            if not res: 
                self.fail("Cannot find pattern %s in %s" % (pat, filename))
    
    def assert_all_patterns_not_in_file(self, filename, pats):
        """Assert if none of the patterns passed are included in the file."""
        if type(pats) == str:
            pats = (pats,)
        txt = fu.read_file(filename)
        for pat in pats:
            res = re.findall(pat, txt)
            if res: 
                self.fail("Should not find pattern %s in %s" % (pat, filename))
    
    def should_crawl_and_log(self, agent_cfg, urls, expected_strs, unexpected_strs=[]):
        # TODO: add support for normal browsers 
        if agent_cfg.has_key("type") and 'chrome' in agent_cfg['type']:
            br = ag.ChromeAgent()
        else:  
            br = ag.HeadlessAgent()
        
        if not agent_cfg.has_key("timeout"):
            agent_cfg["timeout"] = DEFAULT_TEST_CRAWL_TIMEOUT        
        
        br.setOptions(agent_cfg)
        cr_job = ag.CrawlJob(br)
        cr_job.urls = [urls,] if isinstance(urls, basestring) else urls
        cr_job.url_tuples = zip(xrange(1, len(urls)+1), urls)
        
        ag.run_crawl(cr_job)
        
        self.assertTrue(os.path.isdir(cr_job.job_dir), 'No job folder created!')
        for idx, url in  enumerate(cr_job.urls):
            outfile = os.path.join(cr_job.job_dir, fu.get_out_filename_from_url(url, str(idx+1)))  
            self.assertTrue(os.path.isfile(outfile), 'Cannot find log file %s' % outfile)
            self.assert_all_patterns_in_file(outfile, expected_strs)
            self.assert_all_patterns_not_in_file(outfile, unexpected_strs)
            
    def new_temp_file(self,filename):
        """Add file to remove-list."""
        self.files_to_remove.append(filename)
        return filename
    
    def abs_test_file_name(self, filename):
        """Return full path for file."""
        base = os.getcwd()
        return os.path.join(base, filename)
    
    
    def should_crawl_and_find_swfs(self, url, expected_strings=(None, None), unexpected_strings=(None, None), crawler_type='chrome_lazy'):
        expected_fields, expected_values = expected_strings
        unexpected_fields, unexpected_values = unexpected_strings
        
        crawl_id = ag.crawl_sites([(1, url),], crawler_type, num_crawl_urls=1)
        
        db_conn = dbu.mysql_init_db()
        db_curs = db_conn.cursor(mdb.cursors.DictCursor)
        
        rows = swu.get_swf_obj_from_db('crawl_id', int(crawl_id), db_curs)
        
        if expected_fields:
            found_dict = {}
            for field in expected_fields:
                found_dict[field] = False
        
        for row in rows:
            if expected_fields:
                for expected_field, expected_value in zip(expected_fields, expected_values):
                    if expected_value in row[expected_field]:
                        found_dict[expected_field] = True
                        print 'found in ',  row[expected_field]
                    
            if unexpected_values:
                for unexpected_field, unexpected_value in zip(unexpected_fields, unexpected_values) :
                    if unexpected_value in row[unexpected_field]:
                        self.fail('Unexpected field %s with unexpected value %s found' %(unexpected_field, unexpected_value))                    
        if expected_fields:
            for field, found in found_dict.iteritems():
                if not found:
                    self.fail('Cannot find %s' % field)

        db_curs.close()
        db_conn.close()
    
    @classmethod
    def tearDownClass(cls):
        for f in cls.files_to_remove: # remove test files
            print f, 'to be removed'
            if os.path.lexists(f):
                os.unlink(f)
                
                
                
