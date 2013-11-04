
import unittest
import os
import inspect
import fileutils as fu
import utils as ut
import swfutils as swfu
from fpdtest import FPDTest

class Test(FPDTest):    
        
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_write_to_file(self):
        filename = self.new_temp_file('write_test.txt')
        random_str = ut.rand_str(100)
        fu.write_to_file(filename, random_str)
        self.assertEqual(random_str, fu.read_file(filename))

    def test_read_file(self):
        file_content = fu.read_file(os.path.realpath(__file__))
        if not 'whatever I write here' in file_content:
            self.fail('Cannot read itself')
    
    def test_add_symlink(self):
        test_link = self.new_temp_file('test_link') # symbolic link
        src_file = self.new_temp_file('linktest.txt') 
        fu.write_to_file(src_file, "link test")
        
        fu.add_symlink(test_link, src_file)
        self.failUnless(os.path.lexists(test_link))
        
    
    def test_grep_in_dir(self):
        # test if it can find a filename pattern in txt files
        matches = list(fu.gen_grep_in_dir('files', r'asdf[0-9]+\.swf', r'*.txt'))
        shouldbe = [('files/regexp2.txt', 'asdf898952325.swf')]
        self.assertListEqual(shouldbe, matches, "")
        
        # test if it can find a files (including those in the subfolder) with a more generic pattern and
        shouldbe =set((('files/regexp.txt', '012340123rgxpttest1'), 
                      ('files/regexp.txt', '012340123rgxpttest2'), 
                      ('files/sub/regexp.txt', '012340123rgxpttest1')))
        matches = set(fu.gen_grep_in_dir('files', r'[0-5]+rgxpttest[12]', r'*.txt')) 
        self.assertSetEqual(shouldbe, matches)
    
    def test_gen_open(self):
        """ test if files are opened correctly """
        files = ['files/swflogs.txt', 'files/hertrxcrawl.log'] 
        result = [f.readline().startswith('yahoo') for f in fu.gen_open(files)]
        self.assertListEqual(result, [True, False])
    
    def test_gen_find_files(self):
        # Should match files in subdirectories
        results = set(fu.gen_find_files('regexp*.txt', 'files'))
        regex_files = set(('files/regexp2.txt', 
                           'files/regexp.txt', 
                           'files/sub/regexp.txt'))
        self.assertSetEqual(results, regex_files)
        
        results = set((fu.gen_find_files('*.log', 'files')))
        log_files = set(['files/hertrxcrawl.log'])
        self.assertSetEqual(results, log_files)
        
        # should match .as and .flr files
        files = list(fu.gen_find_files(swfu.AS_SOURCE_FILE_PATTERN, 'files'))
        if not len(files) or not 'TweenPlugin.as' in files[0]:
            self.fail("Couldn't match .as file in directory")
        
    
    def test_gen_grep_in(self):
        
        matches = fu.gen_grep_in('files', r'asdf[0-9]+\.swf', '*.txt')
        self.failUnless(inspect.isgenerator(matches)) # test if it returns a generator
        shouldbe = [('files/regexp2.txt', 'asdf898952325.swf')]
        match_list = list(matches)
        self.assertListEqual(match_list, shouldbe)
        
        matches = list(fu.gen_grep_in('files', r'a', 'NONONOMATCH'))
        self.assertListEqual(matches, [], "Should not match NONONOMATCH")
        
        # should also match file with the same name in the subfolder
        result = set(fu.gen_grep_in('files', r'wsed\d+.js', 'regexp.txt'))
        shouldbe = set([('files/regexp.txt', 'wsed123456789.js'), 
                        ('files/sub/regexp.txt', 'wsed123456789.js')])
        self.assertSetEqual(result, shouldbe)
         
        # this one shouldn't match the other file (regexp.txt) in the subfolder
        result = list(fu.gen_grep_in('NONONOMATCH.txt', r'a'))
        self.assertListEqual(result, [], "Should not match in non-existent file")
    
    def test_gen_cat_file(self):
        result = fu.gen_cat_file('files/regexp.txt')
        self.failUnless(inspect.isgenerator(result)) # test if it returns a generator
        self.assertEqual(6, len(list(result)))
        
    def test_gen_cat(self):    
        somelist = [1, 2, 3, 4]
        result = list(fu.gen_cat(([1,2], [3, 4])))
        self.assertListEqual(result, somelist)
        
        # concat'ing mixed input
        result = list(fu.gen_cat((['1','2'], [3])))
        mixedlist = ['1', '2', 3]
        self.assertListEqual(result, mixedlist)
        
        # concat'ing files
        as_file_names = fu.gen_find_files('*.as', 'files/fp')
        self.failUnless(len(list(as_file_names)) > 1)
        
        
    def test_gen_grep_in_lines(self):
        loglines = ('http://foo.com/abc.swf',
                    'http://foo.org/def.swf',
                    'http://bar.com/abc.swf',
                    'http://bar.org/def.swf')
        
        fplines = fu.gen_grep_in_lines(r'abc.swf|def.swf',loglines)
        self.failUnless(inspect.isgenerator(fplines))
        self.assertEqual(4, len(list(fplines)))

    def test_file_occurence_vector(self):              
        result = fu.file_occurence_vector('files/fp/fp_funs.as',
                                                swfu.FP_ACTIONSCRIPT_STR_LIST)
        shouldbe = (0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertTupleEqual(result, shouldbe)
        
        # Test with an empty file
        result = fu.file_occurence_vector('files/emptyfile.txt',
                                                swfu.FP_ACTIONSCRIPT_STR_LIST)
        shouldbe = (0,)*len(swfu.FP_ACTIONSCRIPT_STR_LIST)
        self.assertTupleEqual(result, shouldbe)
    
    
    def test_hash_file(self):
        filename = self.new_temp_file('hash_test.txt')
        random_str = ut.rand_str(1000)
        fu.write_to_file(filename, random_str)
        self.assertEqual(fu.hash_file(filename, 'sha1'), 
                         ut.hash_text(random_str, 'sha1'), 
                         'SHA1 hashes don\'t match')
        self.assertEqual(fu.hash_file(filename), ut.hash_text(random_str), 
                         'Hashes with default algo don\'t match')
    
    def get_base_filename_from_url(self):
        url = 'http://youtube.com'
        prefix = '2'
        self.assertEqual(fu.get_base_filename_from_url(url, prefix), '%s-http-youtube-com' % (prefix))
        
        url = 'youtube.com/'
        prefix = '2'
        self.assertEqual(fu.get_base_filename_from_url(url, prefix), '%s-youtube-com-' % (prefix))
        
    def test_get_out_filename_from_url(self):
        url = 'http://youtube.com'
        prefix = '2'
        self.assertEqual(fu.get_out_filename_from_url(url, prefix), '%s-http-youtube-com.txt' % (prefix))
        self.assertEqual(fu.get_out_filename_from_url(url, prefix, '.txt'), '%s-http-youtube-com.txt' % (prefix))
        self.assertEqual(fu.get_out_filename_from_url(url, prefix, '.log'), '%s-http-youtube-com.log' % (prefix))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()