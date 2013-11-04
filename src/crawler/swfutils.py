
import os, re
import pickle
import json
import itertools
import commands as cmds
import fileutils as fu
import utils as ut
import dbutils as dbu
from log import wl_log

AS_SOURCE_FILE_PATTERN = '*.[af][sl]*'
FP_ACTIONSCRIPT_STR_LIST = ['enumerateFonts\(true', 'getFontList', '[cC]apabilities', '[cC]apabilities\.os', 'screenDPI', 
              'screenResolutionX', 'screenResolutionY', '[cC]apabilities\.language', 
              '[cC]apabilities\.version', 'manufacturer', 'serverString', 'getTimezoneOffset', 
              'getLocal', 'XMLSocket', 'Math\.min', 'Math\.max', '[mM][dD]5', '[sS][hH][aA][123][258][864]', 
              'ExternalInterface\.call', 'ExternalInterface\.addCallback', 'sendAndLoad', 'URLLoader', 'navigateToURL', 'loadMovie',
              'createUID', 'getUrl', 'javascript', 'crypt', 'allowDomain', 'allowInsecureDomain', 'loadPolicyFile', 'URLRequest', 'LoadVars']

BASE_FP_DETECTIVE_FOLDER = os.path.expanduser('~/fpbase')
FFDEC_PATH = os.path.join(BASE_FP_DETECTIVE_FOLDER, 'run', 'ffdec', 'ffdec.jar')

class SwfInfo():
    def __init__(self):
        self.id = None
        self.rank = 0
        self.local_path = ''
        self.domain = ''
        self.page_url = ''
        self.duplicate = 0
        self.referer = ''
        self.url = ''
        self.occ_vector = ''
        self.feat_vector = ''
        self.filename = ''
        self.hash = ''
        self.occ_string = ''
        self.crawl_id = 0
        self.site_info_id = 0
        
        
    def reset(self):
        self.__init__()

class SwfSrcInfo():
    def __init__(self):
        self.id = None
        self.swf_id = None
        self.local_path = ''
        self.source = ''
        self.occ_vector = ''
        self.feat_vector = ''
        self.hash = ''
        
    def reset(self):
        self.__init__() 
    
def is_swf_file(swf_path):
    """Return True if this is a swf files. Just wraps get_swf_version for better readability."""
    return bool(get_swf_version(swf_path))

def get_swf_version(filename):
    """Return version number if Flash file, otherwise return 0. Uses linux file command"""
    if os.path.exists(filename):
        cmd = 'file "%s"' % filename #use linux file command
        status, cmd_out = cmds.getstatusoutput(cmd)
        if not status: # command executed successfully
            if 'Macromedia Flash' in cmd_out: # flash files should have that 
                return int(cmd_out.split()[-1]) # number following last space is the version number
            
    return 0


def gen_find_swf_files(top_dir):
    """Find Flash files under a given directory."""
    for filename in fu.gen_find_files('*', top_dir): # don't rely on file extension
        if is_swf_file(filename): # test with Linux file command   
            yield filename

def human_readable_occ_vector(vector):
    """Return list of ActionScript function and property names for a given occurrence vector."""
    return list(itertools.compress(FP_ACTIONSCRIPT_STR_LIST, vector))


def get_occurence_vector_from_swf(swf_filename, out_dir=''):
    cum_pattern = [0]*len(FP_ACTIONSCRIPT_STR_LIST)
    for src_file in gen_decompile_swf(swf_filename, out_dir):
        vector = fu.file_occurence_vector(src_file, FP_ACTIONSCRIPT_STR_LIST)
        cum_pattern = [x+y for (x, y) in zip(cum_pattern, vector)]
    
    wl_log.info("Cum Vector for %s %s" % (swf_filename[len(out_dir):], human_readable_occ_vector(cum_pattern)))
    return cum_pattern

def gen_decompile_swfs_in_dir(top_dir):
    """Decompile flash files under given dir, return an iterator for each source & swf pairs."""
    for swf_path in gen_find_swf_files(top_dir): # iterate over swf files
        for src_path in gen_decompile_swf(swf_path):
            yield src_path, swf_path
            
def is_decompiled(swf_path):
    """Check if there is a src folder with some files in it.
    
    Note that this function is specific to our naming/directory schema.
     
    """
    swf_dir = os.path.dirname(swf_path)
    src = os.path.join(swf_dir, 'src')
    if os.path.isdir(src) and os.listdir(src) != []:
        return True
    else:
        return False

def get_domain_from_path(path):
    """Return domain from a path. Matches leftmost stem that matches a domain name

    Note that this may return nonsense if an upper directory have a name similar to a domain name.
    """
    for stem in path.split('/')[:-1]:
        if re.match(r'\S+\.[a-z]{2,3}', stem):
            return stem
    
    return 'UnknownDomain'

def unpickle(pickled_file):
    return pickle.load( open(pickled_file, "rb"))

def get_swf_info(swf_path):
    """Populate a swf_info dict for given file."""
    
    UNPICKLE = False # problems with class defn TODO
    
    swf_info = SwfInfo()
    swf_info.domain = get_domain_from_path(swf_path)
    swf_info.local_path = swf_path
    swf_info.filename = os.path.basename(swf_info.local_path) 
    
    if UNPICKLE:
        pickled_file_path = swf_path +'.txt' # this was our convention - add a txt to swf path
        if os.path.exists(pickled_file_path) and UNPICKLE:
            swf_info = unpickle(pickled_file_path)
    
    return swf_info 

def get_feat_vector(occ_vector):
    """TODO: map occurrences of AS scripts to some semantics to ease analysis.
    
    e.g. both getfontlist() (ActionScript2) and enumerateFonts(True) (AS3) 
    do the same thing (get system fonts)    
    
    """
    return occ_vector # to implement

def get_swf_obj_from_db(by, query_param, db_cursor):
    if by is 'id':
        db_cursor.execute('SELECT * FROM swf_obj WHERE id = %s', (query_param,))
    elif by is 'rank':
        db_cursor.execute('SELECT * FROM swf_obj WHERE rank = %s', (query_param,))
    elif by is 'crawl_id':
        db_cursor.execute('SELECT * FROM swf_obj WHERE crawl_id = %s', (query_param,))
    elif by is 'hash':
        db_cursor.execute('SELECT * FROM swf_obj WHERE hash = %s', (query_param,))
    return db_cursor.fetchall()


   
def add_swf_to_db(swf_info, db_conn):
    """Add swf_info into db."""
    #domain = get_domain_name_from_path(swf_file)
    return dbu.insert_to_db(db_conn, "INSERT INTO swf_obj (id, rank, local_path, domain, page_url, \
        duplicate, swf_url, occ_vector, feat_vector, hash, referer, occ_string, crawl_id, site_info_id) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        (None, swf_info.rank, swf_info.local_path, swf_info.domain, swf_info.page_url, 
         swf_info.duplicate, swf_info.url, vector_to_str(swf_info.occ_vector), vector_to_str(swf_info.feat_vector), swf_info.hash, swf_info.referer, swf_info.occ_string, swf_info.crawl_id, swf_info.site_info_id)) # None is for autoincrement

#!!! TODO Refactor functions below this line 
def gen_decompile_swf(swf_path, out_dir=''):
    """Decompile a Flash file with the available decompilers."""
    if not os.path.isfile(swf_path):
        return
    
    if not out_dir:
        base_dir = os.path.dirname(swf_path)
        out_dir = ut.rand_str() + '-src'
        out_dir = os.path.join(base_dir, out_dir)
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    cmd_ffdec = 'java -jar ' + FFDEC_PATH + ' -export as "' + out_dir + '" "' + swf_path + '"'  
    timeout_prefx = 'timeout -k 5 30 ' # linux specific
    
    ffdec_status, ffdec_output = cmds.getstatusoutput(timeout_prefx + cmd_ffdec)
    write_decomp_log(swf_path, ffdec_status, ffdec_output, '', '')
        
    for flash_src_file in fu.gen_find_files(AS_SOURCE_FILE_PATTERN, out_dir):
        yield flash_src_file

def write_decomp_log(swf_path, ffdec_status, ffdec_output, flare_status, flare_output):
    TIME_OUT_EXIT_CODE = -1 # return code for linux timeout command
    
    log_str = 'Decompile: %s || ' % os.path.basename(swf_path)
    log_str += 'ffdec: %d' % ffdec_status
    if ffdec_status:
        log_str += ' timeout' if ffdec_status == TIME_OUT_EXIT_CODE else ' error'
    else:
        log_str += ' OK'
        
    wl_log.info(log_str)


def update_swf_vector(swf_id, vector, db_cursor):
    db_cursor.execute('UPDATE swf_obj SET occ_vector=? WHERE id=?', (vector, swf_id))  # update vector for this source file 

def vector_to_str(vector):
    return json.dumps(vector)

def str_to_vector(db_str):
    return tuple(json.loads(db_str))
