"""
expression matrix parser/validator
"""
import csv
import numpy as np
import pandas as pd
from lrgasp import LrgaspException
from lrgasp import gopen, iter_to_str
from lrgasp.defs import validate_feature_ident
from lrgasp.data_sets import get_lrgasp_rna_seq_metadata

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

def validate_replicates(experiment_md, expression_mat):
    """validate that samples match those for the experiment and that all samples
    are in the matrix."""
    rna_seq_md = get_lrgasp_rna_seq_metadata()
    sample_cols = sample_column_names(expression_mat)

    def _check_in_expr():
        "check that all columns are in the experiment"
        for sc in sample_cols:
            if sc not in experiment_md.libraries:
                raise LrgaspException(f"matrix column '{sc}' is not listed in experiment_md.libraries for '{experiment_md.experiment_id}'")

    def _build_run_replicates(file_accs):
        "create a set with tuples of (run_acc, replicate_number)"
        run_reps = set()
        for file_acc in file_accs:
            file_md = rna_seq_md.get_file_by_acc(file_acc)
            run_reps.add((file_md.run_acc, file_md.biological_replicate_number))
        return run_reps

    def _check_covers_expr():
        """check that every run and replicate for an experiment is in matrix"""
        expr_rr = _build_run_replicates(experiment_md.libraries)
        mat_rr = _build_run_replicates(sample_cols)
        if len(mat_rr) > len(expr_rr):
            raise LrgaspException(f"BUG: matrix has more run replicates than experiment: matrix='{mat_rr}' experiment='{expr_rr}'")
        missing_rr = expr_rr - mat_rr
        if len(missing_rr) > 0:
            missing_desc = iter_to_str(["{}/{}".format(*rr) for rr in missing_rr])
            raise LrgaspException(f"matrix does not have an entries for all run and replicate in experiment, missing: {missing_desc}")

    _check_in_expr()
    _check_covers_expr()

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
                validate_replicates(experiment_md, expression_mat)
        return expression_mat
    except (LrgaspException, pd.errors.ParserError, pd.errors.EmptyDataError, ValueError) as ex:
        raise LrgaspException(f"Parse of expression matrix TSV failed: {expression_tsv}") from ex
