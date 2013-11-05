import os
import functools
import subprocess
import socket
import fileutils as fu
import utils as ut
import swfutils as swu
import dbutils as dbu
import log_parser as lp
from time import sleep
from log import wl_log
from libmproxy import flow

MITM_LOG_EXTENSION = 'mlog'
MAX_FILENAME_LEN = 256

MITM_MAX_TRIES = 2       
MAX_PORT_NO = 65535
MIN_PORT_NO = 1024
PORT_TRY_TIMEOUT = 2
REMOVE_DMP_FILES = True # remove mitm dump files or not...

def get_free_port():
    """Get a free port number for mitmdump.
    
    http://stackoverflow.com/questions/1365265/on-localhost-how-to-pick-a-free-port-number?#answer-1365284
    
    """
    max_tries = 0
    while max_tries < MITM_MAX_TRIES:
        max_tries += 1
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            port = s.getsockname()[1]
        except Exception as ex:
            wl_log.critical('Exception when trying to bind to socket %s ' % ex)
            sleep(1)
        else:
            return port
    return None

def run_mitmdump(basename, timeout, logging=False):
    """Run mitmdump as a subprocess in the background with a timeout."""
    port = get_free_port()
    if not port: # we cannot get a free port
        return None, None
    
    dump_file = "%s.dmp" % basename
    cmd_re_dir = '' # for redirecting stderr to stdout and teeing
    quite_option = '-q' # mitmdump option to be quiet - no log
    
    if logging:
        mitm_log_file = "%s.%s" % (basename, MITM_LOG_EXTENSION)
        cmd_re_dir = ' 2>&1 |tee %s' % mitm_log_file # redirect all output to log file
        quite_option = '' # we don't want be quite!
        
    cmd = 'timeout %s mitmdump %s -z --anticache -p %s -w %s %s' % (timeout, quite_option, port, dump_file, cmd_re_dir)
    # -z: Try to convince servers to send us uncompressed data. mitmdump -h | grep "\-z" for info
    
    wl_log.info('mitmdump cmd %s' % cmd)
    subp = subprocess.Popen(cmd, shell=True) # shell=True - must be careful
    return port, subp.pid

def init_mitmproxy(basename, timeout, logging):
    try:
        port, pid = run_mitmdump(basename, timeout+1, logging) # runs a mitmdump process with the timeout+1 sec
    except:
        wl_log.critical('Exception initializing mitmdump')
    else:
        wl_log.info('mitmdump will listen on port %s, pid %s' % (port, pid))

    return "127.0.0.1:%s " % port if port and pid else ""

def process_dump(log_filename, crawl_id):
    basename = log_filename[:-4]
    dirname = os.path.dirname(log_filename)
    store_swfs_todir = functools.partial(store_swfs, dir_path=dirname, prefix=basename)
    parse_mitm_dump(basename, store_swfs_todir, crawl_id)
    
def parse_mitm_dump(basename, worker, crawl_id):
    dumpfile = basename +'.dmp'
    wl_log.info("Will parse mitm dump %s for crawl: %s" % (dumpfile, crawl_id))
    requests = []
    responses = []
    if os.path.isfile(dumpfile):
        fr = flow.FlowReader(open(dumpfile))
        try: 
            for msg in fr.stream():
                requests.append(msg.request.get_url())
                # responses.append(msg.response.get_url())
                worker(msg, crawl_id) # this worker func should take care of db insertion, logging etc.
        except flow.FlowReadError as exc:
            pass
            #wl_log.critical("Error reading mitm dump %s" % exc)
    else:
        wl_log.critical("Cannot find mitm dump %s" % dumpfile)
    
    doma_info = lp.DomainInfo()
    doma_info.requests = requests
    doma_info.responses = responses
    doma_info.crawl_id = crawl_id
    doma_info.url = ""
    doma_info.fc_dbg_font_loads = []
    doma_info.fp_detected = lp.get_fp_from_reqs(requests)
    doma_info.log_complete = 1
    print os.path.basename(dumpfile[:-4]).split('-')[0]
    doma_info.rank = int(os.path.basename(dumpfile).split('-')[0]) if '-' in dumpfile else 0
    db_conn = dbu.mysql_init_db()
    site_info_id = dbu.add_site_info_to_db(doma_info, db_conn)
    
    # parse 
    log_file = basename + '.txt'
    if not os.path.isfile(log_file):
        log_file = basename + '.' + MITM_LOG_EXTENSION
        
    insert_js_fun = functools.partial(lp.insert_js_info_to_db, site_info_id=site_info_id, db_conn=db_conn)
    lp.parse_crawl_log(log_file, insert_js_fun, crawl_id) # parse log, insert js info to db

    db_conn.commit()
    db_conn.close()
    wl_log.info("Parsed %s OK" % (dumpfile))
    if REMOVE_DMP_FILES:
        os.remove(dumpfile)
    
# http://wwwimages.adobe.com/www.adobe.com/content/dam/Adobe/en/devnet/swf/pdf/swf-file-format-spec.pdf
# http://src.chromium.org/viewvc/chrome/trunk/src/net/base/mime_sniffer.cc - FLV is no interest to us
SWF_MAGIC_NUMBERS = ('FWS', 'CWS', 'ZWS') # http://en.wikipedia.org/wiki/SWF#cite_note-swfspec-1

def store_swfs(msg, crawl_id, dir_path='/tmp', prefix='?'):
    
    referer = msg.request.headers['Referer'][0] if msg.request.headers['Referer'] else ""
    
    if msg.response and msg.response.content:
        print msg.request.get_url()
        if (msg.response.content[:3] in SWF_MAGIC_NUMBERS): # to wide, but decompiler will discard them
            
            swf_hash = ut.hash_text(msg.response.content)
            swf_url = msg.request.get_url()
            
            db_conn = dbu.mysql_init_db()
            db_cursor = db_conn.cursor(dbu.mdb.cursors.DictCursor)
            rows = swu.get_swf_obj_from_db('hash', swf_hash, db_cursor)
            
            if not rows:
                swf_filename = os.path.join(dir_path, "%s-%s" % (prefix, msg.request.path.split('/')[-1]))
                swf_filename = swf_filename[:MAX_FILENAME_LEN]
                if not swf_filename.endswith('.swf'):
                    swf_filename += '.swf'
                    
                wl_log.info("SWF saved %s referrer: %s" % (os.path.basename(swf_filename), referer))
                
                fu.write_to_file(swf_filename, msg.response.content)
                vector = swu.get_occurence_vector_from_swf(swf_filename, os.path.join(dir_path, prefix))
                duplicate_swf = 0
            else:
                wl_log.info("A swf with same hash exists in DB: %s %s" % (swf_hash, swf_url))
                vector = swu.str_to_vector(rows[0]['occ_vector'])
                swf_filename = rows[0]['local_path']
                duplicate_swf = 1
            
            rank, domain = prefix.rsplit('/')[-1].split('-', 1)
            swf_info = swu.SwfInfo()
            
            swf_info.rank = rank # this might be fake
            swf_info.domain = domain
            swf_info.local_path = swf_filename
            swf_info.occ_vector = vector
            swf_info.hash = swf_hash
            swf_info.url = swf_url
            swf_info.referer = referer        
            swf_info.duplicate = duplicate_swf # !!! Y for repeated swfs(that we know before) 
            swf_info.feat_vector = []
            swf_info.page_url = ''
            swf_info.occ_string = ' '.join(swu.human_readable_occ_vector(vector))
            swf_info.crawl_id = crawl_id
            
            swu.add_swf_to_db(swf_info, db_conn)
            db_conn.commit()
            db_cursor.close()
            db_conn.close()
            
            
        elif '.swf' in msg.request.path:
            wl_log.warning(".swf in path but content seems non-swf %s %s" % (msg.request.path, msg.response.content[:100]))
        else:
            pass
            #wl_log.info("Won't store content %s" % (msg.request.path))
