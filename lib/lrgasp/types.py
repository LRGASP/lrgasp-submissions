"""
Declarations of metadata identifiers, types, and functions to operate on them.
"""
import re
from lrgasp import LrgaspException
from lrgasp.symEnum import SymEnum, auto

class Challenge(SymEnum):
    """Challenge identifiers"""
    iso_detect_finished = auto()
    iso_quant = auto()
    iso_detect_draft = auto()

class ExperimentType(SymEnum):
    "type of a experiment, assumed from Challenge type"
    model = auto()
    expression = auto()

def challengeToExperimentType(challenge):
    assert isinstance(challenge, Challenge)
    if challenge is Challenge.iso_quant:
        return ExperimentType.expression
    else:
        return ExperimentType.model

class ResultFileType(SymEnum):
    "type of a submitted data file"
    model_GTF = auto()
    read_model_map = auto()
    expression_matrix = auto()

class ExpressionUnits(SymEnum):
    "Units used in expression matrix"
    RPM = auto()
    RPKM = auto()
    FPKM = auto()
    TPM = auto()
    counts = auto()

def validate_symbolic_ident(ident):
    if not ident.isidentifier():
        raise LrgaspException(f"not a valid symbolic identifier: '{ident}'")

def validate_feature_ident(ident):
    if (not ident.isascii()) or (not ident.isprintable()) or re.search("\\s", ident):
        raise LrgaspException(f"invalid feature identifier, must be composed of ASCII, printable, non-white-space characters: '{ident}'")
