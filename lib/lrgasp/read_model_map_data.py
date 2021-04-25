"""
read-to-model map parser/validator
"""
import sys
import csv
from collections import defaultdict, namedtuple
from lrgasp import LrgaspException, gopen
from lrgasp.defs import validate_feature_ident

csv.field_size_limit(sys.maxsize)

# note: pandas was a bad fit for this due to multi-indexing

READ_ID = "read_id"
TRANSCRIPT_ID = "transcript_id"

class ReadModelPair(namedtuple("ReadModelPair", ("read_id", "transcript_id"))):
    """a read mapped to a model or None"""
    pass

class ReadModelMap(list):
    """read to model map container, adding lazy multiple indexes"""
    def __init__(self):
        self._read_id_idx = None
        self._transcript_id_idx = None

    def add(self, pair):
        self.append(pair)

    def _build_idx(self, col_name):
        idx = defaultdict(list)
        for rec in self:
            val = getattr(rec, col_name)
            if val is not None:
                idx[val] = rec
        idx.default_factory = None
        return idx

    def get_by_read_id(self, read_id):
        if self._read_id_idx is None:
            self._read_id_idx = self._build_idx("read_id")
        return self._read_id_idx.get(read_id)

    def get_by_transcript_id(self, transcript_id):
        if self._transcript_id_idx is None:
            self._transcript_id_idx = self._build_idx("transcript_id")
        return self._transcript_id_idx.get(transcript_id)

def _parse_header(reader):
    header = next(reader, None)
    if header is None:
        raise LrgaspException("Empty TSV file, requires a header line")
    try:
        read_id_col = header.index(READ_ID)
    except ValueError:
        raise LrgaspException(READ_ID + " column required")
    try:
        trans_id_col = header.index(TRANSCRIPT_ID)
    except ValueError:
        raise LrgaspException(TRANSCRIPT_ID + " column required")
    return read_id_col, trans_id_col, len(header)

def _parse_row(read_id, transcript_id):
    validate_feature_ident(read_id)
    validate_feature_ident(transcript_id)
    if transcript_id == '*':
        transcript_id = None
    return ReadModelPair(read_id, transcript_id)

def _tsv_reader(fh):
    # allows for extra columns, but all rows must have the same
    reader = csv.reader(fh, dialect=csv.excel_tab)
    read_id_col, trans_id_col, width = _parse_header(reader)
    for row in reader:
        if len(row) != width:
            raise LrgaspException(f"TSV row requires {width} columns found {len(row)}, row is '{row}'")
        yield _parse_row(row[read_id_col], row[trans_id_col])

def load(model_map_tsv):
    read_model_map = ReadModelMap()
    try:
        with gopen(model_map_tsv) as fh:
            for pair in _tsv_reader(fh):
                read_model_map.add(pair)
        if len(read_model_map) == 0:
            raise LrgaspException("TSV contains no data")
        return read_model_map
    except (LrgaspException, FileNotFoundError, csv.Error) as ex:
        raise LrgaspException("Parse of reads-to-models TSV failed: {}".format(model_map_tsv)) from ex
