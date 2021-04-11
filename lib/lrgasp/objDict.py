# Copyright 2006-2018 Mark Diekhans
# Copyright of original unknown (https://goodcode.io/articles/python-dict-object/)

# dictionary with keys as object files, based on:
# https://goodcode.io/articles/python-dict-object/
from collections import defaultdict

class ObjDict(dict):
    """Dict object where keys are field names.
    This is useful for JSON by doing:
       json.load(fh, object_pairs_hook=ObjDict)
    """
    __slots__ = ()

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class DefaultObjDict(defaultdict):
    """defaultdict-based object where keys are field names.
    This is useful for JSON by doing:
       json.load(fh, object_pairs_hook=DefaultObjDict)
    """
    __slots__ = ()

    def __init__(self, dtype):
        super().__init__(dtype)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
