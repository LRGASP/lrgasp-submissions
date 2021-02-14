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

def gopen(path):
    "open a file for reading, allowing compressed files"
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    else:
        return open(path)
