"""
Parse FASTA of RNA sequences to get ids.
"""
from fasta_reader import read_fasta
from lrgasp import LrgaspException

def _load_fasta_rec(rna_ids, rec):
    if rec.id in rna_ids:
        raise LrgaspException(f"duplicate RNA id '{rec.id}'")
    rna_ids.add(rec.id)
    if len(rec.sequence) == 0:
        raise LrgaspException(f"empty RNA sequence '{rec.id}'")

def _load_fasta(rna_fasta):
    rna_ids = set()
    with read_fasta(rna_fasta) as fh:
        for rec in fh:
            _load_fasta_rec(rna_ids, rec)
    if len(rna_ids) == 0:
        raise LrgaspException("no RNA sequences in FASTA")
    return frozenset(rna_ids)

def load(rna_fasta):
    """load RNA ids from FASTA"""
    try:
        return _load_fasta(rna_fasta)
    except Exception as ex:
        raise LrgaspException(f"Parse of RNA FASTA file failed: {rna_fasta}") from ex
