"""
read-to-model map parser/validator
"""
import csv
import pandas as pd
from lrgasp import LrgaspException
from lrgasp.identifiers import featureIdentValidate

required_columns = ("read_id", "transcript_id")

def validate_header(read_model_map):
    for col in required_columns:
        if col not in read_model_map.columns:
            raise LrgaspException(f"TSV must have column '{col}'")

def validate_data(read_model_map):
    if read_model_map.size == 0:
        raise LrgaspException("TSV contains no data")
    if (read_model_map.isnull().values.any()):
        raise LrgaspException("empty or missing values in columns")
    read_model_map.read_id.apply(lambda ident: featureIdentValidate(ident, "read identifier"))
    read_model_map.transcript_id.apply(lambda ident: featureIdentValidate(ident, "transcript identifier"))

def validate(read_model_map):
    validate_header(read_model_map)
    validate_data(read_model_map)

def read_model_map_load(model_map_tsv):
    try:
        read_model_map = pd.read_csv(model_map_tsv,
                                     dialect=csv.excel_tab,
                                     header=0,
                                     dtype=str)
        validate(read_model_map)
        return read_model_map
    except (LrgaspException, pd.errors.ParserError, pd.errors.EmptyDataError) as ex:
        raise LrgaspException("Parse of reads-to-models TSV failed: {}".format(model_map_tsv)) from ex
