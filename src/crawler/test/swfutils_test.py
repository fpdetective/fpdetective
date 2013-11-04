
import unittest
import swfutils as swfu
import dbutils as dbu
import fileutils as fu
from fpdtest import FPDTest
import MySQLdb as mdb

class Test(FPDTest):

    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
        
    def setUp(self):
        #test_db_file = ':memory:'
        #schema = '../swf_schema.sql'
        self.db_conn = dbu.mysql_init_db('fp_detective_test') # get a cursor for db        
        self.db_cursor = self.db_conn.cursor(mdb.cursors.DictCursor)
    
    def tearDown(self):
        self.db_conn.close()

    def test_human_readable_occ_vector(self):
        all_fp_as_strs = swfu.FP_ACTIONSCRIPT_STR_LIST
        
        all_ones = (1,)*len(all_fp_as_strs)
        self.assertListEqual(swfu.human_readable_occ_vector(all_ones), all_fp_as_strs)
        
        all_zeros = (0,)*len(all_fp_as_strs)
        self.assertListEqual(swfu.human_readable_occ_vector(all_zeros), [])
        
        occ_test_vector = (0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        swfu.human_readable_occ_vector(occ_test_vector)
        hr_test_vector = ['getFontList', '[cC]apabilities', 'screenDPI', 'screenResolutionX', 
         'screenResolutionY', '[cC]apabilities\\.language', '[cC]apabilities\\.version', 
         'serverString', 'getTimezoneOffset', 'XMLSocket']
        
        self.assertListEqual(swfu.human_readable_occ_vector(occ_test_vector), hr_test_vector)
        
    def test_get_domain_from_path(self):
        domain_name = swfu.get_domain_from_path
        self.assertEqual(domain_name('/abc.com/xyz/frs/abc.swf'), 'abc.com')
        self.assertEqual(domain_name('/xyz.org/abc.com/frs/abc.swf'), 'xyz.org')
        self.assertEqual(domain_name('/old.dir/abc.com/frs/abc.swf'), 'old.dir') # fails in this case

    def test_get_swf_version(self):
        self.failIf(swfu.get_swf_version('files/emptyfile.txt'))
        self.assertEqual(swfu.get_swf_version('files/AYB.swf'), 4) # thanks to https://github.com/claus/as3swf/
        self.assertEqual(swfu.get_swf_version('files/FontList.swf'), 14) # thanks to https://github.com/cubiq/underpants-project/
        
        
    def test_is_swf_file(self):
        self.failIf(swfu.is_swf_file('files/regexp'))
        self.failUnless(swfu.is_swf_file('files/AYB.swf'))
        self.failUnless(swfu.is_swf_file('files/FontList.swf'))

    def test_vector_to_str(self):
        tp = (1,0,1,0,1,1,1,0)
        db_str = swfu.vector_to_str(tp)
        self.assertEqual(tp, swfu.str_to_vector(db_str)) 
    
    def compare_swf_info(self, row, swf_info):
        self.assertEqual(row['local_path'], swf_info.local_path)
        self.assertEqual(row['domain'], swf_info.domain)
        self.assertEqual(row['page_url'], swf_info.page_url)
        self.assertEqual(row['duplicate'], swf_info.duplicate)
        self.assertEqual(row['swf_url'], swf_info.url)
        self.assertEqual(swfu.str_to_vector(row['occ_vector']), swf_info.occ_vector)
        self.assertEqual(swfu.str_to_vector(row['feat_vector']), swf_info.feat_vector)
        self.assertEqual(row['hash'], swf_info.hash)
        self.assertEqual(row['referer'], swf_info.referer)
                
    def populate_swf_info(self):
        swf_info = swfu.SwfInfo()
        swf_info.local_path = 'test/test.swf' 
        swf_info.domain = 'test.com'
        swf_info.page_url = 'http://test.com/homepage'
        swf_info.duplicate = 1
        swf_info.url = 'http://test.com/test.swf'
        swf_info.occ_vector = (1,0,1,0,1,1,1,0)
        swf_info.feat_vector = (1,0,1,0,1,1,1,1)
        swf_info.hash = 'adfefef31313065sdf0s3d0f3s5df03s53asd3f30sdf'
        swf_info.referer = 'http://test.com/homepage' 
        swf_info.occ_string = 'getFontList'
        swf_info.crawl_id = 123
        swf_info.site_info_id = 1234
        
        return swf_info
    
    def test_add_swf_to_db(self):
        swf_info = self.populate_swf_info()
        
        swf_id = swfu.add_swf_to_db(swf_info, self.db_conn)
        
        if not self.db_cursor.execute('SELECT * FROM swf_obj WHERE id = %s', (swf_id,)):
            self.fail("Cannot find SWF in db")
                
        row = self.db_cursor.fetchone()

        self.compare_swf_info(row, swf_info)    
    
    def test_add_same_swf_to_db(self):
        swf_info = self.populate_swf_info()
        swf_info.duplicate = 1 # we've seen this swf before
        
        swf_id = swfu.add_swf_to_db(swf_info, self.db_conn)
        
        rows = swfu.get_swf_obj_from_db('hash', swf_info.hash, self.db_cursor)
        if rows:
            vector = swfu.str_to_vector(rows[0]['occ_vector'])
            swf_filename = rows[0]['local_path']
            new_swf = 1
        
        swf_info.filename = swf_filename
        swf_info.duplicate = new_swf
        swf_info.occ_vector = vector
            
        swf_id_2 = swfu.add_swf_to_db(swf_info, self.db_conn)
        
        if not self.db_cursor.execute('SELECT * FROM swf_obj WHERE id = %s', (swf_id,)):
            self.fail("Cannot find SWF in db")
        
        row_orig = self.db_cursor.fetchone()
        
        if not self.db_cursor.execute('SELECT * FROM swf_obj WHERE id = %s', (swf_id_2,)):
            self.fail("Cannot find second SWF in db")
        
        row_second = self.db_cursor.fetchone()
        
        self.compare_swf_info(row_orig, swf_info)
        self.compare_swf_info(row_second, swf_info)
    
    def test_get_swf_obj_from_db(self):
        swf_info = self.populate_swf_info()
        swf_id = swfu.add_swf_to_db(swf_info, self.db_conn)
        rows = swfu.get_swf_obj_from_db('id', swf_id, self.db_cursor)
        self.assert_(len(rows), 'No SWF can be found in DB')
        for row in rows:
            self.assertTrue('http' in row['swf_url'], 'swf url is does not have http in it')

        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()