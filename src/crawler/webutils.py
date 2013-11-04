
import publicsuffix
import os.path as ospath
from urlparse import urlparse
from urllib2 import urlopen
from log import wl_log

ALEXA_TOP1M_PATH = ospath.join(ospath.expanduser('~/fpbase'), 'run', 'top-1m.csv') # !!! we expect this file to be there...

def swf_name_from_url(swf_url):
    """Return swf filename from given URL.
    TODO: see the commented test in webutils_test.py file.
    
    """
    parsed = urlparse(swf_url)
    return parsed.path.split('/')[-1]
 
def read_url(uri):
    """Fetch and return a URI content."""
    w = urlopen(uri)
    return w.read()

def strip_url_scheme(url):
    """Remove scheme (http://, data:) field from given URL."""
    scheme = urlparse(url)[0] # [0] is scheme part
    if scheme:
        return url[len(scheme):].lstrip(':/') # strip preceding ://
    else:
        return url
    
def gen_url_list(stop, start=1, get_rank=False, filename = "", sep=','):
    """Yield URLs for a given rank range from a given file (or default Alexa list).
    
    start and stop is inclusive and 1-based indexes (to match the ranks).
    """
    if not filename:
        filename = ALEXA_TOP1M_PATH
    
    if not ospath.isfile(filename):
        wl_log.critical('Cannot find URL list (Top Alexa CSV etc.) file!')
        return
    
    for line in open(filename).readlines()[start-1:stop]:
        if sep in line:
            rank, site_url = line.split(sep, 1) # we expect a comma between rank and URL (Alexa format)
                                                #beware: URLs may also include commas.
            site_url =  site_url.rstrip()
            if get_rank: # if caller asked for rank
                yield int(rank), site_url  
            else:
                yield site_url
        else:
            if get_rank:
                yield 0, line.rstrip() # we couldn't find the rank, just send 0
            else:
                yield line.rstrip() # no comma
            
class PublicSuffix():
    """Just an I/F for public suffix module."""
    def __init__(self):
        self.psl = publicsuffix.PublicSuffixList()
    
    def get_public_suffix(self, url):
        try:
            return self.psl.get_public_suffix(urlparse(url).hostname)
        except Exception as e:
            wl_log.critical('Exception(%s) parsing url: %s' %(e, url))
            return ''


    
