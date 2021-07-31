"""
Definitions of metadata identifiers, types, and functions to operate on them.
"""
import re
from collections import defaultdict
from lrgasp import LrgaspException
from lrgasp.symEnum import SymEnum, auto

# fixed file names, without .gz
ENTRY_JSON = "entry.json"
EXPERIMENT_JSON = "experiment.json"
MODELS_GTF = "models.gtf"
READ_MODEL_MAP_TSV = "read_model_map.tsv"
EXPRESSION_TSV = "expression.tsv"
DE_NOVO_RNA_FASTA = "rna.fasta"

class Challenge(SymEnum):
    """Challenge identifiers, value matches challenge number"""
    iso_detect_ref = 1
    iso_quant = 2
    iso_detect_de_novo = 3

class DataCategory(SymEnum):
    """categories of experiments based on data accepted"""
    long_only = auto()
    short_only = auto()
    long_short = auto()
    long_genome = auto()
    freestyle = auto()

class Platform(SymEnum):
    """Simplified sequencing platform, mostly used if figuring out LibraryCategory"""
    Illumina = auto()
    PacBio = auto()
    ONT = auto()

class LibraryPrep(SymEnum):
    """Type of library prep"""
    CapTrap = auto()
    dRNA = auto()
    R2C2 = auto()
    cDNA = auto()

class Sample(SymEnum):
    """LRGASP sample identifier"""
    WTC11 = auto()
    H1_mix = auto()
    ES = auto()
    blood = auto()
    mouse_simulation = auto()
    human_simulation = auto()

class Species(SymEnum):
    """Species identifiers"""
    human = auto()
    mouse = auto()
    manatee = auto()
    simulated = auto()

class Repository(SymEnum):
    """Public data repositories"""
    SRA = auto()
    ENA = auto()
    INSDC = auto()
    ENC = auto()

class RefGenome(SymEnum):
    """LRGASP reference genomes"""
    GRCh38 = auto()
    GRCm39 = auto()

class Gencode(SymEnum):
    """LRGASP GENCODE version"""
    GENCODE_V38 = auto()
    GENCODE_VM27 = auto()

def validate_symbolic_ident(ident):
    if not ident.isidentifier():
        raise LrgaspException(f"not a valid symbolic identifier '{ident}'")
    return ident

def validate_feature_ident(ident):
    if (not ident.isascii()) or (not ident.isprintable()) or re.search("\\s", ident) or (len(ident) == 0):
        raise LrgaspException(f"'{ident}' is not a valid feature identifier, must be composed of ASCII, printable, non-white-space characters")
    return ident

def validate_synapse_ident(ident):
    if not re.match("^syn[0-9]{4,30}$", ident):
        raise LrgaspException(f"'{ident}' is not a valid Synapse identifier")
    return ident

def validate_entry_ident(entry_id):
    """check that an entry is prefix with one of the challenge ids, return the Challenge identifier that
    matches"""
    for ch in Challenge:
        if entry_id.startswith(str(ch) + '_'):
            return ch
    valid_pre = ", ".join([str(ch) + '_*' for ch in Challenge])
    raise LrgaspException(f"entry_id '{entry_id}' must be prefixed with a challenge id {valid_pre}")

def sample_to_species(sample):
    if sample in (Sample.WTC11, Sample.H1_mix):
        return Species.human
    elif sample == Sample.ES:
        return Species.model
    elif sample == Sample.blood:
        return Species.manatee
    else:
        raise LrgaspException(f"bug mapping sample '{sample}' to a species")


_challenge_sample_map = {
    Challenge.iso_detect_ref: frozenset([Sample.WTC11, Sample.H1_mix, Sample.ES, Sample.mouse_simulation, Sample.human_simulation]),
    Challenge.iso_quant: frozenset([Sample.WTC11, Sample.H1_mix, Sample.mouse_simulation, Sample.human_simulation]),
    Challenge.iso_detect_de_novo: frozenset([Sample.blood, Sample.ES]),
}

def _build_sample_challenge_map():
    # reverse mapping
    s2c = defaultdict(set)
    for c in _challenge_sample_map:
        for s in _challenge_sample_map[c]:
            s2c[s].add(c)
    s2c.default_factory = None
    for s in s2c.keys():
        s2c[s] = tuple(sorted(s2c[s]))
    return s2c

# challenges are sorted by value
_sample_challenge_map = _build_sample_challenge_map()

def get_challenge_samples(challenge_id):
    return _challenge_sample_map[challenge_id]

def sample_to_challenges(sample):
    return _sample_challenge_map[sample]

def is_simulation(sample):
    return sample in (Sample.human_simulation, Sample.mouse_simulation)

def challenge_desc(challenge_id):
    return f"Challenge {challenge_id.value} ({str(challenge_id)})"
