"""
expression matrix parser/validator
"""
import csv
import pandas as pd
import numpy as np
from lrgasp import LrgaspException
from lrgasp import gopen
from lrgasp.defs import validate_feature_ident

def check_row_consistency(expression_tsv):
    """Pandas just pads or ignores inconsistent number of columns,
    so to validate the matrix is consistent, we need to make another pass.
    """
    # note: if pandas was given a header, it will error on long rows, but not short ones
    minLen = maxLen = None
    with gopen(expression_tsv) as fh:
        for row in csv.reader(fh, dialect=csv.excel_tab):
            if minLen is None:
                minLen = maxLen = len(row)
            else:
                minLen = min(len(row), minLen)
                maxLen = max(len(row), maxLen)
    if minLen is None:
        raise LrgaspException("TSV is empty")
    if minLen != maxLen:
        raise LrgaspException(f"TSV has an inconsistent number of columns: min={minLen}, max={maxLen}")

def sample_column_names(expression):
    "return all but ID column"
    return [col for col in expression.columns if col != "ID"]

def validate_header(expression_mat):
    if "ID" not in expression_mat.columns:
        raise LrgaspException("TSV must have column 'ID'")
    if len(expression_mat.columns) < 2:
        raise LrgaspException("TSV must have at least one sample column")

def check_column_type(expression_mat, col):
    "validate column type is correct"
    if expression_mat.dtypes[col] not in (np.float64, np.int64):
        raise LrgaspException(f"Invalid value(s) in column '{col}', must be a number or NA, appears to contain other types, induced type is '{expression_mat.dtypes[col]}'")

def validate_data(expression_mat):
    if expression_mat.size == 0:
        raise LrgaspException("TSV contains no data")
    expression_mat.ID.apply(validate_feature_ident)
    for col in sample_column_names(expression_mat):
        check_column_type(expression_mat, col)

def load(expression_tsv):
    try:
        check_row_consistency(expression_tsv)
        with gopen(expression_tsv) as fh:
            expression_mat = pd.read_csv(fh,
                                         dialect=csv.excel_tab,
                                         header=0,
                                         converters={"ID": str})
            validate_header(expression_mat)
            expression_mat.set_index("ID", drop=False, inplace=True, verify_integrity=True)
            validate_data(expression_mat)
        return expression_mat
    except (LrgaspException, pd.errors.ParserError, pd.errors.EmptyDataError, ValueError) as ex:
        raise LrgaspException(f"Parse of expression matrix TSV failed: {expression_tsv}") from ex
