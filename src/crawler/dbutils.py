
import sqlite3
import MySQLdb as mdb
from time import time
from common import FPDDBException
from contextlib import closing
from log import wl_log

DB_IP_ADDRESS = 'localhost'

def mysql_init_db(db_name='fp_detective'):
    db_conn = None
    try:
        db_conn = mdb.connect(DB_IP_ADDRESS, 'root',  '1q2w3e4r', db_name); #!!! mustreplace
    except mdb.Error, e:  
        print "Error %d: %s" % (e.args[0],e.args[1])

    return db_conn

def insert_to_db(db_conn, query, args):
    with closing( db_conn.cursor(mdb.cursors.DictCursor) ) as db_cursor:
    #db_cursor = db_conn.cursor(mdb.cursors.DictCursor)
        try:
            db_cursor.execute(query, args)
        except Exception as ex:
            wl_log.critical('Exception executing query: %s %s' % (query, args))
            raise ex
        db_conn.commit()
        return db_cursor.lastrowid

    
def update_crawl_time(db_conn, crawl_id):
     
    with closing( db_conn.cursor(mdb.cursors.DictCursor) ) as db_cursor:
        try:
            db_cursor.execute("UPDATE crawl_job SET finish_time= %s WHERE crawl_id = %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), crawl_id))
        except Exception as ex:
            wl_log.critical('Exception executing UPDATE query: %s %s')
            raise ex
        db_conn.commit()
        return db_cursor.lastrowid
    
def get_entry_from_db(db_conn, table, by='id', value=None):
    with closing( db_conn.cursor(mdb.cursors.DictCursor) ) as db_cursor:
    #db_cursor = db_conn.cursor(mdb.cursors.DictCursor)
        db_cursor.execute('SELECT * FROM %s WHERE %s = %s' % (table, by, value))
        return db_cursor.fetchall()  

def get_site_info_from_db(db_conn, by='id', value=None):
    return get_entry_from_db(db_conn, 'site_info', by, value)  

def get_js_info_from_db(db_conn, by='id', value=None):
    return get_entry_from_db(db_conn, 'js_info', by, value)  

def get_crawl_job_from_db(db_conn, by='id', value=None):
    return get_entry_from_db(db_conn, 'crawl_job', by, value)  


def add_site_info_to_db(doma_info, db_conn):
    return insert_to_db(db_conn, "INSERT INTO site_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                  (None, ' '.join(doma_info.requests),   ' '.join(doma_info.responses), doma_info.crawl_id, doma_info.url, " ".join(doma_info.fp_detected), ','.join(doma_info.fc_dbg_font_loads), len(doma_info.fc_dbg_font_loads), doma_info.rank, None, doma_info.log_complete))
    

def add_js_info_to_db(doma_info, db_conn, site_info_id):
    return insert_to_db(db_conn, "INSERT INTO js_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                  (None, doma_info.rank, doma_info.url, ','.join(doma_info.fonts_loaded), str(doma_info.fonts_by_origins),
                    doma_info.num_font_loads, doma_info.num_offsetWidth_calls, doma_info.num_offsetHeight_calls,
                    '', int(site_info_id), ','.join(doma_info.fpd_logs), doma_info.crawl_id)) # skip inserting log
     
def update_crawl_job(cr_job, db_conn):
    return insert_to_db(db_conn, "UPDATE crawl_job SET num_crawl_urls=%s, max_parallel_procs=%s,\
       browser_mitm_proxy=%s, fc_fontdebug=%s, cmd=%s WHERE crawl_job.id = %s", 
      (cr_job.num_crawl_urls, cr_job.max_parallel_procs, cr_job.crawl_agent.use_mitm_proxy, cr_job.crawl_agent.fc_fontdebug, cr_job.crawl_agent.cmd_line_options, cr_job.crawl_id))

def add_crawl_job_to_db(crawl_job, db_conn):
    return insert_to_db(db_conn, "INSERT INTO crawl_job VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                  (None, crawl_job.num_crawl_urls, '', crawl_job.crawl_agent.type, crawl_job.crawl_agent.user_agent_str, \
                   crawl_job.max_parallel_procs, crawl_job.job_dir, crawl_job.index_html_log, crawl_job.crawl_agent.binary_path, crawl_job.crawl_agent.use_mitm_proxy, 
                   crawl_job.crawl_agent.fc_fontdebug, crawl_job.crawl_agent.cmd_line_options, crawl_job.desc, None, None))


def sqlite_init_db(db_file, schema_file=None):
    """Init a sqlite db with a schema file."""
    try:
        dbConnection = sqlite3.connect(db_file, isolation_level=None) # isolation_level=None for auto commits 
        dbConnection.row_factory = sqlite3.Row
        dbConnection.text_factory = lambda x: unicode(x, "utf-8", "replace") #solves unicode encoding problems
        if schema_file:
            with open(schema_file) as f:
                dbConnection.cursor().executescript(f.read())
            dbConnection.commit()
        
        return dbConnection        
    except:        
        raise FPDDBException("Can't initialize database: %s with schema file: %s" % (db_file, schema_file)) # TODO are there cases where we don't want to die
