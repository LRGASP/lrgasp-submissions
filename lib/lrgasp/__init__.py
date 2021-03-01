import os.path as osp
import sys
import gzip

__version__ = "0.5.0"

class LrgaspException(Exception):
    pass

def handle_prog_errors(ex):
    """Prints error messages without call stack and exit. For expected exceptions """
    print("Error: " + str(ex), file=sys.stderr)
    exc = ex.__cause__
    while exc is not None:
        print("    caused by: " + str(exc), file=sys.stderr)
        exc = exc.__cause__
    exit(1)

def defined_file_path(dirname, uncomp_name):
    """get the path to a file that must exist and may optional be compressed"""
    p = osp.join(dirname, uncomp_name)
    if osp.exists(p):
        return p
    comp_name = uncomp_name + ".gz"
    p = osp.join(dirname, comp_name)
    if osp.exists(p):
        return p
    raise LrgaspException(f"can't find required file {comp_name} or {uncomp_name} in {dirname}")

def gopen(path):
    "open a file for reading, allowing compressed files"
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    else:
        return open(path)
