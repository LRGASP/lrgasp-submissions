"""
expression matrix parser/validator
"""
import csv
import numpy as np
import pandas as pd
from lrgasp import LrgaspException
from lrgasp import gopen
from lrgasp.defs import validate_feature_ident

##
# In order to detect empty columns and short rows, disallow space as a NA value, as well
# as remove other weirder values
##
na_values = frozenset(['NaN', 'NA', 'nan', 'null', '-nan', 'n/a', 'N/A', 'NULL', '-NaN'])


class ExpressionMatrix:
    """Expression matrix and operations to access columns by file or biosample accession"""
    def __init__(self, df):
        self.df = df

def sample_column_names(expression_mat):
    "return all but ID column"
    return [col for col in expression_mat.df.columns if col != "ID"]

def validate_header(expression_mat):
    if "ID" not in expression_mat.df.columns:
        raise LrgaspException("TSV must have column 'ID'")
    if len(expression_mat.df.columns) < 2:
        raise LrgaspException("TSV must have at least one sample column")

def check_column_type(expression_mat, col):
    "validate column type is correct"
    if expression_mat.df.dtypes[col] not in (np.float64, np.int64):
        raise LrgaspException(f"Invalid value(s) in column '{col}', must be a number, NA, or NaN, appears to contain other types or a short row")

def validate_data(expression_mat):
    if expression_mat.df.size == 0:
        raise LrgaspException("TSV contains no data")
    expression_mat.df.ID.apply(validate_feature_ident)
    for col in sample_column_names(expression_mat):
        check_column_type(expression_mat, col)

def validate_biosamples(experiment_md, expression_mat):
    """validate that samples match those for the experiment and that all samples
    are in the matrix."""
    pass
    # biosample_map = get_experiment_biosample_file_map(experiment)
    # sample_cols = sample_column_names(expression_mat)

def load(expression_tsv, experiment_md=None):
    "if experiment_md is provide, validate samples"
    try:
        with gopen(expression_tsv) as fh:
            # na_value handling is needed to detect empty cells and short
            # rows, preventing implicit conversion to NaN.
            df = pd.read_csv(fh, dialect=csv.excel_tab, header=0,
                             converters={"ID": str},
                             na_values=na_values,
                             keep_default_na=False)
            expression_mat = ExpressionMatrix(df)
            validate_header(expression_mat)
            expression_mat.df.set_index("ID", drop=False, inplace=True, verify_integrity=True)
            validate_data(expression_mat)
            if experiment_md is not None:
                validate_biosamples(experiment_md, expression_mat)
        return expression_mat
    except (LrgaspException, pd.errors.ParserError, pd.errors.EmptyDataError, ValueError) as ex:
        raise LrgaspException(f"Parse of expression matrix TSV failed: {expression_tsv}") from ex
