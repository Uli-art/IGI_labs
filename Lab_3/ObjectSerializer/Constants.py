import enum
import types


JSON_FORMAT = 'json'
XML_FORMAT = 'xml'
YAML_FORMAT = 'yaml'
TOML_FORMAT = 'toml'

class EntityTypes(enum.Enum):
    UNDEFINED = 1
    NONE = 2
    BOOL = 3
    INT = 4
    FLOAT = 5
    STRING = 6
    LIST = 7
    SET = 8
    TUPLE = 9
    DICT = 10
    OBJECT = 11
    CLASS = 12
    FUNCTION = 13
    CELL = 14
    CODE = 15
    BYTES = 16
    MODULE = 17
    ITERATOR =18


PARAMS_FOR_CODE_REPLACE = ("co_argcount", "co_posonlyargcount",
                           "co_kwonlyargcount", "co_nlocals",
                           "co_stacksize", "co_flags",
                           "co_firstlineno", "co_code",
                           "co_consts", "co_names",
                           "co_varnames", "co_freevars",
                           "co_cellvars", "co_filename",
                           "co_name", "co_linetable")


NONSERIALIZABLE_TYPES = (
    types.WrapperDescriptorType,
    types.MethodDescriptorType,
    types.BuiltinFunctionType,
    types.MappingProxyType,
    types.GetSetDescriptorType,
    types.BuiltinMethodType
)

UNSERIALIZABLE_DUNDER = (
    "__mro__",
    "__base__",
    "__basicsize__",
    "__class__",
    "__dictoffset__",
    "__name__",
    "__qualname__",
    "__text_signature__",
    "__itemsize__",
    "__flags__",
    "__weakrefoffset__",
    "__objclass__",
    "__doc__"
)
