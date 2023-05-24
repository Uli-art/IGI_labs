import inspect
import types

PRIMITIVES = (int, float, bool, str, type(None))
SEQUENCES = (list, tuple, set)


def is_primitive(obj):
    return type(obj) in PRIMITIVES


def is_sequence(obj):
    return type(obj) in SEQUENCES


def is_dict(obj):
    return type(obj) == dict


def is_collection(obj):
    return is_sequence(obj) | is_dict(obj)


def is_object(obj):
    return isinstance(obj, object)


def is_class(obj):
    return inspect.isclass(obj)


def is_function(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def is_method(obj):
    return inspect.ismethod(obj)


def is_cell(obj):
    return isinstance(obj, types.CellType)


def is_code(obj):
    return isinstance(obj, types.CodeType)


def is_builtin_type(obj):
    return is_primitive(obj) or is_collection(obj)


def is_bytes(obj):
    return isinstance(obj, bytes)


def is_module(obj):
    return isinstance(obj, types.ModuleType)


def is_iterator(obj):
    return hasattr(obj, "__iter__") and hasattr(obj, "__next__")


def xml_escape(obj: str):
    return obj.replace("<", "&lt;").replace(">", "&gt;")


def xml_unescape(obj: str):
    return obj.replace("&lt;", "<").replace("&gt;", ">")