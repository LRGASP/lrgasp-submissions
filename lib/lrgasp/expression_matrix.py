"""
expression matrix parser/validator
"""
import csv
import pandas as pd
import numpy as np
from lrgasp import LrgaspException
from lrgasp import checkValidFeatureIdent
from lrgasp import gopen

def check_row_consistency(expr_mat_tsv):
    """Pandas just pads or ignores inconsistent number of columns,
    so to validate the matrix is consistent, we need to make another pass.
    """
    minLen = maxLen = None
    with gopen(expr_mat_tsv) as fh:
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

def sample_column_names(expr_mat):
    "return all but ID column"
    return [col for col in expr_mat.columns if col != "ID"]

def validate_header(expr_mat):
    if "ID" not in expr_mat.columns:
        raise LrgaspException("TSV must have column 'ID'")
    if len(expr_mat.columns) < 2:
        raise LrgaspException("TSV must have at least one sample column")

def check_column_type(expr_mat, col):
    "validate column type is correct"
    if expr_mat.dtypes[col] != np.float64:
        raise LrgaspException(f"Invalid value(s) in column '{col}', must be a number or NA, appears to contain strings")

def validate_data(expr_mat):
    if expr_mat.size == 0:
        raise LrgaspException("TSV contains no data")
    expr_mat.ID.apply(lambda ident: checkValidFeatureIdent(ident, "transcript identifier"))
    for col in sample_column_names(expr_mat):
        check_column_type(expr_mat, col)

def validate(expr_mat):
    validate_header(expr_mat)
    validate_data(expr_mat)

def expr_mat_load(expr_mat_tsv):
    try:
        check_row_consistency(expr_mat_tsv)
        expr_mat = pd.read_csv(expr_mat_tsv,
                               dialect=csv.excel_tab,
                               header=0,
                               converters={"ID": str})
        validate(expr_mat)
        return expr_mat
    except (LrgaspException, pd.errors.ParserError, pd.errors.EmptyDataError) as ex:
        raise LrgaspException("Parse of expression matrix TSV failed: {}".format(expr_mat_tsv)) from ex
