
import sys
import os
import parallelize
import mitm
import common as cm
import fileutils as fu
import dbutils as dbu
import utils as ut
import log_parser as lp
import crawler as cr
from functools import partial
from webutils import gen_url_list
from time import strftime, sleep
from random import random

user_path = os.path.expanduser
join_path = os.path.join

KILL_PROC_AFTER_TIMEOUT = 5
from log import wl_log

PHANTOM_COMMON_OPTIONS = '--web-security=false --disk-cache=false --ignore-ssl-errors=true --cookies-file=/dev/null --local-storage-path=/dev/null'
CHROME_COMMON_OPTIONS = '--allow-running-insecure-content --disable-background-networking --ignore-certificate-errors  --no-sandbox --disk-cache-size=0 --enable-logging=stderr --v=1'

# TODO pass parameters to same JS file instead of having many JS files... 

# User Agent strings 
UA_STR_CHROMIUM_32_LIN = 0
UA_STR_IE_9_WIN7 = 1
UA_STRINGS = ('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1673.0 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)', # IE9 on Win7
)

ERR_CMD_TIMEDOUT = 31744

MAX_PARALLEL_PROCESSES = 100 # max no of processes in parallel
MAX_PARALLEL_PROCESSES_FLASH = 50 # max no of processes in parallel
MAX_CHROME_INST_PARALLEL = 20 # max no of processes in parallel

AGENT_CFG_PHANTOM_MOD_HOME_PAGE = {
                         'type': 'lazy',
                         'post_visit_func': lp.parse_log_dump_results,
                         'binary_path': cm.PHANTOM_MOD_BINARY,
                         'cmd_line_options': PHANTOM_COMMON_OPTIONS,
                         'fc_fontdebug': 0,
                         'main_js': cm.CASPER_JS_LAZY_HOMEPAGER,
                         'timeout': 90
                        }



AGENT_CFG_DNT_PHANTOM_LAZY = {
                         'type': 'dnt',
                         'post_visit_func': lp.parse_log_dump_results,
                         'binary_path': cm.PHANTOM_MOD_BINARY,
                         'cmd_line_options': PHANTOM_COMMON_OPTIONS,
                         'main_js': cm.CASPER_JS_DNT_LAZY, # sends DNT=1 header
                         'timeout': 90
                        }

AGENT_CFG_PHANTOM_MOD_CLICKER = {
                        'type': 'clicker',
                         'post_visit_func': lp.parse_log_dump_results,
                         'binary_path': cm.PHANTOM_MOD_BINARY,
                         'cmd_line_options': PHANTOM_COMMON_OPTIONS,
                         'main_js': cm.CASPER_JS_CLICKER,
                         'timeout': 210
                        }

AGENT_CFG_CHROME_LAZY = {
                    'type': 'chrome_lazy',
                    'binary_path': cm.CHROME_MOD_BINARY,
                    'use_mitm_proxy': True,
                    'post_visit_func': mitm.process_dump, # register function to post-process data
                    'cmd_line_options': CHROME_COMMON_OPTIONS,
                    'timeout': 50
                    }

AGENT_CFG_CHROME_CLICKER = {
                    'type': 'chrome_clicker',
                    'binary_path': 'python %s' % cm.CRAWLER_PY_PATH,
                    'use_mitm_proxy': True,
                    'post_visit_func': mitm.process_dump,
                    'timeout': 240
                    }
   
class CrawlJob(object):
    def __init__(self, agent):
        self.job_dir = create_job_folder()
        self.desc = ''
        self.urls = []
        self.url_tuples = []
        self.num_crawl_urls = 0
        self.max_parallel_procs = MAX_PARALLEL_PROCESSES
        self.crawl_agent = agent
        self.crawl_agent.crawl_job = self
        self.crawl_agent.job_dir = self.job_dir # for passing to multiprocessing worker - should find a better way
        self.index_html_log = os.path.join(self.crawl_agent.job_dir, 'index.html')
        self.db_conn = dbu.mysql_init_db('fp_detective')
        self.crawl_id = dbu.add_crawl_job_to_db(self, self.db_conn)
        self.crawl_agent.crawl_id = self.crawl_id
    
    def __del__(self):
        if (self.db_conn):
            dbu.update_crawl_time(self.db_conn, self.crawl_id)
            self.db_conn.commit()
            self.db_conn.close()
        
    def setOptions(self, cfg):
        """Set options for crawl job."""
        for key in cfg.keys():
            setattr(self, key, cfg[key]) # values are not checked or sanitized! Should we? !!!
            
        if self.crawl_agent: # if we have ua agent, set job-related properties 
            self.crawl_agent.crawl_job = self
            self.crawl_agent.job_dir = self.job_dir # for passing to multiprocessing worker - should find a better way
        
        dbu.update_crawl_job(self, self.db_conn)    
        
class CrawlAgent(object):
    """Class for crawls agent."""
    def __init__(self):
        self.user_agent_str = UA_STRINGS[UA_STR_CHROMIUM_32_LIN] # Chromium 25 on Ubuntu is default 
        self.binary_path = cm.PHANTOM_MOD_BINARY
        self.cmd_line_options = PHANTOM_COMMON_OPTIONS
        self.use_mitm_proxy = False # mitm
        self.mitm_proxy_logs = False # disable mitmproxy logging
        self.crawl_job = None # to be set by crawljob
        self.job_dir = ''
        self.fc_fontdebug = 0 # set FC_DEGUB env variable to 0 before running the agent.
        self.crawl_id = 0
        
    def setOptions(self, cfg):
        """Set options for crawler agent."""
        for key in cfg.keys():
            setattr(self, key, cfg[key]) # values are not checked or sanitized! Should we? !!!
            # print 'setoptions', key, '=>', cfg[key]  
        return self
    
class HeadlessAgent(CrawlAgent):
    """Class for headless crawler agents such as CasperJS and PhantomJS."""
    def __init__(self):
        self.type = 'lazy' # lazy will only visit homepages, clicker will click links on the page 
        self.main_js = cm.CASPER_JS_LAZY_HOMEPAGER # JS that PhantomJS will execute - first parameter
        self.timeout = 90 # time to wait before killing the browser process
        self.screenshot = False # take a screenshot or not
        self.casper_client_js = 'NO_CLIENT_JS' # casper should not load any client scripts
        self.post_visit_func = lp.parse_log_dump_results # worker function that will run after visit 
        super(HeadlessAgent, self).__init__()

class ChromeAgent(CrawlAgent):
    """Class for Chromium based crawler."""
    def __init__(self):
        
        self.binary_path = 'python %s' % cm.CRAWLER_PY_PATH
        self.type = 'chrome_lazy'
        self.timeout = 90
        self.screenshot = '' #
        self.main_js = '' # irrelevant for chrome
        self.casper_client_js = ''
        self.post_visit_func = mitm.process_dump
        self.use_mitm_proxy = True # use mitmdump to save flash files
        self.mitm_proxy_logs = False # disable logging from mitmproxy
        self.cmd_line_options = ''
        super(ChromeAgent, self).__init__()


def get_visit_cmd(agent_cfg, proxy_opt, stdout_log, url):
    """Return command for a visit."""
    xvfb = ''
    caps_name = ''
    clientjs = ''
    
    if 'chrome' in agent_cfg['type']:
        proxy_opt = '--proxy-server=%s' % proxy_opt
        redir_str =  '2>&1 | tee %s' % stdout_log # chrome logs to stderr, we redirect it to stdout
        cmd_line_options = agent_cfg['cmd_line_options'] + \
            ' --disk-cache-dir=/tmp/tmp_cache%s --user-data-dir=/tmp/temp_profile%s' % (ut.rand_str(), ut.rand_str())
        xvfb = 'xvfb-run --auto-servernum' # use xvfb for chrome
    else:
        proxy_opt = '--proxy=%s' % proxy_opt
        redir_str = ' > %s' % stdout_log # redirect all output to log file
        cmd_line_options = agent_cfg['cmd_line_options']
        caps_name =  stdout_log[:-4] + '.png' if agent_cfg['screenshot'] else 'NO_SCREENSHOT' 
        clientjs = agent_cfg['casper_client_js']
    
    # TODO separate cmd construction for chrome and phantomjs
    cmd = 'export FC_DEBUG=%s; %s timeout -k %s %s %s %s %s %s %s %s %s %s' \
        % (agent_cfg['fc_fontdebug'], xvfb, KILL_PROC_AFTER_TIMEOUT, agent_cfg['timeout'], agent_cfg['binary_path'], 
           cmd_line_options, proxy_opt, agent_cfg['main_js'], url, 
           caps_name, clientjs, redir_str)
    
    return cmd

def crawl_worker(agent_cfg, url_tuple):
    """Crawl given url. Will work in parallel. Cannot be class method."""
    MAX_SLEEP_BEFORE_JOB = 10 # prevent starting all parallel processes at the same instance
    sleep(random() * MAX_SLEEP_BEFORE_JOB) # sleep for a while
    
    try:
        idx, url = url_tuple
        idx = str(idx)
        
        stdout_log =  os.path.join(agent_cfg['job_dir'], fu.get_out_filename_from_url(url, str(idx), '.txt'))
       
        if not url[:5] in ('data:', 'http:', 'https', 'file:'):
            url = 'http://' + url
        
        proxy_opt = mitm.init_mitmproxy(stdout_log[:-4], agent_cfg['timeout'], agent_cfg['mitm_proxy_logs']) if agent_cfg['use_mitm_proxy'] else ""
        
        if not 'chrome_clicker' in agent_cfg['type']:
            cmd = get_visit_cmd(agent_cfg, proxy_opt, stdout_log, url)
            wl_log.info('>> %s (%s) %s' % (url, idx, cmd))
            status, output = ut.run_cmd(cmd) # Run the command
            if status and status != ERR_CMD_TIMEDOUT:
                wl_log.critical('Error while visiting %s(%s) w/ command: %s: (%s) %s' % (url, idx, cmd, status, output))
            else:
                wl_log.info(' >> ok %s (%s)' % (url, idx))
            
        else:
            cr.crawl_url(agent_cfg['type'], url, proxy_opt)
            
        sleep(2) # this will make sure mitmdump is timed out before we start to process the network dump
        if agent_cfg['post_visit_func']: # this pluggable function will parse the logs and do whatever we want
            agent_cfg['post_visit_func'](stdout_log, crawl_id=agent_cfg['crawl_id'], url=url)
            
    except Exception as exc:
        wl_log.exception('Exception in worker function %s %s' % (url_tuple, exc))


def logger_fn(logger, level, msg):
    fn = getattr(logger, level) # level is info, debug, critical etc
    fn(msg)

def run_crawl(cr_job):
    cr_agent = cr_job.crawl_agent
    url_tuples = cr_job.url_tuples

    # only copy the variables that'll be used by the agent. Parallelization requires picklable variables. 
    cfg_dict = dict([(i, cr_agent.__dict__[i]) for i in \
                     ['fc_fontdebug', 'post_visit_func', 'timeout', 'binary_path', \
                      'use_mitm_proxy', 'mitm_proxy_logs', 'cmd_line_options', 'main_js', \
                      'casper_client_js', 'screenshot', 'job_dir', 'index_html_log', 'type', 'crawl_id'] if i in cr_agent.__dict__])

    worker = partial(crawl_worker, cfg_dict)
    
    parallelize.run_in_parallel(url_tuples, worker, cr_job.max_parallel_procs)
    
    lp.close_index_html(cr_job.index_html_log)
    
def prep_run_folder():
    """Create a base run folder if it does not exist, add jobs and logs subfolders.
    
    base --> base folder
    -- logs
    ---- fpd-20130402-080141.log --> application log
    -- jobs
    ---- 20130567 --> job folder
    ------ 1-google-com.txt etc. output files (font logs, stdout logs from crawler)
    """
    if not os.path.isdir(cm.BASE_FP_RUN_FOLDER):
        os.mkdir(cm.BASE_FP_RUN_FOLDER)
        os.mkdir(cm.BASE_FP_JOBS_FOLDER)
        os.mkdir(cm.BASE_FP_LOGS_FOLDER)
                
def create_job_folder():
    """Prepare output folder."""
    prep_run_folder()
    output_dir = os.path.join(cm.BASE_FP_JOBS_FOLDER, strftime("%Y%m%d-%H%M%S"))
    if os.path.isdir(output_dir):
        output_dir = os.path.join(cm.BASE_FP_JOBS_FOLDER, strftime("%Y%m%d-%H%M%S"))
    
    os.mkdir(output_dir)
        
    fu.add_symlink(os.path.join(cm.BASE_FP_JOBS_FOLDER, 'latest'), output_dir)
    return output_dir
    
def crawl_sites(url_tuples, crawler_type, num_crawl_urls=0, max_parallel_procs=MAX_PARALLEL_PROCESSES):
    if crawler_type == 'lazy':                    
        agent_cfg = AGENT_CFG_PHANTOM_MOD_HOME_PAGE
        agent = HeadlessAgent()
    elif crawler_type == 'clicker':
        agent_cfg = AGENT_CFG_PHANTOM_MOD_CLICKER
        agent = HeadlessAgent()
    elif crawler_type == 'chrome_lazy':
        agent_cfg = AGENT_CFG_CHROME_LAZY
        agent = ChromeAgent()
    elif crawler_type == 'chrome_clicker':
        agent_cfg = AGENT_CFG_CHROME_CLICKER
        agent = ChromeAgent()
    elif crawler_type == 'dnt': # TODO scripts should take DNT as a parameter 
        agent_cfg = AGENT_CFG_DNT_PHANTOM_LAZY
        agent = HeadlessAgent()    
        
    agent.setOptions(agent_cfg)
    cr_job = CrawlJob(agent)
    
    job_cfg = {
              'desc': "Crawl for browser fingerprint detection", 
              'max_parallel_procs': max_parallel_procs,
              'urls':  [],
              'url_tuples':  url_tuples,
              'num_crawl_urls': num_crawl_urls
              }
    
    cr_job.setOptions(job_cfg)
    wl_log.info('Will crawl with agent config: %s and job config: %s' %(agent_cfg, job_cfg))
    run_crawl(cr_job)
    return cr_job.crawl_id

def crawl_site_for_font_probing(url, agent_config, job_config=None):
    """Visit a site for font probing and return results."""
    
    ha = HeadlessAgent()
    cr_job = CrawlJob(ha)
    ha.setOptions(agent_config)
    
    job_cfg = job_config or {
                  'desc': 'Crawl for font probing detection', 
                  'max_parallel_procs': MAX_PARALLEL_PROCESSES,
                  'urls':  (url,),
                  'num_crawl_urls':1
                  }
    cr_job.setOptions(job_cfg)
    run_crawl(cr_job)
    
    for json_file in fu.gen_find_files("*.json", cr_job.job_dir):
        return lp.load_domainfo_from_json_file(json_file)
    
    return None # no json file can be found

if __name__ == '__main__':
    
    start = 1 # start from the first ranked item in the (Alexa) file 
    stop = 0 # start from the first ranked item in the (Alexa) file
    max_parallel_procs = MAX_PARALLEL_PROCESSES
    url_file = ''
    args = sys.argv[1:]
    
    if not args:
        print 'usage: --url_file url_file --stop stop_pos [--start start_pos] --type [lazy | clicker | chrome_lazy | chrome_clicker | dnt | screenshot] --max_proc max_parallel_processes'
        sys.exit(1)
    
    if args and args[0] == '--url_file':
        url_file = args[1]        
        del args[0:2]
    
    if args and args[0] == '--stop':
        stop = int(args[1])        
        del args[0:2]
    
    if args and args[0] == '--start':
        start = int(args[1])        
        del args[0:2]
    
    if args and args[0] == '--type':        
        crawler_type = args[1]
        del args[0:2]
    
    if args and args[0] == '--max_proc':
        max_parallel_procs = int(args[1])        
        del args[0:2]
    
    if args:
        print 'some arguments are not processed, check your command: %s' % (args)
        sys.exit(1)
    
    if not stop or not crawler_type:
        print 'Cannot get the arguments for stoplimit %s or crawler_type%s' % (stop, crawler_type)
        sys.exit(1)
        
    url_tuples = gen_url_list(stop, start, True, url_file)
    crawl_sites(url_tuples, crawler_type, 1+stop-start, max_parallel_procs)
