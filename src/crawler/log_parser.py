# -*- coding: utf-8 -*-
import common as cm
import fileutils as fu
import dbutils as dbu
from log import wl_log
from webutils import PublicSuffix
import os
import re
import operator
import parallelize
from functools import partial
import simplejson as json
import fp_regex as fpr
from sets import Set

MITM_LOG_EXTENSION = 'mlog' # !!! TODO  remove duplicate definition
pub_suffix = PublicSuffix()
FONT_LOAD_THRESHOLD = 30
EXT_LINK_IMG = '<img title="Open in a new tab" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAVklEQVR4Xn3PgQkAMQhDUXfqTu7kTtkpd5RA8AInfArtQ2iRXFWT2QedAfttj2FsPIOE1eCOlEuoWWjgzYaB/IkeGOrxXhqB+uA9Bfcm0lAZuh+YIeAD+cAqSz4kCMUAAAAASUVORK5CYII=" />'


class DomainInfo:    
    def __init__(self):        
        self.rank = 0
        self.log_filename = ""
        self.url = ""
        self.fonts_loaded = []
        self.fonts_by_origins = {}
        self.requests = []
        self.responses = []   
        self.num_font_loads = 0
        self.num_offsetWidth_calls = 0
        self.num_offsetHeight_calls = 0
        self.fp_detected = []
        self.crawl_id = 0
        self.fpd_logs = []
        self.fc_dbg_font_loads = []
        self.log_complete = 0
        
def mark_if_fp(url):
    """Wrap given string in red if it includes a fp-related substring.""" 
    for fp_regex, fper in fpr.FINGERPRINTER_REGEX.iteritems():
        if re.search(fp_regex, url):
            return '<span class="red" title="%s">%s</span>' % (fper, url)
    return url

def generate_results_page(domaInfo):    
    """Generate results page for the given domain information."""
    
    back_link = '<div><a href="index.html">Index</a></div>'
    rank_str = "<h2>%s - %s -  <a href='%s' target='_blank'>%s</a></h2>" % (str(domaInfo.rank), domaInfo.url, domaInfo.url, EXT_LINK_IMG)
    
    fonts_list = ' &bull; '.join('<span style="font-family:%s">%s</span>' %(font_name, font_name) for font_name in domaInfo.fonts_loaded) 
    
    font_div = "<div class='fonts'><p><b>%s</b> fonts loaded, <b>%s</b> num_offsetWidth_calls, <b>%s</b> num_offsetHeight_calls</p>\
        \n<div class='font_list'>%s</div></div>" % (len(domaInfo.fonts_loaded), domaInfo.num_offsetWidth_calls, domaInfo.num_offsetHeight_calls, fonts_list)
    
    unique_urls = set(domaInfo.responses + domaInfo.requests)
    unique_http_urls = [url for url in unique_urls if re.match(r"https?:\/\/[^.]+\.[^.]", url)] # filter out data urls
    
    unique_domains = set(pub_suffix.get_public_suffix(url) for url in unique_http_urls if url.startswith('http'))
    unique_domains = [mark_if_fp(address) for address in sorted(unique_domains)]
    domain_list = "<ul class='domains'>\n<li>%s</li></ul>" % ("</li>\n<li>".join(unique_domains))
    
    unique_urls = ["<a href='%s' target='_blank'>%s</a> - %s" %\
                    (address, EXT_LINK_IMG, mark_if_fp(address)) for address in sorted(unique_http_urls)]
    url_list = "<ul class='urls'>\n<li>%s</li></ul>" % ("</li>\n<li>".join(unique_urls))
    
    domains_div = "<div class='domains'><p> Number of different domains loaded: <b>"\
     + str(len(unique_domains)) + "</b></p><div class='domains_list'> " + domain_list + "</div></div>"
    
    urls_div = "<div class='urls'><p> Number of different URLs loaded: <b>"\
     + str(len(unique_urls)) + "</b></p>\n<div class='urls_list'> " + url_list + "</div></div>"
    
    font_orig_str = "<p>Fonts per origin</p><ul>"
    for orig, fonts in domaInfo.fonts_by_origins.iteritems():
        font_orig_str += "<li>%s: %s %s</li>" % (json_field_name_to_origin(orig), len(fonts), fonts)
    font_orig_str += "</ul>"
    
    html_str = "<html>\n<head>\n<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\
    \n<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\
    \n<style>span.red{color:red; font-weight:bold;}\
    \n</style>\n</head>\n<body>" + back_link + rank_str + font_div + font_orig_str + domains_div + urls_div + "\n</body>\n</html>"
    
    output_filename = domaInfo.log_filename[:-4] + ".html"
    
    fu.write_to_file(output_filename, html_str)
    

def generate_index_file(path):
    table_str = '<table><th>Rank</th><th>Domain</th><th># fonts requested</th>'
    fonts_dict = {}
    i = 0
    for json_file in fu.gen_find_files("*.json", path):
        i = i + 1
        wl_log.info("%s - %s" % (i, json_file))
        domaInfo = load_domainfo_from_json_file(json_file)
        if domaInfo.num_font_loads > FONT_LOAD_THRESHOLD or domaInfo.fp_detected:
            fonts_dict[domaInfo.log_filename] = domaInfo.num_font_loads
            
    sorted_font_dict = sorted(fonts_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    for filename, num_font_loaded in sorted_font_dict:
        #if num_font_loaded > FONT_LOAD_THRESHOLD:
        rank,domain = get_rank_domain_from_filename(filename)
        output_filename = os.path.basename(filename)[:-4] + ".html"
        table_str += '<tr><td>'+  rank + '</td><td><a href="' + output_filename + '">' + domain \
                + '</a></td><td>' + str(num_font_loaded) +  '</td></tr>' 
        
    table_str += '</table>'
    
    html_str = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\
            <meta http-equiv='Content-Type' content='text/html; charset=utf-8' /> </head><body>" + table_str + "</body></html>"
    index_filename = os.path.join(path, "index.html")
    fu.write_to_file(index_filename, html_str.encode('utf-8'))

def get_rank_domain_from_filename(filename):
    return os.path.basename(filename)[:-4].split('-', 1)

def dump_json_and_html(domaInfo):
    """Dump object to json file and generate html results"""
    dump_json(domaInfo)
    dump_html(domaInfo)

def insert_domain_info_to_db(domaInfo):
    db_conn = dbu.mysql_init_db()
    site_info_id = dbu.add_site_info_to_db(domaInfo, db_conn)
    dbu.add_js_info_to_db(domaInfo, db_conn, site_info_id)
    db_conn.commit()
    db_conn.close()

def insert_js_info_to_db(domaInfo, site_info_id, db_conn):
    dbu.add_js_info_to_db(domaInfo, db_conn, site_info_id)
    
def get_index_filename_for_domain_info(domaInfo):
    return  os.path.join(os.path.dirname(domaInfo.log_filename), "index.html")

def add_index_html_line(domaInfo):
    ind_file = get_index_filename_for_domain_info(domaInfo)
    html_filename = os.path.basename(domaInfo.log_filename)[:-4] + ".html"
    row_str = '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (domaInfo.rank, html_filename, domaInfo.url, domaInfo.num_font_loads, domaInfo.num_offsetWidth_calls,domaInfo.num_offsetHeight_calls, ",".join(domaInfo.fp_detected))
    fu.append_to_file(ind_file, row_str)

def dump_html(domaInfo):
    # wl_log.info("Generating HTML %s %s %s" % (domaInfo.url, domaInfo.num_font_loads, domaInfo.fonts_loaded))
    if domaInfo.num_font_loads > FONT_LOAD_THRESHOLD or domaInfo.fp_detected:
        generate_results_page(domaInfo)
        add_index_html_line(domaInfo)
    
def dump_json(domaInfo):
    """Dump object to json file."""
    json_filename = domaInfo.log_filename[:-4] + ".json"
    # wl_log.info("Dumping to %s %s %s %s" % (json_filename, domaInfo.url, domaInfo.num_font_loads, domaInfo.fonts_loaded))
    tmp_fonts_by_origins = {}
    for origin, fonts in domaInfo.fonts_by_origins.iteritems():
        json_key = origin_to_json_field_name(origin) # we need to replace dots in domain names
        tmp_fonts_by_origins[json_key] = list(fonts)
    
    domaInfo.fonts_by_origins = tmp_fonts_by_origins
    
    with open(json_filename, 'w') as outfile:
        json.dump(domaInfo.__dict__, outfile, encoding="utf-8")
    

def parse_crawl_logs(path, no_of_procs=16):
    files = fu.gen_find_files("*.txt", path)    
    log_worker = partial(parse_crawl_log, dump_fun=dump_json_and_html)
    parallelize.run_in_parallel(files, log_worker, no_of_procs)
    wl_log.info("Worker processes are finished, will generate index")

def process_crawl_logs(path, no_of_procs=16):
    """Parse crawl logs in a directory."""
    parse_crawl_logs(path, no_of_procs)
    generate_index_file(path)

def origin_to_json_field_name(origin):
    return origin.replace('.','DOT')
    
def json_field_name_to_origin(origin):
    return origin.replace('DOT', '.')
         
def parse_crawl_log(filename, dump_fun=None, crawl_id=0, url=""):
    """Populate domain info object by parsing crawl log file of a site.
    Call dump function to output dump log.
    
    Logs to be parsed with this function are generated by setting env. variable FC_DEBUG=1 to 1 or logs from the browser. 
    See, fontconfig library for details.  
    
    """
    origins_to_fonts = {} # will keep origin to loaded fonts mapping
    
    domaInfo = DomainInfo()
    
    file_content = fu.read_file(filename)
    wl_log.info('Parsing log for %s %s' % (url, filename))
    
    # Read canvas events and print them to log in canvas
    urls_read_from_canvas = Set()
    urls_wrote_to_canvas = Set()
    
    
    canvas_log = os.path.join(cm.BASE_FP_LOGS_FOLDER, str(crawl_id) + "canvas.log")
    read = wrote = False
    for read_event in cm.CANVAS_READ_EVENTS:
        if read_event in file_content:
            read = True
            break
    for write_event in cm.CANVAS_WRITE_EVENTS:
        if write_event in file_content:
            wrote = True
            break

    if read and wrote:
        wl_log.info('Found both canvas read and write events in log %s, registering in : %s' % (filename, canvas_log))
        with open(canvas_log, "a+") as f:
            f.write(" ".join([domaInfo.rank, domaInfo.url, event_url]))
    
#     for line in file_content.splitlines():        
#         if not line.startswith("FPLOG"):
#             continue
#         event_url = line.split()[-1]
#         for read_event in cm.CANVAS_READ_EVENTS:
#             if read_event in line:
#                 urls_read_from_canvas.add(event_url)
#         for write_event in cm.CANVAS_WRITE_EVENTS:
#             if write_event in line:
#                 urls_wrote_to_canvas.add(event_url)
#     
#     with open(canvas_log, "a") as f:
#         f.write("rank" + ";" + "visit_url" + ";" + "rw_event_url")
#         for event_url in list(urls_read_from_canvas & urls_wrote_to_canvas):
#             f.write(domaInfo.rank + ";" + domaInfo.url + ";" + event_url)

    fonts_by_fc_debug = re.findall(r"Sort Pattern.*$\W+family: \"([^\"]*)", file_content, re.MULTILINE) # match family field of font request (not the matched one) 
    domaInfo.num_offsetWidth_calls = len(re.findall(r"Element::offsetWidth", file_content)) # offset width attempts
    domaInfo.num_offsetHeight_calls = len(re.findall(r"Element::offsetHeight", file_content)) # offset height attempts
    # TODO add getBoundingClientRect
     
    font_and_urls = re.findall(r"CSSFontSelector::getFontData:? (.*) ([^\s]*)", file_content) # output from modified browser
    #print 'font_and_urls', font_and_urls  
    
    font_face_pairs = re.findall(r"CSSFontFace::getFontData (.*)->(.*)", file_content) # output from modified browser
    #print 'font_and_urls', font_and_urls
    domaInfo.log_complete = int(bool(re.findall(r"Finished all steps!", file_content))) # output from modified browser
    #print 'domaInfo.log_complete', domaInfo.log_complete
    js_log_prefix = ">>>FPLOG"
    fpd_logs = re.findall(r'%s.*' % js_log_prefix, file_content) # output from modified browser
    domaInfo.fpd_logs = [call[len(js_log_prefix)+1:] for call in set(fpd_logs)]
    
    for font_name, font_url in font_and_urls:
        if font_url.startswith('http') and len(font_name) > 1  and not font_name[:5] in ('data:', 'http:', 'https'):
            #font_name = font_name.rsplit(' ', 1)[0] if font_name.endswith(' onURL:') else font_name # TODO: unify chrome source code to log as Phantom do. then remove this line 
            font_name = font_name.lower().strip()
#             origin = pub_suffix.get_public_suffix(font_url)\
            origin = font_url
            if origin in origins_to_fonts:
                origins_to_fonts[origin].add(font_name)
                #print 'added', font_name, 'to', origin, origins_to_fonts[origin]  
            else: 
                origins_to_fonts[origin] = set([font_name,])
        
    for font, face in font_face_pairs:
        font = font.lower().strip()
        face = face.lower().strip()
        # replace all occurrences of this font-family name with the face
        for fonts_by_origin in origins_to_fonts.itervalues():
            try:
                fonts_by_origin.remove(font)
            except: # we cannot find this font in this origin's list
                pass
            else:
                fonts_by_origin.add(face)
                # print 'removed', font, 'added', face
    
    for origin, fonts in origins_to_fonts.iteritems():
        domaInfo.fonts_by_origins[origin] = list(fonts)
        domaInfo.fonts_loaded += domaInfo.fonts_by_origins[origin]
    

    domaInfo.fc_dbg_font_loads = list(set([font.lower() for font in fonts_by_fc_debug \
                    if not font[:5] in ('data:', 'http:', 'https')])) # filter out the data urls and web fonts

         
    domaInfo.fonts_loaded = list(set([font.lower() for font in domaInfo.fonts_loaded \
                    if not font[:5] in ('data:', 'http:', 'https')])) # filter out the data urls and web fonts
    
    requests = re.findall(r"^requested: (http.*)", file_content, re.MULTILINE)
    if not requests and filename.endswith(MITM_LOG_EXTENSION):
        requests = re.findall(r"(http.*)", file_content, re.MULTILINE)
    responses = ''
    # populate domain info obj 
    
    domaInfo.num_font_loads = len(domaInfo.fonts_loaded)
    domaInfo.requests = list(set(requests))
    domaInfo.responses = list(set(responses))
    domaInfo.fp_detected = get_fp_from_reqs(requests)
    domaInfo.url = url
    domaInfo.rank = get_rank_domain_from_filename(filename)[0]  # !!! rank may not be right. It's only true if we make top Alexa crawl.
    domaInfo.log_filename = filename
    domaInfo.crawl_id = crawl_id
    
    if dump_fun: # call dump function
        try:
            dump_fun(domaInfo)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            wl_log.exception("Exception while dumping %s: %s" % (domaInfo.url, exc))

                  
def get_fp_from_reqs(requests):
    """Return FP provider list given a set of requests.""" 
    fp_list = [] # list of fp providers detected
    for fp_regex, fper in fpr.FINGERPRINTER_REGEX.iteritems():
        for req in requests: # for each requests
            if re.search(fp_regex, req):
                fp_list.append(fper) 
    
    return uniq_list(fp_list)

def uniq_list(mylist):
    return list(set(mylist))
    
def parse_log_dump_html(filename):
    parse_crawl_log(filename, dump_html)    

def parse_log_dump_json(filename):
    parse_crawl_log(filename, dump_json)    

def parse_log_dump_json_and_html(filename):
    parse_crawl_log(filename, dump_json_and_html)

def parse_log_dump_results(filename, method='db', crawl_id=0, url=""):
    if method is 'db':
        parse_crawl_log(filename, insert_domain_info_to_db, crawl_id, url=url)
    elif method is 'json':
        parse_crawl_log(filename, dump_json_and_html,url=url)
    else:
        parse_crawl_log(filename, dump_html,url=url)

def load_domainfo_from_json_file(json_file):
    """Load JSON file to a domain info."""
    domain_info_obj = DomainInfo()
    domains_to_fonts = {}
    with open(json_file, 'r') as json_src:
        # object_hook=lambda d: namedtuple('X', d.keys())(*d.values())
        doma_info_dict = json.load(json_src)
        for json_friendly_origin in doma_info_dict['fonts_by_origins'].iterkeys():
            origin = json_field_name_to_origin(json_friendly_origin)
            domains_to_fonts[origin] = doma_info_dict['fonts_by_origins'][json_friendly_origin]
    
        # Make an object from the dict
        for key in doma_info_dict.keys():
            if key is not 'fonts_by_origins':
                setattr(domain_info_obj, key, doma_info_dict[key])
            else:
                setattr(domain_info_obj, key, domains_to_fonts)
            
        return domain_info_obj

def get_json_filename_from_log_filename(log_filename):
    """Return corresponding JSON filename for a given log file."""
    return log_filename[:-4] + ".json"    

def load_domainfo_for_log_file(log_filename):
    # parse_crawl_log(log_filename)
    json_file = get_json_filename_from_log_filename(log_filename)
    return load_domainfo_from_json_file(json_file)


def close_index_html(index_file):
    # wl_log.info('Will close %s' % index_file)
    # TODO: add check to don't close a file twice 
    if not os.path.isfile(index_file):
        fu.write_to_file(index_file, '') # create an empty file
        
    index_src = fu.read_file(index_file) 
    if index_src.startswith('<html'):
        wl_log.info('Index file %s  already closed' % index_file)
        return
    
    scripts_src = """<script type="text/javascript" language="javascript" src="http://homes.esat.kuleuven.be/~gacar/jscss/jquery-1.9.1.min.js"></script>
    
    <style type="text/css" title="currentStyle">
        @import "../../js/css/demo_page.css";
        @import "../../js/css/demo_table.css";
    </style>
    <script type="text/javascript" language="javascript" src="http://homes.esat.kuleuven.be/~gacar/jscss/jquery.dataTables.min.js"></script>
    <script type="text/javascript" charset="utf-8">
        $(document).ready(function() {
            $('#results').dataTable( {
            "aaSorting": [[ 2, "desc" ]]
            } );
        } );
    </script>"""
        
        
    html_str = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\
            <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />" + scripts_src + "</head>\n<body><table id ='results'>\
            \n<thead><tr><th>Rank</th><th>Domain</th><th>Fonts</th><th>OffsetWidth</th><th>OffsetHeight</th><th>FP found</th></tr></thead>" +  index_src + '</table></body></html>' 
    
    fu.write_to_file(index_file, html_str)



