import os.path as osp
import sys
import gzip
import traceback
import logging
from collections.abc import Iterable
from lrgasp import loggingOps

__version__ = "1.2.0"

class LrgaspException(Exception):
    pass

# exceptions that should result in a call to handle_prog_errors
prog_error_excepts = (LrgaspException, FileNotFoundError)

def handle_prog_errors(ex, debug=None):
    """Prints error messages without call stack and exit. For expected exceptions """

    # --logDebug will enable debug, however we currently just send to stderr,
    # as we need basic errors to stderr always
    if debug is None:
        debug = (loggingOps.getLrgaspLogger().level == logging.DEBUG)

    print("Error: " + str(ex), file=sys.stderr)
    if debug:
        traceback.print_tb(ex.__traceback__, file=sys.stderr)
    exc = ex.__cause__
    while exc is not None:
        print("caused by: " + str(exc), file=sys.stderr)
        if debug:
            traceback.print_tb(exc.__traceback__, file=sys.stderr)
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
    raise LrgaspException(f"can't find required file '{comp_name}' or '{uncomp_name}' in '{dirname}'")

def existing_datafile_name(path):
    """Given a name without .gz, return the path with or without .gz, depending
    on which one exists, error if both or neither exist"""
    pathgz = path + ".gz"
    if osp.exists(path) and osp.exists(pathgz):
        raise LrgaspException(f"file exists as both compressed and uncompressed versions: {pathgz} and {path}")
    if osp.exists(pathgz):
        return pathgz
    elif osp.exists(path):
        return path
    else:
        raise LrgaspException(f"missing file; neither compressed or uncompressed exist: {pathgz} and {path}")

def gopen(path):
    "open a file for reading, allowing compressed files"
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    else:
        return open(path)

def iter_to_str(values):
    """Generate string of values for use in error messages.  Sets will be sorted.
    if it is non-iterable, return str"""
    if not isinstance(values, Iterable):
        return str(values)
    elif isinstance(values, (set, frozenset)):
        return ", ".join([str(v) for v in sorted(values)])
    else:
        return ", ".join([str(v) for v in values])
