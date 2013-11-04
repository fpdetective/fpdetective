import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import utils as ut
#from random import randint
from fpdtest import FPDTest
from time import sleep, time

class UtilsTest(FPDTest):
        
    def test_cancel_timeout(self):
        start_time = time()
        ut.timeout(1)
        sleep(0.3)
        ut.cancel_timeout()
        elapsed_time = time() - start_time
        self.assertLess(elapsed_time, 5, 'Cancel time does not work. %s' % elapsed_time)
    
    def test_rand_str(self):
        # Test default parameters
        random_str = ut.rand_str()
        self.assertEqual(ut.DEFAULT_RAND_STR_SIZE, len(random_str), 
                         "rand_str does not return string with default size!")
        self.failIf(set(random_str) - set(ut.DEFAULT_RAND_STR_CHARS), "Unexpected characters in string!")
        
        # Test with different sizes and charsets
        sizes = [1, 2, 10, 100] 
        charsets = (ut.DEFAULT_RAND_STR_CHARS, ut.DIGITS)
        for size in sizes:
            for charset in charsets:
                random_str = ut.rand_str(size, charset)
                self.assertEqual(len(random_str), size, 
                                 "Random string size is different than expected!")
                self.failIf(set(random_str) - set(ut.DEFAULT_RAND_STR_CHARS), 
                            "Unexpected characters in string!")     
        

    def test_occurence_vector(self):
        grpattern = ['pat1', 'pat2', 'pat3']
        occ_vector = ut.occurence_vector # assign to a local var for brevity
        
        text = 'pat2 pat1 foo pat3 bar pat3'
        self.assertEqual((1,1,1), occ_vector(text, grpattern))
        
        text = 'pat1 foo bar bar foo pat3' 
        self.assertEqual((1,0,1), occ_vector(text, grpattern))
        
        text = 'pat1 foo pat3'
        grpattern = ['pat1']
        self.assertEqual((1,), occ_vector(text, grpattern))
    
        grpattern = ['xyz']
        self.assertEqual((0,), occ_vector(text, grpattern))
    
        text = 'pat1pat2pat3'
        grpattern = ['pat1', 'pat2', 'pat3']
        self.assertEqual((1, 1, 1), occ_vector(text, grpattern))
        
        grpattern = ['pat5', 'pat5']
        self.assertEqual((0, 0), occ_vector(text, grpattern))
    
    def test_cosine_similarity(self):
        self.assertEqual(1.0, ut.cosine_similarity([0,1], [0,1]))
        self.assertEqual(0.0, ut.cosine_similarity([1,0], [0,1]))
        self.should_raise_for_diff_len_args(ut.cosine_similarity, [0, 1], [0])
        self.should_raise_for_diff_len_args(ut.cosine_similarity, [0], [])
        # self.assertR Equal(0.0, ut.cosine_similarity([1,0,1,1], [0,0,1]))
    
    def test_hamming_dist(self):
        hamming_dist = ut.hamming_dist
        self.assertEqual( hamming_dist([0, 1], [0, 1]), 0 )
        self.assertEqual( hamming_dist([0, 0], [1, 1]), 2 )
        self.assertEqual( hamming_dist([1, 0, 0, 0], [0, 1, 1, 1]), 4)
        self.assertEqual( hamming_dist("abc", "abd"), 1)
        self.assertEqual( hamming_dist("cba", "abc"), 2)
        self.should_raise_for_diff_len_args(ut.hamming_dist, "cba", "abcDEF")
    
    def test_jaccard_index(self):
        jacc = ut.jaccard_index
        self.assertEqual(jacc([1,1], [1,1]) , 1.0)
        self.assertEqual(jacc([1,1], [0,1]) , 0.5)
        self.assertEqual(jacc([1,0], [0,1]) , 0.0)
        self.assertEqual(jacc([1,1,1,1], [0,1,0,1]) , 0.5)
        self.should_raise_for_diff_len_args(ut.hamming_dist, [0], [0,1])
 
    def test_is_unique(self):
        self.assertEqual(ut.is_unique([1,2,3]), True)
        self.assertEqual(ut.is_unique((1,2,3,4)), True)
        self.assertEqual(ut.is_unique([1]), True)
        self.assertEqual(ut.is_unique([]), True)
        self.assertEqual(ut.is_unique([1,2,3,1]), False)
        self.assertEqual(ut.is_unique((1,1)), False)
        self.assertEqual(ut.is_unique([1,1]), False)
                 
        
   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_init_db']
    unittest.main()
