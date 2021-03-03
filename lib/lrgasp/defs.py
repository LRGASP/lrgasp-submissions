"""
Definitions of metadata identifiers, types, and functions to operate on them.
"""
import re
from lrgasp import LrgaspException
from lrgasp.symEnum import SymEnum, auto

# fixed file names, without .gz
ENTRY_JSON = "entry.json"
EXPERIMENT_JSON = "experiment.json"
MODELS_GTF = "models.gtf"
READ_MODEL_MAP_TSV = "read_model_map.tsv"
EXPRESSION_TSV = "expression.tsv"

class Challenge(SymEnum):
    """Challenge identifiers"""
    iso_detect_ref = auto()
    iso_quant = auto()
    iso_detect_de_novo = auto()

class Sample(SymEnum):
    """LRGAPS sample identifierd"""
    WTC11_Hs = auto()
    H1_DE_Hs = auto()
    ES_Mm = auto()
    Manatee = auto()

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
    if (not ident.isascii()) or (not ident.isprintable()) or re.search("\\s", ident) or (len(ident) == 0):
        raise LrgaspException(f"invalid feature identifier, must be composed of ASCII, printable, non-white-space characters: '{ident}'")

def validate_synapse_ident(ident):
    if not re.match("^syn[0-9]{4,30}$", ident):
        raise LrgaspException(f"not a valid Synapse identifier: '{ident}'")

def validate_entry_ident(entry_id):
    """check that an entry is prefix with one of the challenge ids, return the Challenge identifier that
    matches"""
    for ch in Challenge:
        if entry_id.startswith(str(ch) + '_'):
            return ch
    valid_pre = ", ".join([str(ch) + '_*' for ch in Challenge])
    raise LrgaspException("entry_id {} must be prefixed with a challenge id ({})".format(entry_id, valid_pre))
