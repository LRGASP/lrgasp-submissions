"""
Declarations of metadata identifiers and functions to operate on identifiers
"""
import re
from lrgasp import LrgaspException
from lrgasp.symEnum import SymEnum, auto

class Challenge(SymEnum):
    """Challenge identifiers"""
    iso_detect_finished = auto()
    iso_quant = auto()
    iso_detect_draft = auto()

def symbolicIdentValidate(ident, description, prefix=None):
    if not ident.isidentifier():
        raise LrgaspException(f"not a valid {description} identifier: '{ident}'")
    if (prefix is not None) and (not ident.startwith(prefix)):
        raise LrgaspException(f"{description} must start with {prefix}: '{ident}'")

def featureIdentValidate(ident, description):
    if (not ident.isascii()) or (not ident.isprintable()) or re.search("\\s", ident):
        raise LrgaspException(f"not a valid {description} identifier, must be composed of ASCII, printable, non-white-space characters: '{ident}'")
