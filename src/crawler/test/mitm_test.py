
import unittest
import os
from fpdtest import FPDTest
from utils import run_cmd 
import mitm

from time import time, sleep

TIME_TOLERANCE = 1


class mitmcfg:
    outfile = '/tmp/mitmout'
    dmpfile = outfile + '.dmp'   
     
class Test(FPDTest):
        
    def setUp(self):
        self.new_temp_file(mitmcfg.outfile) # this will be removed by base class
        self.new_temp_file(mitmcfg.dmpfile) # this will be removed by base class
        self.pids = []
        
    def tearDown(self):        
        for pid in self.pids:
            run_cmd('kill %s' % pid)
            print 'Killing mitmdump proc with id: %s' % pid
        if os.path.isfile(mitmcfg.dmpfile):
            os.remove(mitmcfg.dmpfile)
        
    def assert_port_and_pid_is_ok(self, port, pid, msg):
        self.assertIsNotNone(pid, "Process id is empty, %s" % msg)
        self.pids.append(pid)
        self.assertIsNotNone(port, "Port is empty, %s" % msg)
         
    def assert_port_and_pid_is_empty(self, port, pid, msg):
        self.assertIsNone(pid, "Process id is not empty, %s" % msg)
        self.pids.append(pid)
        self.assertIsNone(port, "Port is not empty, %s" % msg)
        
    def test_should_return_port_pid_and_create_out_file(self):
        port, pid = mitm.run_mitmdump(mitmcfg.outfile, 2) # call with a port number
        self.assert_port_and_pid_is_ok(port, pid, "cannot start mitmdump with default port")
        self.assert_is_file(mitmcfg.dmpfile, "Output file %s is missing" % mitmcfg.dmpfile)
        
    def test_should_work_with_default_port(self):
        port, pid = mitm.run_mitmdump(mitmcfg.outfile, 2) # call without a port number
        self.assert_port_and_pid_is_ok(port, pid, "cannot start mitmdump with default port")
        self.assert_is_file(mitmcfg.dmpfile, "Output file %s is missing, cannot start mitmdump with default port" % mitmcfg.dmpfile)

    def test_should_run_process_async(self):
        start = time()
        mitm.run_mitmdump(mitmcfg.outfile, 60) # call with a long timeout, 60sec
        time_passed = time() - start
        self.assertLess(time_passed, mitm.PORT_TRY_TIMEOUT+TIME_TOLERANCE, "mitmdump didn't return immediately %s " % time_passed)
     
    def test_should_run_multiple_instances_together(self):
        for i in xrange(50): # run 50 mitmdump instances together 
            i += 1
            sleep(0.2)
            try:
                mitm.run_mitmdump(mitmcfg.outfile, 5) # call with a long timeout, 60sec
            except:
                self.fail("Cannot start %s mitmdump process in parallel" % i)
    
    def test_get_free_port(self):
        port = mitm.get_free_port()
        self.assert_(port > mitm.MIN_PORT_NO, "get_free_port return privileged port")
        self.assert_(port < mitm.MAX_PORT_NO, "get_free_port return out of range port")
            

    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()