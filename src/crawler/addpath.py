from os.path import dirname
from os.path import realpath
import sys

def append_parent_to_sys_path():
    """Append parent dir to python path."""
    sys.path.append(dirname(dirname(realpath(__file__)))) # adds parent dir path to pythonpath