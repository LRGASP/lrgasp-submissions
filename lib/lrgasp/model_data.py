"""
Simplified GTF parser/validator
"""
import numpy as np
import warnings
from gtfparse import read_gtf, ParsingError
from lrgasp import LrgaspException

class Transcript:
    def __init__(self, transcript_id):
        self.transcript_id = transcript_id
        self.exons = []

    def sort(self):
        self.exons.sort(key=lambda e: (e.seqname, e.start, -e.end))

class Models(list):
    def __init__(self):
        self.by_transcript_id = {}

    def _obtain_transcript(self, transcript_id):
        trans = self.by_transcript_id.get(transcript_id)
        if trans is None:
            trans = self.by_transcript_id[transcript_id] = Transcript(transcript_id)
            self.append(trans)
        return trans

    def add_exon(self, exon):
        self._obtain_transcript(exon.transcript_id).exons.append(exon)

    def sort(self):
        for trans in self.by_transcript_id.values():
            trans.sort()

class GtfException(LrgaspException):
    pass

def fixup_empty_attr(gtf_df, col_name):
    """make empty None"""
    gtf_df[col_name] = np.where(gtf_df[col_name] == '', None, gtf_df[col_name])

def fixup_attr(gtf_df, col_name):
    """make an attribute None in empty or not specified"""
    if col_name in gtf_df.columns:
        fixup_empty_attr(gtf_df, col_name)
    else:
        gtf_df[col_name] = None

def fixup_gtf_attrs(gtf_df):
    fixup_attr(gtf_df, "transcript_id")
    fixup_attr(gtf_df, "gene_id")
    fixup_attr(gtf_df, "reference_gene_id")
    fixup_attr(gtf_df, "reference_transcript_id")

def load_exons(models_gtf):
    """load GTF exons into a list of Series objects of exons"""
    # gtfparse uses pandas read_csv with deprecated options:
    #   error_bad_lines=True,
    #   warn_bad_lines=True,
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', '.*_bad_lines argument.*', category=FutureWarning)
        gtf_df = read_gtf(models_gtf)
    gtf_df = gtf_df.loc[gtf_df.feature == 'exon']
    if len(gtf_df) == 0:
        raise GtfException("no exon records found")
    fixup_gtf_attrs(gtf_df)
    return [gtf_df.iloc[i] for i in range(len(gtf_df))]

def rec_desc(rec):
    return "{} at {}:{}-{}".format(rec.feature, rec.seqname, rec.start, rec.end)

def validate_exon(exon):
    if exon.transcript_id is None:
        raise GtfException("must specify transcript_id attribute: " + rec_desc(exon))
    if exon.gene_id is None:
        raise GtfException("must specify gene_id attribute: " + rec_desc(exon))
    if exon.start > exon.end:
        raise GtfException("start must be <= end: " + rec_desc(exon))
    if exon.strand not in ('+', '-', '.'):
        raise GtfException("strand must be '+', '-', or '.': " + rec_desc(exon))

def validate_exons(exons):
    if len(exons) == 0:
        raise LrgaspException("no exons found in GTF file")
    for exon in exons:
        validate_exon(exon)

def build_transcripts(exons):
    models = Models()
    for exon in exons:
        models.add_exon(exon)
    return models

def check_trans_field_same(trans, attr):
    vals = set([e[attr] for e in trans.exons])
    if len(vals) > 1:
        raise GtfException("all exons in transcript {} must have same value for {}, found {}".format(trans.transcript_id, attr, list(sorted(vals))))

def validate_transcript(trans):
    # do gene_id first, as it can explain other problems
    check_trans_field_same(trans, "gene_id")
    check_trans_field_same(trans, "seqname")
    check_trans_field_same(trans, "strand")
    check_trans_field_same(trans, "reference_gene_id")
    check_trans_field_same(trans, "reference_transcript_id")

def validate_transcripts(models):
    if len(models.by_transcript_id) == 0:
        raise LrgaspException("no transcripts found in GTF file")
    for trans in models.by_transcript_id.values():
        validate_transcript(trans)

def load(models_gtf):
    """Validate GTF, returns exons grouped into transcripts"""
    try:
        exons = load_exons(models_gtf)
        validate_exons(exons)
        models = build_transcripts(exons)
        validate_transcripts(models)
        return models
    except (LrgaspException, ParsingError, ValueError) as ex:
        raise GtfException("Parse of GTF failed: {}".format(models_gtf)) from ex
