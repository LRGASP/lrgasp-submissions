import sys
import gzip

def handle_prog_errors(ex):
    """Prints error messages without call stack and exit. For expected exceptions """
    print("Error: " + str(ex), file=sys.stderr)
    exc = ex.__cause__
    while exc is not None:
        print("    caused by: " + str(exc), file=sys.stderr)
        exc = exc.__cause__
    exit(1)

class LrgaspException(Exception):
    pass

def gopen(path):
    "open a file for reading, allowing compressed files"
    if path.endswith(".gz"):
        return gzip.open(path)
    else:
        return open(path)
