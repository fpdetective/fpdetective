
import os
import logging
import common as cm
from time import strftime
from fileutils import add_symlink


LOG_PREFIX = 'fpd'

def init_log_handler(handler, logger, level, frmt):
    """ Initialize log handler."""
    handler.setLevel(level)
    handler.setFormatter(frmt)
    logger.addHandler(handler)

def get_logger(logname, logtype='fc', level=logging.DEBUG, frmt=None, filename=''):
    """Create and return a logger with the given name.
    
    logtype f: file, c: console, fc: both
    
    """
    logger = logging.getLogger(logname)
    logger.setLevel(level)
    frmt = frmt or logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    if 'f' in logtype: # if 
        base_name = filename if filename else '%s-%s.log' % (logname, strftime("%Y%m%d-%H%M%S")) 
        log_filename  = os.path.join(cm.BASE_FP_LOGS_FOLDER, base_name)
        fh = logging.FileHandler(log_filename)
        init_log_handler(fh, logger, logging.DEBUG, frmt)
        linkname = os.path.join(cm.BASE_FP_LOGS_FOLDER, 'latest')
        add_symlink(linkname, log_filename)
        
    if 'c' in logtype:
        ch = logging.StreamHandler()
        init_log_handler(ch, logger, logging.INFO, frmt)
    
    return logger

wl_log = get_logger(LOG_PREFIX, logtype='fc')

