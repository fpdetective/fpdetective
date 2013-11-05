

import re
import utils as ut
from common import CHROME_DRIVER_BINARY, CHROME_MOD_BINARY
from time import time, sleep
from selenium import webdriver
from log import wl_log
from webutils import PublicSuffix

pub_suffix = PublicSuffix()

# TODO: better link detection
LINK_LABELS = ('Sign In', 'Sign Up', 'Sign On', 'Register', 'Login', 'Log-in', 'Log-on', 'Sign')
LINK_URLS = ('login', 'logon', 'sign', 'register', 'subscri', 'log-in', 'log-on', 'join', 'sell', 'member',
                   'auth', 'account', 'user', 'password', 'store', 'shop', 'my') # TODO add other patterns

SLEEP_AFTER_PAGE_LOAD = 5
NO_OF_LINKS_TO_CLICK = 50
MAX_LINKS_TO_CLICK = 25
CRAWLER_GET_TIMEOUT = 10
CRAWLER_GET_HARD_TIMEOUT = 10
CRAWLER_CLICKER_VISIT_TIMEOUT = 210

WAIT_AFTER_LOAD = 5;
WAIT_AFTER_RELOAD = 1;
WAIT_AFTER_CLICK = 5;

def init_browser(br_type, cmd_args=""):
    
    if br_type is 'firefox':
        fp = webdriver.FirefoxProfile()        
        #fp.add_extension(extension=os.path.expanduser('~pathto/fourthparty.xpi')) # TODO: integrate fourthparty 
        return webdriver.Firefox(firefox_profile=fp)    
    else:
        ch = webdriver.ChromeOptions()
        ch.binary_location = CHROME_MOD_BINARY
        for cmd_arg in cmd_args:
            if cmd_arg:
                ch.add_argument(cmd_arg)
                #wl_log.info("Chrome arguments %s" % cmd_arg)
            
        return webdriver.Chrome(executable_path=CHROME_DRIVER_BINARY,
                                  chrome_options=ch)
        #Note: chromedriver can only retrieve the name and value of set cookies (no domain, path, etc.)
        
def extract_onclick_elements(br):
    """Return elements with onclick event handler."""
    return br.find_elements_by_xpath('//*[@onclick]') #
     
def extract_links(br):
    """Extract FP related links from the current page."""
    links_to_visit_text = list(ut.flatten([br.find_elements_by_partial_link_text(linktext) for linktext in LINK_LABELS]))
    links_to_visit_url = list(ut.flatten([br.find_elements_by_xpath('//a[contains(@href,"%s")]' % linkurl) for linkurl in LINK_URLS]))
    links_to_visit = [link for link in links_to_visit_text + links_to_visit_url if link]
    
    if len(links_to_visit) < NO_OF_LINKS_TO_CLICK: # if we cannot find links by href and link texts
        links_to_visit += extract_onclick_elements(br)  # we search for all elements with onclick event handler
    wl_log.info('%s links were found on %s' % (len(links_to_visit), br.current_url))
    
    return links_to_visit


def is_external(href, curr_url):
    """Return True if link is pointing to another domain."""
    if not href or not re.match(r"https?:\/\/[^.]+\.[^.]", href):
        return False
    
    href_domain = pub_suffix.get_public_suffix(href)
    curr_domain = pub_suffix.get_public_suffix(curr_url)    
    
    #wl_log.info("URL %s domain: %s href: %s domain %s" % (curr_url, curr_domain, href, href_domain));
    return href_domain != curr_domain

def is_mailto_link(href):
    """Return true of this is a mailto: link."""
    return True if re.match(r"mailto:.*", href) else False 
        

def is_clickable(el, page_url):
    """Return true if item is clickable, i.e. displayed, internal and http(s) link."""
    href = el.get_attribute('href')
    return el.is_displayed() and not is_external(href, page_url) and not is_mailto_link(href)

def click_to_xpath_selector(br, page_url, selector):
    #wl_log.info('Will find els by selector %s on %s' % (selector, page_url))
    els = br.find_elements_by_xpath(selector)
    for el in els:
        if is_clickable(el, page_url):
            href = el.get_attribute('href') or "?"
            try:
                el.click()
            except Exception as es:
                wl_log.warning('Exception while clicking: href: %s %s %s' % (href, es, page_url))                
            else:
                wl_log.info('Clicked!: href: %s %s %s' % (href, selector, page_url))
                sleep(WAIT_AFTER_CLICK)
                get_and_sleep(br, page_url)
                return 1
    #wl_log.debug('No clickable element found for: %s %s' % (selector, page_url))
    return 0 # we couldn't find any element to click

def lazy_crawler(br, page_url):
    get_and_sleep(br, page_url)

def click_crawler(br, page_url):
    num_clicked_links = 0
    get_and_sleep(br, page_url)
    wl_log.info("Click crawler will click on %s" % page_url)
    for label in LINK_LABELS:
        num_clicked_links += click_to_xpath_selector(br, page_url, '//a[contains(text(), "'+ label + '")]')
        #num_clicked_links += click_by_link_text(br, page_url, label)
    
    for url_string in LINK_URLS:
        num_clicked_links += click_to_xpath_selector(br, page_url, '//a[contains(@href,"' + url_string + '")]')
    
    wl_log.info("Clicked %s links, will click %s more" % (num_clicked_links, MAX_LINKS_TO_CLICK - num_clicked_links))
    for i in xrange(1, MAX_LINKS_TO_CLICK - num_clicked_links):
        click_to_xpath_selector(br, page_url, "(//a|//*[@onclick])[position()=%s]" % i)
        
def crawl_url(crawler_type, page_url, proxy_opt):
    
    if 'clicker' in crawler_type:
        worker = click_crawler
    else:
        worker = lazy_crawler
    
    br = init_browser('chrome', ['--allow-running-insecure-content', '--ignore-certificate-errors', '--disk-cache-size=0', \
                                         '--enable-logging', '--v=1', "--proxy-server=%s" % proxy_opt])
            
    if not page_url.startswith('http') and not page_url.startswith('file:'): 
        page_url = 'http://' + page_url
        
    wl_log.info('***Will crawl  %s***' % page_url)
    
    try:
        ut.timeout(CRAWLER_CLICKER_VISIT_TIMEOUT)
        worker(br, page_url) # run the worker function
    except ut.TimeExceededError as texc:
        wl_log.critical('***CRAWLER_CLICKER_VISIT_TIMEOUT at %s (%s)' % (page_url, texc))
    finally:    
        br.quit()
      
def crawl_urls(br_type, urls, fn=lambda x:x):
    for url in urls:
        try:
            br = init_browser(br_type)
        except:
            wl_log.critical('Init browser')
        else:
            try:
                crawl_url(br, url, fn)
            except Exception as e:
                wl_log.error("Error crawling %s: %s" %(url, e))
            br.quit()
        
def get_and_sleep(br, page_url):
    """Load page and sleep for a while."""
    try:                 
        start_time = time()
        br.get(page_url)
        elapsed_time = time() - start_time
        wl_log.info("Page %s loaded in %s" % (page_url, elapsed_time))                 
    except Exception as exc:
        wl_log.info('Error loading page %s %s' % (page_url, exc))
        br.quit()
    else:
        #wl_log.info('Will sleep after reload %s' % page_url)
        br.execute_script("window.onbeforeunload = function(e){};")
        sleep(SLEEP_AFTER_PAGE_LOAD)        
            