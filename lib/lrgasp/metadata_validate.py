"""Functions for validating metadata"""
import re
from collections import namedtuple
import validators.url
import validators.email
from lrgasp import LrgaspException

class Field(namedtuple("Field",
                       ("name", "dtype", "allow_empty", "optional", "validator"))):
    """Specify information for basic validation of a field.
    - dtype is a Python type (str, list, SymEnum, etc).  If type is other than
      str or list, the type is used to convert the value and saved back in the object.
    - validator is a callable to validate the type
    """
    def __new__(cls, name, dtype=str, *, allow_empty=False, optional=False, validator=None):
        return super().__new__(cls, name, dtype, allow_empty, optional, validator)


def _convert_type(desc, field, obj, val):
    try:
        setattr(obj, field.name, field.dtype(val))
    except ValueError as ex:
        raise LrgaspException(f"{desc} field {field.name} is not a valid {field.dtype}: {val}") from ex

def _validate_value(desc, field, obj, val):
    try:
        field.validator(val)
    except ValueError as ex:
        raise LrgaspException(f"{desc} field {field.name} is not a valid: {val}") from ex

def _check_field_present(desc, field, obj):
    val = getattr(obj, field.name)
    if not isinstance(val, field.dtype):
        raise LrgaspException(f"{desc} field {field.name} must be a {field.dtype.__name__}")
    elif field.dtype not in (str, list):
        _convert_type(desc, field, obj, val)
    if (not field.allow_empty) and (len(val) == 0):
        raise LrgaspException(f"{desc} field {field.name} must be a non-empty {field.dtype.__name__}")
    if field.validator is not None:
        _validate_value(desc, field, obj, val)

def _check_field_missing(desc, field, obj):
    if not field.optional:
        raise LrgaspException(f"{desc} field {field.name} is required")

def _check_field(desc, field, obj):
    if field.name in obj:
        _check_field_present(desc, field, obj)
    else:
        _check_field_missing(desc, field, obj)

def validate_email(val):
    if validators.email(val) is not True:
        raise LrgaspException(f"invalid email address: {val}")

def validate_url(val):
    if validators.url(val, public=True) is not True:
        raise LrgaspException(f"invalid URL: {val}")

def validate_http_url(val):
    validate_url(val)
    if not (val.startswith("http:") or val.startswith("https:")):
        raise LrgaspException(f"must be an HTTP URL: {val}")

def validate_md5(val):
    "checks MD5 string"
    if not re.search("^[a-fA-F0-9]{32}$", val):
        raise LrgaspException(f"MD5 must be a 128-bit hexadecimal number: {val}")

def check_from_defs(desc, fields, obj):
    """basic check of fields given a definition table"""
    for field in fields:
        _check_field(desc, field, obj)
