import sys

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

class ErrorReporter:
    """report and count errors"""

    MAX_ERRORS = 50

    def __init__(self):
        self.cnt = 0

    def error(self, msg, filename=None, linenum=None):
        "error and continue checking, if max not exceeded"
        if filename is not None:
            print(filename + ":", end="", file=sys.stderr)
        if linenum is not None:
            print(linenum + ":", end="", file=sys.stderr)
        if (filename is not None) or (linenum is not None):
            print(" ", end="", file=sys.stderr)
        print("Error:", msg, file=sys.stderr)
        self.cnt += 1
        if self.cnt > self.MAX_ERRORS:
            raise LrgaspException("maximum errors reached, {} error(s) found".format(self.cnt))

    def fatal(self, msg, filename=None, linenum=None):
        "error and stop"
        self.error(msg, filename, linenum)
        self.stop()

    def stop(self):
        "can't continue because it makes no sense to continue validating"
        raise LrgaspException("{} error(s) encountered ".format(self.cnt))

    def stopIfErrors(self):
        if self.cnt > 0:
            self.stop()

def isValidSymbolicIdent(ident, description, prefix=None):
    pass
