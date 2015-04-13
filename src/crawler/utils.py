from __future__ import division

import re 
import os
import commands
import operator
import sys
import hashlib
import signal
from random import choice
from itertools import imap
from itertools import chain
from log import wl_log
from common import TimeExceededError
from numpy import dot
from numpy.linalg import norm

ASCII_LOWERCASE_CHARS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'

DEFAULT_RAND_STR_SIZE = 6
DEFAULT_RAND_STR_CHARS = ASCII_LOWERCASE_CHARS + DIGITS

def die(last_words):
    """Log last words and exit."""
    wl_log.critical(last_words)
    sys.exit(1)    

def nop():
    """No-op, just pass."""
    pass
    
def rand_str(size=DEFAULT_RAND_STR_SIZE, chars=DEFAULT_RAND_STR_CHARS):
    """Return random string given a size and character space."""
    return ''.join(choice(chars) for _ in range(size))


def occurence_vector(text, patterns):
    """Search for the occurrences of grpattern, which should be composed of groups(or'ed patterns).
    
    Return a binary vector that represents the occurrences of each regexp groups in order
    
    """
    vector = []
    regexes = [re.compile(r'%s' % pattern) for pattern in patterns]
    for regex in regexes:
        vector.append(1 if regex.search(text) else 0) 
    return tuple(vector) # TODO just changed to tuple!


def cosine_similarity(v1, v2):
    """Return cosine similarity for two binary vectors."""
    assert len(v1) == len(v2)
    return float(dot(v1,v2) / (norm(v1) * norm(v2)))

def jaccard_index(v1, v2):
    """Return Jackard Distance for two binary vectors."""
    assert len(v1) == len(v2)
    return sum(imap(operator.and_, v1, v2)) / sum(imap(operator.or_, v1, v2))
    
def hamming_dist(v1, v2):
    """Return Hamming Distance for two binary vectors."""
    assert len(v1) == len(v2)
    return sum(imap(operator.ne, v1, v2))

def flatten(listOfLists):
    "Flatten one level of nesting."
    return chain.from_iterable(listOfLists)
    
def all_subdirs_of(top_dir='.'):
    """Return subdirectories of given dir."""
    result = []
    for dir_name in os.listdir(top_dir):
        dir_path = os.path.join(top_dir, dir_name)
        if os.path.isdir(dir_path): result.append(dir_path)
    return result


def hash_text(text, algo='sha1'):
    """Return the hash value for the text."""
    h = hashlib.new(algo)
    h.update(text)
    return h.hexdigest()

def is_unique(elements):
    """Return True if all elements in all tuples with this index is unique."""
    return len(elements) == len(set(elements))

def raise_signal(signum, frame):
    raise TimeExceededError, "Timed Out"

def timeout(duration):    
    """Timeout after given duration."""    
    signal.signal(signal.SIGALRM, raise_signal) # SIGALRM is only usable on a unix platform        
    signal.alarm(duration) # alarm after X seconds

def cancel_timeout():
    signal.alarm(0)

def run_cmd(cmd):
    return commands.getstatusoutput('%s ' %(cmd))
    
def is_installed(pkg_name):
    """Check if a package is installed."""
    cmd = 'which %s' % pkg_name
    status, _ = run_cmd(cmd)
    return False if status else True
