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

def validate_header(expression):
    if "ID" not in expression.columns:
        raise LrgaspException("TSV must have column 'ID'")
    if len(expression.columns) < 2:
        raise LrgaspException("TSV must have at least one sample column")

def check_column_type(expression, col):
    "validate column type is correct"
    if expression.dtypes[col] not in (np.float64, np.int64):
        raise LrgaspException(f"Invalid value(s) in column '{col}', must be a number or NA, appears to contain other types, induced type is ({expression.dtypes[col]})")

def validate_data(expression):
    if expression.size == 0:
        raise LrgaspException("TSV contains no data")
    expression.ID.apply(validate_feature_ident)
    for col in sample_column_names(expression):
        check_column_type(expression, col)

def load(expression_tsv):
    try:
        check_row_consistency(expression_tsv)
        with gopen(expression_tsv) as fh:
            expression = pd.read_csv(fh,
                                     dialect=csv.excel_tab,
                                     header=0,
                                     converters={"ID": str})
            validate_header(expression)
            expression.set_index("ID", drop=False, inplace=True, verify_integrity=True)
            validate_data(expression)
        return expression
    except (LrgaspException, pd.errors.ParserError, pd.errors.EmptyDataError, ValueError) as ex:
        raise LrgaspException("Parse of expression matrix TSV failed: {}".format(expression_tsv)) from ex
