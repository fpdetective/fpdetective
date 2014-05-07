
import os
import platform

expanduser = os.path.expanduser 
join = os.path.join

if 'x86_64' in platform.processor():
    arch = '64'
else:
    arch = '32'
    
JOBS_FOLDER = 'jobs' # each crawl job will have a folder under jobs
LOGS_FOLDER = 'logs' # logs are stored here TODO: should we store logs in job folders?

BASE_FP_DETECTIVE_FOLDER = expanduser('~/fpbase')
BASE_FP_RUN_FOLDER = join(BASE_FP_DETECTIVE_FOLDER, 'run')
BASE_FP_BIN_FOLDER = join(BASE_FP_RUN_FOLDER, 'bins')
BASE_FP_JOBS_FOLDER = join(BASE_FP_RUN_FOLDER, JOBS_FOLDER)
BASE_FP_LOGS_FOLDER = join(BASE_FP_RUN_FOLDER, LOGS_FOLDER)
BASE_FP_SRC_FOLDER = join(BASE_FP_DETECTIVE_FOLDER, 'src/crawler')
BASE_PHANTOM_FOLDER = join(BASE_FP_BIN_FOLDER, 'phantomjs')

PHANTOM_BINARY = join(BASE_PHANTOM_FOLDER, "phantomjs%s" % arch) # path to phantomjs binary (don't use down-rev platform package)
PHANTOM_MOD_BINARY = join(BASE_PHANTOM_FOLDER, "phantomjs%smod" % arch) # path to modified phantomjs binary
CHROME_BINARY =  "chromium-browser" # use platform package
CHROME_MOD_BINARY =  join(BASE_FP_BIN_FOLDER, "chromium%s/chrome" % arch) # path to our modified chrome binary
CHROME_DRIVER_BINARY = join(BASE_FP_BIN_FOLDER, 'chromedriver/chromedriver%s' % arch)
CASPER_BINARY = join(BASE_FP_BIN_FOLDER, "casperjs/bin/casperjs") # path to casperjs binary

JS_BASE_PATH = join(BASE_FP_SRC_FOLDER, 'js') # !!! we expect symlink fpbase be present at the home folder. 

CASPER_JS_CLICKER = join(JS_BASE_PATH, 'casper_clicker.js')
CASPER_JS_LAZY_HOMEPAGER = join(JS_BASE_PATH, 'casper_lazy_homepager.js')
CASPER_JS_DNT_LAZY = join(JS_BASE_PATH, 'phantom_lazy_DNT.js')

CRAWLER_PY_PATH = join(BASE_FP_SRC_FOLDER, 'crawler.py')
BASE_TEST_URL_ONLINE = 'http://homes.esat.kuleuven.be/~gacar/phtest/' 
BASE_TEST_URL = 'file://' + BASE_FP_SRC_FOLDER + '/test/files/' 


EVENT_FILLTEXT      = "CanvasRenderingContext2D\tfillText"
EVENT_STROKETEXT    = "CanvasRenderingContext2D\tstrokeText"
EVENT_TODATAURL     = "HTMLCanvasElement\ttoDataURL"

CANVAS_READ_EVENTS = (EVENT_TODATAURL)
CANVAS_WRITE_EVENTS = (EVENT_FILLTEXT, EVENT_STROKETEXT)


class FPDException(Exception):
    def __init__(self, msg=None, trace=None):
        self.msg = msg
        self.trace = trace

    def __str__(self):
        exception_msg = "Exception: %s " % repr(self.msg)
        if self.trace is not None:
            exception_msg = "%s; Stacktrace: %s " \
                % (exception_msg, str(self.trace))
        return exception_msg

class FPDDBException(FPDException):
    pass

class TimeExceededError(Exception):
    pass