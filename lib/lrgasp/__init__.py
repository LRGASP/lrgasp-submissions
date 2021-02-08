import sys
import re

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

def checkValidSymbolicIdent(ident, description, prefix=None):
    if not ident.isidentifier():
        raise LrgaspException(f"not a valid {description} identifier: '{ident}'")
    if (prefix is not None) and (not ident.startwith(prefix)):
        raise LrgaspException(f"{description} must start with {prefix}: '{ident}'")

def checkValidFeatureIdent(ident, description):
    if (not ident.isascii()) or (not ident.isprintable()) or re.search("\s", ident):
        raise LrgaspException(f"not a valid {description} identifier, must be composed of ASCII, printable, non-white-space characters: '{ident}'")
