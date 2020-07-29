import numpy as np
from collections import defaultdict
from gtfparse import read_gtf, ParsingError

class GtfErr(Exception):
    pass

def fixup_empty_attr(gtf_df, col_name):
    """make empty None"""
    gtf_df[col_name] = np.where(gtf_df[col_name] == '', None, gtf_df[col_name])

def fixup_optional_attr(gtf_df, col_name):
    """make an optional attribute None in empty or not specified"""
    if col_name in gtf_df.columns:
        fixup_empty_attr(gtf_df, col_name)
    else:
        gtf_df[col_name] = None

def fixup_gtf_attrs(gtf_df):
    if "transcript_id" not in gtf_df.columns:
        raise GtfErr("GTF exons must have transcript_id attribute")
    fixup_empty_attr(gtf_df, "transcript_id")
    if "gene_id" not in gtf_df.columns:
        raise GtfErr("GTF exons must have gene_id attribute")
    fixup_empty_attr(gtf_df, "gene_id")
    fixup_optional_attr(gtf_df, "reference_gene_id")
    fixup_optional_attr(gtf_df, "reference_transcript_id")

def _load_exons(gtf_file):
    gtf_df = read_gtf(gtf_file)
    gtf_df = gtf_df.loc[gtf_df.feature == 'exon']
    if len(gtf_df) == 0:
        raise GtfErr("no exon records found")
    fixup_gtf_attrs(gtf_df)
    return [gtf_df.iloc[i] for i in range(len(gtf_df))]

def load_exons(gtf_file):
    """load GTF exons into a list of Series objects of exons"""
    try:
        return _load_exons(gtf_file)
    except (ParsingError, GtfErr) as ex:
        raise GtfErr("parse of {} failed".format(gtf_file)) from ex

def rec_desc(rec):
    return "{} at {}:{}-{}".format(rec.feature, rec.seqname, rec.start, rec.end)

def trans_desc(trans):
    return trans[0].transcript_id

def group_transcripts(gtf_records):
    """group records into transcripts"""
    transcripts = defaultdict(list)
    for rec in gtf_records:
        transcripts[rec.transcript_id].append(rec)
    for trans in transcripts.values():
        trans.sort(key=lambda e: (e.seqname, e.start, -e.end))
    return transcripts

def group_genes(transcripts):
    """group transcripts into genes"""
    genes = defaultdict(list)
    for trans in transcripts.values():
        genes[trans[0].gene_id].append(trans)
    return genes

def validate_exon(exon):
    if exon.transcript_id is None:
        raise GtfErr("must specify transcript_id attribute: " + rec_desc(exon))
    if exon.gene_id is None:
        raise GtfErr("must specify gene_id attribute: " + rec_desc(exon))
    if exon.start > exon.end:
        raise GtfErr("start must be <= end: " + rec_desc(exon))
    if exon.strand not in ('+', '-', '.'):
        raise GtfErr("strand must be '+', '-', or '.': " + rec_desc(exon))

def validate_exons(exons):
    for exon in exons:
        validate_exon(exon)

def check_trans_field_same(trans, attr):
    vals = set([e[attr] for e in trans])
    if len(vals) > 1:
        raise GtfErr("all exons in transcript {} must have same value for {}, found {}".format(trans_desc(trans), attr, list(sorted(vals))))

def validate_transcript(trans):
    # do gene_id first, as it can explain other problems
    check_trans_field_same(trans, "gene_id")
    check_trans_field_same(trans, "seqname")
    check_trans_field_same(trans, "strand")
    check_trans_field_same(trans, "reference_gene_id")
    check_trans_field_same(trans, "reference_transcript_id")

def validate_transcripts(transcripts):
    for trans in transcripts.values():
        validate_transcript(trans)

def validate_genes(genes):
    pass

def _validate(exons):
    validate_exons(exons)
    transcripts = group_transcripts(exons)
    validate_transcripts(transcripts)
    genes = group_genes(transcripts)
    validate_genes(genes)

def validate(gtf_file):
    exons = load_exons(gtf_file)
    try:
        _validate(exons)
    except GtfErr as ex:
        raise GtfErr("validation of {} failed".format(gtf_file)) from ex
